# PRD via AI Without Losing Why

## Summary

**One-sentence:** Pins a PRD authoring procedure that uses AI for drafting but locks the 'why' (customer evidence, business outcome, anti-goals) before any LLM expansion; output is a PRD spec with citation chain.

**One-paragraph:** Pins a PRD authoring procedure that uses AI for drafting but locks the 'why' (customer evidence, business outcome, anti-goals) before any LLM expansion; output is a PRD spec with citation chain. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- PM uses LLM to draft PRDs but downstream eng cannot tell signal from filler.
- Pre-feature kickoff: align 'why' before AI expands 'what' into prose.
- Anti-feature creep: anti-goals locked first so AI suggestions cannot reintroduce cut scope.
- Audit existing AI-drafted PRDs: identify which sections lost the 'why' under prose.

## Applies If (ALL must hold)

- Feature has ≥3 customer interview citations or ≥1 quantitative signal.
- Business outcome is one measurable sentence ('move X by Y in Z weeks').
- Anti-goals (explicit out-of-scope) can be listed.
- PM has authority to reject AI output that drifts from locked 'why'.

## Skip If (ANY kills it)

- No customer evidence — apply customer-discovery methodology first.
- No measurable business outcome — PRD will be aspirational.
- AI tool not approved for use in product specs (compliance gate).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer evidence pack | ≥3 quoted interviews + ≥1 quant signal | research |
| Business outcome | one measurable sentence | PM |
| Anti-goals list | ≥3 explicit out-of-scope items | PM |
| Approved AI tool | name + version + compliance status | ops |

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
| `draft-prd-via-ai-without-losing-why` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md.j2` | Markdown skeleton conforming to the output contract |
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract Generated from `templates/artefact-skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prd-via-ai-without-losing-why.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[ai-feature-spec-contract]]
- [[north-star-metric-design]]
- [[annual-roadmap-vs-quarterly-okr-stitch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "prd_id": "prd-onboarding-2026q2",
  "owner": "pm@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "why": {
    "customer_evidence": [
      {
        "interview_id": "i-1",
        "quote": "I gave up after the second step"
      }
    ],
    "quant_signal": "drop-off at step-2 = 41%",
    "evidence": "BI view fct_onboarding 2026-05"
  },
  "outcome": {
    "metric": "step-2 completion",
    "target": "+15pp",
    "window": "8 weeks",
    "evidence": "Q2 OKR doc"
  },
  "anti_goals": [
    "no full onboarding rewrite",
    "no new pricing tiers",
    "no SSO additions"
  ],
  "scope": [
    "replace step-2 with progressive disclosure",
    "add inline help microcopy",
    "instrument funnel events"
  ],
  "citation_chain": [
    {
      "section": "why",
      "source_id": "i-1"
    },
    {
      "section": "outcome",
      "source_id": "okr-q2"
    }
  ],
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
