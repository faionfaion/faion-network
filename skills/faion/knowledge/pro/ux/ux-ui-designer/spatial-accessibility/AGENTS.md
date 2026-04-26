# Spatial Accessibility

## Summary

A methodology for designing AR/VR/MR interfaces that work across motor, visual, cognitive, and motion-sensitivity differences. Every spatial interaction must support at least two input modalities and have a non-spatial fallback. Seated-mode parity is mandatory — if an interaction requires standing or arm-raising, a seated alternative must be documented.

## Why

Spatial UI introduces accessibility barriers that standard WCAG 2.2 does not address: six-degrees-of-freedom movement, implicit hand-tracking assumptions, immersive field-of-view constraints, and motion sickness. Platform review guidelines (Apple HIG, Meta VRC.PC.UX) include accessibility checks; failure blocks store approval and poses injury risk in enterprise XR contexts.

## When To Use

- Designing AR/VR/MR experiences on Vision Pro, Quest, PS VR2, HoloLens, or WebXR.
- Adapting an existing flat UI for a spatial platform — need seated mode, gaze fallback, motion-comfort settings.
- Submitting an app to App Store or Meta Horizon Store.
- Designing enterprise XR (industrial training, medical) where injury risk is non-zero.

## When NOT To Use

- 2D mobile/desktop apps — use standard WCAG 2.2 / mobile a11y; spatial tradeoffs do not apply.
- Pure passthrough video apps with no UI overlay — accessibility reduces to standard video a11y (captions, contrast).
- Throwaway VR demos for a single internal user — full spatial-a11y program is overkill before validation.

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Input-modality matrix rules, seated-mode requirements, comfort settings, caption placement |
| `content/02-agent-patterns.xml` | Agentic audit workflow, subagent roles, prompt pattern, platform-specific gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/alt-input-matrix.ts` | TypeScript auditor: checks each interaction has minimum 2 input modalities |

## Scripts

none
