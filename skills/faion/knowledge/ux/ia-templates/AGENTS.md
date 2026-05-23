# Information Architecture — Templates

## Summary

**One-sentence:** Produce the four canonical IA artefacts — sitemap, taxonomy document, navigation specification, page inventory — using shared templates so every project starts from the same skeleton.

**One-paragraph:** Produce the four canonical IA artefacts — sitemap, taxonomy document, navigation specification, page inventory — using shared templates so every project starts from the same skeleton.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- An IA framework has been chosen and now needs concrete artefacts.
- Multiple contributors must produce IA documents consistently across pages.
- An audit needs to compare current site structure against a documented baseline.
- A content migration requires a page inventory with owners and metadata.
- Stakeholders need a single source of truth for the navigation specification.

## Skip If (ANY kills it)

- Project is below 20 pages — a single sitemap diagram is sufficient.
- No agreed IA framework yet — run ia-framework first.
- Contributors will not maintain the artefacts after handover.
- Headless CMS already encodes structure as content models — extend those instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved IA framework | markdown | ia-framework output |
| Content inventory CSV | csv | Page-listing export |
| Stakeholder owner map | markdown | Org chart + product team |
| Brand and label guidelines | markdown | Marketing or design system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-researcher/ia-framework` | Framework decisions drive which templates to instantiate. |
| `solo/ux/ux-ui-designer/content-audit` | Inventory artefact feeds the page-inventory template. |

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
| `templates/ia-templates.json` | JSON skeleton conforming to the output contract schema. |
| `templates/ia-templates.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ia-templates.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[ia-framework]]
- [[content-audit]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
