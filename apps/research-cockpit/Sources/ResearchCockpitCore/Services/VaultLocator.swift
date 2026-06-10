import Foundation

public struct VaultLocation: Equatable, Sendable {
    public var root: URL

    public init(root: URL) {
        self.root = root.standardizedFileURL
    }

    public var llmWikiExecutable: URL {
        root.appendingPathComponent("bin/llm-wiki")
    }

    public var rawDirectory: URL {
        root.appendingPathComponent("raw")
    }

    public var wikiDirectory: URL {
        root.appendingPathComponent("wiki")
    }

    public var isValid: Bool {
        VaultLocator.isVault(root)
    }
}

public enum VaultLocator {
    public static func defaultCandidates(homeDirectory: URL = FileManager.default.homeDirectoryForCurrentUser) -> [URL] {
        [
            homeDirectory.appendingPathComponent("Documents/llm-knowledge-wiki"),
            homeDirectory.appendingPathComponent("llm-knowledge-wiki"),
            homeDirectory.appendingPathComponent("Documents/GitHub/llm-knowledge-wiki")
        ]
    }

    public static func findDefaultVault(homeDirectory: URL = FileManager.default.homeDirectoryForCurrentUser) -> VaultLocation? {
        defaultCandidates(homeDirectory: homeDirectory)
            .first(where: isVault)
            .map(VaultLocation.init(root:))
    }

    public static func isVault(_ url: URL) -> Bool {
        let fileManager = FileManager.default
        return fileManager.fileExists(atPath: url.appendingPathComponent("bin/llm-wiki").path)
            && fileManager.fileExists(atPath: url.appendingPathComponent("raw").path)
            && fileManager.fileExists(atPath: url.appendingPathComponent("wiki").path)
            && fileManager.fileExists(atPath: url.appendingPathComponent("docs/agent-contract.md").path)
    }
}
