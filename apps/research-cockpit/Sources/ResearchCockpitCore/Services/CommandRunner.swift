import Foundation

public struct ShellCommand: Equatable, Identifiable, Sendable {
    public var id: UUID
    public var label: String
    public var executable: String
    public var arguments: [String]
    public var workingDirectory: URL?

    public init(
        id: UUID = UUID(),
        label: String,
        executable: String,
        arguments: [String] = [],
        workingDirectory: URL? = nil
    ) {
        self.id = id
        self.label = label
        self.executable = executable
        self.arguments = arguments
        self.workingDirectory = workingDirectory
    }

    public var commandLine: String {
        ([executable] + arguments).map(Self.shellDisplay).joined(separator: " ")
    }

    private static func shellDisplay(_ value: String) -> String {
        if value.rangeOfCharacter(from: .whitespacesAndNewlines) == nil {
            return value
        }
        return "'" + value.replacingOccurrences(of: "'", with: "'\\''") + "'"
    }
}

public struct CommandResult: Identifiable, Equatable, Sendable {
    public var id: UUID
    public var label: String
    public var commandLine: String
    public var exitCode: Int32
    public var stdout: String
    public var stderr: String
    public var startedAt: Date
    public var endedAt: Date

    public init(
        id: UUID = UUID(),
        label: String,
        commandLine: String,
        exitCode: Int32,
        stdout: String,
        stderr: String,
        startedAt: Date,
        endedAt: Date
    ) {
        self.id = id
        self.label = label
        self.commandLine = commandLine
        self.exitCode = exitCode
        self.stdout = stdout
        self.stderr = stderr
        self.startedAt = startedAt
        self.endedAt = endedAt
    }

    public var succeeded: Bool {
        exitCode == 0
    }

    public var combinedOutput: String {
        [stdout, stderr]
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
            .joined(separator: "\n")
    }
}

public protocol CommandRunning {
    func run(_ command: ShellCommand) async -> CommandResult
}

public final class ProcessCommandRunner: CommandRunning {
    public init() {}

    public func run(_ command: ShellCommand) async -> CommandResult {
        await Task.detached(priority: .userInitiated) {
            let startedAt = Date()
            let process = Process()
            let stdoutPipe = Pipe()
            let stderrPipe = Pipe()

            process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
            process.arguments = [command.executable] + command.arguments
            process.currentDirectoryURL = command.workingDirectory
            process.standardOutput = stdoutPipe
            process.standardError = stderrPipe

            do {
                try process.run()
                process.waitUntilExit()
                let endedAt = Date()
                let stdout = String(data: stdoutPipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8) ?? ""
                let stderr = String(data: stderrPipe.fileHandleForReading.readDataToEndOfFile(), encoding: .utf8) ?? ""
                return CommandResult(
                    label: command.label,
                    commandLine: command.commandLine,
                    exitCode: process.terminationStatus,
                    stdout: stdout,
                    stderr: stderr,
                    startedAt: startedAt,
                    endedAt: endedAt
                )
            } catch {
                return CommandResult(
                    label: command.label,
                    commandLine: command.commandLine,
                    exitCode: -1,
                    stdout: "",
                    stderr: error.localizedDescription,
                    startedAt: startedAt,
                    endedAt: Date()
                )
            }
        }.value
    }
}
