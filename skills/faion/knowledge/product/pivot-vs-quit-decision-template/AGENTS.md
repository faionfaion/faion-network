# Pivot vs Quit Decision Template

## Summary

**One-sentence:** Pins a decision record comparing pivot-to-v2 versus full shutdown using product signals, runway, founder energy, and customer pull; output is a signed decision-record artefact.

**One-paragraph:** Pins a decision record comparing pivot-to-v2 versus full shutdown using product signals, runway, founder energy, and customer pull; output is a signed decision-record artefact. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Solo founder facing failed v1 launch with measurable customer signal disagreement.
- Co-founder pair where one wants pivot and one wants quit — needs single source of truth.
- Pre-shutdown audit before refunding customers or pivoting positioning.
- Investor / board comm: explain pivot OR shutdown with explicit evidence trail.

## Applies If (ALL must hold)

- Product launched ≥3 months ago with measurable usage data.
- Founder energy + runway constraints have been honestly assessed in writing.
- ≥3 customer interviews completed in the last 30 days.
- Pivot hypothesis (v2 candidate) is specific and testable, not vague.

## Skip If (ANY kills it)

- Pre-launch — no signal to evaluate, use pmf-rubric-for-solos instead.
- Founder cannot commit to honest assessment of energy / runway — decision will be theatre.
- Quit option already politically decided — write a closure plan, not a comparison.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Usage data snapshot | 3 months of activity events | warehouse |
| Customer interview notes | ≥3 transcripts last 30 days | user research |
| Financial runway | months of expenses covered | accounting |
| Energy + commitment self-rating | scale 1-5 with notes | founder |

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
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-pivot-vs-quit-decision-template` | sonnet | Output drafting needs structure + light judgement. |
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
| `scripts/validate-pivot-vs-quit-decision-template.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[pmf-rubric-for-solos]]
- [[portfolio-sunset-decision-frame]]
- [[freelancer-to-saas-time-box]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "decision_id": "pivot-quit-acme-2026q2",
  "owner": "alex@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "current_state": {
    "weekly_active": 28,
    "mrr": 410,
    "runway_months": 8,
    "evidence": "BI snapshot 2026-05-22 + bank 2026-05-22"
  },
  "pivot_option": {
    "description": "Reposition to enterprise procurement teams",
    "hypothesis": "10 procurement teams pre-pay $500/mo within 60 days",
    "evidence": "3 procurement interviews 2026-05"
  },
  "quit_option": {
    "description": "Refund all paid users + open-source codebase + sunset domain",
    "cost": "$2,100 refunds + 2 weeks of cleanup",
    "evidence": "Stripe refund estimate 2026-05-22"
  },
  "criteria_scores": {
    "customer_pull_pivot": 3,
    "customer_pull_quit": 0,
    "founder_energy": 3,
    "runway_fit_pivot": 4,
    "runway_fit_quit": 5
  },
  "decision": "pivot",
  "rationale": "procurement signal strong + runway fits 60-day test",
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
