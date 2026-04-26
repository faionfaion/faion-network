# Agent Integration — Tax Compliance & Filing

## When to use
- US-based solopreneur or small-team SaaS hitting first profitable year and needs quarterly-estimate cadence.
- Multi-state nexus surfaces (selling SaaS into CA/NY/WA, physical-goods crossing thresholds) and you need a sales-tax compliance plan.
- Year-end planning when LLC profit clears the threshold for S-Corp election (~$80K SE income).
- International seller hitting EU/UK VAT thresholds, OSS registration, or Stripe Tax onboarding.

## When NOT to use
- As a substitute for a CPA on novel situations: equity comp, R&D credits, multi-entity structures, ERC, audit defense.
- For determining liability in jurisdictions you've never operated in — agents will produce confident-sounding but wrong nexus interpretations.
- When a notice has already arrived from IRS / state agency — go directly to a tax pro; agent helps draft response only.
- Real-time tax calculations on customer transactions — use Stripe Tax / Avalara / TaxJar APIs, not an LLM.

## Where it fails / limitations
- Tax law is jurisdiction-specific and time-sensitive; LLM training data lags 6-18 months and frequently states pre-2024 rules as current.
- Safe-harbor calculation depends on whether last-year AGI exceeded $150K — agents miss the 110% nuance constantly.
- State sales-tax thresholds vary ($100K or 200 transactions in some, $500K elsewhere) — flat reasoning fails.
- "Personal vs business" allocation rules (home office, vehicle, meals 50% post-2023) require source-document review, not summarization.
- Penalty-and-interest math depends on federal short-term rate published quarterly; LLMs hallucinate rates.

## Agentic workflow
Use Claude subagents to organize records, reconcile bookkeeping exports against bank statements, classify expenses, surface deduction candidates, and prepare a CPA handoff packet. Never let an agent file a return or commit to a tax position — the agent prepares; the human (and ideally a CPA) decides. Pipeline: monthly bookkeeping reconciliation (agent) → category audit (agent) → quarterly estimate calc draft (agent) → CPA review (human) → year-end deduction sweep (agent) → filing (human + tax software).

### Recommended subagents
- `general-purpose` — receipt parsing (vision input), expense categorization, transaction matching against statements.
- `password-scrubber-agent` — redact bank/SSN/EIN data before any logs or shared snippets leave local disk.
- Custom `tax-prep-agent` (build): owns the year-end CPA-handoff folder; outputs P&L, mileage log summary, deduction schedule, asset register.

### Prompt pattern
- "Given this CSV of business-bank-account transactions for Q1, propose IRS Schedule C category for each row. Flag any with confidence < 0.8. Total per category in a summary table."
- "Compare last-year tax-return Form 1040 line 24 with current YTD profit. Compute safe-harbor quarterly = max(prior-tax × 1.0 or 1.1 if AGI > $150K, current × 0.25). Show both numbers and flag higher."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `beancount` / `fava` | Plain-text double-entry bookkeeping with audit trail | `pip install beancount fava` |
| `hledger` | Plain-text accounting alternative | https://hledger.org |
| `ofxparser` (Python) | Parse bank OFX/QFX exports | `pip install ofxtools` |
| `pdftotext` (poppler) | Extract text from receipts/W-2s/1099s | `apt install poppler-utils` |
| `csvkit` | Slice/dice CSV exports from QuickBooks/Stripe | `pip install csvkit` |
| Stripe CLI | Pull `tax_transactions` for sales-tax filing | `stripe login` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| QuickBooks Online | SaaS | API yes | De-facto US small-biz bookkeeping |
| Wave | SaaS | API limited | Free tier, basic API |
| Xero | SaaS | API yes | Best API of bookkeeping platforms |
| FreshBooks | SaaS | API yes | Service-business focus |
| TurboTax | SaaS | No public API | Consumer/sole-prop filing |
| TaxAct | SaaS | No public API | Cheaper alternative |
| Stripe Tax | SaaS | API yes | Calc + collect + remit US/EU |
| Avalara AvaTax | SaaS | API yes | Enterprise-grade sales-tax |
| TaxJar | SaaS | API yes | SMB sales-tax + auto-file |
| Anrok | SaaS | API yes | SaaS-native sales-tax |
| Pilot / Bench | SaaS | API limited | Bookkeeping-as-service |
| Gusto | SaaS | API yes | Payroll-tax filing |
| 1099 / W-2 generators (Track1099, Tax1099) | SaaS | API yes | Year-end contractor docs |

## Templates & scripts
See `templates.md` for tax calendar and year-end checklist. Inline safe-harbor calc:

```python
# safe_harbor.py — quarterly federal estimate
def quarterly_estimate(prior_year_tax, prior_year_agi, current_ytd_profit, ytd_quarter):
    multiplier = 1.10 if prior_year_agi > 150_000 else 1.00
    safe_harbor_annual = prior_year_tax * multiplier
    current_method_annual = current_ytd_profit * (4 / ytd_quarter) * 0.30  # ~30% blended
    target_annual = max(safe_harbor_annual, current_method_annual)
    paid_to_date = 0  # plug in actual prior-quarter payments
    return (target_annual / 4) - 0  # simplistic per-quarter

print(f"Q estimate: ${quarterly_estimate(24000, 145000, 80000, 2):,.0f}")
```

## Best practices
- Separate accounts day 1: business checking + business credit card; commingling is the single biggest audit risk for small operators.
- Sweep 25-30% of every payout into a tax-savings sub-account on receipt; never spend pretax cash.
- Keep a single source-of-truth folder structure (`taxes/<year>/<quarter>/`) and back it up to two locations.
- Reconcile monthly, not annually; year-end reconciliation is where deductions get lost.
- Convert receipts to PDF + structured row in an "expenses" CSV/Beancount file at capture time.
- Reassess S-Corp election yearly once SE-eligible income passes ~$80K; stop overpaying SE tax.
- For multi-state SaaS, register for "marketplace facilitator" treatment first if you sell on a marketplace; reduces direct nexus.

## AI-agent gotchas
- LLMs cite rules from prior tax years confidently — always require the agent to cite IRS publication number + revision date; verify against IRS.gov.
- Threshold drift: standard deduction, mileage rate, HSA limits, 401(k) limits change yearly; agent must pull current-year values, not infer.
- State-specific advice: do not trust an agent on California / New York / Washington edge cases without a CPA in the loop.
- Agent should never claim a deduction percentage ("you can deduct 100% of meals") without quoting the underlying source — meals are 50% by default since 2023.
- Don't paste full tax IDs, SSNs, EINs, or bank account numbers into prompts — use scrubber pipeline first; expect agents to leak anything in their context.
- Agents miss the difference between "tax filing deadline" and "estimated payment deadline" (April 15 includes both Q1 + prior-year filing). Force explicit dual labeling.
- For audit response or 1099-K reconciliation issues, escalate to human + CPA immediately; never let agent draft anything that looks like legal/IRS-facing communication without sign-off.

## References
- IRS Tax Calendar for Small Businesses: https://www.irs.gov/businesses/small-businesses-self-employed/irs-tax-calendar-for-businesses-and-self-employed
- IRS Pub 334 (Tax Guide for Small Business): https://www.irs.gov/forms-pubs/about-publication-334
- IRS Pub 505 (Tax Withholding and Estimated Tax): https://www.irs.gov/forms-pubs/about-publication-505
- Stripe Tax docs: https://stripe.com/docs/tax
- TaxJar State Sales-Tax Guides: https://www.taxjar.com/sales-tax/states
- AICPA / NASBA state tax pages
