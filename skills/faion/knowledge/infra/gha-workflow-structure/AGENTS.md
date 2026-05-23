# GitHub Actions — Workflow Structure

## Summary

**One-sentence:** Generates a workflow-structure config (trigger types + concurrency groups + jobs-as-DAG via needs + environment protection + scheduled jobs + manual escape hatch).

**One-paragraph:** Generates a workflow-structure config (trigger types + concurrency groups + jobs-as-DAG via needs + environment protection + scheduled jobs + manual escape hatch). The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Pipeline з кількома jobs що мають dependencies (build → test → deploy).
- PR builds де per-branch concurrency має cancel-on-new-push.
- Deployment pipelines з environment protection + approvals.
- Scheduled workflows (nightly) з manual escape hatch.

## Applies If (ALL must hold)

- Workflow has ≥2 jobs with a dependency relationship.
- Multiple triggers (PR, push, schedule, dispatch) drive the same pipeline.
- Concurrency control is needed (cancel-PR-on-new-push, serialize deploys).
- Manual override (workflow_dispatch) is required for emergencies.

## Skip If (ANY kills it)

- Single-job workflow with single trigger — structure ceremony is gratuitous.
- Pipeline already lives in another CD tool and GHA is only a hook.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Job inventory | list (name, depends-on) | Eng team |
| Trigger requirements | table (event → workflow) | Eng team |
| Environment list with approvers | YAML | Platform team |
| Concurrency policy | table (trigger → behavior) | CI team |

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
| `draft-gha-workflow-structure` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton conforming to the output contract |
| `templates/config-instance.json` | JSON instance of a filled config artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gha-workflow-structure.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/infra/cicd-engineer/AGENTS.md`
- [[finops-framework]]
- [[gitops-core-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
