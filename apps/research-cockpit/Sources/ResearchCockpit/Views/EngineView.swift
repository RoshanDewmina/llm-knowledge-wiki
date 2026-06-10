import SwiftUI

struct EngineView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                PageHeader(
                    title: "Engine",
                    subtitle: "Advanced Hermes, launchd, skills, and provider surfaces for repair and debugging."
                )

                Panel(title: "Hermes") {
                    HStack {
                        PrimaryActionButton(
                            title: "Status",
                            systemImage: "bolt.horizontal",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHermesStatus() }
                        }

                        PrimaryActionButton(
                            title: "Gateway",
                            systemImage: "network",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHermesGateway() }
                        }

                        PrimaryActionButton(
                            title: "Cron",
                            systemImage: "calendar.badge.clock",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHermesCronList() }
                        }
                    }

                    HStack {
                        SecondaryActionButton(
                            title: "Skills",
                            systemImage: "list.bullet.rectangle",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHermesSkillsList() }
                        }

                        SecondaryActionButton(
                            title: "LaunchAgent",
                            systemImage: "gearshape.2",
                            isDisabled: store.isBusy
                        ) {
                            Task { await store.runLaunchAgentStatus() }
                        }
                    }
                }

                Panel(title: "Findings") {
                    if store.healthFindings.isEmpty {
                        Text("Run an engine check to populate findings.")
                            .foregroundStyle(.secondary)
                    } else {
                        ForEach(store.healthFindings) { finding in
                            FindingRow(finding: finding)
                            Divider()
                        }
                    }
                }

                CommandLogView(results: store.recentResults)
            }
            .padding(20)
        }
    }
}
