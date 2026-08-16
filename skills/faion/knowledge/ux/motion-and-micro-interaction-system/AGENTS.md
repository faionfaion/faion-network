# Motion and Micro-Interaction System

## Summary

**One-sentence:** Tokenised motion system (durations, easings, choreography rules, prefers-reduced-motion, perceived-perf budget) sitting alongside the design-system colour and typography token sets.

**One-paragraph:** Tokenised motion system (durations, easings, choreography rules, prefers-reduced-motion, perceived-perf budget) sitting alongside the design-system colour and typography token sets. The methodology pins inputs to citable sources, runs ≥5 testable rules to reject fabricated or un-anchored outputs, and emits an artefact that a downstream agent or named human reviewer can sign off without re-deriving the reasoning. Decision tree in `content/06-decision-tree.xml` routes the caller to apply-or-skip based on observable signals.

**Ефективно для:**

- Adding a motion layer to a design system that only ships colour and type tokens.
- Eliminating per-screen ad-hoc animations across a product surface.
- Pinning a single 'easing.standard' value so engineers stop copying from CodePen.
- Coordinating perceived-perf budget with the FE performance team.
- Wiring the system into Figma variables and Style Dictionary output.

## Applies If (ALL must hold)

- The triggering activity for motion-and-micro-interaction-system appears in the operator's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer for the artefact — output will be orphaned regardless of quality.
- Inputs are not available from a citable source-of-truth (paraphrased substitutes are worse than skipping).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Input brief | Markdown or ticket | operator / upstream methodology |
| Source-of-truth refs | URLs, transcript ids, dashboard snapshots | external systems |
| Prior artefact (if any) | this methodology's prior output | repository / doc store |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/ux/` parent skill context | vocabulary, neighbouring methodologies |
| [[design-system-governance]] | upstream context this methodology builds on |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output per step | 800 |
| `content/05-examples.xml` | essential | Worked end-to-end example anchored to the output contract | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → conclusion referencing rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applies-or-skip` | sonnet | Apply decision tree against observable signals. |
| `fill-motion-and-micro-interaction-system-artefact` | sonnet | Bounded template fill with citation discipline. |
| `synthesize-recommendation` | opus | Cross-input synthesis + rationale write-up. |


## Templates

| File | Purpose |
|------|---------|
| `templates/output-skeleton.md.j2` | Minimal skeleton conforming to the output contract |
| `templates/output-skeleton.md` | Minimal skeleton conforming to the output contract Generated from `templates/output-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Smallest filled-in example used by `validate-<slug>.py --self-test` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-motion-and-micro-interaction-system.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns; pre-commit; CI on each artefact change |


## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[design-system-governance]]
- [[semantic-tokens-and-modes]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from observable input signals (presence of required prerequisites, fit of the triggering activity, availability of citable sources) and routes the caller to one of the rule conclusions in `content/01-core-rules.xml` — either apply the full methodology, apply a reduced variant, or skip and route to a sibling methodology.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/_smoke-test.json`

```json
{
  "owner": "ruslan@faion.net",
  "last_touched": "2026-05-23T12:00:00Z",
  "template_version": "1.1.0",
  "artefact_id": "motion-and-micro-interaction-system-2026-05-23",
  "system_id": "draft",
  "duration_tokens": [
    "draft-item"
  ],
  "easing_tokens": [
    "draft-item"
  ],
  "choreography_rules": [
    "draft-item"
  ],
  "reduced_motion_policy": "draft",
  "perceived_perf_budget_ms": 1,
  "platform_outputs": [
    "draft-item"
  ],
  "owners": "draft",
  "evidence": [
    {
      "source": "https://example.com/source-1",
      "citation": "verbatim quote from source"
    }
  ],
  "status": "ready_for_review"
}
```
