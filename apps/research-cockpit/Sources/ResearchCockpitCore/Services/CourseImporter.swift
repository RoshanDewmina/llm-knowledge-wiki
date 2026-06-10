import Foundation

public struct CourseImportSummary: Equatable, Sendable {
    public var course: CourseMetadata
    public var ingestCommands: [ShellCommand]

    public init(course: CourseMetadata, ingestCommands: [ShellCommand]) {
        self.course = course
        self.ingestCommands = ingestCommands
    }
}

public final class CourseImporter {
    private let store: CourseMetadataStore
    private let fileManager: FileManager

    public init(store: CourseMetadataStore, fileManager: FileManager = .default) {
        self.store = store
        self.fileManager = fileManager
    }

    public func importSources(
        from inputURLs: [URL],
        courseName: String,
        term: String
    ) throws -> CourseImportSummary {
        let sourceFiles = try expandedFiles(from: inputURLs)
        var course = CourseMetadata.newCourse(courseName: courseName, term: term)
        if let existing = try store.loadAll().first(where: { $0.slug == course.slug }) {
            course = existing
        }

        let rawDirectory = store.rawDirectory(for: course.slug)
        try fileManager.createDirectory(at: rawDirectory, withIntermediateDirectories: true)

        var importedSources: [CourseSource] = []
        var ingestCommands: [ShellCommand] = []

        for inputURL in sourceFiles {
            let destinationURL = try uniqueDestinationURL(
                for: inputURL.lastPathComponent,
                in: rawDirectory
            )
            if inputURL.standardizedFileURL != destinationURL.standardizedFileURL {
                try fileManager.copyItem(at: inputURL, to: destinationURL)
            }

            let rawRelativePath = relativePath(from: store.vaultRoot, to: destinationURL)
            let sourceSlug = Slug.make("\(course.slug)-\(destinationURL.deletingPathExtension().lastPathComponent)")
            let source = CourseSource(
                displayName: destinationURL.lastPathComponent,
                sourceKind: CourseSourceKind.infer(from: destinationURL),
                rawRelativePath: rawRelativePath,
                originalPath: inputURL.path,
                sourcePageSlug: sourceSlug
            )
            importedSources.append(source)
            ingestCommands.append(
                CommandCatalog.ingest(
                    rawRelativePath: rawRelativePath,
                    vaultRoot: store.vaultRoot,
                    title: "\(course.courseName): \(destinationURL.deletingPathExtension().lastPathComponent)",
                    slug: sourceSlug
                )
            )
        }

        course.recordSources(importedSources)
        try store.save(course)
        return CourseImportSummary(course: course, ingestCommands: ingestCommands)
    }

    public func createStudyGuideScaffold(for course: CourseMetadata) throws -> GeneratedOutput {
        let sourceRefs = try existingSourcePageRefs(for: course)
        let outputRelativePath = "wiki/studies/courses/\(course.slug)/study-guide.md"
        let outputURL = store.vaultRoot.appendingPathComponent(outputRelativePath)
        try fileManager.createDirectory(
            at: outputURL.deletingLastPathComponent(),
            withIntermediateDirectories: true
        )

        let now = ISO8601DateFormatter().string(from: Date())
        let sourcePageLinks = sourceRefs
            .map { "- \($0)" }
            .joined(separator: "\n")
        let citationLinks = sourceRefs
            .map { "- [[\($0)]]" }
            .joined(separator: "\n")
        let sourceTrace = course.sources.isEmpty
            ? "- No imported sources yet."
            : course.sources.map { "- `\($0.rawRelativePath)` -> `wiki/sources/\($0.sourcePageSlug ?? "pending").md`" }.joined(separator: "\n")

        let title = yamlQuoted("\(course.courseName) Study Guide")
        let markdown = """
        ---
        title: \(title)
        type: output
        created: \(now)
        updated: \(now)
        status: stub
        confidence: 0.3
        related:
          - studies/courses/\(course.slug)
        source_pages:
        \(sourcePageLinks.isEmpty ? "  []" : sourcePageLinks.replacingOccurrences(of: "- ", with: "  - "))
        compiled_at: \(now)
        ---

        # \(course.courseName) Study Guide

        ## Source Trace

        \(sourceTrace)

        ## Study Plan

        - Build the exact evidence anchors for the highest-value source pages.
        - Turn each major lecture or chapter into active-recall prompts.
        - Promote only cited claims into the final guide.

        ## Key Topics

        - To be filled after source review.

        ## Practice

        - Generate a quiz from the matching study slug after source review.

        ## Contradictions

        No contradiction is currently recorded.

        ## Citations

        \(citationLinks.isEmpty ? "- Pending source-page review." : citationLinks)
        """

        try markdown.write(to: outputURL, atomically: true, encoding: .utf8)
        return GeneratedOutput(
            kind: .studyGuide,
            title: "\(course.courseName) Study Guide",
            relativePath: outputRelativePath,
            commandLine: "Research Cockpit study guide scaffold"
        )
    }

    public func createQuizScaffold(for course: CourseMetadata, count: Int = 12) throws -> GeneratedOutput {
        let sourceRefs = try existingSourcePageRefs(for: course)
        let outputRelativePath = "wiki/studies/courses/\(course.slug)/quiz.md"
        let outputURL = store.vaultRoot.appendingPathComponent(outputRelativePath)
        try fileManager.createDirectory(
            at: outputURL.deletingLastPathComponent(),
            withIntermediateDirectories: true
        )

        let now = ISO8601DateFormatter().string(from: Date())
        let title = yamlQuoted("\(course.courseName) Quiz")
        let sourcePageLines = sourceRefs.map { "  - \($0)" }.joined(separator: "\n")
        let questions = (1...max(1, count)).map { index -> String in
            let ref = sourceRefs[(index - 1) % sourceRefs.count]
            return "\(index). From [[\(ref)]], write one answerable exam-style question and cite the exact evidence anchor before trusting the answer."
        }.joined(separator: "\n")

        let markdown = """
        ---
        title: \(title)
        type: output
        created: \(now)
        updated: \(now)
        status: stub
        confidence: 0.3
        related:
          - studies/courses/\(course.slug)
        source_pages:
        \(sourcePageLines)
        compiled_at: \(now)
        ---

        # \(course.courseName) Quiz

        ## Questions

        \(questions)

        ## Answer Key

        Add answers only after checking exact source evidence.

        ## Contradictions

        No contradiction is currently recorded.

        ## Citations

        \(sourceRefs.map { "- [[\($0)]]" }.joined(separator: "\n"))
        """

        try markdown.write(to: outputURL, atomically: true, encoding: .utf8)
        return GeneratedOutput(
            kind: .quiz,
            title: "\(course.courseName) Quiz",
            relativePath: outputRelativePath,
            commandLine: "Research Cockpit quiz scaffold"
        )
    }

    public func createFlashcardScaffold(for course: CourseMetadata, count: Int = 20) throws -> GeneratedOutput {
        let sourceRefs = try existingSourcePageRefs(for: course)
        let outputRelativePath = "wiki/studies/courses/\(course.slug)/flashcards.tsv"
        let outputURL = store.vaultRoot.appendingPathComponent(outputRelativePath)
        try fileManager.createDirectory(
            at: outputURL.deletingLastPathComponent(),
            withIntermediateDirectories: true
        )

        var rows = ["topic\tprompt\tanswer\tsource"]
        for index in 1...max(1, count) {
            let ref = sourceRefs[(index - 1) % sourceRefs.count]
            rows.append("source-\(index)\tWrite a high-value flashcard from [[\(ref)]].\tFill after exact evidence review.\t\(ref)")
        }
        try rows.joined(separator: "\n").write(to: outputURL, atomically: true, encoding: .utf8)
        return GeneratedOutput(
            kind: .flashcards,
            title: "\(course.courseName) Flashcards",
            relativePath: outputRelativePath,
            commandLine: "Research Cockpit flashcard scaffold"
        )
    }

    private func expandedFiles(from inputURLs: [URL]) throws -> [URL] {
        var result: [URL] = []
        for inputURL in inputURLs {
            var isDirectory: ObjCBool = false
            guard fileManager.fileExists(atPath: inputURL.path, isDirectory: &isDirectory) else {
                continue
            }
            if isDirectory.boolValue {
                let enumerator = fileManager.enumerator(
                    at: inputURL,
                    includingPropertiesForKeys: [.isRegularFileKey],
                    options: [.skipsHiddenFiles, .skipsPackageDescendants]
                )
                while let child = enumerator?.nextObject() as? URL {
                    let values = try child.resourceValues(forKeys: [.isRegularFileKey])
                    if values.isRegularFile == true {
                        result.append(child)
                    }
                }
            } else {
                result.append(inputURL)
            }
        }
        return result.sorted { $0.path < $1.path }
    }

    private func uniqueDestinationURL(for fileName: String, in directory: URL) throws -> URL {
        let base = URL(fileURLWithPath: fileName).deletingPathExtension().lastPathComponent
        let extensionName = URL(fileURLWithPath: fileName).pathExtension
        var candidate = directory.appendingPathComponent(fileName)
        var index = 2
        while fileManager.fileExists(atPath: candidate.path) {
            let suffix = extensionName.isEmpty ? "-\(index)" : "-\(index).\(extensionName)"
            candidate = directory.appendingPathComponent(base + suffix)
            index += 1
        }
        return candidate
    }

    private func relativePath(from root: URL, to child: URL) -> String {
        let rootPath = root.standardizedFileURL.path
        let childPath = child.standardizedFileURL.path
        if childPath.hasPrefix(rootPath + "/") {
            return String(childPath.dropFirst(rootPath.count + 1))
        }
        return childPath
    }

    private func yamlQuoted(_ value: String) -> String {
        let escaped = value
            .replacingOccurrences(of: "\\", with: "\\\\")
            .replacingOccurrences(of: "\"", with: "\\\"")
        return "\"\(escaped)\""
    }

    private func existingSourcePageRefs(for course: CourseMetadata) throws -> [String] {
        let refs = course.sources
            .compactMap(\.sourcePageSlug)
            .map { "sources/\($0)" }
            .filter { ref in
                fileManager.fileExists(
                    atPath: store.vaultRoot.appendingPathComponent("wiki/\(ref).md").path
                )
            }
        if refs.isEmpty {
            throw CourseImporterError.noIngestedSourcePages(course.slug)
        }
        return refs
    }
}

public enum CourseImporterError: LocalizedError, Equatable {
    case noIngestedSourcePages(String)

    public var errorDescription: String? {
        switch self {
        case .noIngestedSourcePages(let slug):
            return "No ingested source pages exist for `\(slug)` yet. Import sources and let llm-wiki ingest finish before generating study outputs."
        }
    }
}
