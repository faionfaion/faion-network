# Multimodal VUI Design

## Summary

Design methodology for interfaces that combine voice input with visual display — pattern-matching voice commands to on-screen card/carousel output while maintaining touch fallbacks for every voice state. Every dialogue turn must declare: voice prompt, visual state (max 5 items), valid touch actions, and silence fallback.

## Why

Voice-only interfaces cannot display structured data; screen-only interfaces add friction for hands-free or glanceable contexts. Multimodal design bridges them, but amplifies errors when done poorly — missing touch fallbacks strand users who switch modalities mid-task. The per-turn structure enforces completeness before prototyping.

## When To Use

- Smart TV, smart display, kiosk, or automotive HMI combining voice with a screen
- Voice assistants surfacing structured data (product cards, search results, maps)
- Accessibility-first products where users alternate between touch and voice
- Conversational commerce (search → carousel → voice-confirm purchase)

## When NOT To Use

- Audio-only environments (earbuds, phone IVR) — no screen; use pure VUI
- Text-heavy B2B tools (dashboards, IDEs) — voice adds friction with no multimodal benefit
- Products where latency >2s is unacceptable — ASR + LLM + TTS chain is inherently slow
- Teams without dedicated voice UX expertise — multimodal amplifies design errors

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns-and-rules.xml` | Multimodal patterns, turn structure rules, fallback strategy |
| `content/02-tools-and-gotchas.xml` | CLI tools, services, agent workflow, AI gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/dialogue-turn-schema.json` | JSON schema for a single multimodal dialogue turn |
| `templates/validate-turns.py` | Script: validates dialogue tree for missing touch fallbacks and visual overload |
| `templates/prompt-design-dialogue.txt` | Agent prompt: generate multimodal dialogue script for a given task and device |
