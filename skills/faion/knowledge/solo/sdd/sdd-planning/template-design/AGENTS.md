# Template: Design Document

## Summary

A fill-in-the-blanks template for design.md — the document that answers "HOW are we building it?" after spec.md is approved. Covers Reference Documents, Overview, Architecture Decisions (AD-X in ADR format), Components, Data Flow, Data Models, API Endpoints, Files (CREATE/MODIFY), Testing Strategy, Risks, and FR Coverage table.

## Why

Design docs without a fixed structure cause structural drift between features: some have FR Coverage tables, others do not; some ADs include Consequences, others skip them. A shared template enforces completeness — every required section is present — and makes review automatable (section presence checks, AD count, FR traceability).

## When To Use

- After spec.md is approved and before writing implementation-plan.md.
- Generating a new design.md for any feature driven by approved requirements.
- Reviewing an existing design doc for structural completeness against required sections.
- Calibrating output format when a new design-writing agent is added to the pipeline.

## When NOT To Use

- Before spec.md is approved — template fields will be guesswork without grounded requirements.
- For a task that affects a single file — full design doc overhead is unjustified; write the task directly.
- As a living document — design.md should be frozen after approval; use task files for implementation details.
- As a substitute for contracts.md — API endpoints belong in contracts, not in design.

## Content

| File | What's inside |
|------|---------------|
| `content/01-template-rules.xml` | Rules for using the template correctly: fill order, required sections, AD format requirements, FR coverage reconciliation, anti-patterns. |
| `content/02-checklist.xml` | Phase-by-phase checklist: prepare document, document ADs, define components, document data flow, define data models, specify API endpoints, list files, define testing strategy, identify risks, FR/AD coverage mapping, quality gate review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/design.md` | Complete design.md template with all required sections and placeholder text. |
| `templates/design-section-check.py` | Script to verify all required sections are present and count ADs and FR traces. |
