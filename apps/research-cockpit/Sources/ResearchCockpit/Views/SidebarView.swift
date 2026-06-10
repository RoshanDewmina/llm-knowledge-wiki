import SwiftUI

struct SidebarView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        VStack(spacing: 0) {
            List(selection: $store.selection) {
                ForEach(CockpitSection.allCases.filter { store.isAdvancedMode || $0 != .engine }) { section in
                    Label(section.title, systemImage: section.systemImage)
                        .tag(section)
                }
            }
            .listStyle(.sidebar)

            Divider()

            VStack(alignment: .leading, spacing: 10) {
                Toggle("Advanced", isOn: $store.isAdvancedMode)
                    .toggleStyle(.switch)

                if let vaultRoot = store.vaultRoot {
                    Label(vaultRoot.lastPathComponent, systemImage: "externaldrive")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                } else {
                    Label("No vault selected", systemImage: "exclamationmark.triangle")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                if let active = store.activeCommandLabel {
                    Label(active, systemImage: "hourglass")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                        .lineLimit(1)
                }
            }
            .padding(12)
        }
    }
}
