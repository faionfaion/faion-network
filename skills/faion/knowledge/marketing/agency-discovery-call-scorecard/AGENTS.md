# Agency Discovery Call Scorecard

## Summary

**One-sentence:** Generates a 0-100 numeric scorecard (fit / budget / urgency / decision-maker) post-discovery-call so agencies compare leads on a single axis.

**One-paragraph:** Generates a 0-100 numeric scorecard (fit / budget / urgency / decision-maker) post-discovery-call so agencies compare leads on a single axis. Use it when agency веде >1 discovery call/тиждень — потрібен порівняльний signal. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Agency веде >1 discovery call/тиждень — потрібен порівняльний signal.
- Score consumed for binary decision (advance/reject/prioritize).
- Чотири осі: fit, budget, urgency, decision-maker з weighted points.
- Weekly retro reviews scorecard calibration drift.

## Applies If (ALL must hold)

- The agency runs more than one discovery call a week, so leads need one comparable score.
- A written ICP (industry, size, service line) exists for the fit anchors to count against.
- The agency knows its annual contract value bands, so budget anchors can be currency ranges.
- The person who was on each call can score it within 24 hours with a quote per axis.
- A weekly pipeline retro exists where advance rate and close rate of advanced leads are looked at.

## Skip If (ANY kills it)

- One discovery call a week or fewer: qualify by judgement and revisit at higher volume.
- No written ICP: write the criteria first; fit anchors cannot be observable without them.
- The score is wanted for a "discuss" band rather than a binary advance / reject: this rubric has one threshold by design.
- Calls are scored days later from CRM notes by someone who was not on them: the evidence rule cannot be met.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ICP criteria | three named criteria: industry, company size, service line | agency positioning doc |
| Closed-deal history | closed-won / closed-lost with annual value and who signed, last two quarters | CRM export |
| Annual contract value bands | floor and ceiling amounts with currency | finance / founders |
| Discovery call notes or recording | transcript or notes with prospect quotes on budget, timing, sign-off | the call, within 24 hours |
| Previous rubric version | rubric JSON with version, date, reason | this methodology's earlier output |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 8 rules: four axes, weights sum to 1, observable anchors, 0-100 formula, single threshold, verified decision-maker, 24h scoring with evidence, versioned calibration | 1750 |
| `content/02-output-contract.xml` | essential | Draft-07 schema of the versioned rubric: four axes with two-decimal weights (sum 1.0, max 0.5), observable anchors per axis type, 0-100 formula, single threshold with the binary rule, weekly same-version retro, and scored leads with anchor index, evidence and authority per axis within 24 hours; valid and invalid rubrics; 8 forbidden patterns | ~3750 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 7 steps: write the ICP criteria, set the four axes and weights, write observable anchors, fix formula and threshold, score each call within 24 hours with evidence and verified authority, validate, run the weekly same-version retro | ~1450 |
| `content/05-examples.xml` | recommended | Complete rubric v3 (0.3 / 0.3 / 0.2 / 0.2, EUR budget bands, threshold 60) with Nordwind Logistics scored at 75 and advanced, note per value, plus the rubric as usually written and what the validator prints | ~1900 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-agency-discovery-call-scorecard.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/agency-discovery-call-scorecard.rubric.md.j2` | Markdown rubric skeleton: version block, four axes with observable anchors, formula and threshold, weekly retro, one scored-call block |
| `templates/agency-discovery-call-scorecard.rubric.md` | Markdown rubric skeleton: version block, four axes with observable anchors, formula and threshold, weekly retro, one scored-call block. Generated from `templates/agency-discovery-call-scorecard.rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/agency-discovery-call-scorecard.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-discovery-call-scorecard.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
