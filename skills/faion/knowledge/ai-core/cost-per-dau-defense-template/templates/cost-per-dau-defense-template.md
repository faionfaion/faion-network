<!--
purpose: 1-page Markdown skeleton for cost-per-DAU defense report.
consumes: cost ledger aggregate, drivers, peer benchmark, plan.
produces: single Markdown report for finance / business review.
depends-on: content/02-output-contract.xml schema.
token-budget-impact: ~190 tokens.
-->

# Cost-Per-DAU Defense — &lt;feature&gt;

- **report_id**: cpd-&lt;feature&gt;-q2-2026
- **owner**: &lt;handle — single named human, never "team"&gt;
- **last_reviewed**: 2026-05-22
- **version**: 1.0.0

## The number

**$0.0412 / DAU / day** measured over the last 30 days, against 84,210 DAU.

## Top 3 drivers (sum 75 percent)

| Driver | Pct |
|---|---|
| long-context inference | 38 |
| embedding refresh | 22 |
| redundant tool calls | 15 |

## Peer benchmark

- Perplexity Pro inference share: $0.038/DAU (https://example.com/perplexity-earnings-q1-2026, accessed 2026-05-19).

## 90-day plan (owner: kim@acme.com)

- Target: **$0.025 / DAU / day**
- Interventions:
  1. Swap to haiku for sub-100-token queries.
  2. Enable prompt caching on top 1000 questions.
  3. Deduplicate tool calls per session.

## Notes

&lt;e.g., 'ready for owner review', or 'supersedes cpd-...'.&gt;
