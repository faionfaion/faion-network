# Decision Rationale Capture

## Summary

**One-sentence:** A versioned decision record capturing the decision, alternatives considered, evidence, dissent, and named owner so the program can audit 'why did we do X?' a year later.

**One-paragraph:** Programs forget why they made decisions; the next change request asks 'wait, why did we exclude option B?' and no one remembers. This methodology pins decisions in a versioned record: decision text, alternatives considered, evidence cited, dissent acknowledged, named owner, last_reviewed. Output: a YAML / Markdown record per decision committed to the decision log.

**Ефективно для:**

- Architectural decisions on long-lived systems.
- Vendor / build / buy decisions.
- Compliance-relevant decisions audited later.
- Stakeholder-conflict resolutions where dissent matters.

## Applies If (ALL must hold)

- the decision has long-term consequences (>3 months impact)
- named owner accepts the record
- evidence sources exist and are citable
- the decision is non-trivial (alternatives existed)

## Skip If (ANY kills it)

- trivial day-to-day decisions — overhead > value
- decision not yet made — use decision-options-memo-template instead
- no named owner — fix ownership first

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| decision text | MD | BA / PM |
| alternatives considered | MD | BA |
| evidence sources | URLs / MD | BA |
| named owner | org chart | BA / PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[decision-options-memo-template]] | Source of options + recommendation. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: bound scope, typed input, named owner, versioned record, detector-first | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for decision record: decision, alternatives, evidence, dissent, owner, version, last_reviewed | 700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: inputs invented, owner collapsed, post-hoc rationale, version frozen, scope creep | 900 |
| `content/04-procedure.xml` | essential | 4-step procedure: capture decision → list alternatives → cite evidence → record dissent + owner | 600 |
| `content/06-decision-tree.xml` | essential | Tree on long-term impact + alternatives presence + owner availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill. |
| `synthesize_decision` | sonnet | Per-decision authoring. |
| `review_for_compliance` | opus | High-stakes regulated decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-rationale-capture.json` | JSON skeleton for the decision record. |
| `templates/decision-rationale-capture.md` | Markdown skeleton with required fields. |
| `templates/_smoke-test.md` | Minimum viable decision record. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-rationale-capture.py` | Validates the decision record against the JSON Schema. | After decision is made; pre-commit on the decision log. |

## Related

- [[decision-options-memo-template]]
- [[cr-impact-memo-template]]
- [[cr-options-matrix-template]]
- [[definition-of-done-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
