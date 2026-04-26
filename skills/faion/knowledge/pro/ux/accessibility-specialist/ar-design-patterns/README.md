# AR Design Patterns

## Problem

AR must blend seamlessly with the real world without overwhelming users or obscuring important environmental information. Poor AR design causes disorientation, cognitive overload, and safety issues.

## Solution: Context-Aware AR Design

### AR Use Cases and Patterns

| Use Case | Pattern | Example |
|----------|---------|---------|
| **Navigation** | Ground-level overlays, directional arrows | Walking directions on sidewalk |
| **Shopping** | Product visualization at scale | Furniture in your room |
| **Training** | Step-by-step guidance overlays | Assembly instructions on object |
| **Collaboration** | Shared annotations in space | Team reviewing 3D model |
| **Information** | Contextual labels and data | Museum exhibit details |
| **Gaming** | World-anchored objects | Pokémon in environment |
| **Maintenance** | Diagnostic overlays | Car engine repair guide |
| **Accessibility** | Real-time translation, audio descriptions | Sign language translation |

### Placement Strategies

**Surface Detection:**
```
Horizontal surfaces:
→ Tables: Documents, 3D models
→ Floors: Large objects, navigation paths
→ Desks: Work tools, controls

Vertical surfaces:
→ Walls: Posters, dashboards, media
→ Doors: Labels, signs
→ Windows: Information overlays

Best practices:
→ Content snaps to detected surfaces
→ Respect physical boundaries
→ Avoid floating mid-air (unstable)
→ Adjust for surface size
```

**Object Recognition:**
```
Attach AR to real objects:
→ Product packaging: Instructions, nutrition
→ Business cards: Contact details
→ Posters: Video content, links
→ Tools: Usage guides
→ Books: Author info, reviews

Scale appropriately:
→ Match object size
→ Update with object movement
→ Fade when object moves out of frame
→ Provide stable anchoring
```

**Image Tracking:**
```
Recognize specific images:
→ Markers and QR codes
→ Logos and branding
→ Natural feature tracking
→ Multiple simultaneous targets

Tracking quality:
→ High contrast images work best
→ Avoid reflective surfaces
→ Good lighting required
→ Fallback to GPS/compass
```

### Design Principles

**1. Respect the Real Environment**
```
Don't:
→ Obscure important real-world objects
→ Block safety hazards from view
→ Overwhelm environment with AR
→ Ignore physical constraints

Do:
→ Keep AR content minimal
→ Make AR dismissible
→ Provide transparency options
→ Allow "AR-free" zones
```

**2. Use Lighting to Integrate**
```
Match environmental lighting:
→ Time of day (sunlight vs. artificial)
→ Light source direction
→ Shadows cast appropriately
→ Reflections on shiny objects

Benefits:
→ AR feels part of real world
→ Reduces uncanny valley effect
→ Better depth perception
→ More realistic experience
```

**3. Clear Virtual/Real Distinction**
```
Users should always know what's real:
→ Subtle visual cues (glow, outline)
→ Different visual treatment
→ Labels for AR content
→ Toggle AR on/off easily

Never:
→ Make AR indistinguishable from reality
→ Hide controls to disable AR
→ Force AR when not needed
```

**4. Allow Environment Scanning**
```
Give user control:
→ Show what device can see
→ Indicate good vs. bad surfaces
→ Warn about poor tracking
→ Let user re-scan if needed

Feedback:
→ "Looking for surfaces..."
→ "Good tracking" indicators
→ "Move device slowly"
→ "More light needed"
```

### Interaction Patterns

**Touch Gestures:**
- Tap to select AR object
- Drag to move object
- Pinch to scale
- Two-finger rotate
- Long press for options

**Gaze and Dwell:**
- Look at object to highlight
- Hold gaze to select (dwell time)
- Look away to deselect
- Accessibility-friendly (no tapping)

**Voice Commands:**
- "Show more information"
- "Hide AR content"
- "Move to table"
- "Make bigger/smaller"
- Essential for accessibility

**Controller/Hardware:**
- Dedicated AR glasses buttons
- Phone volume buttons for actions
- External Bluetooth controllers
- Gamepad support

### Accessibility Considerations

**Visual Accessibility:**
- High contrast AR elements
- Adjustable text size in AR
- Color blind safe palettes
- Option to disable AR entirely

**Motor Accessibility:**
- Voice control for all AR interactions
- Gaze-based selection
- Large tap targets (44x44px minimum)
- Reduce precision requirements

**Cognitive Accessibility:**
- Simple, clear AR interfaces
- Not too much information at once
- Predictable behavior
- Easy exit from AR mode

**Safety:**
- Audio warnings for obstacles
- Reduce AR when moving
- "Safety mode" dims AR
- Haptic warnings for collisions

### Performance and Comfort

**Frame Rate:**
- Minimum 30 FPS (60 FPS ideal)
- Consistent frame timing
- Reduce content if FPS drops
- Warn user about performance

**Battery and Heat:**
- AR is power-intensive
- Provide battery status
- Thermal warnings
- Option to reduce quality

**Motion Comfort:**
- Smooth transitions
- Avoid rapid camera movements
- Gradual AR appearance/disappearance
- Match physical movement

### Testing AR Experiences

**Test in varied environments:**
- Bright outdoor lighting
- Low indoor lighting
- Different surface types
- Various room sizes
- Moving environments

**Test with diverse users:**
- Different heights (AR placement)
- Left and right-handed
- People with disabilities
- Different device types
- Varied internet speeds

### Common Mistakes

1. **Ignoring Environment** - AR that doesn't adapt to space
2. **Too Much Information** - Overwhelming AR overlays
3. **Poor Occlusion** - AR objects don't hide behind real objects
4. **Unstable Tracking** - Jittery, drifting AR content
5. **No Safety Consideration** - AR blocks hazards from view

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement ar-design-patterns pattern | haiku | Straightforward implementation |
| Review ar-design-patterns implementation | sonnet | Requires code analysis |
| Optimize ar-design-patterns design | opus | Complex trade-offs |

## Sources

- [Apple ARKit: Design Guidelines](https://developer.apple.com/design/human-interface-guidelines/ar)
- [Google ARCore: Best Practices](https://developers.google.com/ar/develop/best-practices)
- [Meta Spark AR: Design Guide](https://sparkar.facebook.com/ar-studio/learn/documentation/designing-experiences/)
- [W3C: XR Accessibility User Requirements](https://www.w3.org/TR/xaur/)
- [Nielsen Norman Group: AR UX](https://www.nngroup.com/articles/ar-ux/)
