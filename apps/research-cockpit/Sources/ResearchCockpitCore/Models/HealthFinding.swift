import Foundation

public enum HealthSeverity: String, Codable, Comparable, Sendable {
    case ok
    case warning
    case failure

    public static func < (lhs: HealthSeverity, rhs: HealthSeverity) -> Bool {
        order(lhs) < order(rhs)
    }

    private static func order(_ severity: HealthSeverity) -> Int {
        switch severity {
        case .ok:
            return 0
        case .warning:
            return 1
        case .failure:
            return 2
        }
    }
}

public struct HealthFinding: Identifiable, Equatable, Sendable {
    public var id: String
    public var severity: HealthSeverity
    public var title: String
    public var detail: String
    public var repairAction: String?

    public init(
        id: String,
        severity: HealthSeverity,
        title: String,
        detail: String,
        repairAction: String? = nil
    ) {
        self.id = id
        self.severity = severity
        self.title = title
        self.detail = detail
        self.repairAction = repairAction
    }
}
