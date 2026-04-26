# Design Docs Patterns

## Summary

Write a design document before implementing any feature that takes more than one engineering day. Use lightweight Google-style (1-4 pages: context, goals, non-goals, proposed solution, alternatives, open questions) for team-scoped work. Use heavier formats (Amazon 6-pager, Uber RFC) only for cross-org or executive-audience decisions. Always include a non-goals section and at least two genuine alternatives — not strawmen. Set a review deadline when circulating.

## Why

Design documents catch design flaws when changes are cheap (before code is written), build consensus across teams, and create a record of why decisions were made. Writing forces clarity: the act of explaining a design in prose exposes gaps that discussion alone misses. LLM-generated design docs sound authoritative while missing domain-specific constraints — always require a human review pass.

## When To Use

- Any feature taking more than one engineering day
- Cross-cutting changes affecting multiple modules, services, or teams
- Requirements that are unclear or conflicting — writing exposes gaps
- Generating `design.md` in the SDD lifecycle (spec → design → test-plan → impl-plan)
- Before proceeding to implementation-plan.md generation — design must be marked Approved

## When NOT To Use

- Bug fixes with obvious root cause and one-line solution — PR description is sufficient
- Prototypes and spikes where output is discarded regardless of design quality
- Work taking less than a few hours — overhead exceeds benefit
- Solo purely internal refactors with identical external behavior

## Content

| File | What's inside |
|------|---------------|
| `content/01-format-selection.xml` | When to write a design doc, format selection (lightweight vs heavyweight), lifecycle phases |
| `content/02-writing-rules.xml` | Required sections, non-goals rule, alternatives quality, ADR extraction, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/design-doc-lightweight.md` | Google-style lightweight design doc template (2-4 pages) |
