# Vendor Management Pm

## Summary

**One-sentence:** Vendor Management Pm: produces a versioned, owner-signed artefact that closes the gap 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)'.

**One-paragraph:** Addresses the gap surfaced by 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)': procurement-management has a vendor_score.py but no ongoing vendor-management methodology: cadence of vendor 1:1s, escalation paths, SLA tracking, vendor-of-record decisions, change-management when vendor team rotates. Critical for P4 PMs managing sub-vendors. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a vendor management pm artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Multi-team coordination з vendor-залежностями і dependency-graph reasoning.
- PM веде декілька vendor relationships і потребує structured oversight.
- P6 продукт має vendor SLAs, які треба tracking без full ITIL стека.

## Applies If (ALL must hold)

- task is an instance of 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working vendor management pm artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/pm` | parent domain group — provides operating context for Vendor Management Pm |

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
| `templates/vendor-management-pm.md` | Filled artefact skeleton conforming to 02-output-contract.xml |
| `templates/vendor-management-pm.schema.json` | JSON Schema for the artefact (mirrors content/02-output-contract.xml) |
| `templates/_smoke-test.md` | Minimum-viable filled-in version exercised by scripts/validate-vendor-management-pm.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-management-pm.py` | Validate artefact against 02-output-contract.xml schema. Exit 0/1/2. | After subagent returns; pre-commit on artefact change. |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `role-project-manager/Multi-team coordination & dependency-graph reasoning (P6 product)`
- pro/pm/role-project-manager

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions hold, inputs typed, rules pass) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it before producing the artefact to confirm the methodology applies and the rules pass.
