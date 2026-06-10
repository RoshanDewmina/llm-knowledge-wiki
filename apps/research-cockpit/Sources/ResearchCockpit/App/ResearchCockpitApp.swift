import SwiftUI

@main
struct ResearchCockpitApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate
    @StateObject private var store = CockpitStore()

    var body: some Scene {
        WindowGroup("Research Cockpit", id: "main") {
            ContentView(store: store)
                .frame(minWidth: 1040, minHeight: 680)
        }
        .commands {
            CommandMenu("Cockpit") {
                Button("Run Health") {
                    Task { await store.runHealth() }
                }
                .keyboardShortcut("h", modifiers: [.command, .shift])

                Button("Run Doctor") {
                    Task { await store.runDoctor(fast: true) }
                }
                .keyboardShortcut("d", modifiers: [.command, .shift])

                Divider()

                Button("Open Vault in Finder") {
                    store.openVaultInFinder()
                }
                .keyboardShortcut("o", modifiers: [.command, .shift])
            }
        }

        Settings {
            SettingsView(store: store)
        }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
    }
}
