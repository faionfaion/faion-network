# Spatial UI Patterns

## Problem

Traditional UI components don't work in 3D space.

## Panel Types

| Type | Behavior | Use Case |
|------|----------|----------|
| World-locked | Fixed in space | Reference content |
| Head-locked | Follows gaze | HUD, notifications |
| Body-locked | Follows position | Menus, tools |
| Hand-attached | On hand/wrist | Quick access |

## Window Management

- Multiple floating windows
- Snap to surfaces
- Group related windows
- Minimize to dock
- Spatial memory (return to position)

## Best Practices

**DO:**
- Provide visual anchors
- Maintain consistent scale
- Use depth for hierarchy
- Respect personal space

**DON'T:**
- Place UI too close to face
- Require constant arm raising
- Use tiny touch targets
- Ignore field of view limits

## Sources

- [Apple visionOS Design Principles](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)
- [Meta XR UI Guidelines](https://developer.oculus.com/resources/oculus-design-guidelines/)
- [Spatial UI Best Practices](https://www.nngroup.com/articles/spatial-ui/)
- [Window Management in XR](https://docs.unity3d.com/Packages/com.unity.xr.windowsmr@latest/)
- [3D Interface Design](https://www.interaction-design.org/literature/article/3d-ui-design)
