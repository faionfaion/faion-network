---
slug: finops-agentic-workflow
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a continuous-loop agentic FinOps config (billing-snapshot, tag-auditor, idle-hunter, RI/SP-advisor agents) with human-in-the-loop approval gates and safe-automation gotchas.
content_id: "1fa52a4d464982e7"
complexity: deep
produces: config
est_tokens: 4300
tags: [finops, agentic, cost-automation, human-in-loop, idle-detection]
---
# Agentic FinOps Workflow with AI Agents

## Summary

**One-sentence:** Generates a continuous-loop agentic FinOps config (billing-snapshot, tag-auditor, idle-hunter, RI/SP-advisor agents) with human-in-the-loop approval gates and safe-automation gotchas.

**One-paragraph:** Generates a continuous-loop agentic FinOps config (billing-snapshot, tag-auditor, idle-hunter, RI/SP-advisor agents) with human-in-the-loop approval gates and safe-automation gotchas. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Команд що вже мають tag-coverage ≥80% і readable cost dashboard.
- Сценарії де ручний audit не масштабується (>500 ресурсів, ≥5 акаунтів).
- Mature FinOps — крок 'OPERATE' з людьми в loop на сильному risk gate.
- AI/ML-heavy spend: GPU pools, training jobs, inference endpoints.

## Applies If (ALL must hold)

- Existing FinOps program in 'inform' or 'optimize' phase with stable tagging and cost dashboards.
- Agent execution sandbox (Lambda / Step Functions / Argo) is available with least-privilege IAM.
- Defined approval channel (Slack, Jira) with named approvers per resource class.
- Audit log (CloudTrail / Activity Log) covers every action the agent can take.

## Skip If (ANY kills it)

- FinOps program is pre-INFORM — no tag policy, no dashboards (use finops-framework first).
- No human-approval channel — fully autonomous deletes are blocked by policy.
- Cloud account count <2 and resource count <50 — manual audit still cheaper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Billing data feed | AWS CUR / GCP Billing Export / Azure Cost Mgmt API | Cloud Platform |
| Tag policy + coverage report | YAML + JSON | Cloud Platform |
| Approver registry | YAML (resource_class → approver_email) | FinOps Lead |
| Agent runtime | Lambda/Step Functions/Argo Workflows | Platform team |

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
| `draft-finops-agentic-workflow` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finops-agentic-workflow.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
