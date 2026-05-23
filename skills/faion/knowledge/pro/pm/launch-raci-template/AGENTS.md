---
slug: launch-raci-template
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Launch-specific RACI assigning eng / design / marketing / sales / support owners across the workstreams of a single product launch, covering pre / day / post phases."
content_id: "80b4c6bfc2f0369f"
complexity: medium
produces: spec
est_tokens: 4500
tags: [pm, pro, launch, raci, cross-functional]
---
# Launch RACI Template

## Summary

**One-sentence:** Launch-specific RACI assigning eng / design / marketing / sales / support owners across the workstreams of a single product launch, covering pre / day / post phases.

**One-paragraph:** Launch RACI Template defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Cross-functional product launch with >=3 disciplines involved.
- Need a single artefact stakeholders can point to for 'who owns this on launch day'.
- Ambiguous accountability has bitten the team on a prior launch.
- Launch date is set and at least one rehearsal is scheduled.

## Applies If (ALL must hold)

- Launch involves >=3 disciplines (eng, design, marketing, sales, support, ops, legal — pick any).
- A launch lead is named and has authority to publish the RACI.
- Workstreams can be enumerated (e.g. comms, in-product, support readiness, ops runbook).
- Single Accountable per row is enforceable (the lead can resolve disputes).

## Skip If (ANY kills it)

- Launch is single-discipline (e.g. backend-only refactor) — overhead exceeds value.
- No launch lead is named — RACI without an A column is meaningless.
- Internal experiment (not a customer-facing launch) — use lighter scaffolding.

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
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `launch-raci-template_template_fill` | haiku | Bounded template fill, no judgement. |
| `launch-raci-template_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `launch-raci-template_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the launch RACI artefact. |
| `templates/raci-grid.md` | Markdown skeleton for the workstream-by-RACI grid with pre/day/post phases. |
| `templates/rehearsal-walkthrough.md` | Rehearsal script that walks each row T-14 -> T+14. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-launch-raci-template.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

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
