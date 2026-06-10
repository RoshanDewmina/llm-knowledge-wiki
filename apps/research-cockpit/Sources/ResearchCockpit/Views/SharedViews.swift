import ResearchCockpitCore
import SwiftUI

struct PageHeader: View {
    var title: String
    var subtitle: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.title2.weight(.semibold))
            Text(subtitle)
                .font(.callout)
                .foregroundStyle(.secondary)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}

struct Panel<Content: View>: View {
    var title: String?
    @ViewBuilder var content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            if let title {
                Text(title)
                    .font(.headline)
            }
            content
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }
}

struct PrimaryActionButton: View {
    var title: String
    var systemImage: String
    var isDisabled: Bool = false
    var action: () -> Void

    var body: some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
                .frame(maxWidth: .infinity)
        }
        .controlSize(.large)
        .buttonStyle(.borderedProminent)
        .disabled(isDisabled)
    }
}

struct SecondaryActionButton: View {
    var title: String
    var systemImage: String
    var isDisabled: Bool = false
    var action: () -> Void

    var body: some View {
        Button(action: action) {
            Label(title, systemImage: systemImage)
        }
        .buttonStyle(.bordered)
        .disabled(isDisabled)
    }
}

struct FindingRow: View {
    var finding: HealthFinding

    var body: some View {
        HStack(alignment: .top, spacing: 10) {
            Image(systemName: iconName)
                .foregroundStyle(color)
                .frame(width: 18)

            VStack(alignment: .leading, spacing: 4) {
                Text(finding.title)
                    .font(.subheadline.weight(.semibold))
                Text(finding.detail)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                    .lineLimit(3)
                if let repairAction = finding.repairAction {
                    Text(repairAction)
                        .font(.caption)
                        .foregroundStyle(.tertiary)
                }
            }
        }
    }

    private var iconName: String {
        switch finding.severity {
        case .ok:
            return "checkmark.circle.fill"
        case .warning:
            return "exclamationmark.triangle.fill"
        case .failure:
            return "xmark.octagon.fill"
        }
    }

    private var color: Color {
        switch finding.severity {
        case .ok:
            return .green
        case .warning:
            return .yellow
        case .failure:
            return .red
        }
    }
}

struct CommandLogView: View {
    var results: [CommandResult]

    var body: some View {
        Panel(title: "Command Log") {
            if results.isEmpty {
                Text("No commands run yet.")
                    .foregroundStyle(.secondary)
            } else {
                ForEach(results) { result in
                    DisclosureGroup {
                        VStack(alignment: .leading, spacing: 8) {
                            Text(result.commandLine)
                                .font(.caption.monospaced())
                                .foregroundStyle(.secondary)
                            Text(result.combinedOutput.isEmpty ? "No output." : result.combinedOutput)
                                .font(.caption.monospaced())
                                .textSelection(.enabled)
                        }
                        .padding(.top, 6)
                    } label: {
                        HStack {
                            Image(systemName: result.succeeded ? "checkmark.circle" : "xmark.circle")
                                .foregroundStyle(result.succeeded ? .green : .red)
                            Text(result.label)
                                .lineLimit(1)
                            Spacer()
                            Text("exit \(result.exitCode)")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                    Divider()
                }
            }
        }
    }
}
