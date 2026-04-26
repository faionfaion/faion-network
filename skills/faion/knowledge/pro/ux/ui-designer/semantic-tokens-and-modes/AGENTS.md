# Semantic Tokens and Modes

## Summary

A semantic token layer maps primitive values (`color.blue.500`) to purpose-based aliases (`color.action.primary`) that resolve to different values per mode (light/dark, high-contrast, compact density, brand). Modes are declared per collection in Figma Variables or token JSON; Style Dictionary emits platform-specific output per mode. Every alias must have a value in every declared mode, and contrast pairs must be co-located so validation is automatable.

## Why

Hardcoding primitive tokens in components couples visual decisions to component code. A semantic layer decouples them: adding a dark-mode means adding one set of semantic alias resolutions, not touching every component. Aliasing depth must stay at three levels (primitive → semantic → component) to keep runtime debugging tractable and contrast validation automated.

## When To Use

- Building a token system that supports light/dark, high-contrast, density, or brand modes.
- Migrating from raw color/spacing tokens to a semantic layer.
- Wiring Figma Variables to Style Dictionary so designers and engineers share one source of truth.
- Adding a new mode without doubling component code paths.

## When NOT To Use

- Single-theme apps where modes add cost without payoff — start with raw tokens, promote when the second theme arrives.
- Print or static asset pipelines where mode-switching does not apply.
- Pure animation/motion tokens where mode semantics are rarely meaningful.

## Content

| File | What's inside |
|------|---------------|
| `content/01-semantic-layer.xml` | Three-tier naming, mode matrix structure, alias rules, contrast pair co-location requirement. |
| `content/02-agent-pipeline.xml` | Agentic workflow (aliaser → validator → emitter), recommended subagents, mode-coverage check, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/mode-coverage.py` | Script that fails if any alias is missing a value in any declared mode. |
| `templates/mode-validator-prompt.txt` | Structured-output prompt for a mode-validator subagent including contrast checks. |

## Scripts

none
