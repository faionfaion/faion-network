# Blurred Roles and Team Evolution

## Summary

**One-sentence:** Diagnoses a product team's role overlap (PM/eng/design/data/AI) as a Venn diagram with ownership gaps and duplications; output is a team-evolution report with hire/restructure recommendations.

**One-paragraph:** Diagnoses a product team's role overlap (PM/eng/design/data/AI) as a Venn diagram with ownership gaps and duplications; output is a team-evolution report with hire/restructure recommendations. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Post-Series-A scale-up: who owns what when PM, eng-lead, and design-lead overlap.
- AI-era role drift: PM doing prompt engineering, eng doing user research — diagnose drift.
- Hiring plan input: report says 'no one owns X' or 'two people duplicate Y'.
- Quarterly team review: track ownership gaps over time.

## Applies If (ALL must hold)

- Team has ≥4 people with overlapping responsibilities.
- Role drift symptoms observed (missed handoffs, duplicated work, orphaned decisions).
- Leadership has authority to restructure or hire.
- Team is willing to be candid in interviews / surveys.

## Skip If (ANY kills it)

- Team < 4 — every role gap is obvious without methodology.
- Leadership cannot restructure — diagnosis without action is theatre.
- Team will not be candid — diagnosis will be noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Org chart | roles + reports-to | HR |
| Responsibility map | Notion / RACI doc | PM ops |
| Interview transcripts | 1:1 anonymised notes | team |
| Recent decision log | last 30 days of product decisions + decider | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-blurred-roles-and-team-evolution` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-blurred-roles-team-evolution.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[competitive-positioning]]
- [[ai-feature-spec-contract]]
- [[annual-roadmap-vs-quarterly-okr-stitch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "report_id": "blurred-acme-2026q2",
  "owner": "hr@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "roles": [
    {
      "id": "pm",
      "title": "Product Manager",
      "headcount": 1
    },
    {
      "id": "eng-lead",
      "title": "Eng Lead",
      "headcount": 1
    },
    {
      "id": "design-lead",
      "title": "Design Lead",
      "headcount": 1
    },
    {
      "id": "data",
      "title": "Data Analyst",
      "headcount": 1
    }
  ],
  "overlap_map": [
    {
      "from": "pm",
      "to": "eng-lead",
      "areas": [
        "prompt-engineering",
        "spec authoring"
      ],
      "evidence": "interview 1:1 2026-05"
    }
  ],
  "ownership_gaps": [
    {
      "area": "ML evaluation harness",
      "evidence": "decision log 2026-04 nobody approved"
    }
  ],
  "duplications": [
    {
      "area": "competitor analysis",
      "owners": [
        "pm",
        "design-lead"
      ],
      "evidence": "two parallel reports 2026-04"
    }
  ],
  "recommendations": [
    {
      "action": "Hire ML PM",
      "owner": "cpo@acme.io",
      "due_cycle": "2026-Q3"
    }
  ],
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
