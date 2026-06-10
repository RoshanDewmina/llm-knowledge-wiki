import AppKit
import Foundation
import ResearchCockpitCore

@MainActor
final class CockpitStore: ObservableObject {
    @Published var selection: CockpitSection = .research
    @Published var isAdvancedMode: Bool = false
    @Published var vaultLocation: VaultLocation?
    @Published var courses: [CourseMetadata] = []
    @Published var selectedCourseID: String?
    @Published var healthFindings: [HealthFinding] = []
    @Published var recentResults: [CommandResult] = []
    @Published var activeCommandLabel: String?
    @Published var lastError: String?

    private let runner: CommandRunning

    init(runner: CommandRunning = ProcessCommandRunner()) {
        self.runner = runner
        self.vaultLocation = VaultLocator.findDefaultVault()
        reloadCourses()
    }

    var vaultRoot: URL? {
        vaultLocation?.root
    }

    var selectedCourse: CourseMetadata? {
        guard let selectedCourseID else {
            return courses.first
        }
        return courses.first { $0.id == selectedCourseID } ?? courses.first
    }

    var isBusy: Bool {
        activeCommandLabel != nil
    }

    func setVault(_ url: URL) {
        let location = VaultLocation(root: url)
        vaultLocation = location
        if !location.isValid {
            healthFindings = [
                HealthFinding(
                    id: "invalid-vault",
                    severity: .failure,
                    title: "This folder is not a wiki vault",
                    detail: "Choose a folder containing `bin/llm-wiki`, `raw/`, `wiki/`, and `docs/agent-contract.md`.",
                    repairAction: "Select `/Users/roshansilva/Documents/llm-knowledge-wiki` or run onboarding for a new vault."
                )
            ]
        }
        reloadCourses()
    }

    func reloadCourses() {
        guard let vaultRoot else {
            courses = []
            selectedCourseID = nil
            return
        }
        do {
            let store = CourseMetadataStore(vaultRoot: vaultRoot)
            courses = try store.loadAll()
            if selectedCourseID == nil || !courses.contains(where: { $0.id == selectedCourseID }) {
                selectedCourseID = courses.first?.id
            }
            lastError = nil
        } catch {
            lastError = error.localizedDescription
        }
    }

    func importCourseSources(inputURLs: [URL], courseName: String, term: String) async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        do {
            let metadataStore = CourseMetadataStore(vaultRoot: vaultRoot)
            let importer = CourseImporter(store: metadataStore)
            let summary = try importer.importSources(from: inputURLs, courseName: courseName, term: term)
            selectedCourseID = summary.course.id
            reloadCourses()

            for command in summary.ingestCommands {
                _ = await run(command)
            }
            reloadCourses()
        } catch {
            lastError = error.localizedDescription
        }
    }

    func createStudyGuide() async {
        guard let vaultRoot, var course = selectedCourse else {
            lastError = "Select a course first."
            return
        }
        do {
            let metadataStore = CourseMetadataStore(vaultRoot: vaultRoot)
            let importer = CourseImporter(store: metadataStore)
            let output = try importer.createStudyGuideScaffold(for: course)
            course.recordOutput(output)
            try metadataStore.save(course)
            reloadCourses()
            NSWorkspace.shared.activateFileViewerSelecting([
                vaultRoot.appendingPathComponent(output.relativePath)
            ])
        } catch {
            lastError = error.localizedDescription
        }
    }

    func generateQuiz() async {
        guard let vaultRoot, var course = selectedCourse else {
            lastError = "Select a course first."
            return
        }
        do {
            let metadataStore = CourseMetadataStore(vaultRoot: vaultRoot)
            let importer = CourseImporter(store: metadataStore)
            let output = try importer.createQuizScaffold(for: course)
            course.recordOutput(output)
            try metadataStore.save(course)
            reloadCourses()
            NSWorkspace.shared.activateFileViewerSelecting([
                vaultRoot.appendingPathComponent(output.relativePath)
            ])
        } catch {
            lastError = error.localizedDescription
        }
    }

    func generateFlashcards() async {
        guard let vaultRoot, var course = selectedCourse else {
            lastError = "Select a course first."
            return
        }
        do {
            let metadataStore = CourseMetadataStore(vaultRoot: vaultRoot)
            let importer = CourseImporter(store: metadataStore)
            let output = try importer.createFlashcardScaffold(for: course)
            course.recordOutput(output)
            try metadataStore.save(course)
            reloadCourses()
            NSWorkspace.shared.activateFileViewerSelecting([
                vaultRoot.appendingPathComponent(output.relativePath)
            ])
        } catch {
            lastError = error.localizedDescription
        }
    }

    func runReview() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        _ = await run(CommandCatalog.review(vaultRoot: vaultRoot))
    }

    func runStatus() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        _ = await run(CommandCatalog.status(vaultRoot: vaultRoot))
    }

    func runHealth() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        let result = await run(CommandCatalog.health(vaultRoot: vaultRoot))
        if result.succeeded {
            healthFindings = [
                HealthFinding(
                    id: "health-ok",
                    severity: .ok,
                    title: "Vault health completed",
                    detail: "Review pages, citation linting, and the site manifest were regenerated.",
                    repairAction: nil
                )
            ]
        } else {
            healthFindings = [
                HealthFinding(
                    id: "health-failed",
                    severity: .failure,
                    title: "Vault health failed",
                    detail: result.combinedOutput,
                    repairAction: "Open the command log, fix the reported wiki issue, then rerun Health."
                )
            ]
        }
    }

    func runDoctor(fast: Bool = false) async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        let result = await run(CommandCatalog.doctor(vaultRoot: vaultRoot, fast: fast))
        healthFindings = HealthInterpreter.findings(fromDoctorJSON: result.stdout)
    }

    func runHermesStatus() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        let result = await run(CommandCatalog.hermes(["status"], vaultRoot: vaultRoot, label: "Hermes Status"))
        healthFindings = HealthInterpreter.findings(fromHermesOutput: result.combinedOutput, commandLabel: result.label)
    }

    func runHermesGateway() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        let result = await run(CommandCatalog.hermes(["gateway", "status"], vaultRoot: vaultRoot, label: "Hermes Gateway"))
        healthFindings = HealthInterpreter.findings(fromHermesOutput: result.combinedOutput, commandLabel: result.label)
    }

    func runHermesCronList() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        _ = await run(CommandCatalog.hermes(["cron", "list"], vaultRoot: vaultRoot, label: "Hermes Cron Jobs"))
    }

    func runHermesSkillsList() async {
        guard let vaultRoot else {
            lastError = "Choose a wiki vault first."
            return
        }
        _ = await run(CommandCatalog.hermes(["skills", "list"], vaultRoot: vaultRoot, label: "Hermes Skills"))
    }

    func runLaunchAgentStatus() async {
        _ = await run(CommandCatalog.launchctlGatewayStatus())
    }

    func openVaultInFinder() {
        guard let vaultRoot else { return }
        NSWorkspace.shared.activateFileViewerSelecting([vaultRoot])
    }

    func openVaultInObsidian() {
        guard let vaultRoot else { return }
        NSWorkspace.shared.openApplication(
            at: URL(fileURLWithPath: "/Applications/Obsidian.app"),
            configuration: {
                let configuration = NSWorkspace.OpenConfiguration()
                configuration.arguments = [vaultRoot.path]
                return configuration
            }(),
            completionHandler: nil
        )
    }

    func openRelativePath(_ relativePath: String) {
        guard let vaultRoot, !relativePath.hasPrefix("Command log:") else { return }
        let target = vaultRoot.appendingPathComponent(relativePath)
        NSWorkspace.shared.open(target)
    }

    @discardableResult
    func run(_ command: ShellCommand) async -> CommandResult {
        activeCommandLabel = command.label
        let result = await runner.run(command)
        activeCommandLabel = nil
        recentResults.insert(result, at: 0)
        recentResults = Array(recentResults.prefix(20))
        lastError = result.succeeded ? nil : result.combinedOutput
        return result
    }

}
