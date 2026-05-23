---
slug: task-plan-mode-locked-execution
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a versioned, human-approved plan that the agent must execute verbatim, with replans forbidden mid-flight.
content_id: "82e761183805026a"
complexity: medium
produces: spec
est_tokens: 5100
tags: [plan-mode, locked-execution, agentic-workflow, prompt-injection, approval-gate]
---
# Plan Mode Then Locked Execution

## Summary

**One-sentence:** For any change > 3 files or > 5 min of agent time, force a read-only Plan Mode first, freeze the plan on human approval, then execute the locked plan without silent replans.

**One-paragraph:** For any change that touches more than three files or runs longer than ~5 minutes of agent time, the agent MUST first enter Plan Mode (read-only — no Edit, no Write, no shell side-effects), produce an explicit plan with numbered steps, verification commands, and an `Out of scope` list, secure human approval, then execute the locked plan. The agent is forbidden from re-planning silently mid-execution; any deviation requires a new approved plan, not an in-flight pivot. Locking the plan before execution closes the prompt-injection window, because untrusted data the model encounters during execution cannot rewrite the agreed steps.

**Ефективно для:**

- Багатофайлові refactors, де агент схильний `розповзатися` поза scope.
- Prompt-injection захист: locked plan не переписується untrusted input під час execution.
- Audit trail: approved plan + diff створюють замкнений compliance loop.
- Сабагент-fleet, де один планує, інший виконує — clean handoff.

## Applies If (ALL must hold)

- Change spans more than 3 files OR exceeds ~5 minutes of agent runtime.
- Repository contains executable side-effects (DB migrations, deploys, secret rotations).
- Human reviewer is available to approve the plan before execution.

## Skip If (ANY kills it)

- One-line edit or trivial typo fix on a single file.
- No human approver is available within the agent's runtime window.
- Hard real-time fix needed (production outage) where the locked-plan latency is unacceptable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Change request / ticket | Markdown | issue tracker |
| Repo file inventory | text (find/ls) | agent read-only pass |
| Human approver handle | string | team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom/root-cause/fix) | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with decision gates | 800 |
| `content/05-examples.xml` | essential | Full worked example end-to-end | 900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-output` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plan.md` | Markdown skeleton for the locked plan (numbered steps, verify cmds, out-of-scope, risks). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-plan-mode-locked-execution.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[task-agent-fixable-triage-gate]]
- [[task-worktree-runtime-isolation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
