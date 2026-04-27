# AI + Spatial Computing

## Summary

AI enables spatial interfaces (AR/VR/MR) to adapt contextually — recognizing environments, predicting gestures, routing voice commands, and powering gaze-based accessibility. This methodology covers AI-driven contextual UI adaptation, W3C XAUR accessibility gap analysis for XR apps, and privacy architecture for biometric/spatial data collection.

## Why

Spatial interfaces generate multi-modal sensor data (eye, hand, voice, environment) that static UI patterns cannot handle. AI scene understanding and gesture prediction reduce interaction steps and enable accessibility for motor and visual impairments. Convergence of on-device AI and XR hardware (Vision Pro, Quest 3, HoloLens) creates new UX categories that require purpose-built design patterns.

## When To Use

- Designing or auditing accessibility for AR/VR/MR applications targeting Apple Vision Pro, Meta Quest, or HoloLens
- Implementing AI-driven contextual UI adaptation (environment-aware UX) in a spatial application
- Generating XR accessibility documentation against W3C XAUR requirements
- Prototyping gaze, voice, or gesture interaction flows for spatial interfaces
- Evaluating privacy implications of AI + sensor data collection in a spatial product

## When NOT To Use

- Product targets only 2D web or mobile — spatial patterns add unnecessary complexity
- No access to XR hardware for validation — AI-generated spatial UX without device testing is unreliable
- Real-time AI inference cannot meet the &lt;20ms threshold — on-device AI is mandatory here
- Budget and timeline do not support specialized XR accessibility testing

## Content

| File | What's inside |
|------|---------------|
| `content/01-ai-capabilities.xml` | AI capability map for spatial computing; contextual adaptation patterns; predictive UI |
| `content/02-xr-accessibility.xml` | XAUR coverage per disability type; multi-modal input fallback hierarchy; privacy requirements |
| `content/03-anti-patterns.xml` | Latency constraints, gesture bias, gaze calibration failures, on-device compute limits, gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/interaction-fallback-spec.md` | Spatial interaction pattern spec: primary/secondary/tertiary input + privacy data fields |
| `templates/prompt-xaur-gap-analysis.txt` | Sonnet prompt: XR design spec → structured XAUR gap analysis with recommendations |
