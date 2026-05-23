# Strategy Analysis — Current State

## Summary

**One-sentence:** A documented as-is environment (processes, systems, capabilities, pain points, constraints) with named owners and primary-source evidence per claim.

**One-paragraph:** Future-state work is fantasy without a real current-state baseline. This methodology captures the as-is environment: process maps (BPMN or text), system inventory, capability assessment, pain points with frequency + impact, and constraints (regulatory, contractual, technical). Every claim is owned and evidenced. Output: a current-state spec that feeds `strategy-analysis-future-state` and `strategy-analysis-gap-analysis`.

**Ефективно для:**

- Pre-transformation discovery on legacy systems.
- RFP authoring requiring an accurate as-is description.
- Compliance audits demanding process documentation.
- Re-engineering programs where the process is partially undocumented.

## Applies If (ALL must hold)

- the as-is environment is partially undocumented or contested
- a future-state or gap analysis depends on this artefact
- process / system owners are available for interviews
- evidence sources (logs, screenshots, interviews) are accessible

## Skip If (ANY kills it)

- the as-is is already well-documented (≤90 days old) — refresh selectively
- the engagement is greenfield (no current-state exists) — produce future-state only
- the project is too tactical to warrant a full as-is map

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| business-need spec | MD / wiki | strategy-analysis-business-need |
| system inventory / CMDB extract | CSV / JSON | IT / ops |
| process owners interview availability | calendar | BA |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-analysis-business-need]] | Frames which slices of the as-is are relevant. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: every claim has an evidence source, named process/system owners, pain points quantified, constraints categorised, max depth 3 process levels | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for current-state spec: processes, systems, capabilities, pain-points, constraints | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: narrative without evidence, anonymous owners, infinite process depth, opinionated pain ranking, stale snapshot | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: scope → interview → document → quantify pain → review with owners | 600 |
| `content/05-examples.xml` | essential | Worked example: customer-onboarding as-is spec excerpt | 500 |
| `content/06-decision-tree.xml` | essential | Tree on engagement type + as-is freshness + owner availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `interview_synthesis` | sonnet | Convert interview notes into structured spec rows. |
| `evidence_audit` | haiku | Mechanical check that each claim has a source. |
| `pain_quantification` | sonnet | Convert qualitative pain into frequency + impact. |
| `constraint_categorisation` | sonnet | Categorise constraints into regulatory / contractual / technical / cultural. |

## Templates

| File | Purpose |
|------|---------|
| `templates/current-state-spec.md` | Markdown skeleton with all as-is sections. |
| `templates/process-map.md` | Text-based process map (no ASCII art). |
| `templates/_smoke-test.md` | Minimum viable current-state spec. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-analysis-current-state.py` | Validates current-state spec against the JSON Schema. | After interview round; pre-commit. |

## Related

- [[strategy-analysis-business-need]]
- [[strategy-analysis-future-state]]
- [[strategy-analysis-gap-analysis]]
- [[use-case-modeling]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
