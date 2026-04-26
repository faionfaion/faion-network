# Agent Integration — Financial Planning

## When to use
- Solopreneur has initial revenue and needs to plan sustainable growth
- Product reaches breakeven and owner must decide reinvestment allocation
- Runway drops below 6 months; need scenario modeling to prioritize cuts
- Quarterly review cycle is due and projections need updating
- Preparing for a pricing change or major spend decision (ads, contractor)

## When NOT to use
- Pre-revenue stage with no real data — use financial-basics instead
- Seeking GAAP accounting or investor-grade reporting (requires a CPA, not an agent)
- Complex equity or cap-table planning (use Carta or legal counsel)
- Multi-entity corporate structures — agent assumptions won't hold

## Where it fails / limitations
- Projections rely on assumed growth rates; agents cannot know market conditions
- Variable-revenue businesses (courses, seasonal) need wider safety margins than the templates show
- Agents cannot pull live bank/payment data unless given explicit tool access
- Tax implications vary by jurisdiction — agent output is pre-tax unless context is provided

## Agentic workflow
An agent is most useful here for building and refreshing structured projection tables from raw inputs
(MRR, expense list, churn rate) and formatting a monthly review narrative. The agent should be
given the current P&L snapshot as context, then asked to produce the 3-month or 12-month cash
flow table, flag runway risk, and output the reinvestment allocation using the framework tiers.
Human review is required before any actual spend or distribution decision.

### Recommended subagents
- `faion-growth-agent` (referenced in README) — financial modeling, monthly review generation
- A dedicated `financial-review-agent` could be defined to run monthly: ingest Stripe/QuickBooks export → produce review doc → flag anomalies

### Prompt pattern
```
You are a financial planning assistant for a solopreneur SaaS.
Current state: MRR=$X, monthly expenses=$Y, cash=$Z.
Build a 3-month cash flow table and calculate runway.
Flag if runway drops below 3 months at any point.
Output: markdown table + one-paragraph risk summary.
```

```
Given profit=$X this month, apply the reinvestment framework:
profit < $5K → 50% reinvest / 30% owner / 20% reserve.
Output allocation in dollars and a brief rationale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `stripe-cli` | Pull MRR and charge data locally | https://stripe.com/docs/stripe-cli |
| `ledger` / `hledger` | Plain-text accounting, cash flow queries | https://hledger.org |
| `visidata` | Inspect CSV exports from QuickBooks/Wave | https://www.visidata.org |
| `python -m csv` + pandas | Scripted monthly roll-up from export files | stdlib + pip |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Stripe | SaaS | Yes — REST API | Revenue, MRR, churn data via API |
| Baremetrics | SaaS | Yes — REST API | Pre-computed SaaS metrics (MRR, LTV, CAC) |
| Wave | SaaS | Partial — no public API | Export CSV; agent parses offline |
| QuickBooks Online | SaaS | Yes — REST API (OAuth2) | Full P&L; requires OAuth flow, not trivial |
| ProfitWell | SaaS | Yes — REST API | Subscription analytics, pricing intelligence |
| Mosaic | SaaS | Partial | FP&A platform; API available on paid plans |

## Templates & scripts
Inline script — pulls MRR from Stripe and calculates runway:

```python
import stripe, os

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]

# Sum active subscription MRR
subs = stripe.Subscription.list(status="active", limit=100)
mrr = sum(
    s["items"]["data"][0]["price"]["unit_amount"] / 100
    for s in subs.auto_paging_iter()
    if s["items"]["data"][0]["price"]["recurring"]["interval"] == "month"
)

monthly_expenses = float(os.environ.get("MONTHLY_EXPENSES", "0"))
cash = float(os.environ.get("CASH_BALANCE", "0"))

net = mrr - monthly_expenses
runway = cash / monthly_expenses if monthly_expenses > 0 else float("inf")

print(f"MRR: ${mrr:,.0f}")
print(f"Net monthly: ${net:,.0f}")
print(f"Runway: {runway:.1f} months")
print("WARNING: runway < 3 months" if runway < 3 else "Runway OK")
```

## Best practices
- Always separate owner draw from operating profit before calculating reinvestment — mixing them obscures true business health
- Build the 12-month forecast bottom-up from known customer count and ARPU, not top-down from desired revenue
- Lock a minimum reserve percentage (20%) before any discretionary spend; adjust only after emergency fund is fully funded
- Track CAC and LTV monthly alongside P&L — a healthy margin with deteriorating LTV:CAC signals future cash flow risk
- Run two scenarios each quarter: base case (flat growth) and stress case (20% revenue drop) — stress case sets minimum acceptable runway
- Annual budget should be set in Q4 for Q1 start; mid-year budget revisions need a written rationale to prevent drift

## AI-agent gotchas
- Agents will hallucinate specific financial figures if not given actual data — always inject real numbers as context, not ask the agent to estimate them
- Currency and locale: specify currency symbol and decimal convention explicitly; agents default to USD and may misparse European-format numbers
- Multi-currency businesses require explicit FX rate injection; agents should not look up live rates unless given a real-time tool
- Agents should not store financial data between sessions without an explicit memory/persistence mechanism — each session needs fresh context
- Human-in-loop checkpoint required before any automated payment, transfer, or pricing change triggered by agent output
- Agents may apply the reinvestment framework mechanically without recognizing that exceptional months (e.g., one-time payments) skew the numbers — instruct agent to flag non-recurring revenue separately

## References
- https://www.saastr.com/financial-planning/ — SaaS-specific financial planning patterns
- https://www.profitwell.com/recur/all/financial-metrics — SaaS metrics definitions and benchmarks
- https://baremetrics.com/resources — Real-time dashboard examples and metric explanations
- https://www.mosaic.tech/resources — FP&A methodology for scaling companies
- Profit First by Mike Michalowicz — allocation-first cash management system (especially useful for variable-revenue solopreneurs)
