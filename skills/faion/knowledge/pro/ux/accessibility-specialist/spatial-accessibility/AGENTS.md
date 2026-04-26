# Spatial Accessibility

## Summary

Accessibility methodology for spatial/XR interfaces (Apple Vision Pro, Meta Quest, HoloLens, WebXR) addressing motor limitations, visual and hearing impairment, cognitive load, and motion sensitivity. Core requirements: multiple simultaneous input modalities (gaze + voice + controller + hand), seated mode as the default, 3D captions that face the user, spatial audio navigation for blind users, and alignment with W3C XR Accessibility User Requirements (XAUR).

## Why

Traditional WCAG does not fully cover spatial environments. XAUR is a Working Draft, not normative — but it is the current best-practice reference. Screen reader support in XR is fragmented (VoiceOver works for visionOS native UI but not all Unity/WebXR content); eye-tracking dwell requires hardware (Vision Pro yes, Quest 2 no). Without explicit accessibility design, XR excludes wheelchair users (reach zones), blind users (no audio navigation), deaf users (no captions for spatial audio), and users with vestibular disorders (no locomotion alternatives).

## When To Use

- Designing or shipping for Apple Vision Pro, Meta Quest, HoloLens, Android XR, or WebXR.
- Adding accessibility features to an existing XR application pre-release.
- Auditing an immersive product against W3C XAUR.
- Enterprise XR (training, digital twins, remote assist) where ADA Title II or EAA may apply.
- Adding alternative input modalities to a single-modality XR experience.

## When NOT To Use

- 2D web/mobile a11y — use `a11y-testing` and WCAG 2.2 AA.
- Game-only experiences where motion is core gameplay — apply selectively to menus and settings only.
- Internal R&D prototypes never seen by real users.
- Where the platform's built-in a11y settings fully address user needs without custom work.

## Content

| File | What's inside |
|------|---------------|
| `content/01-input-and-visual.xml` | Multiple input modalities (gaze, voice, head tracking, controller, hand gestures), visual accessibility for blind and low-vision users (spatial audio, haptics, high-contrast). |
| `content/02-seated-mode-and-comfort.xml` | Seated mode implementation (UI positioning, locomotion, interaction zones), hearing accessibility (3D captions, haptic feedback), cognitive load reduction, comfort and safety settings. |

## Templates

| File | Purpose |
|------|---------|
| `templates/xr-scene-audit.py` | Python script auditing a scene manifest JSON for missing voice alias, gaze support, controller mapping, accessible description, and seated compatibility. |
