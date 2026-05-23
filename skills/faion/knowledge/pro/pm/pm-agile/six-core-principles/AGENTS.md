---
slug: six-core-principles
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Audit rubric covering PMBOK 7's six guiding principles: Adopt Holistic View, Focus on Value, Embed Quality, Lead Accountably, Integrate Sustainability, Build Empowered Teams.
content_id: "0eb1cf8ac83170cf"
complexity: medium
produces: rubric
est_tokens: 4200
tags: [pmbok7, principles, decision-making, audit, governance]
---
# Six Core Principles (PMBOK 7)

## Summary

**One-sentence:** Audit rubric covering PMBOK 7's six guiding principles: Adopt Holistic View, Focus on Value, Embed Quality, Lead Accountably, Integrate Sustainability, Build Empowered Teams.

**One-paragraph:** Audit rubric covering PMBOK 7's six guiding principles: Adopt Holistic View, Focus on Value, Embed Quality, Lead Accountably, Integrate Sustainability, Build Empowered Teams. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-six-core-principles.py` enforces the output contract.

**Ефективно для:**

- Quarterly principle audit on a running program.
- Reviewing a PM decision (scope cut, vendor selection, escalation) against the six principles.
- Onboarding new PMs to PMBOK 7 mindset.

## Applies If (ALL must hold)

- PMBOK 7 is the team's governing standard (or being adopted).
- Each principle is testable with at least one observable signal.
- An auditor is available to score each principle 0-3.

## Skip If (ANY kills it)

- Team uses Disciplined Agile, SAFe, or pure Scrum without PMBOK overlay.
- Audit cost exceeds principle-violation cost on this program.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Decision log (90 days) | Markdown/CSV | PM |
| Stakeholder satisfaction signal | NPS or proxy | PM |
| Team-health pulse | survey result | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[seven-performance-domains]] | principles complement domain-based oversight |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-principle` | sonnet | Judgement: artefact → 0-3 score with justification. |
| `aggregate-audit` | haiku | Roll up six scores to RAG. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pmbok7-audit.sh` | Bash audit walker: scores each principle 0-3 from artefact heuristics |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-six-core-principles.py` | Validate the rubric artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[seven-performance-domains]]
- [[team-development]]
- [[value-stream-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

