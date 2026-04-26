# System Design Process

## Summary

A five-phase process (Understand → Scope → Design → Validate → Document) for turning a product brief into a buildable architecture package: requirements list, NFR targets with numeric back-of-envelope estimates, C4 diagrams (L1+L2 minimum), and ADRs per non-obvious decision. LLMs accelerate each phase but require human sign-off at NFR finalization and ADR acceptance.

## Why

Greenfield systems fail most often from skipped NFR quantification and single-option design: the team builds the first idea without comparing alternatives against measurable targets. Forcing back-of-envelope (DAU → RPS → storage → bandwidth) before any diagram prevents over-engineering. The C4 model provides four zoom levels so every audience gets the right abstraction without a whiteboard session.

## When To Use

- Greenfield system design where requirements, NFRs, and scale assumptions are still being captured.
- Replacement/replatform decisions that need a spec, ADRs, and C4 diagrams before code.
- Pre-implementation handoff: turning a product brief into a package the dev agent can execute.
- Internal design exercises where a reviewable artifact (not a whiteboard sketch) is the deliverable.

## When NOT To Use

- Small bug fixes or localized refactors — overkill; use the relevant pattern methodology directly.
- Prototype/spike code where the goal is to learn, not commit to an architecture.
- Domains the team operates daily (CRUD admin tools) — skip to templates.
- Operational incidents — use reliability-architecture and observability instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases-and-nfr.xml` | Five-phase flow, FR vs NFR definitions, NFR attribute table, back-of-envelope formulas, quality gates checklist. |
| `content/02-patterns-and-c4.xml` | Architecture-style decision tree, common design patterns matrix, C4 model overview, LLM workflow steps. |

## Templates

| File | Purpose |
|------|---------|
| `templates/adr-madr.md` | MADR-format ADR template with status, context, decision, consequences. |
| `templates/adr-compact.md` | Compact ADR template with alternatives table. |
| `templates/c4-mermaid.md` | C4 Context, Container, Component, Dynamic, and Deployment diagram skeletons in Mermaid syntax. |
| `templates/design-doc.md` | Full design document template: requirements, high-level design, detailed design, security, trade-offs. |
