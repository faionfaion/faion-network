---
slug: requirements-documentation
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces SRS / BRD / user-story documents conforming to a checked schema, with traceability IDs, acceptance criteria, and review state per requirement.
content_id: "86e3e0418a3be483"
complexity: medium
produces: spec
est_tokens: 4300
tags: [ba, srs, brd, user-story, documentation]
---
# Requirements Documentation

## Summary

**One-sentence:** Produces SRS / BRD / user-story documents conforming to a checked schema, with traceability IDs, acceptance criteria, and review state per requirement.

**One-paragraph:** Produces SRS / BRD / user-story documents conforming to a checked schema, with traceability IDs, acceptance criteria, and review state per requirement. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Regulated industry (fintech, health, gov), де треба SRS під аудит.
- Cross-team handoff: design → dev → QA → ops, де verbal context втрачається.
- Onboarding нових BA/QA — треба стабільний документ замість Slack-археології.
- Contractual SOW, де requirement-набір — частина юридичного зобов'язання.

## Applies If (ALL must hold)

- Engagement requires formal documentation (audit, regulated industry, contractual SOW).
- Multiple downstream consumers (design, dev, QA, ops) need a single source of truth.
- Cross-team handoff where verbal context will be lost.
- Onboarding new team members who need a stable requirements artefact.

## Skip If (ANY kills it)

- Single-developer prototype where the developer is also the BA.
- Pure backlog-driven Scrum where user stories live in Jira and never become an SRS.
- Throwaway experiment with no audit need.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Requirements list | Output of elicitation / data-driven-requirements | BA |
| Traceability schema | Markdown / template | BA team |
| Acceptance criteria template | From acceptance-criteria methodology | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[acceptance-criteria]] | every requirement carries AC |
| [[requirements-traceability]] | requirement IDs feed RTM |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs/actions/outputs | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `structure-srs` | haiku | Mechanical sectioning per IEEE 830 template. |
| `write-requirement-bodies` | sonnet | Light judgement on phrasing + completeness. |
| `validate-schema` | haiku | Run validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/brd-template.md` | Business Requirements Document skeleton. |
| `templates/srs-template.md` | IEEE 830-aligned SRS skeleton. |
| `templates/user-story-template.md` | INVEST-compliant user story template with AC slot. |
| `templates/srs-conformance.yaml` | YAML schema enforced by validator. |
| `templates/srs_conform.py` | Conformance checker that fails CI when SRS source violates the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-requirements-documentation.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[acceptance-criteria]]
- [[requirements-traceability]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
