# Agent Integration — Tax Basics for Solopreneurs

## When to use
- Maintaining a monthly tax-reserve calculator: pull revenue + deductible expense data from accounting software, compute set-aside, sweep to a separate savings account.
- Auto-categorizing transactions into deduction buckets (home office, software, marketing, professional services, equipment) with a human-review queue for ambiguous lines.
- Tracking quarterly estimate due dates and pre-computing payment amounts based on YTD profit.
- Comparing entity tax treatments (Sole Prop vs LLC vs S-Corp) at year-end based on actual numbers, surfacing when the S-Corp election threshold is crossed.
- Generating a year-end tax-prep package for the CPA: P&L, deduction summary, mileage log, equipment register, retirement contribution log.

## When NOT to use
- Filing returns. Agent-prepared returns without a CPA review are a malpractice / penalty risk. The agent prepares supporting docs only.
- Multi-state nexus determination, sales-tax compliance per state, international VAT/GST. Each is a specialist domain; the methodology is single-jurisdiction US-centric.
- Audit response. IRS / state tax authority correspondence is human-only with CPA / EA / tax attorney representation.
- Crypto / DeFi / NFT tax treatment. Agent-classified transactions here are unreliable and the tax code is unsettled.
- Non-US jurisdictions. The methodology references US Code (Schedule C, SE tax, S-Corp election, SEP-IRA). Don't apply to UK, EU, CA, AU, IN.

## Where it fails / limitations
- LLM-classified transactions hallucinate categories. "Software subscription" gets logged as a marketing expense, "client lunch" as travel. Need rules + human gate on edge cases.
- Tax law changes annually. SE wage base, contribution limits, standard mileage rate, Section 179 caps shift each year. Agent prompts that hardcode 2024 figures decay silently.
- "Reasonable salary" for S-Corp is fact-and-circumstance — IRS challenges aggressive splits. Agent should never auto-recommend a salary split below 40% of profit without flagging risk.
- Home office actual-method deduction creates depreciation recapture on home sale. Agent must alert when recommending it.
- Quarterly estimates use safe-harbor rules (110% prior year for high earners). Off-by-one in the rule selection produces underpayment penalties.
- Health insurance self-employed deduction has subtle interaction with spouse's employer-sponsored plan availability. Auto-applying the deduction can be wrong.

## Agentic workflow
The tax agent is a passive accountant assistant: (1) ETL — pulls transactions from QuickBooks / Xero / banks via API; (2) classifier — applies a rules engine first, LLM fallback only on unmatched lines; (3) ledger — posts categorized rows to a tax workbook with confidence scores; (4) human review — low-confidence and high-dollar lines surface to a queue; (5) reports — monthly tax-reserve, quarterly estimate, year-end CPA package. Critical: agent never moves money without explicit per-transfer approval; reserve-sweep is a recommendation, not an action.

### Recommended subagents
- `faion-growth-agent` (methodology frontmatter) — ops-side reporting and reserve calculations.
- `faion-sdd-executor-agent` — wraps year-end tax-prep as an SDD task with a test-plan: every income source reconciled to bank deposit, every deduction backed by receipt, totals tie to bank-balance delta.
- `password-scrubber-agent` — strips SSN/EIN/account numbers from any logged report.

### Prompt pattern
```
Goal: classify last 30 days of business transactions into deduction categories.
Inputs: transactions CSV (date, amount, merchant, memo); category rules table; vendor history.
Method: apply rules first; only call LLM for unmatched rows; require source URL or memo cue for each LLM classification.
Output: classified rows with confidence; rows < 0.8 confidence go to human queue; never silently drop.
Constraint: do NOT classify into "personal" — always require explicit human action to mark personal.
```

```
Goal: compute Q3 estimated tax payment.
Inputs: YTD net profit, prior-year tax liability, prior payments, filing status, state.
Method: safe-harbor lower of (90% current-year, 100% prior or 110% if AGI > $150k) ÷ 4, minus payments-to-date.
Output: payment amount + due date; show the rule applied; flag if any input estimated vs actual.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `quickbooks-python` | QBO API: transactions, categories, reports | https://developer.intuit.com |
| `xero-python` | Xero API equivalent | https://developer.xero.com |
| `plaid-python` | Pull bank transactions where accounting tool isn't connected | https://plaid.com/docs |
| `gnucash-cli` | OSS ledger if avoiding SaaS | https://www.gnucash.org |
| `beancount` / `fava` | Plain-text accounting (agent-friendly, version-controlled) | https://furius.ca/beancount/ |
| `pandas` + `python-dateutil` | Reserve calc, quarterly estimate calc | stdlib pip |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| QuickBooks Online | SaaS | Yes (API) | De facto US small-biz standard. |
| Xero | SaaS | Yes (API) | Strong outside US. |
| Wave | SaaS (free tier) | Partial | Limited API. |
| Bench | SaaS bookkeeping | Limited | Human bookkeepers + portal; agent can pull reports but not categorize. |
| Keeper Tax / Found | SaaS | Yes | Solopreneur-focused expense tracking with API. |
| Gusto / OnPay | SaaS payroll | Yes (API) | S-Corp salary runs. |
| Carry / Solo401k.com | SaaS | Partial | Solo 401k providers; agent can query balance, not contribute. |
| Beancount + Fava | OSS | Yes | Plain-text, GitOps-able books. |
| TurboTax / TaxAct / Drake | SaaS / desktop | Limited | Filing software; agents can prep import files only. |

## Templates & scripts
Inline: monthly tax-reserve calculator. Pulls QBO P&L, applies effective rate, suggests transfer.

```python
def monthly_reserve(revenue: float, deductible: float, effective_rate: float = 0.30) -> dict:
    net_profit = revenue - deductible
    if net_profit <= 0:
        return {"reserve_usd": 0, "note": "no profit; no reserve needed"}
    reserve = round(net_profit * effective_rate, 2)
    se_tax_estimate = round(net_profit * 0.9235 * 0.153, 2)
    return {
        "net_profit": net_profit,
        "reserve_usd": reserve,
        "se_tax_estimate": se_tax_estimate,
        "note": "transfer reserve to dedicated tax savings account; do NOT auto-execute",
    }
```

See `templates.md` for tax-planning checklist, monthly reserve, annual summary.

## Best practices
- Maintain a separate business bank account and dedicated tax-reserve savings account. Mixing personal/business kills deduction defensibility on audit.
- Use rules-based classification first; reserve LLM for tail cases. Determinism > probability for ledgers.
- Save every receipt to object storage (S3/R2) with date + vendor + amount + category metadata. Agent attaches links to ledger rows.
- Re-evaluate S-Corp election annually around mid-year, not at year-end (election is retroactive only if filed timely with reasonable cause).
- Track a mileage log via GPS app (MileIQ/Everlance) and reconcile monthly. The methodology mentions "travel" but mileage is the highest-audit-risk deduction; rigor matters.
- Coordinate retirement contributions with cash-flow forecast — Solo 401k has employee deferral + employer profit-share with separate deadlines.
- Engage a CPA / EA at least annually for review even if doing books in-house; agents are not signatures.

## AI-agent gotchas
- Hard-coded thresholds (SE tax wage base, 401k limit, Section 179) need annual updates. Pin the year explicitly in prompts and refuse to compute if year is stale.
- "Home office deduction" via simplified method ($5/sq ft × ≤300) ≠ actual method. Agent that sums both double-deducts.
- The agent will eagerly classify ambiguous transactions to maximize deductions. Bias toward false negatives (mis-flag as personal) rather than false positives (claim a personal expense as business).
- Quarterly estimate due dates are NOT calendar quarters: Q1 4/15, Q2 6/15, Q3 9/15, Q4 1/15 next year. Naive cron jobs miscompute.
- S-Corp shareholder-employee health insurance has special W-2 treatment (Box 1 income, not subject to FICA). Auto-categorizers miss this and overstate deduction.
- Privacy: tax data includes SSN, bank info, full income. Encrypt at rest, scrub from logs, never paste into a non-private LLM.
- Never let the agent reply on behalf of the founder to IRS notices — even apparently routine letters can have signature/penalty implications.
- Crypto on-chain reconciliation requires cost-basis lots (FIFO/HIFO/spec-id). Generic categorization misses gains/losses entirely.

## References
- https://www.irs.gov/businesses/small-businesses-self-employed
- https://www.irs.gov/forms-pubs/about-publication-535 (Business Expenses)
- https://www.irs.gov/forms-pubs/about-publication-587 (Business Use of Your Home)
- https://www.irs.gov/forms-pubs/about-form-1040-es (Estimated Tax)
- IRS Pub 560 (Retirement Plans for Small Business)
- Bench Tax Guide: https://bench.co/blog/tax-tips/
- Solopreneur S-Corp analysis: NerdWallet / Wise Bread / Kitces.com
