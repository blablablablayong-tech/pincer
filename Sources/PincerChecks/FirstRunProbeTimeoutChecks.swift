import Foundation
import PincerKit
import Synchronization

private final class ProbePendingReceive: Sendable {
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

@MainActor
func runFirstRunProbeTimeoutChecks() async {
    let silent = ProbePendingReceive()
    do {
        let message = try await FirstRunProbe.firstMessage(
            timeout: 0.02, receive: { try await silent.receive() }, cancel: { silent.close() })
        check(message == nil && silent.isClosed && !silent.isWaiting, "probe timeout closes a non-cooperative receive")
    } catch {
        check(false, "probe deadline should return no message, not a receive cancellation: \(error)")
    }
    let cancelled = ProbePendingReceive()
    let job = Task {
        try await FirstRunProbe.firstMessage(
            timeout: 30, receive: { try await cancelled.receive() }, cancel: { cancelled.close() })
    }
    let deadline = Date().addingTimeInterval(1)
    while !cancelled.isWaiting, Date() < deadline { try? await Task.sleep(for: .milliseconds(1)) }
    let wasWaiting = cancelled.isWaiting
    job.cancel()
    let result = await job.result
    if case .failure = result {
        check(wasWaiting && cancelled.isClosed && !cancelled.isWaiting, "closing the wizard cancels its pending receive")
    } else {
        check(false, "a cancelled probe must not succeed")
    }
}
