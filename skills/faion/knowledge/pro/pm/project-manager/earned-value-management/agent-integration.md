# Agent Integration — Earned Value Management

## When to use
- Predictive / hybrid projects with a fixed scope baseline and budget
- Programs with monthly/weekly steering committee status (need objective trend, not narrative)
- Government, defense, infra, large IT — contracts that require ANSI/EIA-748 or similar
- Engagements where "% complete" claims have lost credibility and you need objective measure
- Program forecasting (EAC/ETC) for board approval of additional budget

## When NOT to use
- Pure agile teams shipping continuously — burndown + flow metrics are better fits
- Discovery / R&D phases with no stable baseline
- Projects under 6 weeks or under $50k — overhead exceeds insight
- Internal startup work where speed matters more than financial control
- Soft-cost projects with no convertible-to-dollars effort tracking

## Where it fails / limitations
- Garbage-in: subjective % complete corrupts EV; agents inherit and amplify the bias
- Re-baselining is political; teams gaming SPI/CPI by re-baselining hides true variance
- CPI rarely improves on its own; teams continue forecasting recovery that never happens (the "CPI cliff")
- Effort-driven scopes (consulting hours) can show CPI >1 while the deliverable rots
- Multi-currency programs need FX-hedged EAC; raw conversion lies
- AI-generated work hours muddy AC: how do you cost a 2-second LLM call vs a 4-hour human review?

## Agentic workflow
A schedule-aggregator subagent pulls task progress (Jira/MS Project), labor + materials cost (timesheets, invoices), and computes weekly PV/EV/AC per work package. A metrics-engine produces SV/CV/SPI/CPI/EAC/ETC/TCPI with trend. A variance-analyst flags work packages with CPI < 0.9 or SPI < 0.9 for two consecutive periods, drafts a root-cause hypothesis, and proposes corrective actions. PM reviews; agent updates the EVM dashboard. Re-baselining always requires human approval.

### Recommended subagents
- `schedule-aggregator` — normalizes progress + cost from multiple tools per WBS code
- `evm-calculator` — pure function: inputs PV/EV/AC, outputs full EVM metric set
- `variance-analyst` — interprets metrics, references historical patterns, proposes actions
- `forecast-revisor` — runs 3-point estimates and Monte Carlo on EAC under uncertainty
- `evm-reporter` — emits stakeholder-ready dashboard (markdown/PDF/dashboard JSON)

### Prompt pattern
```
You are an evm-calculator. Inputs: WBS state {wbs.yaml} with {bac, percent_complete,
actual_cost} per package, planned curve {pv_curve.json}. Compute and return JSON
per package: {pv, ev, ac, sv, cv, spi, cpi, eac, etc, vac, tcpi}. Use BAC/CPI for
EAC unless cpi < 0.6 (flag for human re-baseline review).
```

```
You are a variance-analyst. Given metrics {evm.json} for last 6 periods, identify
packages with CPI<0.9 or SPI<0.9 sustained ≥2 periods. For each, draft root-cause
hypothesis citing schedule/risk/scope-change events. Propose 2 corrective actions
with expected impact. Output JSON, do NOT propose re-baselining.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `python` (numpy/pandas) | EVM math, curves, Monte Carlo | `pip install pandas numpy` |
| `gnuplot` / `matplotlib` | Render PV/EV/AC trend chart | https://www.gnuplot.info, mpl docs |
| `jira` (CLI) | Pull WBS-coded issue progress | https://github.com/ankitpokhrel/jira-cli |
| `mpxj` (Java) | Read MS Project / Primavera files | https://www.mpxj.org |
| `gh` | Pull cost-coded issues from labels | https://cli.github.com |
| `tempo` API | Worklog → AC | https://apidocs.tempo.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Microsoft Project (Plan 5) | SaaS | Yes | EVM fields native, Graph API |
| Primavera P6 | Enterprise | Partial | Heavy, EVM-strong, REST limited |
| Smartsheet Resource Mgmt | SaaS | Yes | EVM via custom columns + API |
| Deltek Cobra | Enterprise | Partial | Defense-grade EVMS, ANSI/EIA-748 |
| ProjStream | SaaS | Partial | EVM specialist |
| OpenProject | OSS | Partial | EVM via plugin/extension |
| GanttPRO | SaaS | Yes | Lightweight, REST API |
| ProofHub | SaaS | Yes | Includes time + cost API |
| Toggl Track + custom EVM | SaaS + DIY | Yes | Pull AC, compute EVM in code |

## Templates & scripts
See templates.md for EVM dashboard. Inline EVM calculator:

```python
# evm.py — minimal EVM calculator
from dataclasses import dataclass
@dataclass
class WP:
    bac: float       # budget at completion
    pct_planned: float
    pct_complete: float
    ac: float

def evm(wp: WP) -> dict:
    pv = wp.bac * wp.pct_planned
    ev = wp.bac * wp.pct_complete
    ac = wp.ac
    sv = ev - pv
    cv = ev - ac
    spi = ev / pv if pv else float("nan")
    cpi = ev / ac if ac else float("nan")
    eac = wp.bac / cpi if cpi else float("nan")
    etc = eac - ac
    vac = wp.bac - eac
    tcpi = (wp.bac - ev) / (wp.bac - ac) if wp.bac - ac else float("nan")
    return dict(pv=pv, ev=ev, ac=ac, sv=sv, cv=cv,
                spi=round(spi, 3), cpi=round(cpi, 3),
                eac=round(eac, 0), etc=round(etc, 0),
                vac=round(vac, 0), tcpi=round(tcpi, 3))

if __name__ == "__main__":
    print(evm(WP(bac=100_000, pct_planned=0.50, pct_complete=0.40, ac=55_000)))
```

```python
# eac_montecarlo.py — three-point EAC under uncertainty
import numpy as np
def eac_mc(bac, cpi_min, cpi_likely, cpi_max, n=10000):
    cpi = np.random.triangular(cpi_min, cpi_likely, cpi_max, n)
    eac = bac / cpi
    return {"p10": np.percentile(eac, 10),
            "p50": np.percentile(eac, 50),
            "p90": np.percentile(eac, 90)}
print(eac_mc(100_000, 0.65, 0.75, 0.95))
```

## Best practices
- Use objective % complete: 0/50/100, milestone-based, or units-completed — not opinion
- Lock baseline; require formal re-baseline (CCB) — never silent re-baseline by agent
- Track at WBS level 3-4, not lowest leaf — too granular = noise, too coarse = blind
- Pair EVM with risk register; risk events explain CPI/SPI shifts
- For agile-hybrid: EVM at release (or PI) level, story burndown intra-iteration
- TCPI > 1.10 typically signals project is unrecoverable on current budget — escalate honestly
- Color-code: SPI/CPI in [0.95, 1.05] green, [0.85, 0.95) yellow, < 0.85 red — consistency aids stakeholders

## AI-agent gotchas
- "Percent complete" gathered by an agent from PR counts is a proxy not the truth — calibrate against milestone-based EV
- Currency conversion: agents will silently mix USD/EUR/GBP in AC; enforce single base currency
- Forecasts via `BAC/CPI` are pessimistic for early-stage projects; allow `EAC = AC + (BAC - EV)/CPI×SPI` for schedule-sensitive items, or use Monte Carlo
- Stakeholders ask "are we on track?"; agents that answer "SPI=0.92" without trend lose audience — always include 3-period trajectory
- LLM-generated narratives can mask negative variance with euphemism; require numeric thresholds before wording is allowed
- Effort vs cost confusion: hours × rate; agents must pull rate per role, not flat rate
- AI tooling cost is a real AC component now; meter token spend and include in AC if material
- Re-baselining "fixes" red metrics overnight; treat re-baseline as a P1 event, log it, never automate

## References
- PMI, *Practice Standard for Earned Value Management*, 2nd ed.
- ANSI/EIA-748-D EVMS standard
- DOD EVMS guidance: https://www.acq.osd.mil/asda/dpc/cp/policy/evm.html
- Quentin Fleming, *Earned Value Project Management* (4th ed.)
- DAU EVM Gold Card (cheat sheet): https://www.dau.edu
