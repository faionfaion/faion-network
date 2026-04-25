# Agent Integration — Financial Basics & Tracking

## When to use
- Bootstrapping financial visibility for a solo or small-team SaaS/info-product business.
- Generating monthly P&L from raw bank + Stripe + accounting data without a bookkeeper.
- Computing unit economics (LTV, CAC, payback, gross margin) on demand from MRR/churn/ad-spend feeds.
- Detecting drift in expense categories vs target percentages (alerts when marketing > 30% of revenue, etc.).
- Pre-investor / pre-acquisition: produce a clean snapshot of unit economics and cash position.

## When NOT to use
- Tax filing, audit, or any work that becomes part of an official tax return — needs a CPA, not an agent.
- Multi-currency consolidation with hedging — out of scope.
- Equity, options, 409A valuations, cap tables — different domain (corporate finance).
- Fraud or anomaly investigation — agents can flag but not adjudicate.
- Anything that touches reg-CF, Reg-A, or public-market reporting.

## Where it fails / limitations
- Targets like ">70% gross margin SaaS" are heuristics, not truths; vary by sub-vertical and stage.
- LTV = ARPU/churn formula breaks for high-churn early-stage products and for products with non-linear retention curves; cohort-based LTV is more accurate but heavier.
- CAC math here treats all marketing spend as acquisition; ignores brand/retention spillover.
- "Rule of 40" applies to growth-stage SaaS; misleading for bootstrapped lifestyle businesses.
- Source README assumes US accounting conventions; cash vs accrual distinction left implicit.
- No provision for deferred revenue, refunds-pending, or chargeback reserves.

## Agentic workflow
Stand up a daily ETL agent that pulls Stripe (revenue, refunds, MRR, churn), the bank account (cash, expenses), and the ad platforms (spend by channel), then writes to a sheet/db and emits a Friday email with current-month P&L draft + unit economics dashboard. The principal reviews and corrects categorization. Pair with `ops-pricing-strategy`, `ops-financial-planning`, `ops-tax-basics` for wider workflows.

### Recommended subagents
- `faion-growth-agent` (source README) — primary owner of P&L assembly and unit-econ math.
- `faion-researcher` — benchmarks vs comparable SaaS (Bessemer, OpenView, ChartMogul reports).
- `faion-improver` — quarterly: identify cost-savings opportunities by diffing actuals vs target percentages.
- General-purpose Claude subagent — categorize uncategorized bank transactions using rules + LLM fallback.

### Prompt pattern
```
Inputs: stripe_export.csv (subscriptions), bank_export.csv (all transactions),
ads_export.csv (spend by channel), prior_month.json (categorization rules).
Output: monthly_pnl.json matching the schema in templates.md, plus list of uncategorized
transactions for human review. Do NOT silently bucket "Unknown" into a category.
```

```
Given mrr=<X>, churn=<Y>%, arpu=<Z>, ad_spend=<S>, new_customers=<N>, cogs=<C>,
compute: LTV, CAC, LTV:CAC, payback months, gross margin, Rule of 40.
Flag any metric outside healthy ranges (LTV:CAC<3, payback>12mo, GM<70%).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe` | Pull payments, subscriptions, refunds | `brew install stripe/stripe-cli/stripe` |
| `plaid` API | Bank-account aggregation across institutions | plaid.com/docs |
| `gnucash-cli` | Local OSS double-entry accounting | gnucash.org |
| `ledger` / `hledger` | Plain-text accounting; agent-perfect | hledger.org |
| `beancount` | Plain-text accounting + Python ecosystem | beancount.github.io |
| `ynab-sdk` | YNAB budgeting API | api.ynab.com |
| `quickbooks-online` SDK | QBO API for accounting export/import | developer.intuit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe | SaaS | Yes | Best-in-class API; MRR + churn directly queryable. |
| Mercury | SaaS | Partial | Read-only API for transactions; great for solo. |
| Relay | SaaS | Partial | Bank export; less API-rich than Mercury. |
| QuickBooks Online | SaaS | Yes | Mature API; the de-facto SMB ledger. |
| Xero | SaaS | Yes | API parity with QBO; stronger outside US. |
| Wave | SaaS | Limited | Free tier; weaker API. |
| Baremetrics | SaaS | Yes | Pulls Stripe metrics; chart + dashboard out-of-box. |
| ChartMogul | SaaS | Yes | Stripe + custom; better cohort retention analysis. |
| ProfitWell (Paddle Retain) | SaaS | Yes | Free MRR/churn dashboard; API for retention. |
| Pilot / Bench | SaaS | No | Human bookkeepers; agent prepares inputs only. |
| Beancount + Fava | OSS | Yes | Self-hosted, plain-text; perfect for git-tracked finance. |

## Templates & scripts
See `templates.md` for monthly P&L and unit-economics dashboard. Inline unit-econ helper:

```python
# Unit-economics snapshot
def unit_economics(arpu, monthly_churn_rate, ad_spend, new_customers, gross_margin):
    if monthly_churn_rate <= 0 or new_customers <= 0:
        return {"error": "invalid inputs"}
    ltv = arpu / monthly_churn_rate
    cac = ad_spend / new_customers
    payback_months = cac / (arpu * gross_margin) if arpu * gross_margin > 0 else None
    return {
        "ltv": round(ltv, 2),
        "cac": round(cac, 2),
        "ltv_cac": round(ltv / cac, 2) if cac else None,
        "payback_months": round(payback_months, 1) if payback_months else None,
        "healthy": (ltv / cac >= 3) and (payback_months and payback_months <= 12),
    }

# Example: ARPU $50, churn 5%, $5000 spend, 50 customers, 75% GM
print(unit_economics(50, 0.05, 5000, 50, 0.75))
```

## Best practices
- Separate personal and business banking from day 1; mixing them invalidates most of the categorization automation.
- Use plain-text accounting (beancount/hledger) if you're git-comfortable — agents can review-diff books like code.
- Reconcile monthly within the first 5 days of the next month; later than that, signal is gone.
- Define your unit of "customer" once (signup? first paid? still active?) and never silently change the formula.
- Track cohorted retention (month-over-month survival per signup cohort) instead of aggregate churn for any product older than 6 months.
- Cash-flow forecast at least one quarter ahead; agent can update weekly from current burn + MRR.
- Don't optimize for tax savings at the cost of decision-clarity; prioritize "do I know my numbers" first.

## AI-agent gotchas
- Categorization drift: agents trained on prior months will silently re-bucket new vendors. Always hold out an "unknown" bucket and require human resolution.
- LLMs round numbers in ways that compound; force currency math via Python (Decimal), not natural-language reasoning.
- Stripe MRR includes upgrades/downgrades/coupons in non-obvious ways; do not trust an agent's first-pass MRR calc — reconcile against Stripe's own MRR endpoint.
- Refunds and chargebacks lag revenue by 30-90 days; an agent reporting "this month's profit" before the chargeback window closes will overstate.
- Double-counting risk: contractor payments may appear in both bank and a marketplace's escrow export. Always dedupe by external transaction ID.
- LTV calculations on small N are noise. Suppress dashboards under 100 paid customers — show absolute revenue + raw churn instead.
- Privacy: pushing transaction-level data through external LLM APIs is a leak vector. Use local models for raw data; only summary metrics through Anthropic APIs.

## References
- Y Combinator startup financial models — https://www.ycombinator.com/library/6f-startup-financial-models
- Bessemer State of the Cloud (annual benchmarks) — https://www.bvp.com/atlas/the-state-of-the-cloud-2024
- ChartMogul SaaS metrics glossary — https://chartmogul.com/resources/saas-metrics-cheat-sheet/
- Stripe Sigma + MRR docs — https://stripe.com/docs/billing/subscriptions/metrics
- Beancount documentation — https://beancount.github.io/docs/
- Sibling methodology: `ops-financial-planning/README.md`
- Sibling methodology: `ops-pricing-strategy/README.md`
