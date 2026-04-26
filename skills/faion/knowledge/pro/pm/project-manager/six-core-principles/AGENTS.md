# PMBoK 8 Six Core Principles

## Summary

PMBoK 8 consolidates the PMBoK 7 twelve principles into six: Adopt Holistic View, Focus on Value, Embed Quality, Lead Accountably, Integrate Sustainability, Build Empowered Teams. Every PM artefact or decision is audited against these six as binary pass/fail questions — "passed: true" requires positive evidence, not merely absence of failure. Any failing principle stops the stage gate.

## Why

Abstract principles degrade into platitudes without a concrete decision framework. The six-question audit converts principles into a rejection gate: if any principle is violated, the artefact must be fixed or escalated before proceeding. Paired with measurable indicators (outcomes table for Value, CO2 proxy for Sustainability, DoD for Quality), the audit becomes testable rather than decorative.

## When To Use

- Drafting or reviewing a project charter, decision log, or change request
- Auditing an existing plan for principle gaps (no sustainability section, no value statement)
- Anchoring any PM-domain LLM call with a six-question self-check step at the end
- Migrating a PMBoK 7 twelve-principle plan to PMBoK 8 six-principle structure

## When NOT To Use

- Tactical execution work (sprint planning, ticket triage) — principles are too abstract to give tactical guidance; use methodology checklists
- Non-PMI environments (PRINCE2, IPMA, SAFe) — vocabulary clashes; map to those frameworks' own principles
- Audit/compliance contexts requiring a specific named standard (ISO 21500, ISO 21502) — PMBoK principles are guidance, not certification
- Technical deep-dives (architecture review, security) — principles do not substitute for domain expertise

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Six principles with definitions, concrete indicators, and PMBoK 7 → 8 mapping |
| `content/02-audit-rules.xml` | Audit rules, pass/fail criteria, antipatterns (all-green outputs, sustainability as paragraph) |

## Templates

| File | Purpose |
|------|---------|
| `templates/principle-audit.md` | Six-row audit table: principle / evidence / pass-fail / fix |
