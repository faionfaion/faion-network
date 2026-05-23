# Definition of Done Library

## Summary

**One-sentence:** A library of canonical Definitions of Done indexed by deliverable type (story / feature / release / contractor task) for reuse instead of per-engagement reinvention.

**One-paragraph:** Every engagement re-invents DoD; quality varies wildly; some teams have a 12-item DoD, others have none. The library pins canonical DoDs by deliverable type with rationale per item, so the next engagement picks the relevant DoD, customises ≤3 items, and ships consistent quality. Output: a versioned library + per-engagement chosen-DoD record.

**Ефективно для:**

- Multi-engagement portfolios where DoD variance harms predictability.
- Contractor engagements needing tight AC baselines.
- Pre-engagement BA setup phase.
- Audit programs requiring documented DoD per deliverable type.

## Applies If (ALL must hold)

- the BA / PO owns ≥2 engagements where DoD reuse pays off
- named owner accepts the library
- deliverable types are categorisable (story / feature / release / contractor task)
- library can be reviewed quarterly

## Skip If (ANY kills it)

- single-engagement BA — overhead > value
- team prefers per-engagement bespoke DoD — defer to team preference
- no named owner — defer until owner exists

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| deliverable-type taxonomy | MD | BA / PO |
| prior-engagement DoD samples | MD | BA |
| named owner | org chart | BA / PO |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[contractor-brief-template-self-contained]] | Consumer of the contractor-task DoD. |
| [[use-case-modeling]] | Story / feature DoD anchors to use cases. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: by-type indexing, each item has rationale, ≥3 items per type, named owner per record, quarterly review cadence | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for DoD library: types[], items[], rationale, owner, last_reviewed | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: per-engagement reinvention, missing rationale, anonymous owner, stale library, scope creep into product-level AC | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: collect samples → categorise → write rationale → publish + assign owner | 600 |
| `content/06-decision-tree.xml` | essential | Tree on engagement count + owner + deliverable-type clarity | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-type DoD authoring. |
| `review_for_compliance` | opus | Regulated engagements needing audit-grade DoD. |

## Templates

| File | Purpose |
|------|---------|
| `templates/definition-of-done-library.json` | JSON skeleton for the DoD library. |
| `templates/definition-of-done-library.md` | Markdown skeleton with required fields. |
| `templates/_smoke-test.md` | Minimum viable DoD library. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-definition-of-done-library.py` | Validates the DoD library against the JSON Schema. | After library update; pre-commit. |

## Related

- [[contractor-brief-template-self-contained]]
- [[use-case-modeling]]
- [[user-story-mapping]]
- [[cr-impact-memo-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
