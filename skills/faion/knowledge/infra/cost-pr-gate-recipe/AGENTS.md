# Cost PR Gate Recipe

## Summary

**One-sentence:** Produces a CI gate config that blocks merge when an IaC PR exceeds the team's monthly cost-delta budget.

**One-paragraph:** FinOps content covers visibility and rightsizing but not the 'fail the PR if infrastructure cost delta > X' loop. P6 product teams ship cost regressions because the cost dashboard updates after merge, not before. This methodology pins a CI gate config that computes the projected cost delta from the IaC diff, compares against the service's monthly cost-delta budget, and blocks merge on breach unless a named approver signs off.

**Ефективно для:**

- P6 product-команда, де infra cost росте на кожен sprint без видимості у PR-flow.
- коли потрібен CI-gate що блокує merge при cost-delta вище порогу.
- FinOps visibility є, а enforcement loop — відсутній.
- tier=pro команд із Infrastructure-as-Code (Terraform / Pulumi / CloudFormation).

## Applies If (ALL must hold)

- Team owns IaC (Terraform / Pulumi / CloudFormation) that lands through pull requests.
- Monthly cost-delta budget per service is defined (even as a rough starting number).
- CI system can run a cost-estimate step (Infracost, native pricing API, or equivalent).
- Team agrees that a breached gate blocks merge until an approver signs off.

## Skip If (ANY kills it)

- Team does not own IaC — manual console changes mean there is no PR to gate.
- No monthly cost-delta budget agreed — gate has no threshold to compare against.
- Greenfield prototype where every PR is expected to add cost.
- CI system cannot run cost-estimate step in the time budget (gate would block all merges).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| IaC repository | Terraform / Pulumi / CFN repo | dev team |
| Per-service monthly cost-delta budget | numbers | finance + dev |
| CI workflow file | YAML | platform team |
| Approver matrix | role or named handle | engineering lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill — operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r1-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse-iac-diff` | haiku | Mechanical diff extraction |
| `estimate-cost-delta` | sonnet | Bounded computation with sourced unit rates |
| `decide-merge-or-block` | sonnet | Apply threshold + flag approver |

## Templates

| File | Purpose |
|------|---------|
| `templates/cost-pr-gate.yaml` | CI workflow snippet for the cost gate |
| `templates/skeleton.json` | JSON schema for the gate decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-pr-gate-recipe.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[cost-anomaly-runbook]]
- [[cost-model-spreadsheet-template]]
- [[finops-baseline]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Cost PR Gate Recipe methodology when in doubt about scope or fit.
