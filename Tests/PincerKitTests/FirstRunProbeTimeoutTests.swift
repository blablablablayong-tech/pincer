import Foundation
import Synchronization
import Testing
@testable import PincerKit

/// A receive that deliberately ignores Swift cancellation until its transport is closed.
/// No sockets or shared defaults; this reproduces the task-group deadline failure deterministically.
@Suite("First-run probe deadlines")
struct FirstRunProbeTimeoutTests {
    // Shared CI may take several seconds to schedule tasks. This still catches the 30-second
    // un-cancelled deadline; transport state assertions below check timeout/cancellation correctness.
    private static let schedulingBudget: TimeInterval = 15

    private final class PendingReceive: Sendable {
        private struct State {
            var continuation: CheckedContinuation<URLSessionWebSocketTask.Message, Error>?
            var closed = false
        }
        private let state = Mutex(State())

        var isWaiting: Bool { self.state.withLock { $0.continuation != nil } }
        var isClosed: Bool { self.state.withLock { $0.closed } }

        func receive() async throws -> URLSessionWebSocketTask.Message {
            try await withCheckedThrowingContinuation { continuation in
                let closed = self.state.withLock { state in
                    if state.closed { return true }
                    state.continuation = continuation
                    return false
                }
                if closed { continuation.resume(throwing: CancellationError()) }
            }
        }

        func close() {
            let continuation = self.state.withLock { state in
                state.closed = true
                let continuation = state.continuation
                state.continuation = nil
                return continuation
            }
            continuation?.resume(throwing: CancellationError())
        }
    }

    @Test func timeoutClosesNonCooperativeReceive() async throws {
        let transport = PendingReceive()
        let started = Date()
        let result = try await FirstRunProbe.firstMessage(
            timeout: 0.02, receive: { try await transport.receive() }, cancel: { transport.close() })
        #expect(result == nil)
        #expect(transport.isClosed && !transport.isWaiting)
        #expect(Date().timeIntervalSince(started) < Self.schedulingBudget, "deadline should not wait for a remote close")
    }

    @Test func cancellingProbeClosesNonCooperativeReceive() async throws {
        let transport = PendingReceive()
        let job = Task {
            try await FirstRunProbe.firstMessage(
                timeout: 30, receive: { try await transport.receive() }, cancel: { transport.close() })
        }
        let deadline = Date().addingTimeInterval(Self.schedulingBudget)
        while !transport.isWaiting, Date() < deadline { try await Task.sleep(for: .milliseconds(1)) }
        let waiting = transport.isWaiting
        job.cancel()
        // Always settle the job, even if the scheduling assertion fails.
        let result = await job.result
        #expect(waiting)
        #expect(transport.isClosed && !transport.isWaiting)
        if case .success = result { Issue.record("a cancelled probe must not report a message") }
    }

    @Test func messageWinsWithoutWaitingForDeadline() async throws {
        let transport = PendingReceive()
        let started = Date()
        let message = try await FirstRunProbe.firstMessage(
            timeout: 30, receive: { .string("challenge") }, cancel: { transport.close() })
        if case .string("challenge")? = message {} else { Issue.record("lost the first message") }
        #expect(!transport.isClosed)
        #expect(Date().timeIntervalSince(started) < Self.schedulingBudget)
    }
}
