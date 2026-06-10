import AppKit
import ResearchCockpitCore
import SwiftUI

struct ResearchView: View {
    @ObservedObject var store: CockpitStore
    @State private var courseName = ""
    @State private var term = ""
    @State private var selectedSourceURLs: [URL] = []

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                PageHeader(
                    title: "Research",
                    subtitle: "Import a course pack into the local Markdown vault and ingest each source through llm-wiki."
                )

                HStack(alignment: .top, spacing: 16) {
                    Panel(title: "Course Pack") {
                        TextField("Course name", text: $courseName)
                            .textFieldStyle(.roundedBorder)
                        TextField("Term", text: $term)
                            .textFieldStyle(.roundedBorder)

                        HStack {
                            SecondaryActionButton(
                                title: selectedSourceURLs.isEmpty ? "Choose Sources" : "\(selectedSourceURLs.count) Selected",
                                systemImage: "plus.square.on.square"
                            ) {
                                chooseSources()
                            }

                            PrimaryActionButton(
                                title: "Import and Ingest",
                                systemImage: "tray.and.arrow.down",
                                isDisabled: courseName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty || selectedSourceURLs.isEmpty || store.vaultRoot == nil || store.isBusy
                            ) {
                                Task {
                                    await store.importCourseSources(
                                        inputURLs: selectedSourceURLs,
                                        courseName: courseName,
                                        term: term
                                    )
                                    selectedSourceURLs = []
                                }
                            }
                        }

                        if !selectedSourceURLs.isEmpty {
                            VStack(alignment: .leading, spacing: 4) {
                                ForEach(selectedSourceURLs, id: \.path) { url in
                                    Label(url.lastPathComponent, systemImage: "doc")
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                }
                            }
                        }
                    }
                    .frame(maxWidth: 420)

                    CourseOverviewPanel(store: store)
                }

                CoursesPanel(store: store)
                CommandLogView(results: store.recentResults)
            }
            .padding(20)
        }
    }

    private func chooseSources() {
        let panel = NSOpenPanel()
        panel.canChooseFiles = true
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = true
        panel.title = "Choose course pack files or folders"
        panel.prompt = "Add"
        if panel.runModal() == .OK {
            selectedSourceURLs = panel.urls
        }
    }
}

private struct CourseOverviewPanel: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        Panel(title: "Selected Course") {
            if let course = store.selectedCourse {
                Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 8) {
                    GridRow {
                        Text("Course").foregroundStyle(.secondary)
                        Text(course.courseName)
                    }
                    GridRow {
                        Text("Term").foregroundStyle(.secondary)
                        Text(course.term.isEmpty ? "Unspecified" : course.term)
                    }
                    GridRow {
                        Text("Sources").foregroundStyle(.secondary)
                        Text("\(course.sources.count)")
                    }
                    GridRow {
                        Text("Outputs").foregroundStyle(.secondary)
                        Text("\(course.generatedOutputs.count)")
                    }
                    GridRow {
                        Text("Raw").foregroundStyle(.secondary)
                        Text(course.rawFolder).font(.caption.monospaced())
                    }
                }

                HStack {
                    SecondaryActionButton(title: "Finder", systemImage: "folder") {
                        store.openRelativePath(course.studyFolder)
                    }
                    SecondaryActionButton(title: "Scaffold Guide", systemImage: "doc.badge.plus") {
                        Task { await store.createStudyGuide() }
                    }
                    .disabled(store.isBusy || course.sources.isEmpty)
                }
            } else {
                Text("Import a course pack to start.")
                    .foregroundStyle(.secondary)
            }
        }
    }
}

private struct CoursesPanel: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        Panel(title: "Courses") {
            if store.courses.isEmpty {
                Text("No course metadata found in `.research-cockpit/courses`.")
                    .foregroundStyle(.secondary)
            } else {
                Table(store.courses, selection: $store.selectedCourseID) {
                    TableColumn("Course") { course in
                        VStack(alignment: .leading, spacing: 2) {
                            Text(course.courseName)
                            Text(course.slug)
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    TableColumn("Term") { course in
                        Text(course.term.isEmpty ? "Unspecified" : course.term)
                    }
                    TableColumn("Sources") { course in
                        Text("\(course.sources.count)")
                    }
                    TableColumn("Outputs") { course in
                        Text("\(course.generatedOutputs.count)")
                    }
                }
                .frame(minHeight: 180)
            }
        }
    }
}
