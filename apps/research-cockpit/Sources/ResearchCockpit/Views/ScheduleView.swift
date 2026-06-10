import SwiftUI

struct ScheduleView: View {
    @ObservedObject var store: CockpitStore

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                PageHeader(
                    title: "Schedule",
                    subtitle: "Review the generated queue and scheduled Hermes work without exposing the engine by default."
                )

                Panel(title: "Review Loop") {
                    HStack {
                        PrimaryActionButton(
                            title: "Regenerate Reviews",
                            systemImage: "arrow.clockwise",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runReview() }
                        }

                        SecondaryActionButton(
                            title: "Cron Jobs",
                            systemImage: "calendar.badge.clock",
                            isDisabled: store.vaultRoot == nil || store.isBusy
                        ) {
                            Task { await store.runHermesCronList() }
                        }
                    }

                    if let course = store.selectedCourse {
                        Grid(alignment: .leading, horizontalSpacing: 16, verticalSpacing: 8) {
                            GridRow {
                                Text("Course").foregroundStyle(.secondary)
                                Text(course.courseName)
                            }
                            GridRow {
                                Text("Next review").foregroundStyle(.secondary)
                                Text(course.nextScheduledReview?.formatted(date: .abbreviated, time: .shortened) ?? "Not scheduled")
                            }
                            GridRow {
                                Text("Queue").foregroundStyle(.secondary)
                                Text("wiki/reviews/review-queue.md").font(.caption.monospaced())
                            }
                        }
                    }
                }

                CommandLogView(results: store.recentResults)
            }
            .padding(20)
        }
    }
}
