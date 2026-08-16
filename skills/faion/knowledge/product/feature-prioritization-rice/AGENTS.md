# Feature Prioritization RICE

## Summary

**One-sentence:** Produces a RICE-scored backlog config (Reach × Impact × Confidence ÷ Effort with named units + confidence-floor + evidence citations) so prioritisation stops being a gut-vote ritual.

**Ефективно для:** Solopreneur PMs whose RICE scores rank features but everyone disagrees what 'Reach' or 'Impact' means and Confidence is always 100%.

**One-paragraph:** RICE is widely deployed and widely vibe-coded — Reach gets confused with funnel-step counts, Impact uses an undeclared scale, Confidence defaults to 100%. This methodology pins Reach to a named unit (users / month or sessions / quarter), Impact to a 1-3 scale with anchor examples, Confidence to evidence-citation tiers (high/med/low) with rejection if no source cited, and Effort to person-weeks. Output is consumed by sprint planning + roadmap.

## Applies If (ALL must hold)

- Operator runs ≥5 candidate features competing for limited cycle scope.
- Operator has analytics data for reach estimates.
- Operator can name effort in person-weeks (or hours).
- A named anchor exists for Impact scale.

## Skip If (ANY kills it)

- Pre-PMF with no analytics — Reach is guess-work.
- Operator unwilling to cite Confidence sources — RICE collapses to opinion.
- Single-cycle one-off project — RICE overhead exceeds benefit.
- Already using WSJF / MoSCoW exclusively — pick one method to avoid duplicate scoring.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| candidate feature list | array | operator |
| reach unit chosen | enum (users/mo, sessions/Q, accounts/Y) | founder |
| impact anchor examples | array of 3 strings | team |
| effort unit chosen | enum (person-weeks, hours) | team |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/feature-prioritization-moscow` | Sibling — alternative method; pick one per cycle. |
| `solo/product/product-manager/backlog-management` | Upstream — backlog supplies candidates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `score_each_feature` | haiku | Apply numbers per feature against anchors. |
| `audit_confidence` | sonnet | Verify Confidence has cited source per row. |
| `rank_and_cut` | opus | Synthesis: apply RICE rank, find cut line, generate rationale. |

## Templates

| File | Purpose |
|---|---|
| `templates/feature-prioritization-rice.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/feature-prioritization-rice.md.j2` | Markdown skeleton with the required fields. |
| `templates/feature-prioritization-rice.md` | Markdown skeleton with the required fields. Generated from `templates/feature-prioritization-rice.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rice-scorecard.md.j2` | RICE scorecard skeleton — scores, per-feature rationale, strategic veto, post-ship actuals |
| `templates/rice-scorecard.md` | RICE scorecard skeleton — scores, per-feature rationale, strategic veto, post-ship actuals Generated from `templates/rice-scorecard.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/rice-decision-record.md.j2` | Per-feature RICE decision record with scoring, rank and co-signs. |
| `templates/rice-decision-record.md` | Per-feature RICE decision record with scoring, rank and co-signs. Generated from `templates/rice-decision-record.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-feature-prioritization-rice.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[feature-prioritization-moscow]] — related methodology.
- [[backlog-management]] — related methodology.
- [[rice-for-one-person-cheatsheet]] — related methodology.
- [[rice-for-design]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/feature-prioritization-rice.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.network/schema/feature-prioritization-rice.json",
  "title": "Feature Prioritization RICE Output Contract",
  "type": "object",
  "required": [
    "scoring_round_id",
    "reach_unit",
    "effort_unit",
    "impact_anchors",
    "rows",
    "cut_line",
    "owner",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "scoring_round_id": {
      "type": "string",
      "description": "round id (e.g. 2026-Q2)"
    },
    "reach_unit": {
      "type": "string",
      "description": "named unit"
    },
    "effort_unit": {
      "type": "string",
      "description": "named unit"
    },
    "impact_anchors": {
      "type": "array",
      "description": "3 cited examples",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "rows": {
      "type": "array",
      "description": "feature objects with reach, impact, confidence, effort, source, rice_score",
      "items": {
        "type": "object"
      },
      "minItems": 1
    },
    "cut_line": {
      "type": "number",
      "description": "score threshold"
    },
    "owner": {
      "type": "string",
      "description": "named owner"
    },
    "version": {
      "type": "string",
      "description": "semver"
    },
    "last_reviewed": {
      "type": "string",
      "description": "ISO date",
      "format": "date"
    }
  },
  "additionalProperties": true
}
```
