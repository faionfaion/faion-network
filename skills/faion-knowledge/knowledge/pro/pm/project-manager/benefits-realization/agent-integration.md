# Agent Integration — Benefits Realization

## When to use
- Business case approval requires quantified ROI and a tracking plan
- Post-launch (3, 6, 12 months) benefits review across portfolio of projects
- Investment committee asking "did the last 8 projects pay back?"
- Programs spanning years where outputs precede outcomes by 6-18 months
- Org adopting outcome-based metrics over output-based (PMO maturity step)

## When NOT to use
- Pre-revenue startup pre-PMF — benefits are speculative; track learning instead
- Compliance-driven projects where benefit is "stay legal" (binary, hard to quantify)
- Internal tooling with weak baseline data (no measurable "before")
- Crisis incident response — benefit realization is "stopped bleeding"

## Where it fails / limitations
- Benefit owners are business stakeholders; they leave or re-org and tracking dies
- Attribution: revenue grew, but was it the project or seasonality / market shift?
- Benefits stated to win project approval are rarely revisited; honesty premium is low
- Long benefit horizons (12-36m) outlast PMs, sponsors, and the tracking system
- "Outcome → benefit" requires user adoption and process change, neither of which the project team controls
- Double-counting across portfolio (two projects both claim the same revenue lift)
- AI productivity benefits are hardest: hard to attribute, easy to overstate

## Agentic workflow
A benefits-cataloger subagent extracts benefit statements from business cases, normalizes them into a Benefits Register with metric, baseline, target, owner, and measurement method. A baseline-collector pulls the actual baseline values from source systems before launch. A measurement-runner queries the same sources monthly post-launch, computes % realized vs target, and produces variance analysis. A counterfactual agent estimates attribution (intervention vs market). PM/PO reviews; sponsor signs.

### Recommended subagents
- `benefits-cataloger` — turns prose business cases into structured Benefits Register
- `baseline-collector` — pulls T-0 metric values from analytics/CRM/ERP, freezes them
- `measurement-runner` — periodic pulls vs target, drift detection
- `counterfactual-analyzer` — applies diff-in-diff or synthetic control for attribution
- `benefits-reporter` — exec-ready report with status, trend, recommendations

### Prompt pattern
```
You are a benefits-cataloger. From business case {case.md}, extract benefits
into JSON {id, statement, type: financial|efficiency|quality|strategic|
compliance, metric, baseline_value, baseline_date, target_value, target_date,
owner, source_system, measurement_method}. Reject any benefit lacking a
quantified target or named owner — emit clarifying question instead.
```

```
You are a counterfactual-analyzer. Benefit {b.json}. Pre/post data {ts.csv}.
Use difference-in-differences vs control cohort {control_id} where available;
else synthetic control via {comparator_set}. Return attribution {%} with
confidence band, list of confounders considered.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Transform analytics data into benefit metric tables | https://docs.getdbt.com |
| `metabase-cli` (community) | Pull dashboards / metrics for tracking | https://github.com/metabase/metabase |
| `gcp` / `aws` CLIs | Pull telemetry, BigQuery / Redshift / Athena | gcloud, aws |
| `python` (pandas, statsmodels) | Diff-in-differences, synthetic control | pip |
| `r` | Causal inference packages (CausalImpact, MatchIt) | https://cran.r-project.org |
| `jq` | Parse JSON benefit registers | https://jqlang.github.io/jq/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Salesforce | SaaS | Yes | CRM revenue benefit baseline + realization, REST/SOAP |
| HubSpot | SaaS | Yes | Marketing/sales benefit data |
| Mixpanel / Amplitude | SaaS | Yes | Product analytics for adoption + KPI |
| Looker / Looker Studio | SaaS | Yes | Dashboards via API |
| Tableau | SaaS / desktop | Yes | REST API, embed |
| Power BI | SaaS | Yes | REST API, AAD auth |
| Productboard | SaaS | Partial | Outcome-based roadmap, partial benefits track |
| Aha! | SaaS | Yes | Strategy → benefits link, REST API |
| ProductPlan | SaaS | Partial | Lighter |
| Apptio Targetprocess | SaaS | Yes | Portfolio benefits + spend |
| Anaplan | SaaS | Yes | Financial benefit modeling |

## Templates & scripts
See templates.md for register, report, business case section. Inline benefits-tracker:

```python
# benefits_track.py — pull current values vs target, emit JSON status
import yaml, json, requests, os
reg = yaml.safe_load(open("benefits_register.yaml"))
out = []
for b in reg:
    src = b["source_system"]
    if src == "looker":
        url = f"{os.environ['LOOKER_BASE']}/api/4.0/queries/{b['query_id']}/run/json"
        actual = requests.get(url, headers={"Authorization": f"token {os.environ['LOOKER_TOKEN']}"}).json()[0][b["metric"]]
    elif src == "csv":
        import csv
        with open(b["path"]) as f:
            actual = float(list(csv.DictReader(f))[-1][b["metric"]])
    else:
        actual = None
    if actual is None:
        out.append({**b, "status": "no_data"}); continue
    delta = actual - b["baseline_value"]
    pct_realized = delta / (b["target_value"] - b["baseline_value"]) if b["target_value"] != b["baseline_value"] else 0
    out.append({**b, "actual": actual, "pct_realized": round(pct_realized, 3),
                "status": "on_track" if pct_realized >= 0.7 else "at_risk"})
print(json.dumps(out, indent=2))
```

```python
# diff_in_diff.py — quick DiD for benefit attribution
import pandas as pd, statsmodels.formula.api as smf
df = pd.read_csv("dida.csv")  # cols: y, treated, post, period, unit
model = smf.ols("y ~ treated*post + C(period) + C(unit)", data=df).fit()
print(model.summary().tables[1])  # treated:post coef = ATT
```

## Best practices
- Quantify before approval; "soft benefits" without metric do not count
- Freeze baseline in writing with date and source query — agents can re-pull but not redefine
- Benefit owner ≠ project manager; PM hands off at go-live
- Track leading indicators (adoption, NPS) monthly; lagging (revenue, cost) quarterly
- Build attribution intentionally — pre-register a control cohort or comparator before launch
- Cap claimable benefits at portfolio level to prevent double-counting
- Sunset benefits register at 24 months unless extended — long tails distort portfolio metrics
- Treat under-realization as learning, not blame; publish post-mortems

## AI-agent gotchas
- Agents will fabricate baselines from "industry averages" if the actual baseline is missing — fail closed, demand source
- Counterfactual analysis is easy to do badly; require pre-registered DiD/synth-control plan, do not let agent pick model post-hoc
- Benefit ownership decays silently when owners leave; cron-check that owner email still resolves and projects still active
- Currency, FX, and inflation: agents must use the same deflator for baseline and actual
- Adoption metrics from telemetry can be inflated by bots/automation; segment human vs bot traffic
- ROI calculations: agents tend to ignore time-value-of-money; use NPV, not raw sum
- "Productivity gain from AI" benefit is the most over-claimed category in 2024-2026; require independent validation

## References
- PMI, *Benefits Realization Management Framework*
- Bradley & Cantwell, *Benefits Realization Management* (Routledge)
- John Thorp, *The Information Paradox* — benefits realization origins
- Office of Government Commerce (UK), MSP — managing successful programmes
- Counterfactual analysis: Brodersen et al., *CausalImpact* (Google)
- McKinsey, *Measuring the impact of digital transformations*
