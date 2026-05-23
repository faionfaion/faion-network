---
slug: personas
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces 3-5 research-based personas (≥6 interviews, goal/behaviour clusters, verbatim-quote evidence, scenarios + JTBD pairing) for design-decision grounding.
content_id: "51c7fbd2885d3ed0"
complexity: medium
produces: spec
est_tokens: 4500
tags: [personas, research, user-centered, methodology, ux]
---
# Personas

## Summary

**One-sentence:** Produces 3-5 research-based personas (≥6 interviews, goal/behaviour clusters, verbatim-quote evidence, scenarios + JTBD pairing) for design-decision grounding.

**One-paragraph:** Personas are fictional characters representing key user types, based on research. Cap at 3-5 primary; each carries goals, frustrations, behaviours, context, scenario, and ≥1 verbatim quote tied to a research participant. Cluster on goals + behaviours (not demographics). Pair every persona with a JTBD ('Sarah hires the dashboard to look prepared in meetings'). Date-stamp; mark DRAFT until validated against ≥10 users; re-cluster every research wave (quarterly minimum).

**Ефективно для:**

- Після ≥6 user interviews — patterns emerge, team needs shared shorthand.
- Onboarding new designers / PMs / engineers до користувацької бази.
- Pre-feature discussions з 'would the user want this?' constantly surfacing.
- B2B з distinct buyer / champion / end-user — separate persona per role.

## Applies If (ALL must hold)

- >=6 research interviews completed.
- Team needs shared shorthand for user types.
- Product has identifiable user segments (B2C tiers or B2B roles).

## Skip If (ANY kills it)

- Pre-research — 'made-up' personas reinforce assumptions.
- Pure technical infrastructure where the user IS the developer.
- Single-customer enterprise — stakeholder map is more useful.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview transcripts | ≥6 with participant IDs | user research |
| Clustering rubric | goals + behaviours (NOT demographics) | this methodology |
| JTBD framework | intro | JTBD methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[contextual-inquiry]] | Source of interview transcripts |
| [[diary-studies]] | Longitudinal supplement |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure | 800 |
| `content/05-examples.xml` | essential | Worked example with note | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree routing to rules | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `primary-analysis` | sonnet | Domain-specific judgement. |
| `structured-output-assembly` | sonnet | Schema-conforming JSON build. |
| `validate` | haiku | Deterministic schema check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-template.md` | Per-persona markdown template with all required fields |
| `templates/clustering-prompt.md` | Agent-assisted clustering prompt for transcript synthesis |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-personas.py` | Validate artefact JSON against output schema | Pre-commit / CI on artefact change |

## Related

- [[contextual-inquiry]]
- [[diary-studies]]
- [[focus-groups]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs to a rule-grounded conclusion, every leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
