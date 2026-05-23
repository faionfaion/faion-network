// swift-tools-version:5.10
// purpose: SwiftPM manifest scaffold wiring Harmonize as a dev-dependency for arch tests.
// consumes: ArchTests.swift target source list.
// produces: config (Package.swift wired to Harmonize).
// depends-on: content/02-output-contract.xml; templates/Package.swift.fragment; templates/ArchTests.swift.
// token-budget-impact: low — ~200 tokens.
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [.iOS(.v17), .macOS(.v14)],
    products: [
        .library(name: "Domain", targets: ["Domain"]),
        .library(name: "Presentation", targets: ["Presentation"]),
    ],
    dependencies: [
        .package(url: "https://github.com/perrystreetsoftware/Harmonize.git", from: "1.0.0"),
    ],
    targets: [
        .target(name: "Domain"),
        .target(name: "Presentation", dependencies: ["Domain"]),
        .testTarget(
            name: "ArchitectureTests",
            dependencies: [
                "Domain",
                "Presentation",
                .product(name: "Harmonize", package: "Harmonize"),
            ],
            path: "Tests/Architecture"
        ),
        .testTarget(name: "DomainTests", dependencies: ["Domain"]),
    ]
)
