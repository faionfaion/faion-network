# Agent Integration — Process Mining (BA-core fundamentals)

This file is the **first-principles** companion to the methodology. The sibling
`pro/ba/business-analyst/process-mining-automation/agent-integration.md` covers
the full 4-stage agentic pipeline (extract → mine → assess → recommend). Here
the focus is narrower: *what process mining actually is*, the three
introductory discovery algorithms a BA needs to recognize, and the adoption
decision (should this team even start a process-mining initiative this
quarter?). Read this BEFORE the business-analyst variant.

## When to use

- A BA is being asked to scope a process-mining initiative for the first time
  and needs to brief a steering committee on feasibility *before* tool
  selection.
- Pre-RFP phase: comparing Celonis / UiPath Process Mining / Apromore /
  open-source `pm4py` requires understanding which discovery algorithm each
  uses — vendors hide this behind UX.
- Educating stakeholders who confuse process mining with task mining (desktop
  recording) or with BPM (process modeling). The distinctions decide budget.
- Validating that a candidate event log meets the **three minimum columns**
  (case ID, activity, timestamp) before any tool is procured.
- Choosing a discovery algorithm: Alpha / Heuristic / Inductive Miner have
  different failure modes; picking by guess wastes a month of "why is the
  graph wrong?" debugging.
- Conformance vs discovery vs enhancement — naming the *type* of mining
  question on the table so the right artefact is produced.
- Diagnosing why an existing process-mining deployment produced a
  spaghetti-DFG: usually the algorithm choice, not the data.

## When NOT to use

- The team already has process-mining tooling deployed and a working event
  log — go straight to the business-analyst variant for the operational
  pipeline.
- The question is "what should the process be?" (to-be design) — that is
  BPMN modelling, not mining. Mining only describes as-is.
- Single-system audit log review with <50 cases — use SQL and a pivot table;
  process mining is overkill below ~200 cases per variant.
- Task-level desktop work (clicks, copy-paste between apps) — this is **task
  mining**, a different discipline with different tooling (UiPath Task
  Mining, Microsoft Process Insights). Confusing the two leads to wrong
  vendor purchase.
- Knowledge work without a discrete activity vocabulary (writing,
  negotiation, R&D) — the activity column will collapse to "work" and the
  discovery algorithm will produce one giant blob.
- Compliance-only need where logs are already linear (case → step1 → step2 →
  step3) — a simple SQL aggregation answers it.

## Where it fails / limitations

- **Algorithm mismatch.** Alpha Miner cannot handle loops or noise; running
  it on real-world ticketing data produces an unsound Petri net. Heuristic
  Miner handles noise but loses formal guarantees. Inductive Miner
  guarantees soundness but trades off fitness against precision. A BA who
  cannot name these tradeoffs cannot evaluate a vendor demo.
- **Event log is the methodology.** Process mining literature is thick with
  algorithms; in practice 80% of project effort is **log preparation**:
  defining the case notion, normalising activity labels, fixing
  timestamps, dropping "system events" that pollute the trace. Skipping
  this step is the single biggest cause of failed initiatives.
- **Three columns ≠ usable log.** Even with case_id/activity/timestamp,
  logs fail when: timestamps are date-only (no time), case IDs span
  multiple business processes (must be split), or activities are
  free-text comments that need categorisation.
- **Variant explosion.** A real ITSM log with 5,000 cases will surface
  600+ variants; the discovery graph is unreadable. Without filtering
  (top-K by frequency, fitness threshold) the output is theatre.
- **Confusion with BI.** Stakeholders expect Tableau-style dashboards;
  process mining produces graphs they cannot read. Adoption fails on UX
  perception, not capability.
- **Mining is descriptive, not causal.** It shows that activity B
  follows A in 70% of cases; it does *not* explain why. A BA who treats
  the DFG as causal evidence will recommend the wrong intervention.
- **Privacy / GDPR.** Event logs frequently leak PII through resource
  IDs, customer names embedded in activity strings, and free-text
  attributes. Mining tools persist these.
- **Vendor algorithm opacity.** Celonis and UiPath rebrand standard
  algorithms; the BA must press for "is this Inductive Miner with
  noise filter or Heuristic Miner?" — vendor sales engineers often
  do not know.

## Agentic workflow

For the **fundamentals / adoption** path (this variant), agents do *less*
than in the operational pipeline. The flow is:
**(1) explain** — an LLM subagent generates a one-pager on what process
mining is for the specific stakeholder audience (exec / ops / IT).
**(2) audit log feasibility** — a Python subagent runs a 30-line script
against a sample event-log CSV and reports column completeness, case-ID
cardinality, timestamp coverage, activity vocabulary size, and estimated
variant count, then flags whether the log is mining-ready.
**(3) recommend algorithm** — based on log characteristics (noise level,
loop presence, activity count) the agent picks Alpha / Heuristic /
Inductive and justifies it.
**(4) adoption gate** — the agent emits a go/no-go memo against six
adoption criteria (event-log availability, case volume, stakeholder
literacy, regulatory tolerance, tooling budget, automation downstream
dependency). Only if go: hand off to the business-analyst variant for
the full pipeline.

### Recommended subagents

- `faion-sdd-executor-agent` (this repo: `agents/faion-sdd-executor-agent.md`)
  — Owns the adoption-gate memo as a spec deliverable; routes go/no-go to
  the SDD lifecycle.
- `password-scrubber-agent` (this repo: `agents/password-scrubber-agent.md`)
  — **Mandatory** before any sample log is read by an LLM. Logs leak
  credentials in URL columns and free-text attrs.
- General-purpose `Task` subagent with `pandas` — Runs the feasibility
  audit script (below). Returns a single JSON record; cheap, deterministic.
- `faion-ba-agent` (declared in business-analyst skill front matter) —
  Owns the stakeholder-explainer one-pager. Tunes vocabulary per audience.
- `faion-research-agent` — Vendor algorithm clarification: when a
  candidate vendor is named, fetches the product docs and answers
  "which discovery algorithm with what defaults?".

### Prompt pattern

Adoption-gate prompt:

```
You are scoping a process-mining initiative for <team>.
Inputs: log feasibility audit JSON (attached), business goal, automation
intent (yes/no), regulatory context (GDPR/HIPAA/none), tooling budget tier
(open-source / mid-market / enterprise).
Score each of 6 adoption criteria on 1-5 with one-line evidence.
Output: a 200-word go/no-go memo. If no-go, name the single blocker and
the cheapest experiment to unblock.
```

Algorithm-recommendation prompt:

```
Given log stats: <activity_count>, <variant_count>, <case_count>,
<has_loops>, <noise_estimate>, <self_loops_pct>, recommend one of:
Alpha / Heuristic / Inductive Miner (infrequent variant). State the
single failure mode if the wrong choice is made on this log.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pm4py` | Reference Python lib: Alpha, Heuristic, Inductive miners; XES + CSV import; conformance checking | `pip install pm4py`; https://pm4py.fit.fraunhofer.de/ |
| `ProM` | Academic GUI; widest algorithm coverage including Fuzzy Miner, Genetic Miner | https://promtools.org/ |
| `Disco` (Fluxicon) | Commercial desktop tool, fast for log audit and exploratory mining | https://fluxicon.com/disco/ |
| `Apromore Core` | Open-source web platform; discovery + conformance + comparison | https://apromore.com/ |
| `bupaR` | R ecosystem; strong on event-log preprocessing and visualisation | https://bupar.net/ |
| `xes-standard` validators | Validate XES file structure before mining | bundled with `pm4py` |
| `dfg-visualizer` | Render DFG outputs in CI for review | part of `pm4py` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Celonis EMS | SaaS | Partial — REST API + PQL query language | Market leader; algorithm = proprietary variant of Inductive Miner |
| UiPath Process Mining | SaaS | Limited — UI-driven, API in preview | Tight RPA tie-in; biased toward UiPath bots downstream |
| Microsoft Process Mining (in Power Automate) | SaaS | Yes — Dataverse + Graph API | Best when org is M365-native; algorithm undocumented |
| Apromore Enterprise | SaaS / on-prem | Yes — REST API, Python client | Closest to academic rigour; algorithm transparent |
| `pm4py` (Fraunhofer) | OSS Python lib | Yes — pure scriptable | Reference implementation; embeddable in any agent |
| ProM | OSS desktop | No — GUI only | Use for one-off algorithm experimentation, not pipelines |
| Disco | Commercial desktop | No — GUI only | Fastest for log triage; export CSV for downstream agents |
| IBM Process Mining (myInvenio) | SaaS | Partial — REST | Strong simulation features; expensive |
| QPR ProcessAnalyzer | SaaS | Partial | EU vendor; useful for GDPR-sensitive deployments |

## Templates & scripts

Inline feasibility-audit script (≤50 lines). Run before any vendor demo —
if this fails, no tool will save the project.

```python
# pm-feasibility-audit.py — usage: python pm-feasibility-audit.py log.csv
import sys, json
import pandas as pd

df = pd.read_csv(sys.argv[1])
required = {"case_id", "activity", "timestamp"}
missing = required - set(df.columns)
if missing:
    print(json.dumps({"ready": False, "missing_columns": sorted(missing)}))
    sys.exit(1)

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
ts_bad = int(df["timestamp"].isna().sum())
case_n = int(df["case_id"].nunique())
act_n = int(df["activity"].nunique())
events_per_case = df.groupby("case_id").size()
median_events = float(events_per_case.median())
trace = df.sort_values(["case_id", "timestamp"]).groupby("case_id")["activity"].apply(tuple)
variants = trace.value_counts()
variant_n = int(variants.size)
top10_share = float(variants.head(10).sum() / variants.sum())

verdict = (
    case_n >= 200 and act_n >= 3 and act_n <= 200
    and median_events >= 3 and ts_bad / len(df) < 0.02
)
print(json.dumps({
    "ready": verdict,
    "cases": case_n,
    "activities": act_n,
    "variants": variant_n,
    "median_events_per_case": median_events,
    "top10_variant_coverage": round(top10_share, 3),
    "bad_timestamps": ts_bad,
    "recommended_algorithm": (
        "alpha" if act_n < 15 and variant_n < 30
        else "inductive-infrequent" if variant_n > 100
        else "heuristic"
    ),
}, indent=2))
```

For the full pipeline templates (mining-report.md, automation-matrix.md,
ROI memo) see the business-analyst variant.

## Best practices

- **Name the question first.** Discovery / Conformance / Enhancement are
  three different deliverables — agents that conflate them produce
  graphs nobody asked for.
- **Audit the log before the algorithm.** Run the feasibility script
  above; if `ready: false`, do not proceed regardless of vendor pressure.
- **Keep the activity vocabulary under 50.** If the log has 200 distinct
  activities, the BA must define an activity-grouping taxonomy *first*;
  this is a manual modelling exercise, not an agent task.
- **Pin top-K variants.** Always filter to the top 10 variants by
  frequency for the first review; surface the long tail only after
  the main flow is understood.
- **Pair mining with one stakeholder interview.** Mining shows what
  happened; one 30-minute interview explains why. Skipping the
  interview is the most common failure mode.
- **Disclose the algorithm.** Every mining artefact must name the
  algorithm and parameters; otherwise downstream readers cannot judge
  the graph's reliability.
- **Strip PII at extraction.** Replace user / customer columns with
  hashes before the log leaves the source system. Do not rely on
  the mining tool's "anonymise" feature.

## AI-agent gotchas

- **Hallucinated event-log columns.** LLMs invent plausible column
  names ("CaseKey", "EventTime") that do not exist. Always pin the
  actual column list in the prompt; do not let the agent infer.
- **Algorithm name confusion.** "Inductive Miner" has three variants
  (basic, infrequent, directly-follows). Agents will pick whichever
  appeared more often in training data. Force the variant name.
- **Soundness vs fitness misreport.** LLMs will report "fitness 0.95"
  and call the model good even when soundness is False. Both metrics
  must be returned and the BA must check soundness first.
- **Spaghetti DFG presented as success.** Agents do not "see" graph
  unreadability; they will deliver a 600-node SVG and call the task
  done. Add a node/edge count gate to the workflow (e.g., abort if
  >40 nodes without explicit override).
- **Privacy regression.** Agents that re-derive activity labels from
  free-text fields can re-introduce PII that was scrubbed upstream.
  Re-scrub after any LLM transformation.
- **Vendor demo overconfidence.** Agents primed with vendor marketing
  copy parrot capability claims. Force vendor questions to be answered
  from documentation URLs, not memory.
- **Conformance against fictional model.** Agents happily run
  conformance against a BPMN drawn from a wishful-thinking SOP. The
  reference model must itself be validated by a human SME first.

## References

- Wil van der Aalst, *Process Mining: Data Science in Action* (2nd ed.,
  Springer, 2016) — definitive textbook; chapters 4-7 cover
  Alpha/Heuristic/Inductive miners.
- IEEE Task Force on Process Mining, *Process Mining Manifesto* (2011) —
  the 11 guiding principles every BA should know.
- Leemans, Fahland, van der Aalst, "Discovering Block-Structured Process
  Models from Event Logs" (2013) — Inductive Miner foundational paper.
- Weijters, van der Aalst, "Rediscovering Workflow Models from
  Event-Based Data using Little Thumb" (2003) — Heuristic Miner.
- `pm4py` documentation: https://pm4py.fit.fraunhofer.de/documentation
- IEEE XES standard: https://www.xes-standard.org/
- Sibling agent-integration:
  `pro/ba/business-analyst/process-mining-automation/agent-integration.md`
  — operational 4-stage pipeline.
