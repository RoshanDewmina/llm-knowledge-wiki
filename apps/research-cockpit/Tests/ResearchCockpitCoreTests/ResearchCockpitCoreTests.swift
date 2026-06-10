import XCTest
@testable import ResearchCockpitCore

final class ResearchCockpitCoreTests: XCTestCase {
    func testSlugMakeNormalizesCourseNames() {
        XCTAssertEqual(Slug.make("COMP 1501A: Intro to Game Design"), "comp-1501a-intro-to-game-design")
        XCTAssertEqual(Slug.make("  !!!  ", fallback: "course"), "course")
    }

    func testVaultLocatorRecognizesMinimalVault() throws {
        let root = try makeTemporaryVault()
        XCTAssertTrue(VaultLocator.isVault(root))
    }

    func testCourseImporterCopiesFilesAndBuildsIngestCommands() throws {
        let root = try makeTemporaryVault()
        let sourceDirectory = root.appendingPathComponent("incoming")
        try FileManager.default.createDirectory(at: sourceDirectory, withIntermediateDirectories: true)
        let pdfURL = sourceDirectory.appendingPathComponent("Lecture 01.pdf")
        try Data("pdf".utf8).write(to: pdfURL)

        let store = CourseMetadataStore(vaultRoot: root)
        let importer = CourseImporter(store: store)
        let summary = try importer.importSources(
            from: [pdfURL],
            courseName: "COMP 1501A",
            term: "Winter 2026"
        )

        XCTAssertEqual(summary.course.slug, "comp-1501a-winter-2026")
        XCTAssertEqual(summary.course.sources.count, 1)
        XCTAssertEqual(summary.ingestCommands.count, 1)
        XCTAssertTrue(summary.ingestCommands[0].commandLine.contains("ingest"))
        XCTAssertTrue(FileManager.default.fileExists(atPath: root.appendingPathComponent("raw/courses/comp-1501a-winter-2026/Lecture 01.pdf").path))
        XCTAssertTrue(FileManager.default.fileExists(atPath: root.appendingPathComponent(".research-cockpit/courses/comp-1501a-winter-2026.json").path))
    }

    func testHealthInterpreterReportsMissingCommands() throws {
        let json = """
        {
          "commands": {
            "bun": {"ok": false, "detail": "not found"},
            "python3": {"ok": true, "detail": "/usr/bin/python3"}
          },
          "obsidian": {"ok": false, "detail": "missing"},
          "paths": {
            "wiki": {"ok": true, "detail": "wiki"}
          },
          "failures": ["missing command: bun"]
        }
        """

        let findings = HealthInterpreter.findings(fromDoctorJSON: json)
        XCTAssertTrue(findings.contains { $0.id == "missing-command-bun" })
        XCTAssertTrue(findings.contains { $0.id == "obsidian-missing" })
    }

    func testStudyGuideScaffoldStaysInVault() throws {
        let root = try makeTemporaryVault()
        try writeSourcePage(root: root, slug: "comp-3804-lecture-1")
        let store = CourseMetadataStore(vaultRoot: root)
        let importer = CourseImporter(store: store)
        var course = CourseMetadata.newCourse(courseName: "COMP 3804", term: "Winter 2026")
        course.recordSources([
            CourseSource(
                displayName: "Lecture 1.pdf",
                sourceKind: .pdf,
                rawRelativePath: "raw/courses/comp-3804-winter-2026/Lecture 1.pdf",
                originalPath: nil,
                sourcePageSlug: "comp-3804-lecture-1"
            )
        ])
        try store.save(course)

        let output = try importer.createStudyGuideScaffold(for: course)
        let outputURL = root.appendingPathComponent(output.relativePath)
        XCTAssertTrue(FileManager.default.fileExists(atPath: outputURL.path))
        let body = try String(contentsOf: outputURL)
        XCTAssertTrue(body.contains("[[sources/comp-3804-lecture-1]]"))
    }

    func testCourseQuizAndFlashcardsUseIngestedSourcePages() throws {
        let root = try makeTemporaryVault()
        try writeSourcePage(root: root, slug: "comp-1501a-lecture-1")
        let store = CourseMetadataStore(vaultRoot: root)
        let importer = CourseImporter(store: store)
        var course = CourseMetadata.newCourse(courseName: "COMP 1501A", term: "Winter 2026")
        course.recordSources([
            CourseSource(
                displayName: "Lecture 1.pdf",
                sourceKind: .pdf,
                rawRelativePath: "raw/courses/comp-1501a-winter-2026/Lecture 1.pdf",
                originalPath: nil,
                sourcePageSlug: "comp-1501a-lecture-1"
            )
        ])

        let quiz = try importer.createQuizScaffold(for: course, count: 3)
        let flashcards = try importer.createFlashcardScaffold(for: course, count: 3)

        XCTAssertTrue(FileManager.default.fileExists(atPath: root.appendingPathComponent(quiz.relativePath).path))
        XCTAssertTrue(FileManager.default.fileExists(atPath: root.appendingPathComponent(flashcards.relativePath).path))
        let quizBody = try String(contentsOf: root.appendingPathComponent(quiz.relativePath))
        XCTAssertTrue(quizBody.contains("[[sources/comp-1501a-lecture-1]]"))
    }

    private func makeTemporaryVault() throws -> URL {
        let root = FileManager.default.temporaryDirectory
            .appendingPathComponent("ResearchCockpitTests-\(UUID().uuidString)")
        try FileManager.default.createDirectory(at: root.appendingPathComponent("bin"), withIntermediateDirectories: true)
        try FileManager.default.createDirectory(at: root.appendingPathComponent("raw"), withIntermediateDirectories: true)
        try FileManager.default.createDirectory(at: root.appendingPathComponent("wiki"), withIntermediateDirectories: true)
        try FileManager.default.createDirectory(at: root.appendingPathComponent("docs"), withIntermediateDirectories: true)
        try Data("#!/usr/bin/env bash\n".utf8).write(to: root.appendingPathComponent("bin/llm-wiki"))
        try Data("# Agent Contract\n".utf8).write(to: root.appendingPathComponent("docs/agent-contract.md"))
        return root
    }

    private func writeSourcePage(root: URL, slug: String) throws {
        let sourceURL = root.appendingPathComponent("wiki/sources/\(slug).md")
        try FileManager.default.createDirectory(at: sourceURL.deletingLastPathComponent(), withIntermediateDirectories: true)
        try Data("# \(slug)\n".utf8).write(to: sourceURL)
    }
}
