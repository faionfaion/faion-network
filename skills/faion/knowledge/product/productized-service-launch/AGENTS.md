# Productized Service Launch

## Summary

**One-sentence:** Pins the launch playbook for a productized service (pricing page, outbound list, beta cohort, payment link, ship gates); output is a launch playbook spec with metrics targets.

**One-paragraph:** Pins the launch playbook for a productized service (pricing page, outbound list, beta cohort, payment link, ship gates); output is a launch playbook spec with metrics targets. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Design (see productized-service-design) is approved — ready to launch.
- First-paying-customer milestone: lock launch steps so timing is deliberate, not drift.
- Repeat launch of new productized offer: re-use playbook with deltas.
- Pre-launch dress rehearsal: walk every step before public traffic.

## Applies If (ALL must hold)

- Design spec approved (see productized-service-design).
- Pricing page draft + payment link exist.
- Outbound list (≥30 named prospects) ready.
- Beta cohort (≥3 prospects) committed to first batch.

## Skip If (ANY kills it)

- Design spec not approved — block until approved.
- Outbound list < 30 prospects — launch will starve.
- Beta cohort < 3 — feedback signal will be noise.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved design spec | design spec id | PM / founder |
| Pricing page draft | URL or staged page | marketing |
| Outbound list | ≥30 named prospects with email | sales / founder |
| Beta cohort commitment | ≥3 prospects + start date | sales |

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
| `draft-productized-service-launch` | sonnet | Output drafting needs structure + light judgement. |
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
| `scripts/validate-productized-service-launch.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[productized-service-design]]
- [[productized-service-canvas]]
- [[post-launch-72h-watch-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/artefact-instance.json`

```json
{
  "launch_id": "psl-acme-onboarding-2026q2",
  "owner": "alex@acme.io",
  "last_touched": "2026-05-23T11:00:00Z",
  "design_ref": "psd-acme-onboarding-2026q2",
  "pricing_page": {
    "url": "https://acme.io/services/onboarding",
    "evidence": "page live 2026-05-22"
  },
  "outbound_list": {
    "count": 42,
    "source": "linkedin + warm-intro list",
    "evidence": "outbound sheet 2026-05-22"
  },
  "beta_cohort": [
    {
      "company": "bigco",
      "contact": "vpe@bigco",
      "start": "2026-06-03"
    },
    {
      "company": "midco",
      "contact": "vpe@midco",
      "start": "2026-06-10"
    },
    {
      "company": "smallco",
      "contact": "cto@smallco",
      "start": "2026-06-17"
    }
  ],
  "ship_gates": [
    {
      "name": "payment link live",
      "evidence": "Stripe payment link id"
    },
    {
      "name": "outbound sent",
      "evidence": "outbound campaign id"
    }
  ],
  "metrics_targets": {
    "first_paying_customer_days": 14,
    "reply_rate": 0.25,
    "demo_to_close": 0.2
  },
  "template_version": "1.1.0",
  "status": "ready_for_review"
}
```
