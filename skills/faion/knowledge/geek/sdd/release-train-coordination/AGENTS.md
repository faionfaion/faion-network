---
slug: release-train-coordination
tier: geek
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Generates a release-train artefact (window, freeze rules, branch policy, captain rotation) that closes the cross-role handoff loop.
content_id: "ab468e8c1c4c4d49"
complexity: medium
produces: config
est_tokens: 3400
tags: ["sdd", "release", "coordination", "train", "team"]
---
# Release Train Coordination

## Summary

**One-sentence:** Generates a release-train artefact (window, freeze rules, branch policy, captain rotation) that closes the cross-role handoff loop.

**One-paragraph:** Release Train Coordination produces a config that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Регулярний release window замість 'коли готово'.
- Code-freeze rules видимі для всіх ролей.
- Hot-fix vs feature-release branches — фіксований policy.
- Captain rotation: фейр rotation + owner accountability.
- Cross-role handoff: pm → architect → dev → qa → devops у одному циклі.

## Applies If (ALL must hold)

- Team has ≥3 active developers shipping to a shared environment.
- Multiple releases per quarter where coordination matters.
- Hot-fix path is distinct from feature-release path.

## Skip If (ANY kills it)

- Solo developer or 'deploy when ready' shop.
- Single release per quarter — release train is heavier than needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Release cadence target | Markdown / YAML | tech lead |
| Branch model | Markdown | tech lead |
| Captain rotation roster | YAML | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[definition-of-done-multi-role]] | release train enforces DoD per role |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source + skip rule | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 600 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-release-train-coordination` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/release-train.yml` | YAML config with window + freeze + branch model + rotation |
| `templates/captain-runbook.md` | Markdown runbook for the active release captain |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-release-train-coordination.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[definition-of-done-multi-role]]
- [[sprint-capacity-from-complexity-tags]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
