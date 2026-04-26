# Language & Framework Selection Guide

## Summary

A tier-0 decision router for stack selection. Given a project brief, maps the task type to the canonical language (Python, TypeScript, Go, Rust) and framework (Django, FastAPI, React, Next.js). Provides format/lint/test commands per language. The agent must output a recommendation with two alternatives and an ADR stub — not just a name.

## Why

Without an explicit decision record, agents re-litigate stack choice on every session and often pick the framework most represented in recent prompt history, not the best fit. Anchoring to this guide forces a justification artifact (ADR) that future agents and humans can override with evidence.

## When To Use

- Day-zero greenfield: agent must propose a stack for a project brief.
- A spec says "use the right tool" — this is the canonical default mapping.
- Generating boilerplate format/lint/test commands for CI scaffolding.
- Sanity-check: is the chosen language/framework a mismatch for the stated requirements?

## When NOT To Use

- Team has an existing stack mandate — don't override without an ADR.
- Domains with non-obvious constraints (regulatory, hardware, cloud lock-in) — use a richer ADR flow.
- Picking between equally valid options for a short experiment — decision overhead exceeds value.
- ML/embedded/blockchain/games — table is not authoritative outside web/API scope.

## Content

| File | What's inside |
|------|---------------|
| `content/01-selection-rules.xml` | Language and framework selection rules with decision table and format/test commands per stack. |
| `content/02-adr-and-gotchas.xml` | ADR stub template, agent gotchas, and tool references. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-stub.md` | Architecture Decision Record template for stack selection. |
