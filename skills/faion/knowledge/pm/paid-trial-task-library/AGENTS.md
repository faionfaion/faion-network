# Paid Trial Task Library

## Summary

**One-sentence:** Library of scoped, paid trial-tasks for screening contractors / hires: each entry carries scope, time-box, deliverable, rubric, payout, ip-safety flag.

**One-paragraph:** Paid Trial Task Library defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Micro-agency founder hiring contractors or first 1-3 employees.
- Need to test real-world fit beyond CV + interview.
- Willing to pay for a small bounded task to de-risk hire.
- A rubric-based reviewer is available to score the deliverable.

## Applies If (ALL must hold)

- Open role or contractor opening with >=2 candidates worth testing.
- Founder has budget to pay for trial tasks.
- A reviewer with discipline-relevant skill can score deliverables.
- Tasks can be scoped to <=8 hours each (otherwise it becomes a project).

## Skip If (ANY kills it)

- Hiring on referral with high trust and prior work samples.
- No budget for trial-task payments — unpaid trials are forbidden by Faion ethics rules.
- Tasks would leak proprietary IP that can't be safely scoped.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `paid-trial-task-library_template_fill` | haiku | Bounded template fill, no judgement. |
| `paid-trial-task-library_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `paid-trial-task-library_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the trial-task library artefact. |
| `templates/task-entry.md` | Markdown skeleton for a single trial-task entry. |
| `templates/rubric.md` | Rubric skeleton with good/acceptable/fail anchors. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-paid-trial-task-library.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
