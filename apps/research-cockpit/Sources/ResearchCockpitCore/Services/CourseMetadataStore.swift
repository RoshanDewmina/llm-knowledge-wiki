import Foundation

public final class CourseMetadataStore {
    public let vaultRoot: URL

    private let encoder: JSONEncoder
    private let decoder: JSONDecoder

    public init(vaultRoot: URL) {
        self.vaultRoot = vaultRoot
        self.encoder = JSONEncoder()
        self.decoder = JSONDecoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        encoder.dateEncodingStrategy = .iso8601
        decoder.dateDecodingStrategy = .iso8601
    }

    public var metadataRoot: URL {
        vaultRoot.appendingPathComponent(".research-cockpit/courses")
    }

    public func metadataURL(for slug: String) -> URL {
        metadataRoot.appendingPathComponent("\(slug).json")
    }

    public func studyDirectory(for slug: String) -> URL {
        vaultRoot.appendingPathComponent("wiki/studies/courses/\(slug)")
    }

    public func rawDirectory(for slug: String) -> URL {
        vaultRoot.appendingPathComponent("raw/courses/\(slug)")
    }

    public func loadAll() throws -> [CourseMetadata] {
        let fileManager = FileManager.default
        guard fileManager.fileExists(atPath: metadataRoot.path) else {
            return []
        }
        let files = try fileManager.contentsOfDirectory(
            at: metadataRoot,
            includingPropertiesForKeys: nil,
            options: [.skipsHiddenFiles]
        )
        return try files
            .filter { $0.pathExtension == "json" }
            .map(load)
            .sorted { $0.updatedAt > $1.updatedAt }
    }

    public func load(_ url: URL) throws -> CourseMetadata {
        let data = try Data(contentsOf: url)
        return try decoder.decode(CourseMetadata.self, from: data)
    }

    public func save(_ course: CourseMetadata) throws {
        let fileManager = FileManager.default
        try fileManager.createDirectory(at: metadataRoot, withIntermediateDirectories: true)
        try fileManager.createDirectory(at: studyDirectory(for: course.slug), withIntermediateDirectories: true)
        let data = try encoder.encode(course)
        try data.write(to: metadataURL(for: course.slug), options: .atomic)
        try writeCourseOverview(course)
    }

    public func writeCourseOverview(_ course: CourseMetadata) throws {
        let now = ISO8601DateFormatter().string(from: course.updatedAt)
        let sourceLines = course.sources.isEmpty
            ? "- No sources imported yet."
            : course.sources.map { "- `\($0.rawRelativePath)` (\($0.sourceKind.rawValue))" }.joined(separator: "\n")
        let outputLines = course.generatedOutputs.isEmpty
            ? "- No generated outputs yet."
            : course.generatedOutputs.map { "- `\($0.relativePath)` (\($0.kind.rawValue))" }.joined(separator: "\n")

        let markdown = """
        # \(course.courseName)

        Term: \(course.term.isEmpty ? "Unspecified" : course.term)

        This file is maintained by Research Cockpit. The original course material stays under `\(course.rawFolder)`, and generated study outputs stay in the vault.

        ## Sources

        \(sourceLines)

        ## Generated Outputs

        \(outputLines)

        ## Status

        - Last health status: \(course.lastHealthStatus)
        - Provider status: \(course.providerStatus)
        - Last updated: \(now)
        """

        let overviewURL = metadataRoot.appendingPathComponent("\(course.slug).md")
        try markdown.write(to: overviewURL, atomically: true, encoding: .utf8)
    }
}
