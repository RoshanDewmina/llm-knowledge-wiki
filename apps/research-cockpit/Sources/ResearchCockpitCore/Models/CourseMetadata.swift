import Foundation

public enum CourseSourceKind: String, Codable, CaseIterable, Sendable {
    case pdf
    case note
    case slide
    case transcript
    case link
    case image
    case other

    public static func infer(from url: URL) -> CourseSourceKind {
        let extensionName = url.pathExtension.lowercased()
        switch extensionName {
        case "pdf":
            return .pdf
        case "md", "markdown", "txt", "rtf":
            return .note
        case "ppt", "pptx", "key":
            return .slide
        case "vtt", "srt", "transcript":
            return .transcript
        case "url", "webloc":
            return .link
        case "png", "jpg", "jpeg", "heic", "gif", "tiff":
            return .image
        default:
            return .other
        }
    }
}

public struct CourseSource: Codable, Equatable, Identifiable, Sendable {
    public var id: UUID
    public var displayName: String
    public var sourceKind: CourseSourceKind
    public var rawRelativePath: String
    public var originalPath: String?
    public var sourcePageSlug: String?
    public var importedAt: Date

    public init(
        id: UUID = UUID(),
        displayName: String,
        sourceKind: CourseSourceKind,
        rawRelativePath: String,
        originalPath: String?,
        sourcePageSlug: String? = nil,
        importedAt: Date = Date()
    ) {
        self.id = id
        self.displayName = displayName
        self.sourceKind = sourceKind
        self.rawRelativePath = rawRelativePath
        self.originalPath = originalPath
        self.sourcePageSlug = sourcePageSlug
        self.importedAt = importedAt
    }
}

public enum GeneratedOutputKind: String, Codable, CaseIterable, Sendable {
    case studyGuide
    case quiz
    case flashcards
    case reviewPlan
    case export
}

public struct GeneratedOutput: Codable, Equatable, Identifiable, Sendable {
    public var id: UUID
    public var kind: GeneratedOutputKind
    public var title: String
    public var relativePath: String
    public var commandLine: String
    public var generatedAt: Date

    public init(
        id: UUID = UUID(),
        kind: GeneratedOutputKind,
        title: String,
        relativePath: String,
        commandLine: String,
        generatedAt: Date = Date()
    ) {
        self.id = id
        self.kind = kind
        self.title = title
        self.relativePath = relativePath
        self.commandLine = commandLine
        self.generatedAt = generatedAt
    }
}

public struct CourseMetadata: Codable, Equatable, Identifiable, Sendable {
    public var id: String { slug }

    public var slug: String
    public var courseName: String
    public var term: String
    public var rawFolder: String
    public var studyFolder: String
    public var sources: [CourseSource]
    public var generatedOutputs: [GeneratedOutput]
    public var lastHealthStatus: String
    public var providerStatus: String
    public var nextScheduledReview: Date?
    public var createdAt: Date
    public var updatedAt: Date

    public init(
        slug: String,
        courseName: String,
        term: String,
        rawFolder: String? = nil,
        studyFolder: String? = nil,
        sources: [CourseSource] = [],
        generatedOutputs: [GeneratedOutput] = [],
        lastHealthStatus: String = "Not checked",
        providerStatus: String = "Not checked",
        nextScheduledReview: Date? = nil,
        createdAt: Date = Date(),
        updatedAt: Date = Date()
    ) {
        self.slug = slug
        self.courseName = courseName
        self.term = term
        self.rawFolder = rawFolder ?? "raw/courses/\(slug)"
        self.studyFolder = studyFolder ?? "wiki/studies/courses/\(slug)"
        self.sources = sources
        self.generatedOutputs = generatedOutputs
        self.lastHealthStatus = lastHealthStatus
        self.providerStatus = providerStatus
        self.nextScheduledReview = nextScheduledReview
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    }

    public static func newCourse(courseName: String, term: String) -> CourseMetadata {
        let slugBase = [courseName, term]
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
            .joined(separator: " ")
        let slug = Slug.make(slugBase)
        return CourseMetadata(slug: slug, courseName: courseName, term: term)
    }

    public mutating func recordSources(_ newSources: [CourseSource]) {
        sources.append(contentsOf: newSources)
        updatedAt = Date()
    }

    public mutating func recordOutput(_ output: GeneratedOutput) {
        generatedOutputs.removeAll { $0.relativePath == output.relativePath && $0.kind == output.kind }
        generatedOutputs.append(output)
        updatedAt = Date()
    }
}
