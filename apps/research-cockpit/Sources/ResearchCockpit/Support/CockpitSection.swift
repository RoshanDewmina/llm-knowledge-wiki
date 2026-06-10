import Foundation

enum CockpitSection: String, CaseIterable, Identifiable {
    case research
    case study
    case schedule
    case health
    case engine

    var id: String { rawValue }

    var title: String {
        switch self {
        case .research:
            return "Research"
        case .study:
            return "Study"
        case .schedule:
            return "Schedule"
        case .health:
            return "Health"
        case .engine:
            return "Engine"
        }
    }

    var systemImage: String {
        switch self {
        case .research:
            return "tray.and.arrow.down"
        case .study:
            return "book.pages"
        case .schedule:
            return "calendar.badge.clock"
        case .health:
            return "stethoscope"
        case .engine:
            return "terminal"
        }
    }
}
