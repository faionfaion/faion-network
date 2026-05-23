---
slug: performance-domains-overview
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Assessment report scoring the eight PMBOK 7 performance domains (Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) on a single project, with anchored evidence + remediation actions."
content_id: "e9da0bbf62e4d0c2"
complexity: medium
produces: report
est_tokens: 4400
tags: [pmbok, performance-domains, assessment, outcomes, pm-framework]
---
# Performance Domains Overview

## Summary

**One-sentence:** Assessment report scoring the eight PMBOK 7 performance domains (Stakeholder, Team, Development Approach, Planning, Project Work, Delivery, Measurement, Uncertainty) on a single project, with anchored evidence + remediation actions.

**One-paragraph:** Performance Domains Overview defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- PMs running a PMBOK-aligned project that wants a domain-level health snapshot.
- Coaches assessing a project for systemic gaps (which domain is weakest).
- Quarterly project reviews where a uniform structure is needed across portfolios.
- Onboarding a new lead onto an existing project (fast map of where the bodies are buried).

## Applies If (ALL must hold)

- Project has been running >=8 weeks (8 domains need real evidence to score).
- Assessor has access to plans, retros, status reports, risk register.
- Project has a named sponsor who can act on remediation recommendations.
- Time-box of 2-4h is available for the assessment.

## Skip If (ANY kills it)

- Project is <4 weeks old — domains have no signal yet.
- Assessor has no read access to source artefacts — paraphrased substitutes are worse than skipping.
- No sponsor empowered to act on recommendations — report becomes orphaned.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `performance-domains-overview_template_fill` | haiku | Bounded template fill, no judgement. |
| `performance-domains-overview_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `performance-domains-overview_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the performance-domains assessment artefact. |
| `templates/pd-assessment.sh` | Shell helper that scaffolds an empty assessment markdown for the 8 domains. |
| `templates/assessment-report.md` | Markdown skeleton for the assessment report with 8 domain sections + remediation table. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-performance-domains-overview.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
