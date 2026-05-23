# Distressed Project Diagnostic Script

## Summary

**One-sentence:** Produces a six-week distressed-project rescue diagnostic — who to interview, what numbers to pull, how to triangulate truth between client and team.

**One-paragraph:** Produces a six-week distressed-project rescue diagnostic — who to interview, what numbers to pull, how to triangulate truth between client and team. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у, який заходить на проєкт у кризі — структурований діагноз з джерелами правди, не з 'інтуїції'.

## Applies If (ALL must hold)

- Project is formally classified as distressed (red status, churn risk, contract-default risk).
- A six-week (or shorter) turnaround window is contractually agreed.
- The incoming PM has read access to the project's source-of-truth tools (tracker, code, comms).
- At least one trusted insider on the existing team agrees to a 60-minute interview.

## Skip If (ANY kills it)

- Project is not yet distressed — this is for live triage, not post-mortems.
- No interview access — diagnostic without team voice produces wrong root cause.
- Contract is already terminated — produce a closure record, not a diagnostic.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Tracker access | API/UI | Jira / Linear / GitHub Projects |
| Comms-channel access | Slack/Teams archive | shared channel + read-only audit |
| Client-facing comms log | email/ticket export | account-management tooling |
| 60-minute insider interview slot | calendar invite | existing team roster |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/portfolio-evm-rollup-method` | Cost / schedule signal extraction reuses the same EVM frame. |
| `geek/pm/incident-comms-templates-internal-external` | Comms templates the rescue plan attaches to. |

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
| `interview-list-scaffold` | haiku | Role-based scaffold — pure template fill. |
| `numeric-pulls-extract` | sonnet | Bounded judgement: pick the right query against the tracker. |
| `rescue-plan-synthesis` | opus | Cross-source synthesis + 6-week plan defensible to sponsor. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown skeleton of the six-week rescue diagnostic with interview list, numeric pulls, triangulation matrix, and rescue plan. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-distressed-project-diagnostic-script.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[portfolio-evm-rollup-method]]
- [[incident-comms-templates-internal-external]]
- [[exception-driven-standup-protocol]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether the full diagnostic runs (formal distress + ≥6-week window + interview access) or is blocked/skipped. Run on day 1 of the rescue engagement before any team time is committed.
