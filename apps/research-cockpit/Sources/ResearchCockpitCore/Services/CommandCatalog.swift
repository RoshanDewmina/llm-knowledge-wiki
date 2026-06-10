import Foundation

public enum CommandCatalog {
    public static func llmWiki(_ arguments: [String], vaultRoot: URL, label: String? = nil) -> ShellCommand {
        ShellCommand(
            label: label ?? "llm-wiki \(arguments.joined(separator: " "))",
            executable: "./bin/llm-wiki",
            arguments: arguments,
            workingDirectory: vaultRoot
        )
    }

    public static func ingest(rawRelativePath: String, vaultRoot: URL, title: String? = nil, slug: String? = nil) -> ShellCommand {
        var arguments = ["ingest", rawRelativePath]
        if let title, !title.isEmpty {
            arguments += ["--title", title]
        }
        if let slug, !slug.isEmpty {
            arguments += ["--slug", slug]
        }
        return llmWiki(arguments, vaultRoot: vaultRoot, label: "Ingest \(rawRelativePath)")
    }

    public static func status(vaultRoot: URL) -> ShellCommand {
        llmWiki(["status", "--json"], vaultRoot: vaultRoot, label: "Wiki Status")
    }

    public static func doctor(vaultRoot: URL, fast: Bool = false) -> ShellCommand {
        var arguments = ["doctor", "--json"]
        if fast {
            arguments += ["--skip-site-build", "--skip-vault-checks"]
        }
        return llmWiki(arguments, vaultRoot: vaultRoot, label: "Wiki Doctor")
    }

    public static func health(vaultRoot: URL) -> ShellCommand {
        llmWiki(["health", "--json"], vaultRoot: vaultRoot, label: "Wiki Health")
    }

    public static func quiz(slug: String, vaultRoot: URL, count: Int = 8) -> ShellCommand {
        llmWiki(["quiz", slug, "--n", "\(count)", "--kind", "mixed"], vaultRoot: vaultRoot, label: "Generate Quiz")
    }

    public static func anki(slug: String, vaultRoot: URL, count: Int = 20) -> ShellCommand {
        llmWiki(["anki", slug, "--n", "\(count)", "--style", "mixed"], vaultRoot: vaultRoot, label: "Generate Flashcards")
    }

    public static func query(_ text: String, vaultRoot: URL, limit: Int = 8) -> ShellCommand {
        llmWiki(["query", text, "--limit", "\(limit)"], vaultRoot: vaultRoot, label: "Search Wiki")
    }

    public static func review(vaultRoot: URL) -> ShellCommand {
        llmWiki(["review"], vaultRoot: vaultRoot, label: "Regenerate Review Files")
    }

    public static func export(relativePath: String, vaultRoot: URL) -> ShellCommand {
        llmWiki(["export", relativePath], vaultRoot: vaultRoot, label: "Export \(relativePath)")
    }

    public static func hermes(_ arguments: [String], vaultRoot: URL? = nil, label: String? = nil) -> ShellCommand {
        ShellCommand(
            label: label ?? "hermes \(arguments.joined(separator: " "))",
            executable: "hermes",
            arguments: arguments,
            workingDirectory: vaultRoot
        )
    }

    public static func launchctlGatewayStatus() -> ShellCommand {
        ShellCommand(
            label: "LaunchAgent Status",
            executable: "launchctl",
            arguments: ["print", "gui/\(getuid())/ai.hermes.gateway"]
        )
    }
}
