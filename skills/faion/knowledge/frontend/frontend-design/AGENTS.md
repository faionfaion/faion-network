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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/` parent context | vocabulary, neighbouring methodologies |
| [[design-tokens-basics]] | upstream context this methodology builds on |
| [[css-in-js-basics]] | sibling discipline cited in decision tree |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules: brief first, ≥3-axis divergence, per-variant rationale, working code not mockups, explicit selection, Storybook handoff, discoverable designs folder, screenshot comparison before selection, tokens before components, pinned Storybook versions, colocated component+story+test, skip contract | 1600 |
| `content/01-rules.xml` | essential | Variant-diversity constraints, the 3-5 ceiling, variant-local token persistence, per-variant a11y gate, rationale requirement, runnable variants | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/02-workflow.xml` | medium | Four-phase agent workflow with the brainstorm/refinement dispatch prompts and the agent gotchas | 1400 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom/root-cause/fix, incl. deciding from static frames, components before tokens, Storybook version rot | 1100 |
| `content/04-procedure.xml` | essential | 9-step procedure: brief → brainstorm → render comparison → review → refine → extract tokens → Storybook → components → artefact | 1000 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-frontend-design-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |
| `extract-tokens` | sonnet | Read the selected variant's CSS into primitive + semantic token tiers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-frontend-design.py --self-test` |
| `templates/frontend-spec.md.j2` | Full design-spec skeleton: brief, variant table, chosen variant + rationale, token table, pinned Storybook versions, planned components |
| `templates/frontend-spec.md` | Full design-spec skeleton: brief, variant table, chosen variant + rationale, token table, pinned Storybook versions, planned components Generated from `templates/frontend-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-frontend-design.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |
| `scripts/render-variants.sh` | Render every variant at desktop + mobile widths and stitch the side-by-side comparison grid | Before the selection step; the screenshot gate depends on it |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[design-tokens-basics]]
- [[css-in-js-basics]]
- [[mobile-responsive]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "artefact_id": "frontend-design-2026-05-23",
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "status": "ready_for_review",
  "brief_path": "draft",
  "variants": [
    "item-1",
    {
      "key": "value-1"
    },
    {
      "key": "value-2"
    }
  ],
  "selected_variant": "draft",
  "selection_rationale": "draft",
  "storybook_stories": [
    "item-1"
  ],
  "component_paths": [
    "item-1"
  ]
}
```
