# Warranty Period Sop

## Summary

**One-sentence:** Warranty Period Sop: produces a versioned, owner-signed artefact that closes the gap 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)'.

**One-paragraph:** Addresses the gap surfaced by 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)': Freelancers either swallow free post-launch fixes or fight over them. Need a defined warranty-window SOP: what's in, what's out, how to convert it into a retainer. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a warranty period sop artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Project kickoff to handover (6-12 week engagement) включає post-handover warranty.
- Технічний фрілансер потребує SOP для warranty-period: scope, SLAs, escalation.
- Клієнт хоче знати, що буде покрите free vs. чарджнуте після handover.

## Applies If (ALL must hold)

- task is an instance of 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working warranty period sop artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Warranty Period Sop |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules grounded in the cited gap | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | 700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | medium | One worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/warranty-period-sop.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/warranty-period-sop.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-warranty-period-sop.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-warranty-period-sop.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p3-technical-freelancer/Project kickoff to handover (typical 6-12 week engagement)`
- pro/pm/p3-technical-freelancer

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
