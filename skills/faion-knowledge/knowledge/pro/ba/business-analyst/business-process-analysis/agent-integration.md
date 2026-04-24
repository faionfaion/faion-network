# Agent Integration — Business Process Analysis (Business Analyst)

This variant lives under `pro/ba/business-analyst/` — the BABOK-orchestrator skill. Unlike the `ba-modeling/` sibling (which is project- and BPMN-mechanics-focused), this one drives enterprise-scale BPA: process portfolios, governance bodies, M&A integration playbooks, and ERP/CRM rollouts. The sibling's `agent-integration.md` covers the day-to-day BPMN modelling loop in depth — read it for diagram mechanics, `pm4py`, and Camunda specifics. This file focuses on what changes when the unit of work is "the company's process landscape", not "one process".

## When to use

- M&A integration (buy-side or sell-side) where two organisations' process inventories must be reconciled into a Day-1 / Day-100 / target-state map.
- ERP / CRM / HCM rollout (SAP S/4HANA, Oracle Fusion, Workday, Salesforce, Microsoft Dynamics) — gap-fit against vendor reference processes (APQC PCF, SAP Signavio Value Accelerator, Oracle Modern Best Practice).
- Process portfolio assessment for a digital transformation programme: 100-500 processes scored on maturity (CMMI / PEMM), automation readiness, and customer impact.
- Establishing or auditing a BPMN governance regime: notation standards, naming conventions, level-1/2/3 decomposition rules, modelling-tool conventions.
- Pre-IPO / pre-acquisition process documentation for due diligence (SOX 404, ISO 9001, ISAE 3402/SOC 1) where auditors require process narratives + control points.
- Shared-services / GBS design where multiple business units consolidate into one process model.
- Outsourcing / BPO scoping — RACI, in-scope vs out-of-scope boundary, transition-services agreements.

## When NOT to use

- A single team's local workflow — use the `ba-modeling/business-process-analysis` variant; enterprise governance overhead crushes a one-team scope.
- Greenfield startup with no installed process estate — jump to `use-case-modeling` or `user-story-mapping`.
- Pure customer-experience redesign — use `customer-journey-mapping` (UX) and treat BPA as a downstream consequence.
- Real-time operational dashboards — BPA is portfolio-level, not minute-level.
- Replacing root-cause analysis on a single broken instance — use `5-whys` / fishbone.

## Where it fails / limitations

- **Portfolio inflation.** Enterprise programmes routinely "discover" 800+ processes; LLMs eagerly produce documentation for all of them. Without a Pareto cut, the artefact set is unmaintainable.
- **Reference-model fundamentalism.** Forcing every business onto APQC PCF or SCOR distorts genuine differentiators. Reference frameworks are scaffolding, not law.
- **Governance theatre.** A BPMN governance board produces standards nobody uses. The methodology cannot, by itself, prove adoption — instrumentation is required.
- **Cross-jurisdiction blind spots.** Multi-country processes have legal variants (GDPR vs CCPA vs LGPD; payroll rules per country). LLMs collapse these into one "global" process.
- **Politics-shaped diagrams.** In M&A, the surviving entity's process is documented as canonical even when the acquired entity's is better. The methodology has no political guard-rails.
- **Maturity-score inflation.** Self-assessed CMMI / PEMM levels skew high. Triangulate with evidence (audit findings, defect rates, process-mining conformance).
- **ERP gap-fit theatre.** Vendor reference processes are marketing artefacts. Treat "fit" claims as hypotheses, not conclusions; require a proof-of-configuration before signing.
- **Static snapshot.** Enterprise process landscapes drift quarterly (re-orgs, system changes, regulation). A 6-month-old BPA is already stale unless actively maintained.

## Agentic workflow

Run as a **two-tier orchestration**: an outer "portfolio agent" maintains the inventory, scoring, and governance artefacts; inner "process agents" (one invocation per in-scope process) apply the standard 5-stage BPA loop from the README. The portfolio agent's job is prioritisation (which processes to deep-model now), standards enforcement (every inner agent gets the same rubric and BPMN dialect), and roll-up (heat maps, maturity matrices, automation candidates ranked by `npv × feasibility`). For M&A and ERP work, the portfolio agent additionally maintains a side-by-side comparison table (acquirer vs target, or as-is vs vendor reference) and emits a gap log per process. Hand-offs to `faion-software-architect` and `faion-sdd-executor-agent` happen only after the portfolio agent approves a process for redesign — this prevents agents from racing ahead on processes that are out of scope.

### Recommended subagents

- `faion-business-analyst` (this skill's orchestrator) — Owns the portfolio inventory, governance standards, and stage-gate decisions. Holds the rubric pinned in prompts.
- `faion-ba-modeling` (sibling skill) — Delegated for per-process BPMN modelling; consumes raw evidence, returns conformant BPMN 2.0 XML + `process-documentation.md`.
- `faion-ba-core` (sibling skill) — Stakeholder analysis and elicitation planning; required upstream of any M&A or ERP exercise.
- `faion-research-agent` — Pulls APQC PCF, SCOR, eTOM, ITIL reference processes and vendor reference models (SAP Signavio, Oracle MBP) before the portfolio agent assigns deep-modelling work.
- `faion-software-architect` — Receives approved future-state processes and produces system-level integration / configuration design (ERP module mapping, integration patterns, master-data strategy).
- `faion-sdd-executor-agent` — Downstream implementation: spec → design → tasks (see `agents/faion-sdd-executor-agent.md`).
- General-purpose `Task` subagent for process mining — Drives `pm4py` / Celonis API; returns conformance scores per process to feed the portfolio scorecard.
- `password-scrubber-agent` — Mandatory pre-filter on all inbound evidence (SOPs, ticket exports, transcripts) before any other agent reads them.

### Prompt pattern

Portfolio-agent kickoff (M&A example):

```
Inputs: acquirer-pcf.csv, target-pcf.csv, deal-thesis.md, integration-priorities.md.
Build the Process Portfolio Comparison artefact:
  - Map both inventories to APQC PCF Level 2.
  - For every PCF L2 row, fill: acquirer_owner, target_owner, decision (adopt-acquirer | adopt-target | hybrid | new), rationale (cite deal-thesis line).
  - Flag any L2 with no owner on either side as "GAP — requires design".
  - Output: portfolio.csv + decisions-log.md. Do NOT model individual processes yet.
```

Per-process delegation (after portfolio approves):

```
Process: <PCF L2 code> — <name>.
Rubric: pinned in standards/bpmn-conventions.md (read first).
Evidence: <list of files>. Scrub credentials before reading.
Run the 5-stage BPA loop (README). Output BPMN 2.0 XML + process-documentation.md + process-analysis.md.
Halt at stage 4 (future-state) and emit a review packet for the portfolio agent.
Do NOT advance to stage 5 — validation is a portfolio-level decision.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pm4py` | Process mining, conformance, BPMN 2.0 XML generation | `pip install pm4py` / https://pm4py.fit.fraunhofer.de |
| `bpmn-to-image` | Render BPMN XML → SVG/PNG for stakeholder review packets | `npm i -g bpmn-to-image` |
| `bpmnlint` | Validate BPMN files against governance rules | `npm i -g bpmnlint` |
| `mermaid-cli` (`mmdc`) | Quick L1/L2 portfolio overviews | `npm i -g @mermaid-js/mermaid-cli` |
| `pandas` + `pyjanitor` | Portfolio scoring tables, maturity heat maps | `pip install pandas pyjanitor` |
| `openpyxl` | Read vendor accelerator workbooks (SAP Signavio, Oracle MBP) | `pip install openpyxl` |
| `pdfplumber` / `python-docx` | Extract process steps from existing SOP / due-diligence packs | `pip install pdfplumber python-docx` |
| `whisper.cpp` | Transcribe stakeholder interviews and steering-committee recordings | https://github.com/ggerganov/whisper.cpp |
| `jq` + `csvkit` | Slice ERP / CRM event-log exports | `apt install jq` / `pip install csvkit` |
| `git` + `dvc` | Version BPMN, evidence, and analysis artefacts (DVC for large logs) | https://dvc.org |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| SAP Signavio (Process Manager + Insights + Journey Modeler) | SaaS | Yes — REST API, BPMN export | De-facto enterprise standard; deep value-stream + variant analytics |
| Celonis EMS | SaaS | Yes — Studio APIs, Process Adherence Manager | Industry leader for log-based discovery and conformance |
| Software AG ARIS | SaaS + on-prem | Partial — APIs paid | Long-standing enterprise BPM; strong governance metadata |
| iGrafx | SaaS | Yes — REST | Mid-market enterprise BPM with simulation |
| Camunda 8 (SaaS / self-host) | OSS + SaaS | Yes — REST, Operate, Tasklist APIs | Open BPMN 2.0; pairs well with implementation phase |
| Apromore | OSS + SaaS | Yes — REST | Open-source process mining; pairs with `pm4py` |
| UiPath Process Mining (formerly ProcessGold) | SaaS | Yes — APIs | Strongest tie-in if RPA is part of the future state |
| Microsoft Process Insights / Power Automate Process Mining | SaaS | Yes — Graph API | Default if shop is Microsoft 365-centric |
| LeanIX / Ardoq | SaaS | Yes — REST | EA tools; pair process portfolio with application portfolio (TIME assessment) |
| ServiceNow APM + Process Mining | SaaS | Yes — REST | If ServiceNow is the system of record for IT/HR |
| Mega HOPEX | SaaS / on-prem | Partial | Heavy GRC + risk integration; bureaucratic but audit-grade |
| Confluence / SharePoint | SaaS | Yes — REST | Where the readable narratives end up; agents publish via API |
| Jira / ServiceNow / Salesforce / Workday / SAP / NetSuite | SaaS | Yes — REST / OData / Bulk | Source of event logs for portfolio-wide mining |
| Notion / Coda | SaaS | Yes — REST | Lightweight portfolio dashboards for smaller programmes |

## Templates & scripts

The README ships single-process templates (Process Documentation, Process Analysis); reuse those inside per-process agents. For the portfolio tier, add a scoring artefact. Drop into `.aidocs/<programme>/portfolio/scorecard.csv`:

```
pcf_l2_code,pcf_l2_name,owner,maturity_pemm,volume_per_year,cycle_time_min,nva_pct,automation_candidate_score,risk_score,decision
1.1.1,Define the business concept,VP Strategy,P-2,4,2880,55,2,4,review
1.3.5,Manage customer master data,Data Office,P-3,12000,18,40,5,3,redesign
2.4.2,Process accounts payable,Finance Ops,P-2,180000,9,62,5,2,automate
```

Inline ranking script (≤50 lines) — reads `scorecard.csv`, ranks redesign / automation candidates by `frequency_weighted_nva × feasibility`:

```python
#!/usr/bin/env python3
"""rank_portfolio.py scorecard.csv  -> ranked.csv (top automation/redesign candidates)."""
import sys
import pandas as pd

df = pd.read_csv(sys.argv[1])
required = {"volume_per_year", "cycle_time_min", "nva_pct",
            "automation_candidate_score", "risk_score"}
missing = required - set(df.columns)
if missing:
    sys.exit(f"missing columns: {missing}")

df["nva_minutes_per_year"] = (
    df["volume_per_year"] * df["cycle_time_min"] * df["nva_pct"] / 100
)
# 0-1 normaliser
def norm(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-9)

df["impact"] = norm(df["nva_minutes_per_year"])
df["feasibility"] = norm(df["automation_candidate_score"])  # 1-5
df["risk"] = norm(df["risk_score"])                          # 1-5 (high = harder)
df["score"] = df["impact"] * df["feasibility"] * (1 - 0.5 * df["risk"])

ranked = df.sort_values("score", ascending=False)[
    ["pcf_l2_code", "pcf_l2_name", "owner", "decision",
     "nva_minutes_per_year", "score"]
]
ranked.to_csv("ranked.csv", index=False)
print(ranked.head(20).to_string(index=False))
```

Per-process artefacts continue to live under `.aidocs/<programme>/processes/<pcf-l2-code>/` — `bpmn.xml`, `process-documentation.md`, `process-analysis.md`, `evidence/`. The portfolio agent never edits those; it only reads roll-up metrics.

## Best practices

- **Pareto the inventory first.** Score every L2 process; deep-model only the top decile by `nva_minutes_per_year × strategic_fit`. Document the rest at narrative depth only (one paragraph each).
- **Pin the BPMN dialect early.** Decide level-of-detail (L1 / L2 / L3 / L4), naming convention (verb-noun), pool/lane discipline, and message-flow rules before any modelling starts. Put the rules in `standards/bpmn-conventions.md` and have every agent read them.
- **Anchor to a reference framework, but score the deviation.** APQC PCF / SCOR / eTOM are anchors, not laws. For every deviation from the reference, capture rationale + competitive-differentiation hypothesis.
- **Couple process to application portfolio.** A process that runs on 5 redundant systems is the application-rationalisation case, not just a process case. Cross-link to LeanIX / Ardoq / your CMDB.
- **Make conformance the default validator.** Once an event log exists, run `pm4py` / Celonis monthly against the modelled BPMN. Conformance < 80% → re-document, don't argue.
- **Quantify before redesigning.** Future-state without baseline metrics is a wish list. Demand volume + cycle + cost; if data is missing, run a sampling pilot.
- **Diff future-vs-current as a structured table.** Columns: `step | current actor | future actor | current system | future system | change type | risk | dependency`. Forces specificity and reveals integration prerequisites.
- **For ERP rollouts: gap-fit, then config-fit, then customise-only-as-last-resort.** Document each gap as adopt-standard / configure / extend / build / drop. Agents bias toward "build" — counter with explicit configure-first prompts.
- **For M&A: keep an "ownership decision" log per L2.** acquirer / target / hybrid / new. Tie every decision to a deal-thesis citation; un-cited decisions are blocked.
- **Treat BPMN as code.** Source-control BPMN XML, run `bpmnlint` in CI, code-review changes, tag releases per programme milestone.
- **Plan adoption from day one.** Process docs that nobody reads have zero ROI. Bake in an adoption metric (page views, training completion, audit findings closed) and report it monthly.

## AI-agent gotchas

- **Portfolio bloat.** Without a Pareto rule the agent documents 800 processes at full depth. Hard-cap deep-modelling to the top decile and force narrative-only for the rest.
- **Reference-model auto-fill.** Agents lift APQC PCF text verbatim and pretend it describes the company. Require: every reference-derived sentence must be tagged `[reference]` and reviewed by a human before publication.
- **M&A naming collisions.** Acquirer's "Order to Cash" and target's "Sales Cycle" may be the same process. Force the agent to map both names to a canonical PCF L2 code before comparison.
- **Vendor-marketing leakage.** ERP vendor reference processes embed product names ("S/4HANA Sales Order"). Strip vendor branding before publishing; otherwise diagrams look like sales decks.
- **Cross-country smoothing.** "Hire to retire" looks identical until you check tax + labour law. Force the agent to enumerate jurisdictions and flag legal-variant points.
- **Maturity self-flattery.** PEMM / CMMI self-scores trend high. Require triangulation against at least one external signal (audit finding, defect rate, conformance score).
- **Standard-violations slipped past lint.** Agents emit valid BPMN that violates internal naming convention. Run `bpmnlint` with custom rules, fail the artefact on violation.
- **Hallucinated KPIs.** "AP cycle time: 3.5 days" appears with no source. Hard rule: every metric cell cites file + line; otherwise `Data not available`.
- **Workaround erasure.** Stakeholder transcript says "we email Brian to push the invoice through". Agent rewrites as "exception handling routes via Finance team". Require verbatim quotes for any anomaly and preserve them in `evidence/anomalies.md`.
- **PII / credential / commercial-secret leak.** M&A diligence packs and ERP exports contain everything. Mandatory `password-scrubber-agent` pre-pass; additionally redact deal-pricing, salaries, customer names before any third-party SaaS upload.
- **Cron-mode auto-advance.** Stage-gate decisions are political. In headless mode, agents must freeze at stage 4 and emit a review packet — never auto-promote to stage 5.
- **Token blow-up at portfolio synthesis.** A 500-process landscape exceeds context. Chunk by L1 value chain (one L1 per worker), summarise to scorecard rows, then a final orchestrator pass over the scorecard alone.

## References

- BABOK Guide v3 — KA 7 Requirements Analysis and Design Definition; Techniques 10.34 (Process Analysis), 10.35 (Process Modelling)
- BPMN 2.0 specification — https://www.omg.org/spec/BPMN/2.0/
- APQC Process Classification Framework — https://www.apqc.org/process-frameworks
- SCOR Digital Standard (ASCM) — https://www.ascm.org/learning-development/scor-dx/
- eTOM (TM Forum) — https://www.tmforum.org/oda/business/etom-business-process-framework/
- Hammer M., "The Process Audit", HBR 2007 — PEMM maturity model
- van der Aalst W., *Process Mining: Data Science in Action*, 2nd ed. — https://www.processmining.org
- SAP Signavio Value Accelerators — https://www.signavio.com/products/value-accelerators/
- Oracle Modern Best Practice — https://www.oracle.com/modern-best-practice/
- Sibling: `../../ba-modeling/business-process-analysis/agent-integration.md` (per-process BPMN mechanics, `pm4py`, Camunda)
- This repo's BA orchestrator: `agents/faion-sdd-executor-agent.md`
