# Agent Integration — BA Strategy Basics (Current/Future State & Risk)

## When to use
- Pre-project framing: a stakeholder asks for a "transformation" / "modernization" / "platform migration" and you need a structured current-vs-future state delta before writing a spec.
- Annual or quarterly portfolio planning where multiple change initiatives compete for the same budget and you need a comparable change-strategy document for each.
- After a strategic shift (new CEO, M&A, regulatory change) when previously documented capabilities and gaps must be re-baselined.
- When an SDD `spec.md` is being drafted but the "why now / what's the gap" section is empty — strategy-basics is the upstream artifact that feeds it.
- Vendor/COTS vs. build decisions where you need an explicit gap analysis + solution-options table to defend the choice.
- Investor or board update where capability maturity (1–5) and a roadmap delta are expected as standard slides.

## When NOT to use
- Tactical bug fixes, sprint stories, or single-feature work — overhead exceeds value; use a normal ticket.
- Pure-discovery phase (problem still unproven) — the framework assumes the problem is real and the question is "how do we close the gap"; do problem validation first (`pro/research/user-researcher/problem-validation/`).
- Solo founder, <10-person company, single product line — capability-maturity tables are theatre at that scale; collapse to a one-page SWOT + risk list.
- The change is mandated and non-negotiable (regulatory deadline, vendor end-of-life) — skip "solution options" pretense and go straight to transition planning.
- When stakeholders will not commit to a future-state vision in writing — without that anchor, the gap analysis is fiction.

## Where it fails / limitations
- **Maturity score inflation.** Self-assessed 1–5 capability levels are systematically over-rated by the team that owns the capability. Without an outside reviewer the current state is wrong.
- **Future state as wish list.** Goals/KPIs in templates default to "improve X by 20%" with no baseline measurement plan; the future state becomes uncalibrated.
- **SWOT as filler.** The 2×2 SWOT table in this methodology has the lowest signal-per-cell of any artifact here; teams produce 4 vague bullets and call it strategy. Either drop it or force evidence per cell.
- **Risk register decoupled from gaps.** The `Risk Register` and the `Gap Analysis` live in two tables that never reference each other; in practice, top gaps drive top risks.
- **Build vs. buy table without numbers.** "Pros / Cons / Est. Cost" defaults to qualitative bullets. Without TCO + switching-cost numbers, the recommendation is opinion.
- **Static document, dynamic reality.** Strategy docs age in weeks, not quarters. No version-diff discipline → re-baselining becomes a from-scratch rewrite each time.
- **Assumes single decision-maker.** The framework outputs one recommendation; large orgs need scenario branches (best/worst/expected case) which the templates don't support.

## Agentic workflow
Drive strategy-basics as a **four-phase pipeline** mapping 1:1 to the four sections of the README. Phase 1 (current state) is research-heavy and parallelizable: a researcher subagent pulls public data + internal docs, a process-mining/data-analysis agent produces capability scores from telemetry rather than self-report. Phase 2 (future state) is brainstorm-heavy: run `faion-brainstorm` diverge-converge to propose 3–5 future-state variants, then converge to one. Phase 3 (risk) reuses the `pro/research/researcher/risk-assessment/` pipeline (already enriched with `agent-integration.md`); pre-mortem agents are mandatory. Phase 4 (change strategy) is a synthesis pass that emits the gap analysis + solution options + transition roadmap and hands those off to `faion-sdd-executor-agent` to spawn `backlog/` features. Persist each phase output under `.aidocs/strategy/<initiative-slug>/{current,future,risks,strategy}.md` so each rerun produces a diff, not a rewrite.

### Recommended subagents
- `faion-research-agent` (`skills/faion/knowledge/pro/research/researcher/`) — runs `market` + `competitors` modes to populate the `Threats` and `Opportunities` cells of the SWOT with cited evidence instead of opinion.
- `faion-market-researcher-agent` (referenced from researcher skill) — sizes the Opportunity column with TAM/SAM/SOM numbers; without those, future-state goals are uncalibrated.
- `faion-user-researcher-agent` — converts customer pain points into "Pain Points" rows in the current-state template, with interview citations.
- `faion-brainstorm` skill (entry point `/faion-brainstorm`) — diverge-converge for the future-state vision and for the build/buy/partner solution options table.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts each accepted gap (priority H) into an SDD feature in `backlog/`; transition phases become roadmap milestones.
- A purpose-built **outside-view reviewer agent** (worth creating, not yet in repo) — system prompt: "You are a skeptical board observer. Down-rate any capability-maturity score that lacks numeric evidence." Run after every current-state pass.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub the strategy doc before sharing externally; current-state writeups leak vendor names, internal URLs, and unannounced plans.

### Prompt pattern
Current-state baselining (parallel-friendly):
```
You are a BA conducting current-state analysis for <initiative>. Use only
the artifacts under .aidocs/ and the URLs in <evidence>. Produce the four
tables from strategy-basics/README.md section 1 (Business Context,
Capability Assessment, Pain Points, SWOT). Rules:
- Every capability score 1-5 needs a one-line evidence cell with a link
  or metric. No score without evidence — leave blank instead.
- SWOT cells: max 1 sentence each, must cite a source.
- Pain points: minimum 3, each tied to a stakeholder name + interview ref.
Output as a single markdown file.
```

Future-state convergence after brainstorm:
```
Three future-state variants are in <variants>. Score each on (a) strategic
alignment 1-5, (b) feasibility 1-5, (c) ROI rank, (d) risk count from the
risk-assessment pass. Recommend one variant; for the rejected variants,
list the specific assumption that, if invalidated, would flip the choice.
Emit the Future State Vision template from README.md section 2.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `mermaid-cli` | Render capability-maturity radar charts and transition Gantt from text | `npm i -g @mermaid-js/mermaid-cli` |
| `pandoc` | Convert strategy doc → board PDF / DOCX with the templates intact | `apt install pandoc` |
| `gh` CLI | Spawn one GitHub issue per priority-H gap, label `strategy:gap` | https://cli.github.com |
| `git diff` (snapshot strategy.md monthly) | Track which capabilities, risks, and assumptions changed quarter-over-quarter | built-in |
| `claude` (Anthropic CLI) | Run the four-phase pipeline headless from cron | https://docs.anthropic.com |
| `mdformat` / `markdownlint-cli` | Keep the templates' table alignment from drifting (pre-commit) | `pip install mdformat` |
| Custom `strategy-lint` (inline below) | Reject capability rows without evidence and gaps without owners | inline script below |
| `dot` (Graphviz) | Capability-dependency graphs for transition planning | `apt install graphviz` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Cascade Strategy / ClearPoint | SaaS strategy execution | API limited | Enterprise OKR + initiative tracking; overkill <500 employees. |
| Jira Align (Atlassian) | SaaS portfolio | API yes | Heavy, but capability-maturity → epics mapping is supported; agents can drive via REST. |
| Asana / Linear / Notion (with templates) | SaaS docs+work | API yes | Pragmatic strategy register; the four README templates drop in cleanly. Solo/team default. |
| Miro / Mural | SaaS whiteboard | API limited | Used for SWOT and capability heatmaps in workshops; agent can post the source data via API but visual edit is manual. |
| ProcessMaker / Camunda / SAP Signavio | Process platforms | API yes | Feed real process telemetry into capability scoring instead of self-report. |
| LeanIX / Ardoq / MEGA Hopex | SaaS enterprise architecture | API yes | The "right" tool for capability-maturity at scale; expensive, multi-month rollout. |
| Wardley Maps (`mapscript.io`, `onlinewardleymaps`) | OSS/SaaS hybrid | partial | Better than SWOT for evolving capabilities; LLM can emit Wardley script directly. |
| Tableau / Metabase / Superset | OSS / SaaS BI | API yes | Capability score baselines as live dashboards; treat the strategy doc as an export, not the source of truth. |
| OpenStrategy / Obsidian + Dataview | OSS docs | yes | Markdown-native strategy register; agent-edits via plain files, no API needed. |

## Templates & scripts

The five existing files (README, checklist, templates, examples, llm-prompts) ship the four section templates but are mostly empty (checklist/templates/examples/llm-prompts each are 1-line stubs). The first concrete contribution agents can make is a linter that fails CI when the strategy doc has unowned high-priority gaps or evidence-free capability scores. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# strategy-lint.sh — enforce evidence + ownership in strategy-basics docs.
# Usage: strategy-lint.sh path/to/strategy.md
set -euo pipefail
file="${1:?usage: strategy-lint.sh STRATEGY.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
errs = []
# Capability rows: | name | curr 1-5 | tgt 1-5 | gap | (evidence optional col)
cap_re = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([1-5])\s*\|\s*([1-5])\s*\|\s*(\d+)\s*\|", re.M)
for m in cap_re.finditer(src):
    name, c, t, g = (s.strip() for s in m.groups())
    line_end = src.find("\n", m.end())
    line = src[m.start():line_end]
    if int(g) > 0 and not re.search(r"https?://|see |interview|metric", line, re.I):
        errs.append(f"capability '{name}': gap {g} without evidence link/metric")
# Gap analysis rows priority H must have an owner column or sentence.
gap_re = re.compile(r"^\|\s*[^|]+\|[^|]+\|[^|]+\|[^|]+\|\s*H\s*\|", re.M)
for m in gap_re.finditer(src):
    end = src.find("\n", m.end())
    if "owner" not in src[m.start():end].lower() and "@" not in src[m.start():end]:
        errs.append(f"H-priority gap row missing owner: {src[m.start():end][:80]}")
# Future-state goals must declare baseline + target.
for m in re.finditer(r"\|\s*G\d+\s*\|[^|]+\|[^|]+\|\s*\{?value\}?\s*\|", src):
    errs.append(f"future-state goal row uses placeholder target: {m.group(0)[:80]}")
if errs:
    print("strategy-lint FAIL:"); [print(" -", e) for e in errs]; sys.exit(1)
print("strategy-lint OK")
PY
```

Wire into pre-commit on the repo that owns `.aidocs/strategy/*.md` so unowned gaps and ungrounded capability scores fail before merge.

## Best practices
- **Score capabilities from telemetry, not opinion.** Replace "self-rate 1–5" with measurable proxies (deploy frequency, incident MTTR, NPS, cycle time) and a documented rubric. Agents can pull these via APIs; humans cannot resist optimism on self-rating.
- **One future-state variant is wrong.** Always produce 3 (conservative / expected / aggressive) and explicitly select one with a documented rationale. The variants double as scenario plans when reality drifts.
- **Tie every capability gap to a SMART goal in section 2.** A gap without a corresponding future-state goal is decorative; a goal without a capability gap is detached from the org.
- **Tag every assumption with a falsifier.** "Assumption: customers will accept SaaS" is useless; "Assumption: ≥60% of pilot customers sign annual contracts within 90 days" lets the agent monitor it automatically.
- **Use Wardley mapping when capabilities are mid-evolution.** Static maturity 1–5 hides whether a capability is genesis vs. commodity; Wardley exposes whether to build, buy, or outsource per stage.
- **Rebaseline quarterly with a diff, not a rewrite.** Keep `strategy.md` in git, generate the new pass into `strategy.next.md`, run `git diff` to surface what actually changed; debate the deltas, not the entire doc.
- **Pair with a financial model.** Section-4 ROI is meaningless without a spreadsheet (or notebook) sitting next to it; require a `tco.xlsx` or `roi.ipynb` in the same folder.
- **Cap Risk Register at the top 10.** Section 3 with 30+ rows is unread; drop sub-score-6 risks to an "Accepted" appendix.
- **Stakeholder list ≠ org chart.** Force RACI per goal; "Marketing" as an owner is unowned. Single name per high-priority row.
- **Forbid `{value}` placeholders in committed docs.** They survive rewrites and become permanent embarrassments. The lint script above flags them.

## AI-agent gotchas
- **Optimism leak from briefs.** If the initiative description is written by the sponsor, it primes the agent toward high-confidence current-state scores and low-rated risks. Strip marketing language before feeding into the current-state agent; or run a deliberately adversarial pass.
- **Made-up capability rubrics.** LLMs invent a 1–5 maturity rubric per call; the same capability scores 3 in one pass and 4 in the next. Pin the rubric (CMM-style or a custom one) and provide it as a system-prompt constant.
- **Ungrounded SWOT cells.** Agents fill SWOT effortlessly with plausible-sounding bullets — almost always without sources. Reject any SWOT cell lacking a citation; the lint script can be extended to enforce this.
- **Gap-analysis hallucinated current state.** The agent will assume capabilities exist that don't, especially for "monitoring", "documentation", "training". Force the agent to prove existence (link, ticket, runbook) before listing a capability at level >1.
- **Recommendation bias toward "build".** LLMs default to recommending Option A (build) because "control" reads as a positive trait — ignore TCO and switching costs. Mandate explicit `tco_year_3` and `vendor_lock_in_score` columns in the solution-options table; have the agent fill those before recommending.
- **Goal drift across sections.** Goals appear in current-state SWOT (Opportunities), future-state (Goals), and change-strategy (Recommendation). Agents reword them slightly each time → the same goal looks like three. Use stable IDs (`G1`, `G2`) and have the agent reference IDs, not restate text.
- **No human checkpoint on "Avoid" / "Retire" capabilities.** The framework allows "capability retirements" in section 2; this is a layoff or product kill in real life. Hard human-in-the-loop gate; never let an agent execute that branch autonomously.
- **Silent assumption inheritance.** Future state inherits assumptions from the current-state pass without re-validating them; when conditions change, both states drift together. Re-list assumptions explicitly per phase, with timestamps.
- **Single-agent SWOT is groupthink.** SWOT works because four perspectives clash; one LLM produces one perspective in four cells. Run four separate prompts (insider / customer / competitor / regulator) and consolidate.
- **Confidentiality leak.** Strategy docs name unannounced products, target customers, vendor terms, and unhappy path scenarios. Always run `password-scrubber-agent` (or equivalent) before any external sharing or third-party SaaS upload.

## References
- BABOK Guide v3, Chapter 6: Strategy Analysis. IIBA. https://www.iiba.org/career-resources/a-business-analyst-resources/babok/
- Kaplan, R. & Norton, D. (1996). "The Balanced Scorecard." Harvard Business Press.
- Klein, G. (2007). "Performing a Project Premortem." HBR. https://hbr.org/2007/09/performing-a-project-premortem
- ISO 31000:2018 — Risk management guidelines. https://www.iso.org/iso-31000-risk-management.html
- Wardley, S. "Wardley Maps." https://medium.com/wardleymaps and https://learnwardleymapping.com
- CMMI Institute — Capability Maturity Model Integration. https://cmmiinstitute.com
- McKinsey 7-S framework (current-state lens). https://www.mckinsey.com/business-functions/strategy-and-corporate-finance/our-insights/enduring-ideas-the-7-s-framework
- Sibling methodologies in this repo: `pro/ba/ba-core/strategy-analysis/`, `pro/ba/ba-core/strategy-methods/`, `pro/research/researcher/risk-assessment/`, `pro/pm/pm-traditional/risk-management/`.
