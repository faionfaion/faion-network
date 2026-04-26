# Agent Integration — Benefits Realization

## When to use
- Capital programs and transformation initiatives where the business case promised quantitative benefits (revenue, cost savings, NPS, cycle time).
- Portfolios where investment prioritization needs evidence: post-launch benefit measurement informs the next round.
- Public-sector / regulated programs requiring benefit reporting (NHS / GDS / EU funding rules).
- Mergers and acquisitions where synergy realization is part of the deal thesis.
- ERP / CRM / cloud migration programs that historically delivered outputs but failed to deliver outcomes.
- Pair with `project-closure/`, `lessons-learned/`, `predictive-analytics-pm/`, product `north-star-metrics/`, ba `solution-evaluation/`.

## When NOT to use
- Pre-PMF startups — benefit realization assumes a stable benefit hypothesis; PMF is itself the benefit.
- Pure R&D / option-creating projects where the value is learning, not delivery.
- Projects whose benefits are entirely indirect or strategic (signaling, optionality) — track those qualitatively.
- One-off tactical projects under $50k where measurement cost exceeds benefit insight.
- Programs without a benefit owner — without a business stakeholder accountable, "tracking" is theatre.

## Where it fails / limitations
- Benefit ownership defaults to the PM, who has no operational levers post-handover; the right owner is a business stakeholder.
- Baselines are missed at project start; without a credible "before" measurement, "after" is a fairy tale.
- Attribution is hard — benefits depend on adoption, market conditions, and concurrent initiatives; isolating project impact requires control / cohort design.
- Benefits get over-promised to win approval; tracking is then under-funded to avoid embarrassment.
- LLMs producing benefit narratives default to optimism; structured measurement plus rule-based RAG counter the bias.
- Benefit decay: realized benefits in year 1 fade in year 2 (process drift, staff turnover, system erosion); single-shot measurement misses the curve.
- "Benefit" is conflated with "output" or "outcome"; without disciplined definitions, all three are reported as benefit.
- Politics of measurement — owners under-report when targets are unrealistic, over-report when promotion is on the line.

## Agentic workflow
Benefits live as `benefits/register.yaml` (one entry per benefit: owner, baseline, target, metric source, cadence, prerequisites, enablers, risks, realization curve) plus `benefits/measurements.yaml` (period → metric → actual + variance + evidence link). A subagent ingests measurement data on a fixed cadence (monthly/quarterly), computes realization %, applies a RAG rubric, and writes the benefits realization report. Another agent runs barrier-analysis when realization deviates >X% from plan and proposes corrective actions. Crucially, agents do not own benefits — they observe and report; ownership stays with the named business stakeholder.

### Recommended subagents
- `faion-sdd-executor-agent` — drives benefits as SDD tasks (TASK_register_baseline, TASK_baseline_measurement, TASK_post_launch_M1, TASK_post_launch_Q1, TASK_review_decision).
- Custom `benefit-author-agent` (sonnet) — converts business-case prose into structured benefit entries with mandatory metric, baseline, target, owner, source.
- Custom `measurement-collector-agent` (haiku) — given a cadence, fetches metrics from configured sources (BI, CRM, support desk, NPS) and posts to register.
- Custom `realization-reporter-agent` (sonnet) — computes realization %, RAG, and trend; emits report deterministically; refuses to soften RED without override note.
- Custom `barrier-analyzer-agent` (opus) — when realization < target by >X%, surveys adoption, change-management, system, and external factors; emits cause hypotheses ranked by evidence.
- Custom `attribution-agent` (opus) — for benefits with concurrent initiatives, proposes attribution method (cohort, before/after with controls, holdout) and calls out where attribution is impossible.

### Prompt pattern
```
You are benefit-author. Inputs: business-case.md, scope-baseline.yaml.
For each claimed benefit emit STRICT JSON entry:
{ "id": "B-NN", "description": "...",
  "category": "Financial|Efficiency|Quality|Strategic|Compliance",
  "owner": "<role/name>",
  "metric": "<name>", "baseline": <number|null>,
  "target": <number>, "unit": "...",
  "metric_source": "BI report id / system / dashboard URL",
  "realization_curve": [{ "period": "M1", "expected": 0.10 }, ...],
  "prerequisites": [...], "enablers": [...],
  "attribution_method": "cohort|before_after|holdout|qualitative|none",
  "risks": [...] }
Rules: reject benefits without metric+baseline+target+owner. baseline=null
flags an open task to measure pre-launch; do not invent baselines.
```

Realization report prompt: `Compute realization % per benefit. RAG rubric: GREEN if actual >= 90% of expected curve, YELLOW 70-90%, RED <70%. Always include the evidence link from measurement source. Do not change actuals; if missing, flag as null with reason.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `git` + tags `benefits-baseline-vN` | Version-controlled register and baseline measurements | preinstalled |
| `yq` / `jq` | Patch register.yaml, measurements.yaml | `apt install yq jq` |
| `pandas` | Time-series realization math, cohort analysis | `pip install pandas` |
| `scipy.stats` / `causalimpact` | Attribution and significance testing | `pip install scipy causalimpact` |
| `dbt` | Define metric pipelines once for benefit + analytics use | https://docs.getdbt.com |
| `pre-commit` | Block measurement edits without evidence link | https://pre-commit.com |
| `pandoc` | Render reports to PDF for sponsor review | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Realization curves, benefit tree maps | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Power BI / Tableau / Looker / Metabase | SaaS / OSS | REST | Authoritative dashboard sources; agents read URLs. |
| Snowflake / BigQuery / Databricks | SaaS | REST | Underlying data warehouse; SQL queries feed the register. |
| Salesforce / HubSpot | SaaS | REST | Revenue/conversion/CSAT benefits. |
| ServiceNow / Zendesk / Freshdesk | SaaS | REST | Support cost / ticket reduction benefits. |
| Mixpanel / Amplitude / Pendo | SaaS | REST | Adoption and engagement metrics; cohort analysis. |
| Workday / Personio | SaaS | REST | Productivity / time-savings benefits. |
| Stripe / NetSuite / SAP | SaaS / on-prem | REST/IDoc | Financial benefit ground truth. |
| Confluence / Notion / SharePoint | SaaS | REST | Common register host; weak typing — schema-validate. |
| Aha! / ProductBoard | SaaS | REST | Outcome tracking integrated with roadmap. |
| Driver-tree tools (Cascade, Tability, Hjro) | SaaS | REST | OKR / driver-tree integration. |

## Templates & scripts
README provides Benefits Register, Realization Report, Business Case Benefits Section. Inline below: a script that computes realization % with RAG.

```python
#!/usr/bin/env python3
"""benefits_status.py — realization % and RAG from measurements.yaml."""
import json, sys, yaml, pathlib

def rag(actual: float, expected: float) -> str:
    if expected == 0: return "N/A"
    pct = actual / expected
    if pct >= 0.90: return "GREEN"
    if pct >= 0.70: return "YELLOW"
    return "RED"

def main(register: str, measurements: str, period: str) -> int:
    R = {b["id"]: b for b in yaml.safe_load(pathlib.Path(register).read_text())["benefits"]}
    M = yaml.safe_load(pathlib.Path(measurements).read_text())["measurements"]
    out = []
    for m in [x for x in M if x["period"] == period]:
        b = R[m["benefit_id"]]
        expected = next(p["expected"] for p in b["realization_curve"]
                        if p["period"] == period)
        actual_pct = (m["actual"] - b["baseline"]) / (b["target"] - b["baseline"]) \
            if b["target"] != b["baseline"] else 0
        out.append({"id": b["id"], "actual_pct": round(actual_pct, 2),
                    "expected_pct": expected, "rag": rag(actual_pct, expected),
                    "evidence": m.get("evidence_url")})
    json.dump(out, sys.stdout, indent=2)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
```

## Best practices
- Benefit owner is a named business stakeholder, never the PM; PM facilitates, owner accounts.
- Baseline measurements before go-live are non-negotiable; if you cannot baseline, you cannot claim benefit.
- Every benefit has a single primary metric with explicit data source and pipeline; multi-metric benefits are decomposed.
- Realization curves go in the register (M1, M3, M6, Y1, Y2); single-shot measurement misses decay.
- Attribution method is declared up front; default to "qualitative" rather than fabricating causality.
- Tie benefits to project closure: a project does not close without baseline measurements scheduled and owners committed.
- Track barriers (low adoption, training gap, change resistance, external shock) alongside numbers; without barrier analysis, RED is uninterpretable.
- Pair benefit register with OKRs / north-star metrics to avoid duplicate truth in two systems.
- Sponsor sign-off on benefit definitions is a release gate; "we'll figure out metrics later" is a failure mode.
- Recompute portfolio ROI annually using realized data, not original forecasts.

## AI-agent gotchas
- LLMs over-claim benefits — politeness bias toward sponsor expectations. Force evidence requirements per claim.
- Agents fabricate baselines when the field is empty; require null + open-task flag rather than invented numbers.
- Attribution hallucination — agents will assert causality from correlation; require explicit attribution_method and refuse "implied" causation.
- Privacy: cohort-level metrics may identify individuals (small N, sensitive attributes); enforce k-anonymity before sending to third-party LLMs.
- Realization decay is invisible without time-series; one-shot prompts produce one-shot conclusions. Force agents to read the full curve.
- "Benefit" vs "output" conflation — agents will count "feature shipped" as benefit. Reject any benefit whose metric is project output.
- Sponsor-facing reports invite GREEN washing; deterministic RAG + scrubber + reviewer gate is mandatory.
- Long context: large registers (>50 benefits) blow the prompt; partition by category or owner.
- Barrier-analysis agents over-blame "low adoption" — push them to consider system, training, incentive, and external causes.
- Human-in-the-loop checkpoints (mandatory): benefit creation, baseline lock, target change, RED escalation, attribution method change, portfolio ROI recompute.

## References
- PMI PMBOK 7e — Measurement Performance Domain (Outcomes / Benefits).
- PMI Standard for Program Management — Benefits Management Lifecycle.
- Bradley, G. — "Benefit Realisation Management".
- Ward, J. & Daniel, E. — "Benefits Management: How to Increase the Business Value of Your IT Projects".
- Doerr, J. — "Measure What Matters" (OKR alignment for benefits).
- HM Treasury Green Book / Magenta Book — UK gov benefit management guidance.
- ISO 21500 / 21502 — benefit management guidance.
- Sibling methodologies: `project-closure/`, `lessons-learned/`, `predictive-analytics-pm/`, ba `solution-evaluation/`, product `north-star-metrics/`.
