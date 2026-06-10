import AppKit
import ResearchCockpitCore
import SwiftUI

struct ContentView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        NavigationSplitView {
            SidebarView(store: store)
        } detail: {
            DetailRouterView(store: store)
        }
        .toolbar {
            ToolbarItemGroup {
                Button {
                    chooseVault()
                } label: {
                    Label("Choose Vault", systemImage: "folder")
                }

                Button {
                    Task { await store.runDoctor(fast: true) }
                } label: {
                    Label("Doctor", systemImage: "cross.case")
                }
                .disabled(store.vaultRoot == nil || store.isBusy)

                Button {
                    Task { await store.runHealth() }
                } label: {
                    Label("Health", systemImage: "heart.text.square")
                }
                .disabled(store.vaultRoot == nil || store.isBusy)
            }
        }
    }

    private func chooseVault() {
        let panel = NSOpenPanel()
        panel.canChooseDirectories = true
        panel.canChooseFiles = false
        panel.allowsMultipleSelection = false
        panel.title = "Choose llm-knowledge-wiki Vault"
        panel.prompt = "Choose"
        if panel.runModal() == .OK, let url = panel.url {
            store.setVault(url)
        }
    }
}

private struct DetailRouterView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        switch store.selection {
        case .research:
            ResearchView(store: store)
        case .study:
            StudyView(store: store)
        case .schedule:
            ScheduleView(store: store)
        case .health:
            HealthView(store: store)
        case .engine:
            EngineView(store: store)
        }
    }
}
