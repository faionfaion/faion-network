# Immersive Design Principles

## Problem

Immersion in VR/AR can overwhelm or disorient users. Poor immersive design causes motion sickness, fatigue, anxiety, and safety issues.

## Solution: Balanced Immersive Design

### Immersion Levels

| Level | Description | Example | When to Use |
|-------|-------------|---------|-------------|
| **Passthrough** | Real world + overlays | AR navigation on phone | Information overlay, maintain awareness |
| **Blended** | Mixed real/virtual | MR workspace with virtual monitors | Productivity, collaboration |
| **Immersive** | Full virtual environment | VR game, training simulation | Full focus, controlled environment |
| **Portal** | Windows into virtual | VR meeting room view | Limited immersion, easy exit |

### Design Guidelines

**Use Depth and Layering Thoughtfully:**
```
Near (0.5-2m):
→ UI elements, controls
→ Interactive objects
→ Readable text

Mid (2-10m):
→ Main content
→ Characters, objects
→ Interactive environment

Far (10m+):
→ Scenery, skybox
→ Ambient elements
→ Context setting
```

**Implement Realistic Motion Physics:**
- Objects fall naturally (gravity)
- Momentum and inertia applied
- Collisions feel real
- Audio matches motion
- Haptic feedback synchronized

**Respond to Environmental Context:**
```
Physical space detected:
→ Adjust content to room size
→ Warn about obstacles
→ Reposition UI for comfort
→ Adapt to lighting conditions
```

**Transition Smoothly Between Modes:**
- Gradual fade in/out (not instant)
- Audio cues for transitions
- Visual indicators of mode change
- User-initiated transitions preferred

**Ensure Immersion Enhances, Not Distracts:**
- Purpose-driven immersion
- Option to reduce immersion level
- Easy exit to reality
- Clear distinction between real/virtual

### Motion and Comfort

| Issue | Cause | Solution |
|-------|-------|----------|
| **Motion sickness** | Visual-vestibular mismatch | Fixed reference points, reduced motion, teleportation |
| **Disorientation** | Lost sense of direction | Clear grounding, consistent horizon, north indicator |
| **Eye strain** | Wrong depth of field | Proper convergence distance, focal point guidance |
| **Arm fatigue** | Prolonged interaction | Support positions, alternative inputs, rest prompts |
| **Neck strain** | Looking up/down too much | Comfortable viewing angles, UI at eye level |
| **Simulator sickness** | Frame rate drops, latency | 90+ FPS, <20ms latency, reduce complexity |

### Comfort Settings

**Motion Comfort:**
- Vignetting (reduce FOV during movement)
- Snap turning vs. smooth turning
- Teleportation vs. walking
- Speed control
- Comfort mode (ultra-safe settings)

**Visual Comfort:**
- Brightness adjustment
- Reduce particle effects
- Disable screen shake
- Remove motion blur
- High contrast mode

**Audio Comfort:**
- Volume control per source
- Spatial audio on/off
- Subtitles/captions
- Reduce ambient noise

**Interaction Comfort:**
- Seated mode available
- Controller-free options
- Voice commands
- Reduced precision requirements
- Auto-aim assistance

### Grounding and Reference

**Always provide visual grounding:**
```
Floor/ground plane:
→ Visible at all times
→ Consistent appearance
→ Provides stable reference
→ Clear boundaries

Horizon:
→ Fixed, expected position
→ Helps orientation
→ Reduces nausea
→ Sky/ground distinction
```

**Fixed reference objects:**
- Cockpit in vehicle sims
- Dashboard in driving
- Body awareness (hands, feet)
- Stable UI anchors

### Scale and Proportion

**Human-Scale Objects:**
```
1:1 scale for familiar objects:
→ Doors: 2m tall
→ Tables: 70-75cm high
→ Chairs: 45cm seat height
→ People: Average human size

Benefits:
→ Immediate recognition
→ Correct depth perception
→ Comfortable interaction
```

**Intentionally Different Scale:**
```
When scaling differently, make it obvious:
→ Miniature world: Clearly tiny
→ Giant objects: Clearly huge
→ Provide size reference (human for scale)
→ Transition gradually if changing scale
```

### Lighting and Atmosphere

**Consistent Lighting:**
- Matches real-world expectations
- Time of day appropriate
- Light sources visible
- Shadows enhance depth
- Not too dark (visibility)
- Not too bright (comfort)

**Atmospheric Effects:**
- Fog for depth perception
- Particles for scale reference
- Weather for immersion
- Adjustable/toggle for performance

### Boundaries and Safety

**Guardian/Chaperone System:**
- Visual boundary when approaching walls
- Haptic warning (controller vibration)
- Audio alert option
- Pause experience when crossing
- Easy re-centering

**Play Space:**
- Define minimum space requirements
- Warn if space too small
- Offer seated alternative
- Boundary color customization
- Opacity adjustment

### Accessibility in Immersive Environments

**Vision:**
- High contrast modes
- Large text options
- Audio descriptions
- Haptic feedback alternatives
- Voice navigation

**Hearing:**
- Visual captions for all audio
- Haptic feedback for sounds
- Visual indicators for directional audio
- Adjustable audio balance

**Mobility:**
- Seated mode fully functional
- Teleportation for movement
- Voice commands for all actions
- Controller-free options
- Adjustable height settings

**Cognitive:**
- Simplified UI mode
- Clear instructions
- Pauseable experiences
- No time pressure
- Difficulty adjustment

### Performance Requirements

**Frame Rate:**
```
Minimum: 90 FPS (VR)
Ideal: 120 FPS (VR)
AR: 60 FPS minimum
Never drop below minimum (causes sickness)
```

**Latency:**
```
Head tracking: <20ms
Controller input: <50ms
Visual feedback: <100ms
Exceeding causes disconnect
```

**Resolution:**
- Per-eye rendering
- Foveated rendering (performance)
- Supersampling for quality
- Dynamic resolution scaling

## Sources

- [Meta: VR Best Practices](https://developer.oculus.com/resources/bp-overview/)
- [Apple Vision Pro: Design for Spatial Computing](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)
- [Unity: XR Interaction Toolkit](https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest)
- [Google: Designing for Google Cardboard](https://designguidelines.withgoogle.com/cardboard/)
- [W3C: XR Accessibility User Requirements](https://www.w3.org/TR/xaur/)
