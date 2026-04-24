# Agent Integration — Business Process Analysis

Methodology covers the BPMN-flavored 5-stage analysis cycle (identify → document current → analyze → design future → validate) for understanding how work actually flows. In an agentic setup the flow becomes: ingest evidence (logs, SOPs, transcripts) → emit a structured process model (BPMN XML or DSL) → run quantitative analysis (value/time/cost) → propose future-state diff → hand off to SDD/PM for implementation. Most of the leverage is in the first two stages because LLMs are weak at *discovering* steps but strong at *normalizing* them once raw evidence is collected.

## When to use

- You have raw process evidence (SOP docs, Slack threads, ticket histories, support transcripts, screen recordings) and need a single normalized model before redesign.
- A cross-team workflow shows symptoms of waste (rework loops, long approval queues, dual data entry) and you need a numbers-backed case for change.
- Pre-automation discovery: before writing an n8n workflow, RPA bot, or backend service that replaces a manual process — model the as-is so you don't pave the cowpath.
- Pre-spec stage of a BA-heavy SDD feature: the methodology output (`process-documentation.md` + `process-analysis.md`) becomes input to `requirements-documentation` and `acceptance-criteria`.
- Compliance / audit prep where regulators expect a documented process map with controls and exception handling.

## When NOT to use

- Greenfield product where no current process exists — jump straight to `use-case-modeling` or `user-story-mapping`.
- One-off troubleshooting of a single broken instance — use root-cause-analysis tooling (`5-whys`, fishbone), not full BPA.
- Tactical UI tweaks where the "process" is one click — overhead exceeds benefit.
- Highly creative or knowledge-work flows (R&D, design, writing) where steps are non-deterministic — process mining returns spaghetti diagrams without insight.
- When the team is already mid-redesign and stakeholders have agreed on the future state — re-modelling the as-is delays delivery without changing the outcome.
- Real-time decision making — BPA is slow analysis, not an operational dashboard.

## Where it fails / limitations

- **Ideal-vs-actual gap.** README warns about "documenting the ideal" — LLMs amplify this by smoothing over messy interview transcripts into a tidy linear diagram. Workarounds (the actual value) get edited out.
- **No native BPMN renderer.** The methodology shows arrow-art examples but produces no machine-readable artifact. Without BPMN 2.0 XML you cannot diff, validate, or feed downstream tools (Camunda, Signavio).
- **Value-classification subjectivity.** VA / BN / NVA labels swing with prompt wording; two runs on the same step list disagree in ~20-30% of rows. Needs a rubric or human review.
- **Metrics fabrication.** "Cycle time" and "error rate" tables in the templates invite hallucinated numbers when no data source is supplied. Hard rule: blank or "Data not available" if source absent.
- **Single-pool bias.** README's flow examples are linear; multi-actor swimlanes (typical for B2B processes spanning Sales/Ops/Finance) need extra prompting or the LLM collapses lanes.
- **Future-state hand-waving.** "Auto-approve orders < $1000" is easy to write, hard to scope. Without an explicit "what changes in which system" column, future-state diagrams are unactionable.
- **Improvement pattern overuse.** LLMs default to "automate" for everything; eliminate/simplify (cheaper, faster wins) get under-recommended.
- **Not for event-driven systems.** BPMN sequence flows model deterministic step-by-step work; event-heavy async systems (queues, webhooks, sagas) need event storming or BPMN choreography, not basic process flows.

## Agentic workflow

Run as a 5-stage state machine, one stage per subagent invocation, persisting artifacts between stages so a long session can be resumed. Stage 1 (identify) and stage 2 (document) are evidence-bound — supply raw inputs (interview transcripts, SOP docs, ticket exports) and require the agent to cite source spans. Stage 3 (analyze) is computational — emit tables with formulas, not narrative. Stage 4 (design future) is generative — explicitly score each proposed change against effort/benefit. Stage 5 (validate) is human-in-the-loop — the agent prepares a review packet, a human approves or sends back. Use `faion-ba-agent` (per README front matter) as the orchestrator; delegate process-mining work to a Python subagent that drives `pm4py`.

### Recommended subagents

- `faion-ba-agent` — Orchestrator declared in this methodology's README front matter. Owns the 5-stage state machine and writes `process-documentation.md` / `process-analysis.md` to `.aidocs/`.
- `faion-software-architect` — Consumes future-state model and produces system-level design (which integration eliminates step 4? which queue replaces step 5?).
- `faion-sdd-executor-agent` — Downstream: turns approved future-state into spec → design → tasks (this repo ships `agents/faion-sdd-executor-agent.md`).
- `faion-research-agent` — Upstream when no SOP exists: mine industry reference processes (APQC PCF, eTOM) before interviewing.
- General-purpose `Task` subagent for process mining — Pass it `pm4py` + an event log CSV; it returns a discovered DFG/BPMN.
- `password-scrubber-agent` — Run on raw transcripts/logs *before* feeding to any other agent; SOPs and ticket exports routinely contain credentials.

### Prompt pattern

Stage 2 (document current state) dispatch:

```
Read evidence files: [<paths>]. Build the as-is model for "<process-name>".
Output a single BPMN-DSL block followed by the README "Process Documentation Template".
For every step row, cite the source line/file in the Notes column.
If a step is mentioned by only one source, mark Notes with "single-source — verify".
Do NOT smooth over contradictions; emit a `## Contradictions` section listing them verbatim.
```

Stage 3 (analyze) dispatch:

```
Input: process-documentation.md.
Produce process-analysis.md per the README template.
Rubric for VA/BN/NVA: VA = customer would pay for this step; BN = required by law/policy/system but no customer value; NVA = waiting, rework, transport, duplicate entry.
For Cycle time and Error rate: use only numbers cited in the input. If absent, write "Data not available" — do not estimate.
End with a `Top-3 candidates for elimination` block ranked by NVA-time × frequency.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `pm4py` | Process mining: discover BPMN/DFG from event logs, conformance check | `pip install pm4py` / https://pm4py.fit.fraunhofer.de |
| `bpmn-js` (CLI via `bpmn-to-image`) | Render BPMN XML to SVG/PNG for review packets | `npm i -g bpmn-to-image` / https://github.com/bpmn-io/bpmn-js |
| `mermaid-cli` (`mmdc`) | Quick flowcharts when full BPMN is overkill | `npm i -g @mermaid-js/mermaid-cli` |
| `graphviz` (`dot`) | Render DFG output from `pm4py` | `apt install graphviz` |
| `pandas` | Event log cleanup, throughput analysis, value-add roll-ups | `pip install pandas` |
| `python-docx` / `pdfplumber` | Extract steps from existing SOP Word/PDF docs | `pip install python-docx pdfplumber` |
| `whisper` / `whisper.cpp` | Transcribe stakeholder interviews into evidence text | https://github.com/openai/whisper |
| `jq` | Slice JSON event logs from APIs (Jira, Zendesk, GitHub) | `apt install jq` |
| `csvkit` (`csvgrep`, `csvstat`) | Inspect raw event logs before feeding to `pm4py` | `pip install csvkit` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Camunda 8 / Camunda Modeler | OSS + SaaS | Yes — REST API, Operate API | Open-standard BPMN 2.0; agents can deploy and query running process instances |
| Signavio (SAP) | SaaS | Partially — REST API, paid | Enterprise-grade modeling; expensive but deep value-stream analytics |
| Bizagi Modeler | SaaS + free desktop | Limited — desktop-first | Good free modeler; weak API |
| Lucidchart | SaaS | Partially — REST API | Easy collaboration; export BPMN XML for downstream tooling |
| draw.io / diagrams.net | OSS, free SaaS | Yes — read/write `.drawio` XML | Cheap rendering; no execution semantics |
| Celonis | SaaS (process mining) | Yes — REST API, Studio APIs | Industry leader for log-based discovery; pricey |
| ProcessGold (UiPath Process Mining) | SaaS | Yes — APIs | Tied to UiPath RPA stack |
| Apromore | OSS + SaaS | Yes — REST | Open process mining; pairs well with `pm4py` |
| Disco (Fluxicon) | Desktop | No (desktop) | Strong DFG generator for one-off analyses |
| n8n (this workspace) | OSS, self-hosted | Yes — REST | Implement future-state automation; node-graph maps cleanly to BPMN tasks |
| Zapier / Make | SaaS | Yes — REST | Quick automation of NVA steps without backend changes |
| Jira / Linear / Asana | SaaS | Yes — REST | Source of event logs for ticket-driven processes |
| Zendesk / Intercom | SaaS | Yes — REST | Event logs for support processes |
| Salesforce Flow + Event Monitoring | SaaS | Yes — Bulk API + EM | Source of event logs for sales/service processes |
| GitHub / GitLab | SaaS | Yes — REST | Event logs for engineering/release processes |

## Templates & scripts

The methodology's README ships `Process Documentation` and `Process Analysis` templates inline; reuse them. The siblings `templates.md`, `examples.md`, `checklist.md`, `llm-prompts.md` are placeholders (1 line each) — do not rely on them.

Inline: minimal event-log → DFG discovery (≤50 lines Python) for stage 2 evidence:

```python
#!/usr/bin/env python3
"""
discover_dfg.py  events.csv  --case-col case_id --act-col activity --ts-col timestamp
Outputs:
  out/dfg.svg          directly-follows graph
  out/stats.csv        per-activity frequency, mean duration
"""
import argparse, os
import pandas as pd
import pm4py
from pm4py.algo.discovery.dfg import algorithm as dfg_algo
from pm4py.visualization.dfg import visualizer as dfg_vis

p = argparse.ArgumentParser()
p.add_argument("csv")
p.add_argument("--case-col", default="case_id")
p.add_argument("--act-col",  default="activity")
p.add_argument("--ts-col",   default="timestamp")
p.add_argument("--out",      default="out")
a = p.parse_args()

os.makedirs(a.out, exist_ok=True)
df = pd.read_csv(a.csv, parse_dates=[a.ts_col])
log = pm4py.format_dataframe(
    df, case_id=a.case_col, activity_key=a.act_col, timestamp_key=a.ts_col
)
dfg = dfg_algo.apply(log)
gviz = dfg_vis.apply(dfg, log=log, variant=dfg_vis.Variants.FREQUENCY)
dfg_vis.save(gviz, f"{a.out}/dfg.svg")

stats = (
    df.groupby(a.act_col)
      .agg(count=(a.case_col, "size"))
      .sort_values("count", ascending=False)
)
stats.to_csv(f"{a.out}/stats.csv")
print(f"wrote {a.out}/dfg.svg, {a.out}/stats.csv")
```

Workflow state file (drop into `.aidocs/<feature>/_bpa-state.json`):

```json
{
  "process": "<name>",
  "stages": ["identify", "document", "analyze", "design", "validate"],
  "completed": [],
  "artifacts": {
    "evidence": [],
    "current_state": null,
    "analysis": null,
    "future_state": null
  },
  "metrics_source": "<jira|zendesk|salesforce|manual>"
}
```

## Best practices

- **Demand evidence per step.** Every row of the Process Steps table must cite a source span (file + line, ticket ID, transcript timestamp). No citation → row marked `unverified`, blocked from analysis.
- **Separate the "happy path" from exceptions.** README's flow example merges them. Force two diagrams: one nominal flow + one exception map keyed by trigger event.
- **Quantify before redesigning.** Future-state has no value if current-state metrics are missing. If volume/cycle/cost data is unavailable, run a 2-week sample first.
- **VA/BN/NVA rubric pinned in the prompt.** Without it, classifications drift. Pin examples (3 per category) and require the agent to compare each step against the examples.
- **Frequency-weight the improvements.** A 10-min NVA step that runs 1000×/day beats a 2-hour NVA step that runs once/quarter. Always rank by `nva_minutes × frequency`.
- **Walk the process physically.** When evidence is mostly transcripts, schedule a Gemba-walk session and record screen-share video; transcribe with `whisper` and re-run stage 2.
- **Diff future-vs-current as a table, not prose.** Columns: `step | current actor | future actor | current system | future system | change type | risk`. Forces specificity.
- **Validate against process mining.** If you have event logs, run `pm4py` to discover the DFG and compare to the manually-built BPMN. Discrepancies = workarounds you missed.
- **Keep BPMN in source control.** Store BPMN XML alongside `process-documentation.md` so diffs are reviewable in PRs.
- **Hand off via spec, not diagram.** The output that matters downstream is `requirements-documentation.md` derived from the future-state — diagrams are review aids, not a contract.

## AI-agent gotchas

- **Linear-flow bias.** LLMs collapse parallel branches into sequential steps. Pre-prompt with: "Identify all gateways (XOR/OR/AND); never default to a linear flow."
- **Lost actors.** Single-pool diagrams lose handoffs. Force a swimlane requirement: every step must have an `actor` column; if blank → reject the row.
- **Hallucinated systems.** Agent invents "ERP" or "CRM" generically. Constrain: "Use only system names that appear verbatim in the evidence."
- **Soft metrics.** Without a hard rule the agent fills cycle-time cells with "30 min (estimated)". Hard-block: "If a metric is not directly cited, write `Data not available`."
- **VA/BN/NVA drift between runs.** Same input, different labels on re-run. Mitigate with a fixed rubric + temperature 0 + a determinism check (run twice, compare, escalate diffs).
- **Future-state shopping list.** Agent emits 30 improvements with no prioritization. Cap at 5 + require effort/benefit scores.
- **Workaround erasure.** Stakeholder says "we email Jane because the system is broken" — the agent rewrites this as "data is transferred to Jane". Force verbatim quotes for any anomaly.
- **PII / credential leak.** SOPs and tickets often contain customer data, API keys, internal URLs. Run `password-scrubber-agent` on raw evidence before passing to any LLM tool.
- **BPMN dialect mismatch.** Output looks like BPMN but isn't valid 2.0 XML; downstream Camunda import fails. Always validate with `pm4py.write_bpmn()` or `bpmn-validate`.
- **Loop-mining false positives.** `pm4py` discovers loops where the real process has retries on transient errors. Filter event logs by terminal states before mining.
- **Token blow-up at synthesis.** A 200-step retail process exceeds context. Chunk by sub-process (one BPMN call activity per chunk) and stitch in a final orchestrator pass.
- **Cron-mode interactivity.** The "Validate with stakeholders" stage requires humans. In headless mode, freeze the workflow at stage 4 and emit a review packet — never auto-advance.

## References

- BABOK Guide v3 — Knowledge Area: Requirements Analysis and Design Definition (KA 7), Techniques: Process Modelling (10.35), Process Analysis (10.34)
- BPMN 2.0 specification — https://www.omg.org/spec/BPMN/2.0/
- Process Mining Manifesto (van der Aalst et al.) — https://www.tf-pm.org/resources/manifesto
- `pm4py` documentation — https://pm4py.fit.fraunhofer.de/documentation
- Camunda Modeler + BPMN element reference — https://docs.camunda.io/docs/components/modeler/bpmn/bpmn-coverage/
- APQC Process Classification Framework (PCF) — https://www.apqc.org/process-frameworks
- Sibling methodology: `../use-case-modeling/README.md` (downstream when process triggers user-system interactions)
- Sibling methodology: `../data-analysis/README.md` (downstream when process redesign requires data model changes)
- Sibling methodology: `../acceptance-criteria/README.md` (downstream for future-state validation)
- This repo's BA orchestrator: `agents/faion-sdd-executor-agent.md`
