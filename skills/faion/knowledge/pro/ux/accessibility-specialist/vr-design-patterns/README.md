# VR Design Patterns

## Problem

Full VR lacks real-world context and can cause discomfort, disorientation, and motion sickness. Poor VR design creates barriers for users with disabilities and excludes many potential users.

## Solution: User-Centered VR Design

### VR Environment Design

| Element | Guideline | Purpose |
|---------|-----------|---------|
| **Ground plane** | Always visible, stable surface | Orientation reference, prevents floating feeling |
| **Horizon** | Stable, expected position | Reduces nausea, maintains orientation |
| **Scale** | Human-scale or clearly different | Depth perception, familiarity, comfort |
| **Lighting** | Consistent, comfortable | Visibility without eye strain |
| **Boundaries** | Guardian/chaperone visible | Safety, prevents collisions |
| **Reference objects** | Stable elements (cockpit, dashboard) | Grounding, reduces motion sickness |

### Locomotion Methods

| Method | Comfort Level | Use Case | Accessibility |
|--------|---------------|----------|---------------|
| **Teleportation** | High | General movement | Best for seated users, wheelchair users |
| **Walking (room-scale)** | High | Limited area | Excludes wheelchair users, limited mobility |
| **Controller movement** | Medium | Exploration | Motion sickness risk, needs alternatives |
| **Vehicle/seat** | High | Seated experiences | Wheelchair-friendly, comfortable |
| **Flying** | Low-Medium | Specific use cases | High nausea risk, needs comfort settings |
| **Arm swinging** | Medium | Exercise, immersion | Fatigue risk, exclude motor disabilities |

**Best practice: Offer multiple locomotion options**

### UI in VR

**UI Panel Placement:**
```
Floating panels:
→ 1.5-3m from user
→ Eye level (sitting or standing)
→ Curved to match viewing angle
→ Follow user (diegetic) or world-locked

Never:
→ Lock to head directly (causes nausea)
→ Place too close (<0.5m)
→ Place too far (>10m)
→ Require extreme neck angles
```

**UI Integration:**
```
Diegetic UI (in-world):
→ Holographic displays
→ Screens on objects
→ Wrist-mounted interfaces
→ Feels natural in environment

Non-diegetic UI (meta):
→ Pause menus
→ Settings
→ Health/status bars
→ Needs clear visual distinction
```

**Spatial Audio Feedback:**
- Confirm button press with sound
- 3D positioning of sound sources
- Haptic feedback synchronized
- Audio cues for out-of-view events

**Gaze + Confirm Selection:**
```
User flow:
1. Look at object (gaze)
2. Object highlights
3. Press button to confirm (or dwell)
4. Feedback confirms selection

Benefits:
→ Precise selection
→ Works from distance
→ Accessible (no hand movement)
→ Natural interaction
```

### Comfort and Safety

**Motion Sickness Prevention:**

**Vignetting (Tunnel Vision):**
```
Reduce field of view during movement:
→ Keep center clear
→ Darken/blur edges
→ Intensity based on speed
→ Reduces visual-vestibular mismatch
```

**Fixed Reference Points:**
- Cockpit, vehicle interior
- Ground plane always visible
- Horizon line stable
- Body presence (hands, feet)

**Smooth vs. Snap Turning:**
```
Snap turning (comfort):
→ Instant rotation (15°, 30°, 45°)
→ No smooth rotation
→ Less nausea
→ Preferred for comfort

Smooth turning (immersion):
→ Gradual rotation
→ More immersive
→ Higher nausea risk
→ Offer speed control
```

**Comfort Settings Required:**
- Movement speed control
- Snap vs. smooth turning
- Vignette intensity
- Teleport vs. smooth movement
- Seated mode
- Reduce visual effects

### Accessibility in VR

**Vision:**
- High contrast mode
- Large text options (min 14-16pt)
- Color blind safe palettes
- Audio descriptions for visual elements
- Screen reader integration (experimental)

**Hearing:**
- Visual captions in 3D space
- Subtitle size/position adjustable
- Haptic feedback for sounds
- Visual indicators (flash for alerts)
- Volume controls per source

**Mobility:**
- Seated mode fully functional
- All content reachable when seated
- Teleportation for movement
- Voice commands for all actions
- Controller-free options
- Adjustable height settings

**Cognitive:**
- Simplified UI mode
- Clear, step-by-step tutorials
- No time pressure
- Pauseable experiences
- Difficulty adjustment
- Memory aids (hints, reminders)

### Interaction Patterns

**Hand Controllers:**
```
Trigger: Primary action (grab, shoot)
Grip: Secondary action (hold, grip)
Touchpad/Stick: Movement, menu navigation
Buttons: Jump, interact, menu
```

**Gaze-Based:**
- Look at object to highlight
- Dwell (2 seconds) to select
- Look away to cancel
- Accessible alternative to hand input

**Voice Commands:**
- "Select [object]"
- "Menu"
- "Pause"
- "Help"
- Essential accessibility feature

**Hand Tracking (controller-free):**
- Pinch to select
- Grab to hold
- Point to direct
- Natural but less precise

### Performance Requirements

**Frame Rate:**
```
Minimum: 90 FPS per eye
Ideal: 120 FPS per eye
Never drop below minimum
Reprojection as fallback
```

**Latency:**
```
Motion-to-photon: <20ms total
Head tracking: <10ms
Controller tracking: <10ms
Visual update: <10ms
```

**Resolution:**
- Per-eye rendering
- Foveated rendering (reduce edges)
- Supersampling for clarity
- Dynamic resolution to maintain FPS

### Testing VR Experiences

**Test with diverse users:**
- First-time VR users
- Experienced VR users
- People prone to motion sickness
- Wheelchair users (seated mode)
- Various heights and builds
- Left and right-handed users
- People with disabilities

**Test scenarios:**
- Extended sessions (30+ minutes)
- Different comfort settings
- Seated vs. standing
- Various room sizes
- Poor tracking conditions
- Low/high framerates
- Different IPD settings

### Common Mistakes

1. **Head-locked UI** - UI follows head movement (instant nausea)
2. **Smooth movement only** - No teleport option (excludes many users)
3. **No seated mode** - Requires standing/walking (excludes wheelchair users)
4. **Small text** - Unreadable in VR (min 14-16pt)
5. **No comfort options** - One-size-fits-all (some users can't use)
6. **Extreme neck angles** - UI too high/low (neck strain)
7. **No grounding** - Floating in void (disorientation)
8. **Frame drops** - Performance issues (motion sickness)

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implement vr-design-patterns pattern | haiku | Straightforward implementation |
| Review vr-design-patterns implementation | sonnet | Requires code analysis |
| Optimize vr-design-patterns design | opus | Complex trade-offs |

## Sources

- [Meta: VR Best Practices](https://developer.oculus.com/resources/bp-overview/)
- [Valve: VR Design Guidelines](https://steamcommunity.com/sharedfiles/filedetails/?id=1537149895)
- [Unity: VR Best Practices](https://docs.unity3d.com/Manual/VRBestPractices.html)
- [Google: Designing for Google Cardboard](https://designguidelines.withgoogle.com/cardboard/)
- [W3C: XR Accessibility User Requirements](https://www.w3.org/TR/xaur/)
