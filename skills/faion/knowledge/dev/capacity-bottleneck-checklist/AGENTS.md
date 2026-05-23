# Capacity Bottleneck Checklist

## Summary

**One-sentence:** Produces a versioned capacity-bottleneck checklist that names DB connections, queue throughput, gateway TLS, autoscale lag chokepoints plus a 20% headroom floor and a single owner.

**One-paragraph:** Capacity Bottleneck Checklist takes a pre-launch or scale-event input and emits a versioned, owner-named checklist enumerating the candidate chokepoints (DB connections, queue throughput, gateway TLS, autoscale lag, hot keys, fan-out limits), the measured current headroom, and the gating decision. The 20% spare-capacity floor is non-negotiable; below it, the artefact escalates before commit.

**Ефективно для:**

- Pre-launch або scale event — фіксований owner, не "команда".
- Чек-лист bottleneck'ів (DB pool, TLS gateway, queue, autoscale lag).
- Headroom floor ≥20% — інакше escalate, не committee debate.
- Versioned + last_reviewed артефакт для traceability.

## Applies If (ALL must hold)

- Task is an instance of role-software-architect/Capacity + cost-modelling exercise OR closely-adjacent variant.
- Operator has Prerequisites artefacts available before starting.
- Output will be consumed by a downstream agent or human reviewer.
- Tier == pro or higher.

## Skip If (ANY kills it)

- The team already maintains a working capacity artefact — replace, do not duplicate.
- Greenfield prototype with no production users.
- Regulatory context overrides any in-methodology guidance (defer to legal).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Recent capacity context (last 30 days) | metrics dump | observability |
| Write-access to decision log | repo / wiki | team |
| Named owner candidate | handle/email/role | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[software-developer]] | Parent role context — provides the operating frame for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment on bottlenecks and headroom. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-bottleneck-checklist.json` | JSON skeleton matching the output contract. |
| `templates/capacity-bottleneck-checklist.md` | Markdown skeleton naming the checklist sections. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-capacity-bottleneck-checklist.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-capacity-bottleneck-checklist.py` | Validator script reused as the canonical name across docs. | after subagent returns, before downstream consumer reads |

## Related

- [[cap-pacelc-walkthrough]]
- [[ci-prod-readiness-gates]]

## Decision tree

See `content/06-decision-tree.xml`. Tree gates the workflow on headroom and ownership; below the 20% floor escalates, missing owner blocks output.
