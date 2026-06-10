import SwiftUI

struct SettingsView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        Form {
            Toggle("Show advanced engine surfaces", isOn: $store.isAdvancedMode)

            LabeledContent("Vault") {
                Text(store.vaultRoot?.path ?? "Not selected")
                    .foregroundStyle(.secondary)
                    .lineLimit(1)
            }
        }
        .padding(20)
        .frame(width: 520)
    }
}
