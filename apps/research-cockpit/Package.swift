// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "ResearchCockpit",
    platforms: [
        .macOS(.v14)
    ],
    products: [
        .library(
            name: "ResearchCockpitCore",
            targets: ["ResearchCockpitCore"]
        ),
        .executable(
            name: "ResearchCockpit",
            targets: ["ResearchCockpit"]
        )
    ],
    targets: [
        .target(
            name: "ResearchCockpitCore"
        ),
        .executableTarget(
            name: "ResearchCockpit",
            dependencies: ["ResearchCockpitCore"]
        ),
        .testTarget(
            name: "ResearchCockpitCoreTests",
            dependencies: ["ResearchCockpitCore"]
        )
    ]
)
