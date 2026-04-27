# AI + Spatial Computing

## Summary

Methodology for designing XR (AR/VR/MR) interfaces that adapt to physical environment context using AI scene understanding, gesture prediction, voice integration, and personalization. Covers depth-layer layout, gaze-target sizing, scene-type decision matrices, and graceful degradation for AI failures on Apple Vision Pro, Meta Quest, and WebXR platforms.

## Why

Spatial interfaces generate complex contextual data that static UI rules cannot handle. AI scene classification enables UIs to auto-adapt layouts, pre-position relevant content, and anticipate user intent — reducing interaction friction in environments where traditional 2D patterns fail. Without explicit AI fallback design, failures in scene understanding or gesture prediction degrade UX to zero.

## When To Use

- Designing XR (AR/VR/MR) interfaces that must adapt to physical environment context
- Building AI-driven spatial UI that pre-positions content based on scene understanding
- Generating spatial layout specifications for Apple Vision Pro, Meta Quest, or WebXR targets
- Auditing existing spatial UI for contextual awareness gaps
- Prototyping voice + gesture interaction flows for 3D environments

## When NOT To Use

- Standard 2D web/mobile UI — spatial computing overhead adds no value
- Early concept validation — spatial UX requires hardware to meaningfully test
- Budget-constrained projects where XR hardware deployment is not planned
- Contexts where latency is unacceptable — AI scene understanding adds 50–200ms

## Content

| File | What's inside |
|------|---------------|
| `content/01-design-rules.xml` | Gaze target sizing, depth layer assignments, world-anchor rule, graceful degradation requirements |
| `content/02-ai-capabilities.xml` | Scene understanding, gesture prediction, voice integration, personalization cold-start |
| `content/03-agentic-workflow.xml` | Subagent patterns, prompt templates, tools, services, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/scene-decision-matrix.py` | Scene-type to UI state mapping generator |
| `templates/prompt-spatial-spec.txt` | Prompt for generating spatial UI specifications |
