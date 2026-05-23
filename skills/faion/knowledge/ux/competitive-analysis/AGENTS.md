# Competitive UX Analysis

## Summary

**One-sentence:** Benchmark direct and adjacent competitors on selected UX dimensions using a repeatable rubric so positioning decisions and design choices reference comparable evidence.

**One-paragraph:** Benchmark direct and adjacent competitors on selected UX dimensions using a repeatable rubric so positioning decisions and design choices reference comparable evidence.

**Ефективно для:**

- Solo founders or small teams shipping under time pressure.
- Cross-functional reviewers needing a shared, evidence-grounded artefact.
- Methodology owners maintaining quality gates over time.
- Subagent pipelines that need a deterministic output shape.

## Applies If (ALL must hold)

- Entering a market or repositioning and need a defensible baseline.
- Three to seven direct competitors exist and are publicly accessible.
- Stakeholders disagree on what 'industry standard' looks like.
- Feature parity vs differentiation is being decided.
- A rubric can be agreed before evaluation to avoid cherry-picking.

## Skip If (ANY kills it)

- Novel category with no real competitors — switch to discovery research.
- Closed-platform competitors that cannot be tested without paid access.
- Team will use the report only to justify a pre-made decision.
- Single feature change — heuristic evaluation is cheaper.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Competitor short-list | markdown | Product manager |
| Rubric with weighted criteria | spreadsheet | Research lead |
| Account/test access | credentials | Procurement |
| Screen-capture toolchain | tool list | Researcher |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-ui-designer/heuristic-evaluation` | Heuristic checklist seeds the rubric. |
| `solo/ux/ux-researcher/user-interviews` | User vocabulary informs the criteria. |

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
| `templates/competitive-analysis.json` | JSON skeleton conforming to the output contract schema. |
| `templates/competitive-analysis.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitive-analysis.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[heuristic-evaluation]]
- [[content-audit]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
