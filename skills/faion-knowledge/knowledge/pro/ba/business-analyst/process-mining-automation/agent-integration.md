# Agent Integration — Process Mining and Intelligent Automation Analysis

This methodology pairs two distinct but complementary disciplines: (1) **process mining** — reconstructing actual process flow from event logs in IT systems, and (2) **automation candidate assessment** — scoring discovered processes against RPA/IA fit criteria. In an agentic setup these split cleanly: a Python subagent drives `pm4py` over event-log CSVs to produce a discovered model + variants + bottleneck stats, then an LLM subagent ranks the discovered processes for automation using the README's 6-criterion matrix, then a third agent drafts an ROI memo. The methodology's deliverable is a ranked queue of automation candidates with evidence-backed scores — not a generic "we should automate things" deck.

## When to use

- You have access to system event logs (Jira, ServiceNow, Salesforce, ERP, support tools) and want to find automation candidates without interviewing every team.
- An RPA/IA program is failing or being scoped — you need data-driven candidate selection instead of stakeholder anecdotes ("Karen says invoice entry is a nightmare").
- Conformance audit: documented SOP says path A→B→C, you suspect reality is A→B→D→B→C; mining reveals the actual variants and rework loops.
- Pre-RPA discovery for one specific process — discover the variants before a UiPath/Power Automate developer starts recording, so the bot covers the real branches.
- M&A / post-acquisition: rapidly map "how does this acquired company actually run its order-to-cash" without trusting the inherited documentation.
- Continuous monitoring: deploy mining on a recurring schedule to detect process drift (variant explosion, cycle-time regressions) after a system change.

## When NOT to use

- No event logs exist and cannot be created — process mining has nothing to consume; fall back to `business-process-analysis` with interviews.
- Knowledge work without discrete activities (R&D, creative, exec decisions) — mining produces spaghetti graphs without insight.
- The process is already well-instrumented and stakeholders agree on the as-is — skip mining, go straight to automation scoring.
- Single-instance investigation ("why did invoice #123 fail?") — use log queries, not process mining.
- Pre-decision strategic questions ("should we enter market X?") — mining is execution-level, not strategic.
- Hard real-time decisioning — mining is offline batch analysis with hours-to-days latency, not an operational control plane.
- Fewer than ~200 case instances in the log — statistical patterns are unreliable; the variant analysis will mislead.

## Where it fails / limitations

- **Garbage event logs.** Most enterprise logs lack a stable case ID, a clean activity label, or a reliable timestamp. Mining tools amplify dirty data into confidently-wrong DFGs. Budget 60-80% of effort on log preparation.
- **The XES tax.** `pm4py` and most academic tooling expect XES (XML) format; real systems emit CSV. Conversion is mechanical but error-prone (timezone drift, NULL case IDs, multi-row activities).
- **Spaghetti diagrams.** A high-variability process (e.g., support ticketing with 800 unique paths) renders as an unreadable graph. Without filtering (top-K variants, frequency thresholds) the output is useless.
- **Hallucinated automation ROI.** LLMs cheerfully fabricate "saves 2 FTE = $180k/year" with no source. The README's ROI template invites this. Hard rule: every $ figure must cite log-derived volume + a documented loaded-cost rate.
- **Vendor lock-in masquerading as analysis.** Celonis/UiPath Process Mining bundle discovery + auto-recommendation; their automation suggestions skew toward their own RPA platform.
- **Conformance theater.** Conformance checking against a "designed" model that was itself wishful thinking produces inflated deviation counts. Validate the reference model first.
- **Privacy / GDPR exposure.** Event logs frequently contain PII (user IDs, customer names in activity labels, IP addresses). Mining tools store these; agents passing logs to cloud LLMs leak them.
- **RPA-fragility.** A process that scores 28/30 on the assessment matrix may still be a bad RPA candidate if upstream UIs change frequently — the matrix has no "UI volatility" criterion.
- **Score inflation.** LLMs grade their own assessment; subjective criteria (Standardization, Rule Clarity) drift to 4-5 unless rubric examples are pinned in the prompt.
- **Mining ≠ understanding.** The graph shows *what* happens, not *why*. Causality requires interviews; agents skip this and recommend automation of compensating steps that mask root cause.

## Agentic workflow

Run a 4-stage pipeline. **Stage 1 (extract)** — a connector agent pulls event data from a source system (Jira REST, Salesforce Bulk API, DB SELECT) into a normalized CSV (`case_id, activity, timestamp, resource, attrs`). **Stage 2 (mine)** — a Python subagent runs `pm4py` to produce DFG/Petri net, variant analysis, and bottleneck stats; outputs `mining-report.md` + SVG. **Stage 3 (assess)** — an LLM subagent applies the 6-criterion automation matrix to each top-N variant, citing mining stats for every score. **Stage 4 (recommend)** — a synthesis agent produces a ranked candidate queue with ROI estimates (volume × loaded-cost × cycle-time saved), each row traceable to mining evidence. Use `faion-ba-agent` (declared in business-analyst skill) as orchestrator; delegate mining to a general-purpose `Task` subagent with `pm4py`; checkpoint between stages because re-running stage 1 is expensive.

### Recommended subagents

- `faion-ba-agent` — Orchestrator (per business-analyst skill front matter). Owns the 4-stage state machine, writes outputs to `.aidocs/<feature>/`. Coordinates handoff to PM/Architect agents.
- `password-scrubber-agent` (this repo: `agents/password-scrubber-agent.md`) — **Mandatory first pass** on any raw event log. Logs routinely contain credentials in URLs, free-text comments, exception traces.
- General-purpose `Task` subagent for mining — Equipped with `pm4py`, `pandas`, `graphviz`. Receives normalized CSV, returns DFG SVG + stats CSV + variants JSON.
- `faion-software-architect` — Consumes automation recommendations, decides whether automation lives in n8n / RPA / native code change.
- `faion-sdd-executor-agent` (this repo: `agents/faion-sdd-executor-agent.md`) — Downstream: turns approved automation candidate into spec → design → tasks.
- `faion-research-agent` — Vendor selection: when matrix flags a candidate, research current RPA/IA vendor capabilities and pricing.
- `faion-data-agent` (or general-purpose with `pandas`) — Stage 1 connector: extract from source systems, normalize timestamps and case keys.

### Prompt pattern

Stage 2 (mine) dispatch to Python subagent:

```
Input: events.csv (columns: case_id, activity, timestamp, resource).
Run pm4py: discover DFG (frequency variant), inductive miner Petri net,
variant analysis (top 10 by frequency), bottleneck (mean sojourn time per activity).
Write outputs to .aidocs/<feature>/mining/:
  dfg.svg, petri.svg, variants.json, bottlenecks.csv, mining-report.md.
mining-report.md sections: Log summary | Top variants table | Bottlenecks |
Rework loops | Conformance vs reference model (skip if no reference).
No prose interpretation — facts and tables only.
```

Stage 3 (assess) dispatch:

```
Input: mining-report.md + variants.json + bottlenecks.csv.
For each of the top 5 variants, fill the README "Automation Readiness" matrix.
Rubric:
  Volume = transactions/day from log (cite). 5 if >100, 3 if 20-100, 1 if <20.
  Standardization = 5 if variant covers >70% of cases, 1 if <20%.
  Digital Inputs = 5 if all activities have structured fields in the log; else cite missing.
  Process Stability = 5 if variant share unchanged ±10% over last 6 months (require timestamp window check).
  Exception Rate = inverse of rework-loop frequency (cite bottlenecks.csv).
  Rule Clarity = score only if SOP/policy doc supplied; else mark "needs evidence".
Output one filled matrix per variant; refuse to score if evidence is missing.
End with a ranked Top-3 with ROI estimate using only log-derived volume × stated FTE cost.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pm4py` | Process discovery (DFG, Petri net, BPMN), conformance checking, variant analysis | `pip install pm4py` / https://pm4py.fit.fraunhofer.de |
| `prom-tools` (ProM CLI) | Academic process mining toolkit, batch mode | https://promtools.org |
| `Apromore CLI` | OSS process mining; supports XES + log clustering | https://apromore.com/platform/community-edition |
| `xes-standard` validators (`xeslite`, `pyxes`) | Validate / convert XES event logs | `pip install pyxes` |
| `pandas` + `pyarrow` | Event-log normalization and prep (timestamp parsing, case stitching) | `pip install pandas pyarrow` |
| `graphviz` (`dot`) | Render DFG / Petri net SVG output | `apt install graphviz` |
| `mermaid-cli` (`mmdc`) | Quick BPMN-ish flowcharts for review packets | `npm i -g @mermaid-js/mermaid-cli` |
| `bpmn-to-image` | Render valid BPMN 2.0 XML to SVG/PNG | `npm i -g bpmn-to-image` |
| `csvkit` | Inspect/clean raw event-log CSV before mining | `pip install csvkit` |
| `jq` | Slice JSON event exports from REST APIs | `apt install jq` |
| `presidio-analyzer` | PII redaction in event-log free-text fields before LLM hand-off | `pip install presidio-analyzer presidio-anonymizer` |
| `uipath-cli` | Deploy/manage UiPath bots from terminal | https://docs.uipath.com/orchestrator/cli |
| `pac` (Power Platform CLI) | Deploy Power Automate flows | https://learn.microsoft.com/power-platform/developer/cli |
| `camunda-cloud-cli` (`zbctl`) | Deploy BPMN to Camunda 8; mining-derived models can be executed | https://docs.camunda.io/docs/zeebe/cli |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Celonis EMS | SaaS | Yes — REST + Studio APIs | Market leader; expensive; auto-recommendations bias to Celonis Action Engine |
| UiPath Process Mining (formerly ProcessGold) | SaaS | Yes — APIs | Tightly coupled to UiPath RPA — natural pipeline for automation execution |
| SAP Signavio Process Intelligence | SaaS | Partial — REST | Strong for SAP-centric processes; deep BPMN modeler integration |
| Apromore | OSS + SaaS | Yes — REST | Pairs cleanly with `pm4py` workflows; lower vendor lock-in |
| Fluxicon Disco | Desktop | No (desktop-only) | Best-in-class one-shot DFG visualization; not for automation pipelines |
| Microsoft Power Automate Process Mining | SaaS | Yes — Graph API | Bundled with M365; natural for Office-process discovery |
| QPR ProcessAnalyzer | SaaS | Partial — APIs | European compliance focus |
| ABBYY Timeline | SaaS | Yes — APIs | Document-heavy processes (invoices, contracts) |
| UiPath Studio + Orchestrator | SaaS | Yes — REST | RPA execution platform; deploy + monitor bots via API |
| Automation Anywhere A360 | SaaS | Yes — REST | Cloud-native RPA |
| Blue Prism (SS&C) | SaaS + on-prem | Partial — REST | Enterprise governance focus |
| Microsoft Power Automate | SaaS | Yes — Graph + Power Platform CLI | M365-integrated low-code automation |
| n8n (this workspace) | OSS, self-hosted | Yes — REST | Implement automation candidates as workflows; mining-derived BPMN maps to nodes |
| Camunda 8 | OSS + SaaS | Yes — Zeebe APIs | If mining produces valid BPMN, deploy as executable orchestrator |
| Workato / Tray.io | SaaS | Yes — REST | iPaaS — alternative target for non-UI automation |
| Celonis Action Engine | SaaS | Yes — APIs | Closes the loop: triggers actions on detected process deviations |

## Templates & scripts

The methodology's README ships an "Automation Assessment Matrix" template; reuse it. The siblings `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md` are empty placeholders — do not rely on them.

Inline: minimal mining + assessment scaffold (≤50 lines) for stage 2:

```python
#!/usr/bin/env python3
"""
mine_and_score.py events.csv --out out/
Produces dfg.svg, variants.csv, bottlenecks.csv, top_candidates.json
columns: case_id, activity, timestamp[, resource]
"""
import argparse, json, os
from pathlib import Path
import pandas as pd
import pm4py
from pm4py.algo.discovery.dfg import algorithm as dfg_algo
from pm4py.visualization.dfg import visualizer as dfg_vis
from pm4py.statistics.variants.log import get as variants_get

p = argparse.ArgumentParser()
p.add_argument("csv"); p.add_argument("--out", default="out")
p.add_argument("--top", type=int, default=5)
a = p.parse_args(); Path(a.out).mkdir(exist_ok=True)

df = pd.read_csv(a.csv, parse_dates=["timestamp"])
log = pm4py.format_dataframe(
    df, case_id="case_id", activity_key="activity", timestamp_key="timestamp"
)
dfg = dfg_algo.apply(log)
dfg_vis.save(dfg_vis.apply(dfg, log=log, variant=dfg_vis.Variants.FREQUENCY),
             f"{a.out}/dfg.svg")

variants = variants_get.get_variants(log)
rows = sorted(
    [{"variant": " > ".join(v), "count": len(cs)} for v, cs in variants.items()],
    key=lambda r: -r["count"]
)[: a.top]
pd.DataFrame(rows).to_csv(f"{a.out}/variants.csv", index=False)

dur = (df.groupby("case_id")["timestamp"].agg(["min", "max"])
         .assign(cycle_min=lambda x: (x["max"] - x["min"]).dt.total_seconds() / 60))
total = len(df["case_id"].unique())
candidates = [
    {"variant": r["variant"], "share": r["count"] / total,
     "score_volume": 5 if r["count"] > 100 else (3 if r["count"] > 20 else 1),
     "score_standardization": 5 if r["count"] / total > 0.7 else (3 if r["count"] / total > 0.3 else 1)}
    for r in rows
]
Path(f"{a.out}/top_candidates.json").write_text(json.dumps(candidates, indent=2))
print(f"wrote {a.out}/dfg.svg, variants.csv, top_candidates.json "
      f"(cases={total}, mean_cycle_min={dur['cycle_min'].mean():.1f})")
```

Pipeline state file (drop into `.aidocs/<feature>/_pma-state.json`):

```json
{
  "process": "<name>",
  "stages": ["extract", "mine", "assess", "recommend"],
  "completed": [],
  "source_system": "<jira|salesforce|servicenow|sap|...>",
  "log_window": {"from": "<iso>", "to": "<iso>"},
  "case_count": 0,
  "artifacts": {
    "raw_log": null,
    "scrubbed_log": null,
    "mining_report": null,
    "assessment_matrix": null,
    "candidates": null
  }
}
```

## Best practices

- **Scrub before mining.** Run `password-scrubber-agent` then `presidio-analyzer` on raw logs before any LLM sees them. Activity labels and free-text fields leak PII routinely.
- **Anchor the case ID.** Every dispute about mining output traces back to case-ID instability. Validate before stage 2: `df.groupby("case_id").size().describe()`; if median < 2 events, your case ID is wrong.
- **Filter by frequency before visualization.** Always render DFG with at least an 80% frequency cutoff; full graphs are unreadable and tell you nothing.
- **Score only with citations.** Each cell in the Automation Readiness matrix must reference a stat from `mining-report.md`. Reject scores marked "estimated".
- **Compare top-3 variants, not the average.** Process mining averages hide variant-specific automation opportunities — the long tail is where rework lives.
- **Quantify rework explicitly.** Count loop occurrences (`A → B → A`) per case; loops in cases over 3 events are NVA candidates.
- **Pin the rubric in the prompt.** Subjective criteria (Standardization, Rule Clarity) drift across runs; pin examples and require comparison to examples for every score.
- **ROI from log-derived volume only.** Never accept stakeholder volume estimates when log volume is available. Hourly rate × cycle-minutes-saved × log-volume = hard floor.
- **Pilot one variant before broadcasting recommendations.** Implement the top candidate end-to-end (n8n / RPA bot), measure actual savings for 30 days, then extend the matrix to others.
- **Re-mine after every UI/system change.** Bots break when the UI changes; re-running mining on the post-change log catches drift before it cascades.
- **Eliminate before automating.** If a NVA step can be deleted (a duplicate approval, an obsolete sign-off), eliminate it; do not pave the cowpath with RPA.
- **Keep the BPMN in source control.** Export discovered BPMN XML alongside `mining-report.md` so changes are diffable in PRs.
- **Separate process mining from task mining.** Task mining (desktop activity capture) is a different toolset; don't conflate. Use task mining only when no system-level event log exists.

## AI-agent gotchas

- **Volume hallucination.** Without explicit grounding, LLMs invent transaction volumes. Hard rule: cite a count from `variants.csv` for every Volume score.
- **Activity-name normalization drift.** "Approve PR" / "PR_APPROVED" / "approved purchase request" should collapse to one activity. LLMs may either over-merge (lose detail) or under-merge (variant explosion). Pin a normalization map.
- **PII in activity labels.** Logs like `activity = "Email sent to john.doe@acme.com"` push PII into the LLM context. Pre-redact with regex + `presidio` before mining.
- **Vendor pitch contamination.** When agent has web access, "best RPA tool for X" returns vendor blogs that bias scoring. Restrict to neutral sources or require multi-source corroboration.
- **Loop-mining false positives.** `pm4py` flags loops where the real process has retries on transient errors. Filter event logs by terminal states or remove sub-second consecutive duplicates first.
- **Token blow-up at synthesis.** A 50k-event log exceeds context. Pre-aggregate to variants + per-activity stats; never feed raw log to an LLM.
- **"Estimated" creep.** Agents hide unsupported claims behind "(estimated)". Hard-block: write `Data not available` if no log evidence; refuse to fill the cell otherwise.
- **Auto-bias toward "automate everything".** README's RPA framing nudges agents to recommend automation. Add an explicit `Eliminate | Simplify | Automate` decision in stage 4 with elimination preferred when feasible.
- **Confounding cycle time and lead time.** Cycle time = time the case is being worked; lead time = total elapsed. LLMs use them interchangeably. Define both in the prompt.
- **Fabricated FTE math.** "1.5 FTE saved" with no math shown is a tell. Require the formula: `cycle_min_saved × cases_per_year / (60 × hours_per_FTE_year)`.
- **Deterministic re-runs.** Run scoring twice at temperature 0; flag any cell that differs across runs and route for human review.
- **No automation = no observability.** RPA bots fail silently; recommendation must include monitoring (Orchestrator alerts, n8n error workflow) or it is incomplete.
- **Cron-mode interactivity gap.** Scoring is automatable; selecting which top candidate to pilot is a human decision. Freeze the workflow at stage 4, emit a ranked list, do not auto-advance to implementation.

## References

- Process Mining Manifesto (van der Aalst et al., 2011) — https://www.tf-pm.org/resources/manifesto
- van der Aalst, *Process Mining: Data Science in Action* (2nd ed.) — Springer
- `pm4py` documentation — https://pm4py.fit.fraunhofer.de/documentation
- IEEE XES standard for event logs — https://xes-standard.org
- BABOK Guide v3 — KA 7 (Requirements Analysis and Design Definition), Techniques: Process Modelling (10.35), Process Analysis (10.34), Decision Modelling (10.16)
- Gartner Magic Quadrant for Process Mining (annual) — https://www.gartner.com/en/documents
- Celonis Process Intelligence developer docs — https://docs.celonis.com
- UiPath Process Mining docs — https://docs.uipath.com/process-mining
- Microsoft Power Automate Process Mining — https://learn.microsoft.com/power-automate/process-mining-overview
- Apromore documentation — https://apromore.com/platform/community-edition
- Sibling methodology: `../business-process-analysis/README.md` (use when no event logs exist)
- Sibling methodology: `../decision-analysis/README.md` (downstream when automation requires rule extraction)
- Sibling methodology: `../solution-assessment/README.md` (downstream evaluation of deployed automations)
- This repo's downstream executor: `agents/faion-sdd-executor-agent.md`
- This repo's pre-mining sanitizer: `agents/password-scrubber-agent.md`
