# Solo Late-Fee & Pause-Clause Template

## Summary

**One-sentence:** Drop-in SOW / MSA contract language for tiered late fees + 14-day pause-right + paid re-engagement, with mandatory jurisdiction review per template — so a freelancer is not improvising contract terms during a dispute.

**One-paragraph:** Existing legal-compliance methodologies stop at "send an invoice and chase it." When a client goes 14 / 30 / 60 days past due the freelancer has no contractual lever and ends up negotiating from zero. This methodology pins the actual clause language — 1.5%/month tiered late fee, automatic pause right after 14 days unpaid, paid re-engagement fee on resumption — in a form that pastes into a SOW. Output is a typed `LateFeeClauseSpec` carrying clause text + numeric thresholds + jurisdiction review citation. Tier `pro` because solo SaaS founders rarely need it; freelancers and consultancies need it on every engagement.

**Ефективно для:**

- Drop-in contract clauses for fixed-price / T&M freelance engagements ≥ 4 weeks.
- Cross-jurisdiction reuse with explicit local-lawyer review per template version.
- Sibling to `late-invoice-dunning-sequence` — what to send before invoking pause clause.
- Audit defensibility: every clause cites the jurisdictional opinion that grounds it.

## Applies If (ALL must hold)

- Operator sells services on T&M or fixed-price contract (not subscription).
- Engagements run ≥ 4 weeks.
- Existing SOW or MSA template the clause attaches to.
- Jurisdiction allows late fees (most do, with rate caps).

## Skip If (ANY kills it)

- Product is SaaS / subscription — billing automated, no late-fee mechanic needed.
- Engagement < 2 weeks and pre-paid — overhead exceeds risk.
- Jurisdiction prohibits late fees outright (some EU consumer contexts) — defer to legal.
- Corporate procurement contract in place — their paper, their terms.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Base SOW / MSA template | Markdown / doc | freelancer |
| Local lawyer review (per jurisdiction) | signed memo | counsel |
| Client payment-terms baseline | Net 14/30/60 | client |
| Previous quarter clause usage | JSON | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-change-order-mini-contract]] | Sibling — CR template references this clause for payment terms. |
| [[vendor-margin-defense-checklist]] | Bleed cumulative &gt; 10% triggers pause-clause discussion. |
| [[proposal-red-team-checklist]] | Contract-surface pause-point reviews this clause. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: clause-in-sow-not-email, late-fee-tiered, pause-after-14-days, re-engagement-fee, jurisdiction-review | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `LateFeeClauseSpec` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: clause-in-email, flat-fee, no-pause, no-re-engagement-fee, no-jurisdiction-review, retroactive-application | ~900 |
| `content/04-procedure.xml` | medium | 5-step: jurisdiction review → fill clause → attach to SOW → invoke when overdue → annual update | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: jurisdiction allows? SOW present? overdue days? → invoke / pause / escalate | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `fill-clause` | sonnet | Per-jurisdiction wording adjustments. |
| `assess-overdue` | haiku | Mechanical days-overdue arithmetic. |
| `pause-notification` | sonnet | Diplomatic but firm copy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md.j2` | LateFeeClauseSpec skeleton with clause text + thresholds |
| `templates/skeleton.md` | LateFeeClauseSpec skeleton with clause text + thresholds Generated from `templates/skeleton.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/header.yaml` | Frontmatter schema |
| `templates/_smoke-test.json` | Minimum viable filled `LateFeeClauseSpec` |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-late-fee-and-pause-clause-template.py` | Validate: late-fee tier numeric, pause_days &gt;= 14, re-engagement_fee numeric, jurisdiction review citation | Pre-merge |
| `scripts/staleness-check.py` | Flag specs whose jurisdiction review > 12 months | Weekly cron |

## Related

- [[solo-change-order-mini-contract]]
- [[vendor-margin-defense-checklist]]
- [[proposal-red-team-checklist]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps jurisdiction allowance + SOW presence + days-overdue to invoke / pause / escalate. Every leaf references a rule from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/header.yaml`

```yaml
owner:
  role: ""
  person: ""
last_reviewed: ""
version: ""
```

### `templates/_smoke-test.json`

```json
{
  "spec_id": "smoke",
  "jurisdiction": "US-CA",
  "header": {
    "owner": {
      "role": "freelancer",
      "person": "alex"
    },
    "last_reviewed": "2026-05-10",
    "version": "1.0"
  },
  "late_fee_tiers": [
    {
      "after_days": 14,
      "rate_pct_per_month": 1.5
    },
    {
      "after_days": 30,
      "rate_pct_per_month": 3.0
    }
  ],
  "pause_days": 14,
  "re_engagement_fee_usd": 500,
  "jurisdiction_review": {
    "reviewed_by": "counsel-handle",
    "reviewed_at": "2026-02-10",
    "memo_link": "drive://legal/us-ca-late-fee.pdf"
  },
  "clause_text": "Late payment fees: invoices unpaid beyond 14 days accrue a 1.5%/month fee. After 30 days, 3.0%/month. Pause right: Vendor may suspend work after 14 days unpaid with 5-business-day notice. Re-engagement: $500 paid in advance to resume work after pause."
}
```
