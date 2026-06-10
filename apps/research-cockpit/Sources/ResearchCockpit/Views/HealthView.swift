import SwiftUI

struct HealthView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                PageHeader(
                    title: "Health",
                    subtitle: "Plain-language checks for the vault, dependencies, generated files, and local engine availability."
                )

                Panel(title: "Checks") {
                    HStack {
                        PrimaryActionButton(
                            title: "Status",
                            systemImage: "chart.bar.doc.horizontal",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runStatus() }
                        }

                        PrimaryActionButton(
                            title: "Doctor",
                            systemImage: "cross.case",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runDoctor() }
                        }

                        PrimaryActionButton(
                            title: "Health",
                            systemImage: "heart.text.square",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHealth() }
                        }
                    }

                    HStack {
                        SecondaryActionButton(title: "Finder", systemImage: "folder") {
                            store.openVaultInFinder()
                        }
                        .disabled(store.vaultRoot == nil)

                        SecondaryActionButton(title: "Obsidian", systemImage: "square.on.square") {
                            store.openVaultInObsidian()
                        }
                        .disabled(store.vaultRoot == nil)

                        SecondaryActionButton(
                            title: "Hermes",
                            systemImage: "bolt.horizontal",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHermesStatus() }
                        }
                    }
                }

                Panel(title: "Findings") {
                    if store.healthFindings.isEmpty {
                        Text("Run Doctor or Health to populate findings.")
                            .foregroundStyle(.secondary)
                    } else {
                        ForEach(store.healthFindings) { finding in
                            FindingRow(finding: finding)
                            Divider()
                        }
                    }
                }

                if let lastError = store.lastError, !lastError.isEmpty {
                    Panel(title: "Last Error") {
                        Text(lastError)
                            .font(.caption.monospaced())
                            .textSelection(.enabled)
                            .foregroundStyle(.secondary)
                    }
                }

                CommandLogView(results: store.recentResults)
            }
            .padding(20)
        }
    }
}
