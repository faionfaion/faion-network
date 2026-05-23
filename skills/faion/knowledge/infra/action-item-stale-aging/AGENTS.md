# Action Item Stale Aging

## Summary

**One-sentence:** Produces an aging report on open retro action-items with explicit aging counter and escalation matrix per item.

**One-paragraph:** Action items from retros become zombies. `retro-basics` defines capture, nothing defines aging + escalation. This methodology pins a per-item aging counter, an explicit escalation threshold (default 3 cycles open → escalate; 5 cycles → drop with rationale), a deviation log so unprocessed items still get rationalised, and a named playbook owner who can amend. Output: a per-cycle aging report that surfaces structural problems (missing capability, wrong owner) rather than blaming the individual.

**Ефективно для:**

- retro action-items стають зомбі без owners та escalation — потрібен aging playbook.
- tier=pro команд із >=3 квартальними retros, де відкритих items накопичилось >=20.
- deviations from playbook потрібно логувати з rationale у next retro.
- одна людина named як playbook owner з повноваженням amendment.

## Applies If (ALL must hold)

- Retro action-items have a single backing tracker (issue tracker, doc, board) the agent can read.
- Each item has an owner, even if owner field is currently `unassigned`.
- Cycle cadence is defined (sprint / monthly / quarterly retros).
- A named playbook owner exists and can authorise amendments.

## Skip If (ANY kills it)

- Retros do not produce action items (the gap is upstream — fix retros first).
- Tracker for action items is not queryable (paper / Slack-only retros).
- Cycle cadence is undefined — establish cadence before aging.
- Team has fewer than 5 open action-items — manual review is cheaper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Action-item tracker | issue tracker URL | retro tooling |
| Cycle cadence | weekly / monthly / quarterly | team norms |
| Owner map | YAML / wiki | engineering lead |
| Playbook owner | named handle | team norms |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/devops-engineer` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with statement + rationale + source (5+ rules, includes r5-bound-scope) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | ~900 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom/root-cause/fix | ~1000 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate per step | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree mapping observable signals to a rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input_collection` | haiku | Structured pull from tracker |
| `decision_steps` | sonnet | Apply aging + escalation thresholds |
| `synthesis_writeup` | opus | Final artefact authoring with structural-cause flags |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Aging report skeleton with escalation matrix |
| `templates/skeleton.json` | JSON schema for the aging artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-action-item-stale-aging.py` | Validate produced artefact against the 02-output-contract.xml schema | After subagent returns, before downstream consumer reads |

## Related

- [[retro-basics]]
- [[agency-year-end-close-checklist]]
- [[oncall-rotation-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, owner, downstream consumer) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before applying the Action Item Stale Aging methodology when in doubt about scope or fit.
