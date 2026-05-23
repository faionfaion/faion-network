# Tech Radar (ThoughtWorks-Style)

## Summary

**One-sentence:** Produces a `tech-radar.md` artefact with Adopt / Trial / Assess / Hold quadrants that captures the team's shared opinion on tooling and patterns.

**One-paragraph:** Tech Radar (ThoughtWorks-Style) produces a decision-record that fixes a recurring decision in the sdd domain. It pins the artefact shape, attaches evidence, and blocks unfit inputs via the decision tree. Apply when the preconditions hold; otherwise the decision tree routes you to skip-this-methodology.

**Ефективно для:**

- Запобігти 7 state-mgmt libs у одній репі — фіксована позиція команди.
- Quarterly tech radar review: що ввести / прибрати.
- Onboarding: junior бачить, що команда поточно ADOPT.
- Audit: чому ми обрали X, а не Y — у радарі видно.
- Cross-team alignment: один радар на дивізіон.

## Applies If (ALL must hold)

- Team has ≥5 engineers and growing tech surface.
- Tooling/library choices have become contentious.
- Quarterly review cadence exists or can be established.

## Skip If (ANY kills it)

- Solo or 2-person team — radar is overkill.
- Team has a working radar on cadence already.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tooling inventory | Markdown | tech lead |
| Adoption / hold candidates | Markdown | team |
| Quarterly review schedule | YAML | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | This methodology has no upstream dependencies. |

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
| `draft-tech-radar-thoughtworks-style` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tech-radar.md` | Markdown radar with quadrants + entries + evidence column |
| `templates/tech-radar.schema.json` | JSON Schema for the radar artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tech-radar-thoughtworks-style.py` | Validate produced artefact against schema | CI on each artefact change; pre-commit |

## Related

- [[adr-consequence-evidence-binding]]
- [[internal-rfc-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (input shape, infra availability, decision class) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
