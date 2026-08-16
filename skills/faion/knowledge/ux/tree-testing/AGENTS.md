# Tree Testing: Validate Information Architecture Before Building

## Summary

**One-sentence:** Produces a tree-testing study config that validates a site's information architecture with task-based navigation through a text-only hierarchy — separating IA validation from visual/interaction design.

**One-paragraph:** Tree testing evaluates the findability of topics in a site hierarchy by giving users tasks and navigating a text-only tree (no design, no content). It separates the validation of IA from visual/interaction design and produces data-driven answers (success rate, directness, first-click) for IA debates. This methodology emits a study config: tree dump (≤4 levels), 5-8 tasks ranked by importance, sample plan (≥30 users for stat power), per-task success and directness targets, and analysis plan with first-click + path-trace metrics.

**Ефективно для:**

- Pre-design IA validation — менш дешеві аргументи про навігацію.
- Comparative IA test (variant A vs B).
- Post-launch findability audit для existing site.
- Onboarding-flow nav check без витрат на high-fidelity prototype.

## Applies If (ALL must hold)

- Site has ≥10 nav nodes; IA decisions are still open.
- ≥30 participants representative of audience can be recruited.
- Findings will influence design (not just documented).

## Skip If (ANY kills it)

- Single-page or pure linear flow — no tree to test.
- Visual or interaction questions — use prototype testing instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Proposed nav tree | indented list or JSON | IA designer |
| Task list | Markdown | research |
| Recruiting plan | panel or list | research ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | self-contained methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: text-only-tree, tasks-ranked-by-importance, sample-size-min-30, metrics-mandatory, depth-cap-4-levels | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `build-tree` | haiku | Mechanical extraction. |
| `author-tasks` | sonnet | Task wording neutrality. |
| `analyse-results` | sonnet | Multi-metric synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/tree-test-config.json` | Skeleton tree-test config |
| `templates/task-template.md.j2` | Task-writing template |
| `templates/task-template.md` | Task-writing template Generated from `templates/task-template.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tree-testing.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[surveys]]
- [[diary-studies]]
- [[personas]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by study goal (single vs comparative IA) and enforces depth + metric completeness. Each leaf cites a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/tree-test-config.json`

```json
{
  "tree": {
    "nodes": [
      "home",
      "products"
    ],
    "depth": 1
  },
  "tasks": [],
  "sample_plan": {
    "n_per_arm": 50,
    "arms": [
      "A"
    ]
  },
  "metrics": [
    "success_rate",
    "directness",
    "first_click"
  ]
}
```
