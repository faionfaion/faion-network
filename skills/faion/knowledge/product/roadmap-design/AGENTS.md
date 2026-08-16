# Roadmap Design

## Summary

**One-sentence:** Picks the roadmap format from the uncertainty level, then designs the roadmap in that format with explicit confidence per item, an internal source-of-truth plus one derived external view, and a named review cadence — so the roadmap steers instead of listing wishes.

**One-paragraph:** Replaces feature lists with outcome statements per horizon. Format comes first: uncertainty low → timeline, medium → Now/Next/Later, high → outcome-themed. Now items carry committed scope + owner; Next items carry hypotheses + dependencies; Later items carry bets + open questions. Confidence labels (high/medium/low) prevent the document from being read as a contract. One internal source-of-truth is maintained and every external view is derived from it with metric targets, confidence labels and owners stripped; both artefacts carry an explicit not-doing list and a published cadence.

**Ефективно для:**

- Solo founder or small-team PM whose roadmap doc drifts every 2 weeks; needs a structure that holds shape under reprioritisation without lying about commitments.
- Teams serving ≥2 audiences (internal team, customer, board) from one plan without maintaining two copies by hand.
- Anyone under stakeholder pressure for dates on work whose uncertainty does not support them.
- Audit / review surface: every artefact has an owner, evidence anchors and a review beat.

## Applies If (ALL must hold)

- Multi-stakeholder product where alignment beats individual feature scope.
- Quarterly planning cadence exists or is being established.
- Roadmap will be shared externally or with non-PM stakeholders.
- Uncertainty over the horizon can be assessed as low / medium / high.

## Skip If (ANY kills it)

- Single-developer 1-week scope where a plain task list is sufficient.
- Pre-product phase where there are no users to align with.
- Stable maintenance product with no strategic direction.
- Contract-defined deliverables — the timeline format is forced, so there is no format to design.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategic outcomes / OKRs | markdown | Strategy doc |
| Uncertainty assessment over the horizon | low/medium/high | Team |
| Confidence rubric | table | PM doc |
| Audience list for the roadmap (internal/external) | list | CRM / team |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/okr-setting` | Outcomes anchor the roadmap horizons. |
| `solo/product/product-planning/outcome-based-roadmaps` | Format option when uncertainty over the horizon is high. |
| `solo/product/product-operations/feature-prioritization-rice` | Within-horizon ranking when items contend. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules (format selection, horizons, confidence, cadence, audience split, not-doing) + skip + run rules | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-roadmap-design` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-roadmap-design` | haiku | Schema check + threshold checks; deterministic. |
| `review-roadmap-design` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/roadmap-design.md.j2` | Markdown skeleton for human-readable artefact rendering. |
| `templates/roadmap-design.md` | Markdown skeleton for human-readable artefact rendering. Generated from `templates/roadmap-design.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/roadmap-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/roadmap-diff.py` | Diffs two roadmap snapshots (moved / added / dropped) for the monthly review beat in r9. |
| `templates/external-roadmap.md.j2` | Customer-facing roadmap derived from the internal source of truth. |
| `templates/external-roadmap.md` | Customer-facing roadmap derived from the internal source of truth. Generated from `templates/external-roadmap.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/now-next-later.md.j2` | Internal Now/Next/Later roadmap (medium-uncertainty format). |
| `templates/now-next-later.md` | Internal Now/Next/Later roadmap (medium-uncertainty format). Generated from `templates/now-next-later.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/quarterly-outcome.md.j2` | Quarterly outcome-themed roadmap (high-uncertainty format). |
| `templates/quarterly-outcome.md` | Quarterly outcome-themed roadmap (high-uncertainty format). Generated from `templates/quarterly-outcome.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-roadmap-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[okr-setting]]
- [[outcome-based-roadmaps]]
- [[feature-prioritization-rice]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/roadmap-design.json`

```json
{
  "artefact_id": "roadmap-design-example",
  "version": "1.0.0",
  "last_reviewed": "2026-05-23",
  "horizon_quarters": 3,
  "uncertainty": "medium",
  "format": "now-next-later",
  "horizons": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "external_themes": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "not_doing": [
    "item-1",
    "item-2",
    "item-3"
  ],
  "confidence_rubric": {
    "key": "value"
  },
  "review_cadence": "review_cadence value",
  "audience": "audience value",
  "owner": "@solo-founder"
}
```

### `templates/roadmap-diff.py`

```python
"""roadmap-diff.py — diff two roadmap JSON snapshots for the monthly review (r9).

__faion_header__
purpose: Diff two roadmap snapshots so the monthly review sees what moved
consumes: Two roadmap JSON snapshots (previous and current)
produces: report
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: low — single python file, no output unless run

Usage: python roadmap-diff.py prev.json curr.json

Input JSON schema (each file):
{
  "now": [{"id": str, "theme": str, "confidence": str}, ...],
  "next": [{"id": str, "theme": str, "confidence": str}, ...],
  "later": [{"id": str}, ...]
}

Output (stdout): {"moved": {id: [prev_bucket, curr_bucket]}, "added": [id], "dropped": [id]}
"""
import json
import sys


def index_roadmap(rm: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for bucket in ("now", "next", "later"):
        for item in rm.get(bucket, []):
            result[item["id"]] = bucket
    return result


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: roadmap-diff.py prev.json curr.json", file=sys.stderr)
        sys.exit(2)

    prev = json.load(open(sys.argv[1]))
    curr = json.load(open(sys.argv[2]))

    p, c = index_roadmap(prev), index_roadmap(curr)
    moved = {k: [p[k], c[k]] for k in c if k in p and p[k] != c[k]}
    added = [k for k in c if k not in p]
    dropped = [k for k in p if k not in c]

    print(json.dumps({"moved": moved, "added": added, "dropped": dropped}, indent=2))


if __name__ == "__main__":
    main()
```
