import Foundation

extension FirstRunProbe {
    /// A deadline must stop the underlying receive before the task group can finish.
    /// Cancelling a Swift child task alone need not close its WebSocket.
    package static func firstMessage(
        timeout: TimeInterval,
        receive: @escaping @Sendable () async throws -> URLSessionWebSocketTask.Message,
        cancel: @escaping @Sendable () -> Void) async throws -> URLSessionWebSocketTask.Message?
    {
        try await withTaskCancellationHandler {
            try await withThrowingTaskGroup(of: URLSessionWebSocketTask.Message?.self) { group in
                group.addTask { try await receive() }
                group.addTask {
                    try await Task.sleep(for: .seconds(timeout))
                    return nil
                }
                let first = try await group.next() ?? nil
                // Close the receive before awaiting the cancelled children on scope exit.
                if first == nil { cancel() }
                group.cancelAll()
                return first
            }
        } onCancel: {
            cancel()
        }
    }
}
