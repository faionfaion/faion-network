# Sprint Capacity From Complexity Tags

## Summary

**One-sentence:** Produces a time-estimate-free sprint capacity model that allocates a bi-weekly slot budget from per-task complexity tags (XS/S/M/L/XL), calibrated by rolling completion ratio.

**One-paragraph:** Sprint Capacity From Complexity Tags produces a config that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Avoid time estimates — використовуємо complexity tags замість годин.
- Bi-weekly sprint slot budget: XS=1, S=2, M=4, L=8, XL=16 slots.
- Rolling calibration: коригуємо вагу на основі останніх 3 спринтів.
- Spend-cap: коли capacity вичерпано, нові tasks автоматично blocked.
- Async planning: команда не торгується годинами, лише tag value.

## Applies If (ALL must hold)

- Team rejects time estimates as unreliable.
- Tasks carry complexity tags (XS/S/M/L/XL) or can be tagged.
- Team has ≥3 completed sprints to calibrate weights.

## Skip If (ANY kills it)

- Team still uses time estimates and prefers them.
- Fewer than 3 sprints of history — calibration impossible.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tagged backlog | JSON / tracker export | tracker |
| Sprint history | JSON | tracker |
| Team size + sprint length | YAML | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-tech-lead-grooming-agenda]] | grooming consumes the capacity model |

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
| `draft-sprint-capacity-from-complexity-tags` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/capacity-model.yml` | YAML capacity model: tag→slot weights + team size + sprint length |
| `templates/capacity.schema.json` | JSON Schema for the capacity model |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sprint-capacity-from-complexity-tags.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[pm-tech-lead-grooming-agenda]]
- [[tech-debt-slot-quota-policy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
