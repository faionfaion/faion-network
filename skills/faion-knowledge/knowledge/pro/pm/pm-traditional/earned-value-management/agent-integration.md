# Agent Integration — Earned Value Management (EVM)

## When to use
- Fixed-price or cost-plus contracts where DCMA/DCAA compliance requires reporting EVM (US DoD, NASA, ESA, large defense/aerospace primes).
- Capital programs with multi-year baselines where SPI/CPI trends drive go/no-go reviews and earned-value forecasts feed quarterly board reporting.
- Programs where "% complete" claims have been chronically inflated and a quantitative truth signal is needed.
- Hybrid/agile-at-scale programs that still need finance-grade burn forecasts (EAC, ETC, VAC) tied to story-point velocity.
- Portfolio reporting where many projects feed a rollup; EVM normalizes status across heterogeneous teams.
- Pair with `cost-estimation/`, `schedule-development/`, `wbs-creation/`, `change-control/`, `predictive-analytics-pm/`, `risk-management/`.

## When NOT to use
- Pre-PMF startups, internal R&D, or pure agile teams without baseline budgets — EVM math is meaningless without a credible PV curve.
- Time-and-materials contracts where only AC matters — EVM adds overhead with no decision impact.
- Discovery / spike phases where work is exploratory and "% complete" is undefined.
- Small one-team projects under a quarter — burndown chart and weekly retro provide the same insight cheaper.
- Projects with no WBS or work-package level budgets — EVM rolls up from packages; without them the metrics are fiction.

## Where it fails / limitations
- Garbage in, confident graphs out — bad PV baselines or fabricated "% complete" produce SPI/CPI numbers that look authoritative and lie.
- SPI loses signal near project end (PV converges to BAC and SPI → 1 even when work isn't done); use IEAC and SPI(t) for late-stage.
- EVM assumes linear earning rules; agile work earns in lumps (story acceptance) which makes weekly EVM noisy.
- "0/100" vs. "50/50" vs. "% effort" earning rules give different numbers; rule mix breaks comparability.
- Over-baselining: re-baselining to hide variance turns EVM into a rear-view mirror.
- LLMs producing EVM commentary tend to anchor on "trend will revert"; CPI rarely improves on its own.
- EVM is not enough by itself — pair with risk register and schedule-margin analysis to avoid false confidence.
- Performance index distortions for late tasks; To-Complete Performance Index (TCPI) is more honest near end-of-project.

## Agentic workflow
EVM lives as `evm/baseline.yaml` (BAC, time-phased PV, work packages with earning rules) and `evm/actuals.yaml` (per-period AC, % complete, earned value events). A subagent computes PV, EV, AC, SV, CV, SPI, CPI, EAC, ETC, VAC, TCPI deterministically from these inputs and emits a typed report; another subagent writes the narrative. Earning rules are configurable per work package (0/100, 50/50, % complete, milestone-weighted). Agents never invent numbers — missing inputs surface as nulls with explicit reasons.

### Recommended subagents
- `faion-sdd-executor-agent` — drives EVM tasks (TASK_baseline_pv, TASK_period_close, TASK_eac_review, TASK_rebaseline_request).
- Custom `evm-calculator-agent` (haiku/sonnet) — pure deterministic compute via tool call to `evm_calc.py`; LLM only formats output.
- Custom `evm-narrative-agent` (sonnet) — translates raw indices into board-ready commentary; refuses to soften RED without sponsor override note.
- Custom `earning-rule-agent` (sonnet) — given a work package, recommends earning rule (0/100, 50/50, % complete, milestone) based on duration, deliverable type, and historical data.
- Custom `eac-forecaster-agent` (opus) — produces multiple EAC scenarios (CPI-only, CPI×SPI, ETC=remaining-work) with confidence and assumptions; decision-grade output.
- Custom `rebaseline-validator-agent` (opus) — when re-baselining is requested, audits whether the re-baseline hides variance vs. legitimate scope change; emits decision matrix.
- Custom `audit-evidence-agent` (sonnet) — for DCMA-14 / DCAA reviews, packages traceability from work package → EV event → AC charge → invoice.

### Prompt pattern
```
You are evm-narrative. Inputs: { period_end, BAC, PV, EV, AC,
  SV, CV, SPI, CPI, EAC_scenarios[], TCPI, BCWP_by_wbs[],
  variance_explanations_input[] }.
Emit STRICT JSON:
{ "headline": "<= 1 sentence",
  "rag": "GREEN|YELLOW|RED",
  "drivers": ["WBS-x.y: ..."],
  "actions_recommended": [...],
  "risk_links": ["RISK-NN"],
  "rebaseline_recommended": true|false }
Rules: do not change numeric values. RAG follows {GREEN: SPI>=0.95 & CPI>=0.95;
RED: SPI<0.85 or CPI<0.85; else YELLOW}. Do not soften RED without
"sponsor_override" field with explicit rationale.
```

EAC forecast prompt: `Compute three EAC scenarios with assumptions: (1) CPI-only (most likely if cost trend continues), (2) CPI x SPI (if both indices persist), (3) bottom-up ETC. Express each in currency and as variance vs. BAC. Identify which scenario the team should report and why.`

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pmcalc` (Python) / `pyearnedvalue` | Deterministic EVM compute | `pip install pyearnedvalue` |
| `pandas` | Time-phased baselines + actuals math | `pip install pandas` |
| `matplotlib` / `plotly` | PV/EV/AC + EAC trend charts | `pip install matplotlib plotly` |
| `yq` / `jq` | Patch baseline.yaml / actuals.yaml | `apt install yq jq` |
| `git` + tags | Lock baselines (`baseline-v1`); re-baseline = new tag | preinstalled |
| `pre-commit` | Block actuals edits without supporting evidence link | https://pre-commit.com |
| `pandoc` | Render EVM report packets to PDF | https://pandoc.org |
| `mermaid-cli` (`mmdc`) | Render simple S-curves / RAG dashboards | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Microsoft Project / Project Online | SaaS | REST + Graph | Native EVM fields (BCWS/BCWP/ACWP); Graph API exposes them. |
| Primavera P6 / EPPM | SaaS / on-prem | REST + WS | Defense/aerospace standard; deep EVM. |
| Deltek Cobra / wInsight / MPM | On-prem / SaaS | API | DCMA-aligned EVM analytics tools. |
| Smartsheet / Wrike / Planview | SaaS | REST | Mid-market EVM via templates and rollups. |
| ServiceNow SPM / PPM | SaaS | REST | Enterprise rollup; EVM field support varies. |
| Costpoint / SAP S/4HANA PS | SaaS / on-prem | REST/IDoc | Authoritative AC source; integrate read-only. |
| Jira + Tempo + Advanced Roadmaps | SaaS | REST | Approximation for software programs; needs explicit baselines. |
| Power BI / Tableau / Looker | SaaS | REST | EVM dashboards from baseline + actuals YAML. |
| Excel / Google Sheets | SaaS | REST | Reality of most small EVM implementations; treat as artifact target. |

## Templates & scripts
README provides EVM Dashboard and trend chart. Inline below: a 30-line script that computes the core indices from baseline + actuals YAML.

```python
#!/usr/bin/env python3
"""evm_calc.py — deterministic EVM indices from YAML inputs."""
import json, sys, yaml, pathlib

def main(baseline: str, actuals: str) -> int:
    B = yaml.safe_load(pathlib.Path(baseline).read_text())
    A = yaml.safe_load(pathlib.Path(actuals).read_text())
    BAC = float(B["bac"])
    period = A["period_end"]
    PV = float(B["pv_curve"][period])
    EV = sum(float(p["budget"]) * float(p["pct_complete"])
             for p in A["work_packages"])
    AC = float(A["actual_cost_to_date"])
    SV, CV = EV - PV, EV - AC
    SPI = EV / PV if PV else None
    CPI = EV / AC if AC else None
    EAC = BAC / CPI if CPI else None
    ETC = (EAC - AC) if EAC else None
    VAC = (BAC - EAC) if EAC else None
    TCPI = (BAC - EV) / (BAC - AC) if (BAC - AC) else None
    out = {"period_end": period, "BAC": BAC, "PV": PV, "EV": EV, "AC": AC,
           "SV": SV, "CV": CV, "SPI": SPI, "CPI": CPI,
           "EAC": EAC, "ETC": ETC, "VAC": VAC, "TCPI": TCPI}
    json.dump(out, sys.stdout, indent=2)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
```

## Best practices
- Lock baseline once; re-baseline only via approved scope/CR with audit trail (`baseline-v2`, change-request id, sponsor sign-off).
- Use objective earning rules (milestone-weighted, 0/100 for short tasks, % for long tasks); document the rule per work package.
- Forecast multiple EAC scenarios; reporting only one number hides risk.
- Combine SPI(t) (time-based SPI) with classic SPI to avoid end-of-project signal loss.
- Triangulate against bottom-up ETC every quarter — index-based forecasts drift over time.
- Tie EVM to risk register: every RED index references at least one open risk; closure of a risk should produce visible movement.
- TCPI > 1.10 is rarely recoverable in practice; treat as escalation trigger, not aspirational.
- Do not paper over variance with re-baselining; record the original baseline alongside the new one for audit.
- Earning recognition is event-driven: an EV event posts only when the deliverable passes its acceptance criterion (DoD).
- Sponsor reports include three numbers minimum: SPI, CPI, EAC; don't bury them in narrative.

## AI-agent gotchas
- Never let the LLM compute the numbers; force a tool call to a deterministic calculator and have the LLM only narrate.
- Agents anchor on "improving" trends without basis; require historical CPI/SPI series in the prompt to ground forecasts.
- Re-baselining requests by an LLM are dangerous — it will paper over variance to make RAG green; gate behind opus model + sponsor approval.
- "% complete" hallucination is the biggest risk — agents accept self-reported numbers; ground them in objective evidence (DoD pass, milestone date, count of accepted deliverables).
- Rounding/currency mistakes propagate; standardize unit (USD or EUR), decimals, and time grain (weekly) in the prompt.
- Agents conflate SV (currency) with schedule slip (time); use SV(t) where time impact is the question.
- Long context: a 5-year EVM history blows the prompt; partition by control account / period and feed slices.
- Privacy: actual cost data is commercially sensitive; require DPA when using third-party LLMs and never publish AC outside the EVM owner.
- Sponsor "GREEN washing" via prompt injection — explicit "do not change numbers" rule must be enforced and verified by tool-side computation.
- Human-in-the-loop checkpoints (mandatory): baseline lock, re-baseline approval, EAC scenario selection for board reporting, RED → action plan, audit submission.

## References
- PMI PMBOK 7e — Measurement Performance Domain.
- PMI Practice Standard for Earned Value Management (2nd ed.).
- ANSI/EIA-748 — Earned Value Management Systems.
- DCMA-14 / DCAA — US defense audit standards for EVM.
- Fleming, Q. & Koppelman, J. — "Earned Value Project Management".
- Anbari, F. — "Earned Value Project Management Method and Extensions".
- Lipke, W. — Earned Schedule (extension addressing late-project SPI distortion).
- ISO 21508 — Earned value management in project and programme management.
- Sibling methodologies: `cost-estimation/`, `schedule-development/`, `wbs-creation/`, `change-control/`, `predictive-analytics-pm/`, `risk-management/`.
