# Retainer vs Project Rubric

## Summary

**One-sentence:** A BARS-anchored rubric (4-7 named dimensions on 1-5 anchored scales, evidence per score) that recommends retainer vs project engagement model per opportunity, replacing gut-call sales conversations with a defensible artefact.

**One-paragraph:** Micro-agencies routinely default to project work because it sells faster; retainer revenue is what makes the business viable but founders don't pursue it because no shared rubric exists. This methodology defines the rubric — predictability-of-work, churn-risk, scope-creep risk, margin profile, founder-fatigue impact, etc. — with explicit 1-5 BARS anchors so two reviewers reach the same score. Output is a typed `EngagementRubric` per opportunity carrying scores, evidence per score, aggregated total, and recommended engagement model (retainer / project / hybrid / decline). Versioned + signed; quarterly review compares predictions to actual outcomes.

**Ефективно для:**

- Productizing one service: which existing clients should move to retainer.
- New-opportunity triage: do we pitch retainer, project, or decline?
- Cross-reviewer alignment via BARS anchored scales.
- Quarterly review: rubric predictions vs actual outcomes recalibrate dimensions.

## Applies If (ALL must hold)

- Founder evaluates ≥ 3 retainer-vs-project decisions per year.
- 4-7 named dimensions can be defined and anchored 1-5 each.
- Sample opportunities available for calibration.
- Founder has authority to set engagement model without partner sign-off.

## Skip If (ANY kills it)

- Single dominant engagement model (pure agency or pure SaaS) — rubric is overhead.
- < 3 decisions per year — gut-call cheaper than rule.
- Regulated industry with mandated retainer / contract format.
- No named owner.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Opportunity brief | Markdown | sales / CRM |
| Anchor scoring corpus (≥ 3 known-good) | YAML | history |
| Reviewer panel (≥ 2) | stakeholder register | founder + partner |
| Last quarter rubric outcomes | JSON | this methodology |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[retainer-renewal-decision-rule]] | Sibling — applied to in-flight retainers at renewal. |
| [[vendor-margin-defense-checklist]] | Margin profile dimension consumes weekly margin signal. |
| [[proposal-red-team-checklist]] | Rubric output feeds the proposal red-team's `Scope & Assumptions` pause-point. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: named dimensions, evidence per score, aggregation rule, calibration pass, versioned | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `EngagementRubric` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: cargo-cult, ownership ambiguity, drift, leakage, no outcome review, trigger drift | ~900 |
| `content/04-procedure.xml` | medium | 5-step: scaffold → score each dimension → aggregate → calibrate vs anchors → publish | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: aggregated score → retainer / project / hybrid / decline | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-dimension` | sonnet | Per-dimension BARS judgment with evidence selection. |
| `aggregate-and-recommend` | haiku | Mechanical sum + threshold map. |
| `calibration-pass` | opus | Cross-reviewer alignment with judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | EngagementRubric skeleton with default dimensions |
| `templates/skeleton.md` | EngagementRubric skeleton with default dimensions Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `EngagementRubric` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-retainer-vs-project-rubric.py` | Validate `EngagementRubric`: dimension count, BARS anchors, evidence per score, owner | Pre-merge |
| `scripts/staleness-check.py` | Flag rubrics whose `last_reviewed` > 90 days | Weekly cron |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[retainer-renewal-decision-rule]]
- [[vendor-margin-defense-checklist]]
- [[proposal-red-team-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps aggregated rubric total to retainer / project / hybrid / decline. Every leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/header.yaml`

```yaml
owner:
  role: ""
  person: ""
last_reviewed: ""
version: ""
reviewers: []
```

### `templates/_smoke-test.json`

```json
{
  "opportunity_id": "smoke",
  "header": {
    "owner": {
      "role": "founder",
      "person": "founder-handle"
    },
    "last_reviewed": "2026-05-10",
    "version": "1.0",
    "reviewers": [
      "founder",
      "partner"
    ]
  },
  "dimensions": [
    {
      "dimension_id": "predictability",
      "name": "Predictability of work",
      "score": 4,
      "anchor_text": "Recurring monthly cadence with stable shape",
      "evidence": "brief#cadence"
    },
    {
      "dimension_id": "churn_risk",
      "name": "Churn risk",
      "score": 3,
      "anchor_text": "Stakeholder change every 12mo",
      "evidence": "brief#stakeholders"
    },
    {
      "dimension_id": "scope_creep_risk",
      "name": "Scope creep risk",
      "score": 3,
      "anchor_text": "Some out-of-SOW history",
      "evidence": "transcript-2026-04"
    },
    {
      "dimension_id": "margin_profile",
      "name": "Margin profile",
      "score": 4,
      "anchor_text": "28% margin estimate",
      "evidence": "p_and_l-est.pdf"
    }
  ],
  "aggregate_score": 14,
  "recommendation": "project"
}
```
