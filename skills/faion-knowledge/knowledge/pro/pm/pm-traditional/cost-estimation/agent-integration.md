# Agent Integration — Cost Estimation (PM Traditional)

## When to use
- Producing the initial budget for a feature / project / RFP response with a defensible cost baseline.
- Bottom-up cost roll-up from an approved WBS (each work package gets labor + tools + infra cost).
- Build-vs-buy and build-vs-SaaS decisions where opportunity cost matters.
- Updating the cost baseline after a change-control event so EVM tracking remains valid.
- Solopreneur "true cost" analysis where own time is priced at market rate vs cash out-of-pocket.
- Producing rough order of magnitude (ROM) at idea stage and progressively refining as scope solidifies.

## When NOT to use
- Agile teams that fund the team capacity, not the project. Cost is "team-month run-rate × duration", not bottom-up sum.
- Pre-discovery exploration where requirements are <30% defined. Output will be fantasy precision; use ROM (±50%) instead.
- Already-negotiated fixed-fee contracts — re-estimating internally has no contractual force, only informs margin.
- Small internal tasks (<1 week) where the estimate cost exceeds the work cost.

## Where it fails / limitations
- Three-point estimation gives false precision: PERT mean assumes a beta distribution rarely true in software; pessimistic cost is consistently *under*-estimated by humans and LLMs.
- Contingency reserve sized as a flat 10-25% ignores the risk register; high-risk projects need risk-driven contingency, not a percentage.
- Overhead loading varies by region (1.3x in low-tax markets, 1.8x+ in high-tax / high-benefit markets); a single multiplier is wrong cross-border.
- LLM benchmark hourly rates come from training data 12-24 months stale; current rates can differ by 30%+.
- Currency / FX volatility in multi-region projects is not captured by static numbers.
- Sunk-cost bias: re-estimates after work has started anchor on the original number rather than re-deriving from remaining scope.
- Cost-loaded WBS hides resource calendar effects — a $100k labour line at 50% utilisation actually costs $200k of elapsed budget.

## Agentic workflow
The agent is a calculator + auditor, not a decision-maker. Feed it the WBS (work packages with effort hours), a labor rate card with sources, an infra/tools list, and a risk register; it produces a structured cost baseline (direct, indirect, contingency, management reserve) plus a Monte Carlo sensitivity. A human approves the numbers before they enter the budget. Re-run on every approved change request to keep the baseline live.

### Recommended subagents
- `cost-estimator` — reads `wbs.yaml` + `rates.yaml`, outputs cost-baseline JSON with PERT 3-point per work package.
- `sensitivity-analyzer` — Monte Carlo over the 3-point distributions, returns P50/P80/P95 totals with cost-driver tornado.
- `risk-driven-reserve` — converts risk register entries (probability × impact × cost exposure) into a risk-driven contingency, replacing flat %.
- `faion-sdd-executor` — drives implementation through quality gates once estimates become tasks.

### Prompt pattern
```
Inputs:
- wbs.yaml: [{id, name, effort_optimistic_h, most_likely_h, pessimistic_h, role}]
- rates.yaml: hourly rate per role, with cite source field
- overhead: 1.3 (fully-loaded multiplier on labor)
- risks.yaml: risk register with cost exposure per risk
- duration_months: <int>
- tools.yaml: SaaS subscriptions in scope

Output JSON:
{ "direct_costs_usd": {...},
  "indirect_costs_usd": {...},
  "risk_driven_contingency_usd": ...,
  "management_reserve_usd": ...,
  "cost_baseline_usd": ...,
  "budget_at_completion_usd": ...,
  "sensitivity": {"p50": ..., "p80": ..., "p95": ...,
                  "tornado": [{"driver":"...", "delta":...}]},
  "assumptions": ["...explicit..."] }

Rules:
- No invented rates; rates.yaml must include source per role.
- Round to nearest USD; never $X.XX precision.
- If any input missing, return {"error": "..."} not a guess.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `infracost` | Cloud infra cost from Terraform / Pulumi diff | https://www.infracost.io/ |
| `numpy` + `scipy.stats` | Beta / triangular / lognormal distributions for PERT | https://scipy.org/ |
| `montecarlo-cli` (`mcli`) | Quick CLI Monte Carlo on cost ranges | https://github.com/cetra3/mcli |
| `gh` / `jira-cli` | Pull effort / story-point data for bottom-up | https://cli.github.com/ |
| `awscost-cli` / `gcloud billing` / `az consumption` | Live cloud cost benchmarking | https://docs.aws.amazon.com/cli/latest/reference/ce/ |
| `xlsxwriter` / `openpyxl` | Generate cost worksheets in Excel format | https://xlsxwriter.readthedocs.io/ |
| `currency-converter` (`cnvrt`) | FX rates for multi-region budgets | OpenExchangeRates / ECB API |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Float / Resource Guru | SaaS | Yes — REST | Capacity + rate cards; CSV export |
| Harvest / Toggl | SaaS | Yes — REST | Actual hours by role for re-baselining |
| Forecast (Harvest) | SaaS | Yes — REST | Project budget vs actuals |
| Productive.io | SaaS | Yes — REST | Agency-grade cost + margin |
| Mosaic / Runn | SaaS | Yes — REST | Resource forecasting |
| Infracost | SaaS / OSS | Yes | Infra cost baseline + PR diff |
| Vantage / CloudZero | SaaS | Yes — REST | Cloud unit cost (cost per customer / per request) |
| Notion / Confluence | SaaS | Yes — REST | Where the cost baseline doc lives |
| Excel / Google Sheets API | SaaS | Yes — REST | Cost worksheet generation |
| QuickBooks / Xero API | SaaS | Yes — REST | Actuals reconciliation |

## Templates & scripts
See `templates.md` for the full cost worksheet. Risk-driven contingency snippet (~25 lines):

```python
def risk_contingency(risks):
    """risks: [{name, probability:0-1, cost_impact_usd}]"""
    expected_value = sum(r["probability"] * r["cost_impact_usd"] for r in risks)
    # P80 of monte-carlo over Bernoulli per risk
    import random
    sims = []
    for _ in range(10000):
        sims.append(sum(r["cost_impact_usd"]
                        for r in risks if random.random() < r["probability"]))
    sims.sort()
    return {"expected": round(expected_value),
            "p50": round(sims[5000]),
            "p80": round(sims[8000]),
            "p95": round(sims[9500])}
```

## Best practices
- Cite source on every rate. "Senior engineer = $X" without a source is hallucinated; require the rate card to point to a contract / market survey.
- Use risk-driven contingency, not flat 15%. Sum (probability × cost) of register entries; if list is empty, fix the risk process before the budget.
- Separate management reserve from contingency. Contingency releases on identified risks; management reserve releases on scope changes only.
- Track P80, not P50, in the baseline. P50 means you blow the budget half the time.
- Re-baseline only on approved change requests. Constant re-baselining hides slip; lock the original.
- Compare estimate to actual quarterly; feed estimation error back into the rate card and effort multipliers (calibration).

## AI-agent gotchas
- Rate hallucination: agents emit "$120/hr senior engineer" with no source. Always require rates.yaml as input, never let the model invent.
- Burden multiplier confusion: salary × 1.3 ≠ cost. Add taxes, benefits, equipment, training, idle time; "fully-loaded" can be 1.4-2.0x.
- Currency: agents output USD by default and silently convert; budgets must declare currency per line.
- Contingency double-count: risk-driven reserve PLUS a flat 15% double-charges; pick one.
- Stale benchmark prices: cloud, SaaS subscription, and contractor rates from training data can be 30% off; require live API fetch for high-stakes estimates.
- Effort-vs-elapsed: 40 effort hours is not 5 days when developer is at 60% utilisation; force the agent to multiply by availability.
- LLMs prefer round numbers (5, 10, 15, 25); round numbers are anchors, not estimates. Reject suspiciously round outputs.

## References
- PMI PMBOK Guide 6th Ed., Chapter 7 — Project Cost Management.
- AACE International Recommended Practice 18R-97 (Cost Estimate Classification).
- Hubbard, *How to Measure Anything* (2014) — calibrated estimation.
- McConnell, *Software Estimation: Demystifying the Black Art* (2006).
- COCOMO II model for parametric software estimation.
- Goldratt, *The Goal* — buffer placement vs per-task padding (also relevant to cost contingency).
