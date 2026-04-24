# Agent Integration — Strategy Analysis

> Strategy Analysis is BABOK Knowledge Area 6: business need → current state →
> future state → gap analysis → change strategy. This file covers how a BA
> drives that arc with subagents, where it fails, and which tools the agents
> can actually call. Sibling: `requirements-lifecycle/agent-integration.md`
> picks up *after* the change strategy is signed off; `decision-analysis`
> handles the option-selection step inside change strategy.

## When to use

- A new initiative is starting and a sponsor has handed the BA a vague mandate ("we need to fix customer service") — you need a defensible problem frame before any solution is proposed.
- Annual / quarterly portfolio planning, where N candidate initiatives compete for the same budget and each needs a one-pager linking to a strategic goal, gap, and capability.
- Pre-RFP / pre-business-case work where the change strategy will gate a 7-figure spend; auditors and the steering committee will demand traceability from need to spend.
- Digital transformation programs where current-state assessment must cover process + tech + people + data simultaneously (the README's six-area inventory).
- M&A integration: the acquired entity's current state vs. the post-merger future state, with a gap analysis driving Day-1 / Day-100 / Day-365 plans.
- Regulatory-driven change (SOX, GDPR, DORA, NIS2): the regulator defines the future state externally, the BA must produce the gap and change strategy.
- After a strategy refresh by leadership: each function translates the new corporate strategy into its own future-state and gap, and the BA agents help pull the workstreams onto a shared template.

## When NOT to use

- The "decision" is single-team, single-quarter, low-blast-radius work — a 5-line ADR + a backlog item beats a strategy artifact.
- The future state is already locked by an executive who is not interested in alternatives — the BA producing a "strategy analysis" becomes theatre. Document it as a directive instead.
- Pure incident response / outage post-mortems — those use root-cause analysis, not future-state-vs-current-state framing.
- Early-stage product discovery where customer pain is unproven; using strategy analysis there hardens premature assumptions. Use opportunity-solution-trees / `jobs-to-be-done` / `lean-canvas` first, then strategy analysis once the opportunity is validated.
- Pure financial decisions with directly comparable cash flows — go to NPV / IRR; don't dress them as strategy analysis.
- Operational hot-fixes with a known cause and known patch — overhead exceeds value.

## Where it fails / limitations

- **Solution dressed as need.** The "business need" arrives as "we need a new CRM"; the BA dutifully writes a future state assuming the CRM. The agent must reject solution-shaped need statements (#1 mistake in README) and re-elicit.
- **Current state by anecdote.** Process + tech + people + data inventories are filled by interviewing whoever happened to attend the workshop; whole departments are missing. Without a stakeholder coverage matrix the current state is fiction.
- **Future state as fantasy.** Aspirations get coded as future state ("zero defects", "100% automated"); when the gap is measured, every gap is huge and prioritization collapses. Future state must be falsifiable and time-boxed.
- **Strategic alignment as box-ticking.** Each initiative claims it supports goal G1; nobody checks. Without explicit `traces_to: [GOAL-XXX]` plus a corporate-strategy doc the trace is decorative.
- **Gap analysis without measurement.** Gaps are recorded as prose ("our reporting is slow") instead of measured deltas ("monthly close 9 business days vs. target 3"). Un-measured gaps cannot be prioritized.
- **Change strategy as a single option.** "Build it ourselves" appears as the only path; buy / partner / status-quo / phased never get evaluated. README mandates options — agents skip this when rushed.
- **No status-quo / do-nothing baseline.** Without it, leadership cannot see the cost of inaction; the strategy reads as advocacy.
- **PESTLE / SWOT as weather report.** External-factor analysis lists generic items ("AI is rising") with no link to the org's specific exposure; output gets ignored.
- **Strategy drift after sign-off.** Six months in, scope mutates and the strategy document is never re-opened. Without a change log + quarterly review the rationale rots.
- **Strategy analysis becomes the project.** Months of frame-current-future-gap iteration with no commitment; analysis-paralysis. Time-box every phase; publish v0.1 in days not weeks.

## Agentic workflow

The BA owns *framing* and *judgment*; agents own *coverage*, *traceability*, and *artifact production*. Drive a strategy analysis in five phases.

1. **Frame the business need.** sonnet `need-frame-agent` reads sponsor briefs / steering minutes / strategic-plan docs and emits the JSON need: `{need_statement, drivers[], consequence_of_inaction, decision_maker, time_horizon, ambiguities[]}`. Reject solution-shaped statements; flag missing decision_maker.
2. **Current-state coverage pass.** opus `current-state-agent` walks the six README areas (process, org, tech, people, data, external) and asks per area: *who owns it, what evidence exists, who has not yet been interviewed*. Output is a coverage matrix + a backlog of elicitation gaps. Pair with `pestle-agent` and `swot-agent` for external/internal scans, each citing primary sources.
3. **Future-state definition with measurability gate.** opus `future-state-agent` proposes vision + measurable goals + capability map. A second `future-state-validator` agent rejects any goal without a metric, baseline, target, and target-date. The BA convenes one workshop to lock the future state before gap analysis starts.
4. **Gap analysis with priority + measure.** sonnet `gap-agent` joins current and future state per area; each gap row is `{area, current_metric, future_metric, gap_size, gap_unit, priority_h_m_l, evidence_url}`. Gaps without metrics are flagged for re-elicitation. A `dependency-agent` builds the gap dependency DAG (which gap blocks which) so prioritization is not popularity-weighted.
5. **Change strategy with N≥3 options + status-quo.** opus `change-strategy-agent` generates build / buy / partner / modify / status-quo options against the gap-priority map, each with a cost / time / risk / capability profile. `faion-brainstorm` runs a divergence pass first so the option set is not just the three obvious ones. The BA hands the option set to `decision-analysis` (sibling methodology) for weighted-matrix selection. Final memo + sign-off + commit to `.aidocs/`.

Human-in-the-loop checkpoints: (a) need statement signed by sponsor; (b) future state locked by exec sponsor; (c) change strategy recommendation signed by decision-maker; (d) 90-day post-decision review where the BA + `faion-improver` compare predicted gaps closed vs. actual.

### Recommended subagents

- `faion-brainstorm` — divergence pass on options; without it the change strategy collapses to the three vendors who replied loudest. Most common skip.
- `faion-sdd-executor-agent` — once the change strategy is signed, generates the SDD task tree (constitution → spec → design → implementation-plan) inside `.aidocs/backlog/` for the chosen path.
- `faion-feature-executor` — executes the discrete tasks from the chosen change strategy; each task carries `strategy_id` for traceability back to the gap and need.
- `faion-improver` — quarterly meta-loop: reads strategy analyses signed off 6–12 months ago, compares predicted vs. actual gap closure, and updates `.aidocs/memory/patterns.md` + `mistakes.md` with calibration patterns.
- A custom `need-frame-agent` (sonnet) — emits the `{need_statement, drivers, consequence, decision_maker, time_horizon}` JSON; refuses solution-shaped statements.
- A custom `current-state-agent` (opus) — walks the six README areas; outputs a coverage matrix and elicitation gap backlog.
- A custom `pestle-agent` (sonnet) — six-axis scan with primary-source citations stamped `retrieved_at`.
- A custom `swot-agent` (sonnet) — internal/external 2×2 with each cell carrying evidence URLs and a confidence score.
- A custom `future-state-agent` (opus) — proposes goals; paired `future-state-validator` rejects unmeasurable goals.
- A custom `gap-agent` (sonnet) — joins current/future per area; flags gaps lacking metrics; emits dependency DAG via `dependency-agent`.
- A custom `change-strategy-agent` (opus) — option generation with cost/time/risk/capability profile; hands off to `decision-analysis` matrix.
- `password-scrubber-agent` (in repo) — runs over every artifact before it is committed to `.aidocs/`; strategy docs commonly leak vendor pricing or staff names.

### Prompt pattern

Need framing (run on raw sponsor docs):

```
You are a BA strategy-analysis need-framer. Input: sponsor brief, steering
minutes, exec memos. Output strict JSON:
{
  need_statement: "<= 30 words, outcome-shaped (NOT solution-shaped)",
  drivers: [{driver, source_quote, source_doc}],
  consequence_of_inaction: "<= 30 words, falsifiable",
  decision_maker: {name, role} | null,
  time_horizon: "Q|Y|multi-year",
  strategic_goals_referenced: [GOAL-XXX...],
  ambiguities: [<= 5 items]
}
Rules:
- Reject solution-shaped need ("we need a new CRM"). Re-cast as outcome
  ("we need to reduce time-to-resolution from 8h to 2h") or return an
  ambiguity flag.
- Every driver cites a verbatim source_quote. No driver without evidence.
- If no GOAL-XXX trace exists, flag and DO NOT invent IDs.
```

Future-state validator (run after `future-state-agent`):

```
You are the future-state validator. For each proposed goal:
{
  goal, metric, baseline, baseline_source, target,
  target_unit, target_date, capability_required,
  measurability_check: "pass" | "fail",
  failure_reason: null | "no_metric" | "no_baseline" | "no_target_date"
                   | "not_falsifiable" | "solution_shaped"
}
Refuse to retain any goal whose measurability_check = "fail" unless the BA
passes force=true. If the goal is solution-shaped ("implement chatbot"),
recast as outcome ("self-serve resolution rate >= 40%").
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `claude` CLI | Drive frame / current-state / future-state / gap / strategy passes against a JSON state file | https://docs.anthropic.com/en/docs/claude-code |
| `pandoc` | Render the locked strategy doc to PDF / DOCX for sponsor sign-off | `apt install pandoc` |
| `mermaid-cli` | Render current-state → future-state state diagrams + gap dependency DAG | `npm i -g @mermaid-js/mermaid-cli` |
| `yq` + `jq` | Read/write strategy state stored as YAML/JSON alongside the markdown memo | `apt install yq jq` |
| `gh` | Pull issues / repos / org metadata as evidence for capability-mapping | https://cli.github.com |
| `git` + Conventional Commits | Each strategy revision is a commit; `git log` is the rationale audit trail | preinstalled |
| `pulp` (Python) | Linear programming when budget / capability constraints turn change-strategy options into hard constraints | `pip install pulp` |
| `pandas` + `numpy` | Aggregate current-state metrics; compute gap deltas; export prioritization tables | `pip install pandas numpy` |
| `streamlit` | Live future-state / gap workshop UI; change a target, see new gap | https://streamlit.io |
| `graphviz` (`dot`) | Capability map + gap dependency DAG when mermaid scaling breaks | `apt install graphviz` |
| `papermill` | Parametrize a "strategy-analysis.ipynb" template across N initiatives in portfolio planning | `pip install papermill` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| LeanIX | SaaS (EA) | Yes (REST) | Capability + tech map for current-state inventory; agents read application portfolio |
| Ardoq | SaaS (EA) | Yes (REST) | Strategy-to-capability traceability; lighter than LeanIX |
| Bizzdesign Horizzon | SaaS (EA, ArchiMate) | Limited | Heavyweight EA tool; useful when current state must be modeled in ArchiMate |
| Avolution ABACUS | SaaS (EA) | REST | Multi-criteria scoring of change-strategy options inside the EA model |
| Confluence | SaaS / Server | Yes (REST) | Default home for the locked strategy doc in regulated enterprises |
| Notion | SaaS | Yes (REST) | Lightweight portfolio of strategy-analysis pages; agents draft + embed gap tables |
| Airtable | SaaS | Yes (REST) | Cheap intake for stakeholder-by-area current-state evidence |
| Jira / Linear | SaaS | Yes (REST/GraphQL) | One epic per gap; status moves as gap closes; agents update via API |
| Polarion ALM / Jama | SaaS / on-prem | REST | When the strategy must trace to managed requirements (regulated industries) |
| Smartsheet | SaaS | REST | Non-IT stakeholders' default; agents update via API |
| AnswerThePublic / SimilarWeb / SEMrush | SaaS | Limited | External-factor evidence for PESTLE (T = tech trends, E = economic) |
| Crunchbase / PitchBook | SaaS | REST | Competitor / market evidence in PESTLE + future-state benchmarking |
| Statista / OECD.Stat | SaaS / Open | Yes (CSV) | Macroeconomic baselines for PESTLE-E and target-setting |
| miro / mural | SaaS | Limited (REST partial) | Live SWOT / capability mapping workshops; agents pre-seed the board |
| Streamlit / Hex / Mode | SaaS / OSS | Yes | Workshop-grade re-rank UI when sponsors change targets in real time |

## Templates & scripts

The README ships Business Need Statement, Gap Analysis, and Change Strategy templates plus SWOT / gap examples. This file adds a missing piece: a *future-state measurability validator* — strategy analyses fail most often because future-state goals were never measurable.

```python
# future_state_validator.py — gate goals on metric / baseline / target / date.
# Usage: python future_state_validator.py future_state.yaml
import sys, yaml, datetime as dt

REQUIRED = ("metric", "baseline", "target", "target_date")
OUT = []
data = yaml.safe_load(open(sys.argv[1]))
for g in data.get("goals", []):
    missing = [k for k in REQUIRED if not g.get(k)]
    today = dt.date.today()
    fail = []
    if missing:
        fail.append("missing:" + ",".join(missing))
    td = g.get("target_date")
    if td:
        try:
            d = dt.date.fromisoformat(str(td))
            if d <= today:
                fail.append("target_date_in_past")
            if (d - today).days > 365 * 3:
                fail.append("target_date_>_3y_unfalsifiable")
        except ValueError:
            fail.append("target_date_not_iso")
    if any(w in str(g.get("goal", "")).lower()
           for w in ("implement", "deploy", "build", "buy", "migrate")):
        fail.append("solution_shaped_goal")
    OUT.append({"goal": g.get("goal"), "fail": fail or None})

print(yaml.safe_dump({"validation": OUT}, sort_keys=False))
sys.exit(1 if any(r["fail"] for r in OUT) else 0)
```

Wire this as a pre-commit hook on the strategy doc: any goal failing the gate blocks the commit. Pair with the README's Gap Analysis Template; gaps automatically inherit their metric from validated future-state goals (no metric on the goal → no metric on the gap → no priority, by construction).

## Best practices

- **Reject solution-shaped need statements at the door.** "We need a new CRM" is not a need; "we need to reduce time-to-resolution from 8h to 2h" is. The frame agent must refuse the former.
- **Six-area current-state inventory, every time.** Process / org / tech / people / data / external. Skipping any one is the most reliable failure mode of strategy analysis.
- **Stakeholder coverage matrix before current-state sign-off.** Rows = areas, columns = stakeholder roles, cells = "interviewed yes/no, evidence link". Empty rows block sign-off.
- **Future-state goals must be falsifiable.** Each goal carries metric, baseline, baseline source, target, unit, and target date. Aspirations without metrics get rejected.
- **PESTLE/SWOT cells cite primary sources stamped `retrieved_at`.** Generic prose is rejected; agents will produce it by default.
- **Measure every gap.** No gap without a numeric delta. Un-measured gaps cannot be prioritized and become political.
- **Always score the status-quo option.** Doing nothing is option zero in the change strategy; without it, the doc is advocacy.
- **Cap change-strategy options at 5 + status-quo.** More than 5 collapses into noise; fewer than 3 is a coronation.
- **Trace every goal up to a corporate goal and every gap down to a goal.** `traces_to: [GOAL-XXX]` on goals; `traces_to: [GOAL-XXX]` on gaps; agents validate against the corporate-strategy doc.
- **Time-box phases.** Frame ≤ 1 week; current-state ≤ 2 weeks; future-state ≤ 1 week; gap ≤ 1 week; strategy ≤ 1 week. Past those, the BA escalates.
- **Pre-mortem the recommendation.** "In 12 months we regret picking this — why?" — answers feed the Risks section before sign-off, not after.
- **Schedule a 90-day and 365-day review.** Compare predicted gaps closed vs. actual; log calibration error in `.aidocs/memory/patterns.md`. This is what turns the document into a learning loop.
- **Sign every revision.** Need, future state, change strategy each carry `signed_by`, `signed_at`. Without signatures, the doc is a draft and downstream commitments are fragile.

## AI-agent gotchas

- **Solution-shaped output by default.** LLMs love proposing solutions; they will fill in "we should adopt X" given any need. The frame and future-state agents must be hard-prompted to refuse solutions and explicitly produce outcomes.
- **Generic PESTLE / SWOT.** Agents emit "AI is disrupting industries" cells with no link to the org's specific exposure. Force per-cell `relevance_to_us` field with concrete impact.
- **Hallucinated GOAL-XXX / REQ-XXX traces.** Agents fabricate IDs that look plausible. Validate every trace against the actual `.aidocs/` strategy + requirements catalog with `git grep` before persisting.
- **Hallucinated stakeholders.** Given a sparse brief, agents invent "Sarah from Operations". Pass the actual stakeholder list as input; reject any rater the agent invents.
- **Future-state copying current-state with adjectives.** "Faster", "better", "more integrated" — no metric, no baseline, no date. The validator script rejects these by construction.
- **Gap analysis as prose.** Agents produce paragraphs; you need a structured table. Force schema: `{area, current_metric, current_value, future_metric, future_value, gap, gap_unit, priority, evidence_url}` per row; reject prose.
- **Date-stale evidence.** Tech-landscape and PESTLE evidence go stale fast. Stamp `retrieved_at` on every cell; refuse evidence > 90 days without re-fetching.
- **Order bias on options.** Whichever change-strategy option is mentioned first or last gets favored in the agent's narrative. Randomize option order in every prompt.
- **Cluster around 3 / cluster around H.** Agents regress to the median when scoring gap priority; calibrate by forcing percentile rank ("of these 12 gaps, this is in the worst quartile") instead of free H/M/L.
- **Bulk transitions are dangerous.** A runaway agent that re-writes 30 gap rows is hard to undo. Cap any agent action to N rows per run; require human review on the diff.
- **Wrong-agent invocation.** A `feature-executor` should never *make* a strategy decision; it should fail-closed and ping the BA. Only `change-strategy-agent` produces option sets; only `decision-analysis` selects; only the human signs.
- **Prompt-injected vendor copy.** When PESTLE / current-state evidence is pulled from vendor websites, vendors can plant favorable framing. Strip suspicious instructions; prefer primary sources (filings, regulator publications, the org's own telemetry).
- **Mandatory human checkpoints.** Need statement (sponsor signs), future state (exec sponsor signs), change strategy recommendation (decision-maker signs), 90-day calibration (BA + `faion-improver`). Agents prepare; humans sign.

## References

- IIBA — *BABOK Guide v3*, Knowledge Area 6 *Strategy Analysis* (§6.1–6.4: Analyze Current State, Define Future State, Assess Risks, Define Change Strategy).
- Kaplan & Norton — *The Strategy-Focused Organization* + *Strategy Maps* (current/future-state and capability mapping discipline).
- Porter — *Competitive Strategy* (five-forces; feeds PESTLE-C and current-state external scan).
- Rumelt — *Good Strategy / Bad Strategy* (kernel: diagnosis → guiding policy → coherent action; canonical antidote to fluff future states).
- Christensen — *The Innovator's Dilemma* (when to disrupt vs. sustain; informs build/buy/partner choice in change strategy).
- Treacy & Wiersema — *The Discipline of Market Leaders* (operational excellence / product leadership / customer intimacy archetypes for future-state framing).
- Hammond, Keeney, Raiffa — *Smart Choices* (decision quality discipline; pairs with the `decision-analysis` sibling).
- ISO/IEC/IEEE 29148:2018 Requirements Engineering (criteria/goal traceability discipline).
- The Open Group — *TOGAF ADM* phases A–B (Architecture Vision, Business Architecture) — alternative current/future-state framing for EA-heavy orgs.
- ArchiMate 3.x — modeling language for current/future-state when LeanIX / Bizzdesign / Ardoq is in use.
- Sibling: `pro/ba/business-analyst/decision-analysis/agent-integration.md` — option-selection step inside change strategy.
- Sibling: `pro/ba/business-analyst/requirements-lifecycle/agent-integration.md` — picks up after change strategy sign-off.
- Sibling: `pro/ba/business-analyst/stakeholder-analysis/agent-integration.md` — feeds the current-state coverage matrix.
- Sibling: `pro/ba/business-analyst/business-process-analysis/agent-integration.md` — depth on the process axis of the six-area inventory.
