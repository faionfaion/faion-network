# Card Sorting

## Summary

**One-sentence:** Run open, closed, or hybrid card-sorting sessions with target users to discover how they group content, then synthesise into an evidence-based taxonomy.

**One-paragraph:** Run open, closed, or hybrid card-sorting sessions with target users to discover how they group content, then synthesise into an evidence-based taxonomy.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- New IA needed and the team lacks data on how users group concepts.
- Existing taxonomy is being challenged by analytics or qualitative reports.
- At least 15 representative participants can be recruited.
- Content set is between 30 and 80 items — sorting fatigue stays manageable.
- Team will act on results by adjusting categories before tree-testing.

## Skip If (ANY kills it)

- Below 30 items — first-click testing answers the question more cheaply.
- Above 100 items — split into themed mini-sorts first.
- Single-user internal tool with no shared taxonomy.
- Strong analytics already point to a clear winning taxonomy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Card list with definitions | csv | Content inventory |
| Recruitment screener | form | Research ops |
| Sorting platform setup | url | Optimal Workshop / similar |
| Analysis spreadsheet template | xlsx | Researcher toolbox |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/user-interviews` | Quotes inform card labels and wording. |
| `solo/ux/ux-researcher/ia-framework` | Existing IA hypotheses define candidate categories. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules + run/skip rules | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-artefact` | sonnet | Section-by-section judgement against the rubric. |
| `lint-and-validate` | haiku | Deterministic schema validation + forbidden-pattern check. |
| `final-review` | opus | Cross-section coherence and stakeholder readiness. |

## Templates

| File | Purpose |
|------|---------|
| `templates/card-sorting.json` | JSON skeleton conforming to the output contract schema. |
| `templates/card-sorting.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-card-sorting.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[ia-framework]]
- [[ia-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
