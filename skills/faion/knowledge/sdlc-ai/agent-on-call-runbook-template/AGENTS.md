# Agent On-Call Runbook Template

## Summary

**One-sentence:** Produces a runbook the on-call AI agent can execute step-by-step during incidents, with explicit tool-tier approval gates and read-only defaults.

**One-paragraph:** Agent On-Call Runbook Template produces a playbook-step that fixes a recurring decision in the sdlc-ai domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- AI agent несе on-call за певний клас alerts.
- Read-only by default: жодних write tools без approval.
- Tool-tier gates: tier-1 read, tier-2 mutate з approval.
- Audit trail: кожен step з timestamp + tool used.
- Onboarding: human on-call читає той самий runbook.

## Applies If (ALL must hold)

- AI agent has tool access to monitoring + logs.
- Incident class is well-defined (e.g. 'pod restart loop').
- Tool-tier approval workflow exists.

## Skip If (ANY kills it)

- Incident class undefined — write playbook first.
- No human approver reachable within MTTA window.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Incident class definition | Markdown | DevOps lead |
| Tool tier policy | YAML | DevOps lead |
| Monitoring + logs access spec | Markdown | DevOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[inc-read-only-investigation-default]] | runbook defaults to read-only |
| [[inc-tool-tier-approval-gate]] | runbook respects tier gates |

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
| `draft-agent-on-call-runbook-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/on-call-runbook.md` | Markdown runbook skeleton with step IDs + tool tier column |
| `templates/runbook.schema.json` | JSON Schema for the runbook artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-on-call-runbook-template.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[alert-triage-decision-tree]]
- [[inc-tool-tier-approval-gate]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
