---
slug: frontend-design
tier: solo
group: dev
domain: frontend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Four-phase workflow exploring 3\u20135 distinct UI variants before committing to one: capture requirements, brainstorm via agent into designs/variant-N-slug/, user selects + refines, Storybook + component agents finalise; produces a design folder with N variants and a selected-variant manifest."
content_id: "58bb6eef20d16532"
complexity: deep
produces: playbook-step
est_tokens: 4900
tags: ["frontend", "solo", "design", "variant-exploration", "ui"]
---
# Frontend Design Variant Exploration

## Summary

**One-sentence:** Four-phase workflow exploring 3–5 distinct UI variants before committing to one: capture requirements, brainstorm via agent into designs/variant-N-slug/, user selects + refines, Storybook + component agents finalise; produces a design folder with N variants and a selected-variant manifest.

**One-paragraph:** Four-phase workflow exploring 3–5 distinct UI variants before committing to one: capture requirements, brainstorm via agent into designs/variant-N-slug/, user selects + refines, Storybook + component agents finalise; produces a design folder with N variants and a selected-variant manifest. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Greenfield SaaS landings + dashboards.
- Internal tools where 'just build it' has produced 3 ugly attempts already.
- Solo founders using LLMs to compress design exploration from days to hours.
- Replatforming when an old UI must be re-imagined from scratch.

## Applies If (ALL must hold)

- Starting a new UI surface (landing, dashboard, form) with no visual direction.
- Solo / small-team LLM-assisted design exploration is acceptable.
- Storybook is the deliverable platform.
- Variants must differ on ≥3 axes (typeface, density, color, motion).

## Skip If (ANY kills it)

- Mature design system already constrains options — convergence beats divergence.
- Marketing page where copy / photography drives the design.
- Strict brand-guideline enforcement — variant exploration generates ineligible options.
- One-off internal tool where any UI suffices.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[design-tokens-basics]] | upstream context this methodology builds on |
| [[css-in-js-basics]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-frontend-design-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-frontend-design.py --self-test` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-frontend-design.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |

## Related

- [[design-tokens-basics]]
- [[css-in-js-basics]]
- [[mobile-responsive]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.
