# Agent Integration — Cost Estimation

## When to use
- Producing initial budget for a feature / project / RFP response with a defensible cost baseline.
- Bottom-up estimation from a WBS (each work package gets labor + tools + infra cost).
- Build-vs-buy and build-vs-SaaS decisions where opportunity cost matters.
- Updating the cost baseline after a change-control event.
- Solopreneur "true cost" analysis (own time at market rate vs out-of-pocket).

## When NOT to use
- Agile teams that estimate via story points + #Noestimates / capacity-based forecasting; cost is derived from team-month run-rate, not bottom-up sum.
- Pre-discovery exploration where requirements are < 30% defined; output will be a fantasy. Use ROM (rough order of magnitude, ±50%) instead.
- Fixed-fee contracts already negotiated — re-estimating internally has no contractual force.

## Where it fails / limitations
- Three-point estimation gives false precision: PERT mean assumes a beta distribution rarely true in software; pessimistic cost is consistently *under*-estimated by humans and LLMs.
- Contingency reserve sized as a flat % ignores risk register; high-risk projects need risk-driven reserve, not 15%.
- Overhead loading varies wildly (1.3x for fully-loaded employee in low-tax markets, 1.8x+ in high-tax markets); a single multiplier is wrong by region.
- LLMs benchmark hourly rates from training data 12-24 months stale; current rates can differ by 30%+.
- Currency / FX volatility in multi-region projects is not captured by static numbers.
- Sunk-cost bias: re-estimates after work has started anchor on the original number.

## Agentic workflow
The agent is a calculator + auditor, not a decision-maker. Feed it the WBS (work packages with effort hours), a labor rate card, an infra/tools list, and a risk register; it produces a structured cost estimate (direct, indirect, contingency, management reserve) plus a sensitivity analysis. A human approves the numbers before they enter the budget. Re-run the agent on every scope change to keep the baseline live.

### Recommended subagents
- A `cost-estimator` subagent (define inline) — reads WBS + rate card YAML, outputs a cost-baseline JSON with PERT 3-point per work package.
- A `sensitivity-analyzer` subagent — Monte-Carlo over the 3-point distributions, returns P50 / P80 / P95 totals.
- `faion-sdd-executor` — when estimate becomes a task, drives implementation through quality gates.

### Prompt pattern
```
Inputs:
- wbs.yaml: list of {id, name, effort_hours_optimistic, most_likely, pessimistic, role}
- rates.yaml: hourly rate per role (source: <RFP / contract / internal>)
- overhead: 0.3 (fully-loaded multiplier on labor)
- contingency: risk_register.yaml (use risk-driven, not flat %)
- duration_months: <int>
- tools.yaml: SaaS subscriptions in scope

Output JSON:
{ "direct_costs": {...},
  "indirect_costs": {...},
  "risk_driven_contingency_usd": ...,
  "management_reserve_usd": ...,
  "cost_baseline_usd": ...,
  "budget_at_completion_usd": ...,
  "sensitivity": {"p50": ..., "p80": ..., "p95": ...},
  "assumptions": ["...explicit..."] }

Rules:
- No invented rates; cite source field.
- Round to nearest USD; never $X.XX precision spurious.
- If any input missing, return {"error": "..."} not a guess.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `infracost` | Cloud infra cost from Terraform / Pulumi diff | https://www.infracost.io/ |
| `cost-modeler` (custom) | Spreadsheet-driven Monte Carlo (Excel / Sheets + Python) | n/a |
| `numpy` + `scipy.stats` | Beta / triangular distributions for PERT / 3-point | https://scipy.org/ |
| `montecarlo-cli` (`mcli`) | Quick CLI Monte Carlo on cost ranges | https://github.com/cetra3/mcli |
| `gh` / `jira-cli` | Pull effort / story-point data for bottom-up | https://cli.github.com/ , https://github.com/ankitpokhrel/jira-cli |
| `awscost-cli` / `gcloud billing` | Live infra-cost benchmarking | https://docs.aws.amazon.com/cli/latest/reference/ce/ |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Float / Resource Guru | SaaS | Yes — REST | Capacity + rate cards; export CSV |
| Harvest / Toggl | SaaS | Yes — REST | Actual hours by role for re-baselining |
| Forecast (by Harvest) | SaaS | Yes — REST | Project budget vs actuals |
| Productive.io | SaaS | Yes — REST | Agency-grade cost + margin tracking |
| Mosaic / Runn | SaaS | Yes — REST | Resource forecasting |
| Infracost | SaaS / OSS | Yes | Infra cost baseline + PR diff |
| Vantage / CloudZero | SaaS | Yes — REST | Cloud unit cost (cost per customer / per request) |
| Notion / Confluence | SaaS | Yes — REST | Where the cost baseline doc lives |
| Excel / Google Sheets API | SaaS | Yes | Cost worksheet generation |

## Templates & scripts
See `templates.md` for the worksheet. Inline 3-point + PERT mean + std-dev calculator (Python):

```python
#!/usr/bin/env python3
import json, math, sys
def pert(o, m, p):
    mean = (o + 4*m + p) / 6
    std = (p - o) / 6
    return mean, std
def main(path):
    wbs = json.load(open(path))
    total_mean = total_var = 0.0
    out = []
    for wp in wbs:
        rate = wp["rate_usd"]
        mh, sh = pert(wp["o_h"], wp["m_h"], wp["p_h"])
        cost_mean = mh * rate
        cost_std = sh * rate
        total_mean += cost_mean
        total_var += cost_std ** 2
        out.append({"id": wp["id"], "cost_mean": round(cost_mean, 0),
                    "cost_std": round(cost_std, 0)})
    total_std = math.sqrt(total_var)
    print(json.dumps({"items": out,
        "total_mean_usd": round(total_mean, 0),
        "total_std_usd": round(total_std, 0),
        "p80_usd": round(total_mean + 0.84 * total_std, 0),
        "p95_usd": round(total_mean + 1.65 * total_std, 0)}, indent=2))
if __name__ == "__main__":
    main(sys.argv[1])
```

## Best practices
- Always quote the *source* of every rate (vendor quote, internal rate card v.X, market survey). No source = no rate.
- Use risk-driven contingency: each open risk × probability × impact, sum, round up. Beats flat 15%.
- Report P50 / P80 / P95, not just point estimate. Sponsor approves a P-level, not a number.
- Separate cost baseline (PM-controlled) from management reserve (sponsor-controlled). Don't blend.
- Track cost-baseline version with each change request — diff is the audit trail.
- For solopreneurs, opportunity cost = own hourly market rate (not "free"); buy options often win once you see the line.
- Re-baseline at every milestone gate; never let the original estimate persist past month 2 unchallenged.
- Kill the "fixed price + variable scope" pattern at proposal stage. Either fix scope or use T&M with cap.

## AI-agent gotchas
- LLMs invent rates ("senior dev: $150/hr") confidently. Force `rate_source` field per row; reject estimates without it.
- Pessimistic estimates are systematically too low (anchoring). Add a check: if `p / m < 1.8`, flag for human review.
- Triangular vs beta-PERT is conflated; results differ by ~20% on tails. Pick one and label it.
- Currency: agent outputs USD when WBS was in EUR. Force a `currency` field, fail if mixed.
- Overhead multiplier: 1.3x is North-America baseline; agents apply it globally. Parameterize per region.
- Contingency double-count: agent adds 15% AND a risk-driven reserve. Pick one strategy.
- Numerical hallucination: an LLM doing arithmetic on >5 work packages drifts. Always do math in code (Python tool / spreadsheet API), not in prose.
- "Total budget" output sometimes excludes management reserve — always print Cost Baseline AND BAC.
- LLMs round inconsistently ($91,687 → "$92K"); for budget docs, keep raw and rounded both, label clearly.

## References
- PMBOK Guide 7th Ed. — Planning Performance Domain (Cost) — https://www.pmi.org/pmbok-guide-standards
- Practice Standard for Project Estimating — https://www.pmi.org/learning/library/practice-standard-project-estimating
- "Software Estimation: Demystifying the Black Art", Steve McConnell — https://www.oreilly.com/library/view/software-estimation-demystifying/0735605351/
- AACE International cost-estimate classification — https://www.aacei.org/resources/recommended-practices
- Infracost docs — https://www.infracost.io/docs/
- "How to Lie with Statistics" (relevant to estimation bias) — Darrell Huff
