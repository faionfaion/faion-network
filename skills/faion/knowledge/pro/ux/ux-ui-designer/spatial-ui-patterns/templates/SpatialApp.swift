// SpatialApp.swift — minimal visionOS scene scaffold
// Demonstrates: WindowGroup (body-locked 2D panel), second WindowGroup (tool palette),
// ImmersiveSpace (world-anchored 3D content).
// Only one ImmersiveSpace may be active at a time.
// Requires visionOS 1.0+, RealityKit, SwiftUI.
import SwiftUI
import RealityKit

@main
struct SpatialApp: App {
    @State private var immersionStyle: ImmersionStyle = .mixed

    var body: some Scene {
        // Primary panel — body-locked-ish 2D window (default visionOS window)
        WindowGroup(id: "main") {
            ContentView()
        }
        .windowStyle(.plain)
        .defaultSize(width: 800, height: 600)

        // Tool palette — secondary 2D window, user positions it
        WindowGroup(id: "tools") {
            ToolPaletteView()
        }
        .windowResizability(.contentSize)

        // World-anchored 3D immersive space — activate on demand, one at a time
        ImmersiveSpace(id: "scene") {
            RealityView { content in
                // Anchor at head position for initial placement; user moves it
                let anchor = AnchorEntity(.head)
                anchor.position = [0, 0, -1.5]  // 1.5 m in front, safe comfort distance
                content.add(anchor)
            }
        }
        .immersionStyle(selection: $immersionStyle, in: .mixed)
    }
}

// MARK: - Placeholder views
struct ContentView: View {
    var body: some View { Text("Main Panel") }
}

struct ToolPaletteView: View {
    var body: some View { Text("Tools") }
}
