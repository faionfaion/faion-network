---
slug: finops-framework
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates the program-level FinOps config (phase assessment + team structure + RACI + cadence + phase-specific checklists) that scaffolds the cultural practice end-to-end.
content_id: "bd241fd2c83914aa"
complexity: deep
produces: config
est_tokens: 4300
tags: [finops, cloud-cost, governance, framework, cost-management]
---
# FinOps Framework — INFORM / OPTIMIZE / OPERATE

## Summary

**One-sentence:** Generates the program-level FinOps config (phase assessment + team structure + RACI + cadence + phase-specific checklists) that scaffolds the cultural practice end-to-end.

**One-paragraph:** Generates the program-level FinOps config (phase assessment + team structure + RACI + cadence + phase-specific checklists) that scaffolds the cultural practice end-to-end. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Запуск FinOps program з нуля в компанії з cloud spend ≥$50k/month.
- Маturity audit існуючої програми (де ми зараз: INFORM / OPTIMIZE / OPERATE).
- Сross-functional alignment між Eng / Finance / Business.
- Quarterly executive review: показати phase mix, KPI prog, next steps.

## Applies If (ALL must hold)

- Annual cloud spend ≥$500k (the FinOps overhead pays back).
- Cross-functional sponsorship exists (Eng + Finance + Business lead).
- At least one named FinOps practitioner / lead.
- No formal phase-based framework currently in place.

## Skip If (ANY kills it)

- Single-team org with <$100k annual cloud spend — lightweight cost hygiene is enough.
- No cross-functional sponsorship — framework cannot work alone in eng silo.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cloud spend baseline | $/month + YoY growth | Finance |
| Org structure | team list with owners | HR / Eng leadership |
| Cost dashboard | URL | BI / Platform |
| Mandate from leadership | signed off charter doc | Exec sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/cicd-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-finops-framework` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-framework.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
