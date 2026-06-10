import ResearchCockpitCore
import SwiftUI

struct StudyView: View {
    @ObservedObject var store: CockpitStore
    @State private var queryText = ""

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                PageHeader(
                    title: "Study",
                    subtitle: "Generate study artifacts while keeping source files and outputs inside the vault."
                )

                Panel(title: "Actions") {
                    if let course = store.selectedCourse {
                        Text(course.courseName)
                            .font(.headline)
                        Text(course.studyFolder)
                            .font(.caption.monospaced())
                            .foregroundStyle(.secondary)

                        HStack {
                            PrimaryActionButton(
                                title: "Study Guide",
                                systemImage: "doc.text",
                                isDisabled: store.isBusy || course.sources.isEmpty
                            ) {
                                Task { await store.createStudyGuide() }
                            }
                            PrimaryActionButton(
                                title: "Quiz",
                                systemImage: "checklist",
                                isDisabled: store.isBusy || course.sources.isEmpty
                            ) {
                                Task { await store.generateQuiz() }
                            }
                            PrimaryActionButton(
                                title: "Flashcards",
                                systemImage: "rectangle.stack",
                                isDisabled: store.isBusy || course.sources.isEmpty
                            ) {
                                Task { await store.generateFlashcards() }
                            }
                        }

                        Divider()

                        HStack {
                            TextField("Search the compiled wiki", text: $queryText)
                                .textFieldStyle(.roundedBorder)
                            SecondaryActionButton(
                                title: "Search",
                                systemImage: "magnifyingglass",
                                isDisabled: queryText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || store.isBusy
                            ) {
                                Task {
                                    if let vaultRoot = store.vaultRoot {
                                        await store.run(
                                            CommandCatalog.query(queryText, vaultRoot: vaultRoot)
                                        )
                                    }
                                }
                            }
                        }
                    } else {
                        Text("Import or select a course before generating study outputs.")
                            .foregroundStyle(.secondary)
                    }
                }

                Panel(title: "Generated Outputs") {
                    if let course = store.selectedCourse, !course.generatedOutputs.isEmpty {
                        ForEach(course.generatedOutputs) { output in
                            HStack {
                                Image(systemName: icon(for: output.kind))
                                    .foregroundStyle(.secondary)
                                    .frame(width: 20)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text(output.title)
                                    Text(output.relativePath)
                                        .font(.caption.monospaced())
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                                Button {
                                    store.openRelativePath(output.relativePath)
                                } label: {
                                    Image(systemName: "arrow.up.right.square")
                                }
                                .buttonStyle(.borderless)
                                .disabled(output.relativePath.hasPrefix("Command log:"))
                            }
                            Divider()
                        }
                    } else {
                        Text("No generated outputs recorded yet.")
                            .foregroundStyle(.secondary)
                    }
                }

                CommandLogView(results: store.recentResults)
            }
            .padding(20)
        }
    }

    private func icon(for kind: GeneratedOutputKind) -> String {
        switch kind {
        case .studyGuide:
            return "doc.text"
        case .quiz:
            return "checklist"
        case .flashcards:
            return "rectangle.stack"
        case .reviewPlan:
            return "calendar"
        case .export:
            return "square.and.arrow.up"
        }
    }
}
