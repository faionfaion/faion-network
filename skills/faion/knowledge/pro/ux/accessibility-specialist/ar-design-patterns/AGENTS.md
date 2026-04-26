# AR Design Patterns

## Summary

Design patterns for augmented reality experiences on iOS (ARKit/RealityKit), Android (ARCore), WebAR (8th Wall, model-viewer), and social AR (Snap Lens Studio). Covers surface and object anchoring strategies, interaction patterns (touch, gaze, voice, controller), real/virtual distinction, safety considerations, comfort and performance constraints, and accessibility requirements per W3C XAUR.

## Why

Poor AR design causes disorientation, cognitive overload, and safety hazards when digital overlays obscure real-world objects. Battery life caps sessions at 10-20 minutes on phones; tracking quality varies by lighting, surface texture, and platform. AR-specific accessibility (voice alternatives, high-contrast overlays, gaze selection, exit affordance) is routinely omitted because designers default to touch-and-drag patterns that exclude motor-limited users.

## When To Use

- Designing AR experiences with spatial anchoring for iOS, Android, WebAR, or social AR platforms.
- Selecting an anchoring strategy (horizontal surface, vertical surface, image tracking, object recognition, geo).
- Auditing AR UX for safety, occlusion quality, accessibility, and performance.
- Building retail try-on, maintenance overlay, museum, navigation, or training AR flows.

## When NOT To Use

- Fully-immersive VR with occluded headset — use `vr-design-patterns`.
- Mixed-reality productivity (passthrough Quest / Vision Pro) — use `immersive-design-principles`.
- Pure 2D mobile UI that only overlays a camera feed without spatial anchoring — standard mobile UX applies.
- Low-power smart glasses with no spatial tracking — different constraints (voice-first display-only).

## Content

| File | What's inside |
|------|---------------|
| `content/01-anchoring-strategies.xml` | Anchoring types (horizontal, vertical, image, object, geo) with use cases, fallback chains, and tracking-quality rules. |
| `content/02-interaction-and-safety.xml` | Interaction patterns (touch, gaze, voice, controller), safety rules (obstacle avoidance, AR-free zones), accessibility requirements, performance constraints. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ar-anchor-schema.json` | Anchoring decision schema agents use to specify AR experience config including scale, tracking, lifecycle, exit, and accessibility. |
