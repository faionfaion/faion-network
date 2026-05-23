# Ai In Project Management

## Summary

**One-sentence:** Framework for AI-augmented PM (risk scoring, schedule variance, capacity forecasting, stakeholder digests) anchored to PMBOK 8 AI appendix + DORA 2025 productivity-paradox findings.

**One-paragraph:** Framework for AI-augmented PM (risk scoring, schedule variance, capacity forecasting, stakeholder digests) anchored to PMBOK 8 AI appendix + DORA 2025 productivity-paradox findings. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у, який вводить AI в свій робочий процес — щоб гетати productivity-paradox і не зайти у бутилковий шийку review/deploy.

## Applies If (ALL must hold)

- Team is using PMBOK 8 (or compatible) as the reference frame.
- AI adoption is being formalised across risk + scheduling + reporting.
- Baseline delivery throughput metrics exist (DORA four keys or equivalent).
- Org has a published AI-decision documentation policy.

## Skip If (ANY kills it)

- Team < 3 people — AI-PM overhead exceeds benefit.
- No baseline metrics — AI-augmented optimisation cannot demonstrate improvement.
- Regulated context without established AI decision documentation — comply first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| DORA baseline | dashboard | engineering metrics tool |
| PMBOK 8 reference | doc | PMI publication |
| AI-decision documentation policy | doc | compliance / legal |
| Tracker + Git + budget feeds | API | tooling stack |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/pm-agile/ai-assisted-velocity-anomaly-detection` | Concrete detection pipeline this framework references. |
| `geek/pm/project-manager/ai-pm-tool-integration-recipes` | Concrete tool-integration recipes. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `framework-mapping` | sonnet | Bounded mapping: PMBOK 8 sections to current rituals. |
| `decision-log-scaffold` | haiku | Template fill. |
| `paradox-bottleneck-narrative` | opus | Cross-DORA-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Framework adoption checklist: AI-decision log template + PMBOK 8 mapping table + DORA baseline columns + audit-trail block. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-in-project-management.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ai-assisted-velocity-anomaly-detection]]
- [[ai-pm-tool-integration-recipes]]
- [[ai-powered-pm-tools]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to adopt the framework (baseline + policy + alignment) or block until prerequisites exist. Run at AI-adoption kickoff before any tool is procured.
