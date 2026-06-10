import Foundation

public enum HealthInterpreter {
    public static func findings(fromDoctorJSON jsonText: String) -> [HealthFinding] {
        guard let data = jsonText.data(using: .utf8),
              let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
            return [
                HealthFinding(
                    id: "doctor-json",
                    severity: .warning,
                    title: "Doctor output was not machine-readable",
                    detail: "The app could not parse the doctor report.",
                    repairAction: "Open the command log and inspect the raw output."
                )
            ]
        }

        var findings: [HealthFinding] = []

        if let commands = object["commands"] as? [String: [String: Any]] {
            for (name, status) in commands.sorted(by: { $0.key < $1.key }) {
                if (status["ok"] as? Bool) == false {
                    findings.append(
                        HealthFinding(
                            id: "missing-command-\(name)",
                            severity: .failure,
                            title: "Missing dependency: \(name)",
                            detail: "The command `\(name)` is not available on PATH.",
                            repairAction: "Run `./bin/llm-wiki setup` or install the missing tool, then rerun Doctor."
                        )
                    )
                }
            }
        }

        if let obsidian = object["obsidian"] as? [String: Any],
           (obsidian["ok"] as? Bool) == false {
            findings.append(
                HealthFinding(
                    id: "obsidian-missing",
                    severity: .warning,
                    title: "Obsidian is unavailable",
                    detail: obsidian["detail"] as? String ?? "The Obsidian app or command could not be found.",
                    repairAction: "Install Obsidian or continue using the vault in Finder and the app."
                )
            )
        }

        if let paths = object["paths"] as? [String: [String: Any]] {
            for (path, status) in paths.sorted(by: { $0.key < $1.key }) {
                if (status["ok"] as? Bool) == false {
                    findings.append(
                        HealthFinding(
                            id: "missing-path-\(path)",
                            severity: .failure,
                            title: "Vault path missing: \(path)",
                            detail: "The selected folder does not contain the expected `\(path)` path.",
                            repairAction: "Choose the real llm-knowledge-wiki vault or restore the missing folder."
                        )
                    )
                }
            }
        }

        if let siteBuild = object["site_build"] as? [String: Any],
           (siteBuild["ok"] as? Bool) == false {
            findings.append(
                HealthFinding(
                    id: "site-build",
                    severity: .warning,
                    title: "Local site build failed",
                    detail: siteBuild["stderr"] as? String ?? "The site dependency or build step failed.",
                    repairAction: "Run `bun install` in `apps/site`, then rerun Doctor."
                )
            )
        }

        if let vaultChecks = object["vault_checks"] as? [String: Any],
           (vaultChecks["ok"] as? Bool) == false {
            findings.append(
                HealthFinding(
                    id: "vault-checks",
                    severity: .failure,
                    title: "Vault review checks failed",
                    detail: vaultChecks["stdout"] as? String ?? "The generated wiki checks reported a problem.",
                    repairAction: "Run `./bin/llm-wiki health` and review the generated queue."
                )
            )
        }

        if findings.isEmpty {
            findings.append(
                HealthFinding(
                    id: "doctor-ok",
                    severity: .ok,
                    title: "Core wiki checks passed",
                    detail: "The selected vault has the expected commands, folders, and app dependencies.",
                    repairAction: nil
                )
            )
        }

        return findings.sorted { $0.severity > $1.severity }
    }

    public static func findings(fromHermesOutput output: String, commandLabel: String) -> [HealthFinding] {
        let normalized = output.lowercased()
        if normalized.contains("not found") || normalized.contains("no such file") {
            return [
                HealthFinding(
                    id: "hermes-missing-\(Slug.make(commandLabel))",
                    severity: .warning,
                    title: "Hermes command is unavailable",
                    detail: "`\(commandLabel)` could not run on this Mac.",
                    repairAction: "Advanced users can reinstall or repair Hermes; normal study workflows can still use the local wiki."
                )
            ]
        }
        if normalized.contains("failed") || normalized.contains("error") || normalized.contains("429") {
            return [
                HealthFinding(
                    id: "hermes-warning-\(Slug.make(commandLabel))",
                    severity: .warning,
                    title: "Hermes needs attention",
                    detail: output.trimmingCharacters(in: .whitespacesAndNewlines),
                    repairAction: "Check provider keys, model settings, or the Hermes gateway before relying on scheduled work."
                )
            ]
        }
        return [
            HealthFinding(
                id: "hermes-ok-\(Slug.make(commandLabel))",
                severity: .ok,
                title: "Hermes responded",
                detail: output.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? "The command completed." : output,
                repairAction: nil
            )
        ]
    }
}
