# Agent Drafts Spec Before Coding

## Summary

**One-sentence:** When an AI coding agent is assigned a tracker ticket (Linear, Jira, GitHub, GitLab), its first action MUST be a "current state / desired state / proposed plan" comment, not a code edit. Implementation starts only after explicit human approval.

**One-paragraph:** "Assign to agent → wait for PR" pipelines skip the discovery step; agents fabricate intent, implement the wrong thing, and humans rediscover the misunderstanding at PR review. This methodology pins the rule: the agent's FIRST action on assignment MUST be a structured spec comment with current state, desired state, and proposed plan; implementation only begins after explicit approval (Linear thumbs-up, Jira `/agent approve`, or `agent:approved` label transition). Output is a per-ticket spec artefact linking ticket → spec comment → approval-event → PR.

**Ефективно для:**

- Linear / Jira / GitHub / GitLab ticket assigned to AI coding agent (Copilot, Claude, Codex, Devin).
- Non-trivial scope: feature work, multi-file bug fix, refactor, migration.
- Team із principles "agents fabricate intent" і хоче explicit approval gate.
- Workflow auto-closes ticket on PR merge (Fixes #N) — spec coment стає linkable record of intent.

## Applies If (ALL must hold)

- Ticket is assigned to an AI coding agent as primary owner.
- Ticket has non-trivial scope (feature, multi-file fix, refactor, migration).
- Team has ≥1 human reviewer who can react with thumbs-up or run approval slash command.
- Workflow auto-closes ticket on PR merge (Fixes / Closes link).

## Skip If (ANY kills it)

- Trivial pre-flagged `agent:auto-approve` ticket (typo, dep bump, log tweak).
- Spike / research ticket where the discovery IS the deliverable.
- Hot-path incident response where postmortem ticket comes after the fact.
- Single-author solo project with no second human in the loop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tracker integration | Linear / Jira / GitHub / GitLab API | platform |
| Approval mechanism | thumbs-up emoji / slash command / label | platform |
| Spec template | Markdown | docs |
| Agent dispatch hook | webhook → agent runtime | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[regression-eval-before-fix-rule]] | Same eval-first discipline for bug-fix tickets. |
| [[mr-codemod-refactor-agent]] | Refactor tickets that route to the codemod agent. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 600 |
| `content/05-examples.xml` | essential | Worked spec example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `discover-context` | sonnet | Gather ticket body + linked Notion/Slack + code-intel search. |
| `draft-spec` | sonnet | Structured "current / desired / proposed plan". |
| `wait-and-detect-approval` | haiku | Mechanical: poll for thumbs-up / label / slash command. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-comment.md` | Spec-comment skeleton with current state / desired state / proposed plan blocks. |
| `templates/approval-gate.yaml` | Tracker automation snippet (Linear / Jira) for `agent:approved` label transition. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-task-agent-drafts-spec-before-coding.py` | Validate spec artefact + approval-event linkage. | Pre-PR-open by the agent |

## Related

- [[regression-eval-before-fix-rule]]
- [[mr-codemod-refactor-agent]]
- [[mr-graph-vs-diff-reviewer]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable signals (ticket scope, reviewer presence, auto-approve label) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether the rule applies on a given ticket — the tree terminates either on the active rule or on `skip-this-methodology`.
