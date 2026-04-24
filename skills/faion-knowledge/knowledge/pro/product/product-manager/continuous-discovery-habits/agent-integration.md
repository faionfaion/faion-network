# Agent Integration — Continuous Discovery Habits (Product Manager)

> PM-specific angle. Sibling `solo/product/product-planning/continuous-discovery/` covers planner-side cadence; this file is about the PM as the operator of the weekly touchpoint, OST custodian, and synthesizer of insights into roadmap inputs.

## When to use

- A PM owns one product or product area and needs a defensible weekly cadence (one customer interview per week, minimum) instead of campaign-style research bursts.
- Roadmaps are drifting toward feature-list mode and leadership cannot articulate the outcome each item serves — the OST forces every solution to map to an opportunity to an outcome.
- Product Trio (PM + Design Lead + Tech Lead) is being formed and needs a shared artifact to triangulate on; the OST is the contract.
- Solo PM at a startup wants an LLM to triage support tickets, NPS verbatims, sales-call recordings into the OST as candidate opportunities for trio review.
- Quarterly planning prep — agents synthesize 60–80 interviews into a refreshed OST that becomes input to roadmap, OKRs, and discovery sprints.
- "Why are we building this?" challenges from leadership/board — OST + interview log answer the question with a traceable chain (outcome ← opportunity ← evidence quotes).

## When NOT to use

- Pre-PMF zero-to-one with founder-led customer development — Torres' framework assumes you have a product, an outcome metric, and access to customers. Use `customer-development` and `jobs-to-be-done` instead.
- Compliance/regulated domains where weekly outside-customer interviews require legal review per touchpoint (clinical trials, fintech KYC research) — cadence breaks under the gating overhead.
- B2B with <20 logo accounts and a 12-month sales cycle — weekly interviews aren't sustainable; switch to monthly executive briefings + quarterly synthesis.
- Mature growth-stage where experimentation-at-scale has displaced qualitative discovery; here CDH is a complement (it generates hypotheses), not the primary loop.
- One-shot launches and migrations (rebrand, platform cutover) — they need stakeholder management and program management, not weekly touchpoints.
- Agencies/consultants on fixed-scope contracts — without ownership of the outcome, the OST has no anchor.

## Where it fails / limitations

- "Weekly interview" degrades to "weekly chat with the loudest customer" — PMs over-sample the same 5 power users; agents must enforce sampling diversity (segment, recency, churn-status, plan-tier) before each round.
- OST grows monotonically; without pruning, it becomes a dumping ground. By month 6 most trees have 200+ nodes and become unusable. Need a quarterly archive-or-promote ritual.
- Opportunities get conflated with solutions ("opportunity: build dashboard"). Must reject solution-shaped opportunities; they belong as branches under a real opportunity.
- Discovery-delivery balance (15–20% capacity) is fictional in most teams — engineers stay at 100% delivery, PM does discovery alone, trio collapses to PM-only. CDH fails as a team practice.
- Outcome metric ambiguity — many PMs pick activation/retention proxies that the team can't actually move in a quarter. Agent-driven OST inherits the bad outcome and produces noise.
- Past-behavior interviews still surface aspirational answers when the prompt is loose; LLM transcript-coding amplifies this, mistaking interviewer leading questions for customer signal.
- Synthesis collapses when interview corpora cross >100 transcripts without theming — naive embedding-based clustering returns shallow themes ("users want speed"). Hierarchical theming (axial coding) is needed.
- Tree visualization tools (Miro/FigJam) become the bottleneck — a YAML/JSON tree-as-code is more agent-friendly but humans don't love it.

## Agentic workflow

PM operates the loop; agents handle the mechanical parts. Five hand-offs per week, each gated by PM review.

```
Mon  feedback-triage   (haiku)  → today's queue: tickets/NPS/sales-calls scored as opportunity-candidates
Tue  interview-prep    (sonnet) → research-questions.md + sampling-plan.md (interview today)
Tue  interview-coder   (sonnet) → transcript → coded-quotes.json (past behavior, evidence, snapshot)
Wed  ost-synthesizer   (opus)   → propose tree edits: new opportunity, evidence link, dedup
Thu  trio-prep         (sonnet) → trio-agenda.md: 3 candidate opportunities + assumption tests
Fri  weekly-readout    (sonnet) → weekly-discovery.md, roadmap-input.md (delta vs last week)
```

OST lives at `.aidocs/product_docs/discovery/ost.yaml`. Interview transcripts at `discovery/interviews/<date>-<participant-hash>.md`. All agents read/write through this folder; no in-app SaaS state without an export step.

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `feedback-triage` | haiku | Daily 8am | Support tickets, NPS verbatims, sales-call notes | Top-N opportunity-candidates (JSON) ranked by frequency × outcome-relevance |
| `interview-sampler` | haiku | Weekly | Customer list + segment/recency/status flags | One participant + 3 backups, with diversity rationale |
| `interview-prep` | sonnet | Pre-interview | Current OST, opportunity gap, last 4 transcripts | Research questions, screener, anti-leading-question rewrites |
| `interview-coder` | sonnet | Post-interview | Transcript (text or audio→text) | Coded quotes, snapshot of "story", behavioral evidence flags |
| `ost-synthesizer` | opus | Weekly | All coded quotes since last run, current OST | Proposed tree-diff (add/move/dedup nodes), evidence linkage |
| `assumption-tester` | sonnet | On opportunity-promotion | Solution + key assumptions | List of assumption-test designs (Type-1: desirability/viability/feasibility/usability/ethical) |
| `trio-prep` | sonnet | Pre-trio meeting | OST, recent quotes, capacity allocation | 1-page agenda; 3 opportunities ready for "next solution to test" |
| `weekly-readout` | sonnet | Friday | All week artifacts | weekly-discovery.md + roadmap-input.md |
| `roadmap-mapper` | opus | Quarterly | Full OST, outcome history, capacity | Now/Next/Later updates as deltas to existing roadmap |
| `archive-pruner` | sonnet | Monthly | OST nodes with no edits in 90d | Archive proposals; PM approves |

Cheap models for collection and triage. Sonnet for structured authoring (questions, agendas, readouts). Opus only for synthesis (where the cross-corpus reasoning happens) and for roadmap mapping. Never let opus write a single interview question — it over-articulates.

### Prompt pattern

```xml
<role>You are the {agent} for a Product Manager running Continuous Discovery Habits (Teresa Torres).</role>

<inputs>
  <ost>{path to ost.yaml}</ost>
  <outcome>{measurable outcome metric + current value}</outcome>
  <interviews>{glob: discovery/interviews/2026-04-*.md}</interviews>
  <roadmap>{path to roadmap.yaml — Now/Next/Later}</roadmap>
  <capacity>{discovery_pct: 0.15, delivery_pct: 0.75, debt_pct: 0.10}</capacity>
</inputs>

<rules>
  - Opportunities are unmet needs, pains, desires expressed in the customer's words. Reject any opportunity phrased as "build X" or "add X".
  - Evidence requirement: every opportunity must link to >=1 verbatim quote with participant-id + interview-date.
  - Past-behavior anchoring: interview-prep must produce questions about specific recent instances ("tell me about the last time you..."), never future predictions.
  - One outcome per OST. If asked to span outcomes, refuse and request a separate tree.
  - Never auto-promote an opportunity to roadmap; emit a roadmap-input artifact for human approval.
  - Output JSON to schema {schema_path}; markdown digest <= 60 lines.
  - Surface sampling skew: if last 4 interviews share segment/plan/region, flag and require diversification before next round.
</rules>

<task>{cadence-specific instruction}</task>
```

Pin the OST schema (yaml) and let agents emit tree-diffs as patches, not full rewrites — PM reviews diffs, never raw rewritten trees.

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dovetail-cli` (community / API) | Push/pull research repo, themes, highlights | dovetail.com/api |
| `airtable-cli` / Airtable API | Lightweight OST and interview log | airtable.com/developers/web/api |
| `notion` API + `notion-cli` | OST + interview repo when team lives in Notion | developers.notion.com |
| `productboard` API | Pull feature requests as opportunity-candidates | developers.productboard.com |
| `pendo` API | Behavioral data feeds (event funnels, NPS verbatims) | developer.pendo.io |
| `intercom` API | Conversations + product-tour events | developers.intercom.com |
| `gong-api` / `chorus-api` | Sales/CS call transcripts (B2B) | gong.io/developers |
| `whisper.cpp` / `pyannote` | Local STT for recorded interviews (privacy) | github.com/ggerganov/whisper.cpp |
| `dbt` + warehouse SQL | Outcome metric pull (activation, retention, NPS) | getdbt.com |
| `mermaid-cli` / `graphviz` | Render OST yaml → SVG for the trio meeting | mermaid.js.org / graphviz.org |
| `gh` | OST as PR; trio review by code-review | cli.github.com |
| `~/bin/tg-send` | Notify PM of new opportunity-candidates, missed weekly cadence | NERO |

## Services & apps

| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Dovetail | SaaS | Yes (REST + AI features) | Best research repo; native theming + AI synthesis; strong on transcript coding |
| ProductBoard | SaaS | Yes (REST) | Feature requests + insights; weak on OST visualization, strong on inbound triage |
| Productlift | SaaS | Yes (REST) | Lighter alternative to ProductBoard |
| Notion | SaaS | Yes (REST) | OK as low-budget OST host; weak query/synthesis |
| Airtable | SaaS | Yes (REST) | OST as table works for small trees; breaks at scale |
| Miro / FigJam | SaaS | Partial (REST limited) | Great for the trio session; agents export PNG/JSON; not source of truth |
| Pendo / Amplitude / Mixpanel | SaaS | Yes (REST) | Outcome-metric source; behavioral patterns |
| Hotjar / FullStory | SaaS | Partial | Session replay surfaces opportunities; transcript-quality coding limited |
| Maze | SaaS | Yes (REST) | Rapid prototype testing for assumption tests |
| Gong / Chorus / Avoma | SaaS | Yes (REST) | Conversation intelligence — feed into interview-coder |
| Calendly + Reclaim | SaaS | Yes | Automate weekly interview booking; agent enforces calendar slot |
| Loom / tella.tv | SaaS | Partial | Async customer testimonials; export transcript |
| Continual.ly / Userpilot | SaaS | Yes (REST) | In-product micro-surveys feed feedback queue |
| Tray.ai / n8n / Zapier | iPaaS | Yes | Wire feedback sources → agent queue |
| Mural / Lucidchart | SaaS | Partial | OST visualization for stakeholders |

## Templates & scripts

OST schema (`ost.yaml`) — the central artifact. Tree-as-code; agents emit YAML patches.

```yaml
outcome:
  id: outcome_2026Q2_activation
  metric: pct_new_signups_completing_first_value_action
  baseline: 0.31
  target: 0.45
  owner: pm@team.com

opportunities:
  - id: opp_login_friction
    statement: "I get locked out at SSO and give up before completing setup"
    evidence:
      - quote_id: q_2026-04-12_p042
      - quote_id: q_2026-04-19_p081
    parent: outcome_2026Q2_activation
    last_evidence_date: 2026-04-19
    status: active   # active | parked | shipped | invalidated
    solutions:
      - id: sol_passwordless_link
        assumption_tests:
          - type: desirability
            method: prototype_test
            owner: ux
          - type: feasibility
            method: spike
            owner: tech_lead
        decision: not_started   # not_started | testing | win | kill
```

Friday weekly readout — `weekly-discovery.md` skeleton (Markdown, ≤2 pages):

```markdown
# Discovery Week of 2026-04-22

## Outcome
activation: 0.31 → 0.34 (+0.03 vs baseline)

## Touchpoints
- Interviews this week: 1 (P-091, mid-market, 13mo tenure)
- Diversity vs last 4: segment OK; tenure-skew (all >12mo) -> next sample <6mo

## OST changes (diff)
+ opportunity opp_sso_lockout (3 quotes)
~ opportunity opp_login_friction renamed → opp_setup_dropoff (broader)
- opportunity opp_dark_mode parked (no evidence in 60d)

## Assumption tests run / planned
- sol_passwordless_link prototype: desirability test scheduled Tue
- sol_self_serve_sso spike: tech_lead estimate due Fri

## Roadmap input
- Now: ship sol_setup_progress_indicator (validated, low-effort)
- Next: pilot sol_passwordless_link (assumption test pending)
- Later: re-evaluate sol_self_serve_sso pending feasibility spike

## Open questions for trio
1. Is opp_setup_dropoff a single opportunity or two (auth vs onboarding)?
2. Should we drop opp_dark_mode permanently or revisit Q3?
```

OST diff applier (`scripts/ost_apply.py`, ~30 lines) — agents emit diffs, PM reviews, this script applies:

```python
import sys, yaml, copy
from pathlib import Path

def apply_diff(ost: dict, diff: dict) -> dict:
    out = copy.deepcopy(ost)
    by_id = {o["id"]: o for o in out["opportunities"]}
    for op in diff.get("add", []):
        if op["id"] in by_id:
            raise SystemExit(f"add: id exists {op['id']}")
        out["opportunities"].append(op)
    for op in diff.get("update", []):
        if op["id"] not in by_id:
            raise SystemExit(f"update: missing {op['id']}")
        by_id[op["id"]].update(op)
    for op_id in diff.get("park", []):
        by_id[op_id]["status"] = "parked"
    for op_id in diff.get("archive", []):
        out["opportunities"] = [o for o in out["opportunities"] if o["id"] != op_id]
    return out

if __name__ == "__main__":
    ost = yaml.safe_load(Path(sys.argv[1]).read_text())
    diff = yaml.safe_load(Path(sys.argv[2]).read_text())
    Path(sys.argv[1]).write_text(yaml.safe_dump(apply_diff(ost, diff), sort_keys=False))
```

Cron for the PM week:

```
0 8  * * 1   claude run /discovery-feedback-triage
0 9  * * 2   claude run /discovery-interview-prep
0 16 * * 2   claude run /discovery-interview-code   # after interview
0 9  * * 3   claude run /discovery-ost-synthesize
0 9  * * 4   claude run /discovery-trio-prep
0 16 * * 5   claude run /discovery-weekly-readout
0 9  1 */3 * claude run /discovery-roadmap-mapper   # quarterly
```

## Best practices

- One outcome per OST per quarter. If two outcomes are in scope, build two trees and contend with the cross-tree dependency explicitly — do not merge.
- Pre-commit a sampling-diversity check before every interview round: segment, recency, plan-tier, churn-status. Agent rejects the prep if last 4 interviews are within one slice.
- Treat the interview transcript as source of truth; never let synthesis agents reason from summaries (lossy). Feed the full transcript with quote-level IDs.
- Quote-level provenance is non-negotiable: every opportunity links to >=1 quote_id with participant + date. Without this, the OST is fiction.
- Lock the trio to ONE meeting per week and ship the trio-prep doc 24h before. Without prep, the meeting becomes a status update.
- Discovery-delivery percentage is a contract with engineering, not a PM aspiration. If 15% gets eaten weekly, escalate or shrink scope; do not silently absorb it.
- Park ruthlessly — opportunities with no new evidence in 60 days get parked; archive at 180 days. Tree health beats tree completeness.
- Roadmap-input is a delta artifact, never a rewrite. Quarterly mapper emits "promote / demote / hold / drop" recommendations versus current Now/Next/Later.
- Pair every opportunity with one assumption test type per dimension (desirability, viability, feasibility, usability, ethical). Cheap to enumerate, expensive to skip and learn later.
- Run a calibration interview round monthly: PM listens-only to a CS or sales call, codes it, and compares to interview-coder output. If divergence >25%, retune the coder prompt.
- Token budget: cap ost-synthesizer at 120k tokens per run (full OST + 1 week of transcripts). If over, archive first; never expand context.
- Anonymize PII at coding time, not at synthesis time. Once it's in the corpus, it's leaked.

## AI-agent gotchas

- Interview-coder will paraphrase quotes, breaking provenance. Force verbatim copy of the source span and a separate paraphrase field; downstream agents must consume verbatim only.
- Past-vs-future blindness: LLMs happily accept "I would use X" as evidence. Coder must label every quote as past_behavior | preference | speculation, and synthesizer must filter to past_behavior only for opportunity creation.
- Solution-shaped opportunities slip in when the synthesis prompt is open-ended. Validate every emitted opportunity against a regex/classifier ("starts with verb"=fail; "I/me/my … cannot/struggle/want"=ok).
- OST drift: synthesizer rewrites whole subtrees instead of emitting diffs. Force a JSON-patch (RFC 6902) or YAML-diff format and reject full-tree outputs.
- Sampling bias: feedback-triage over-weights loudest channels (Twitter, NPS detractors). Stratify the queue by source before ranking.
- Cross-segment conflation: one opportunity collapses signals from enterprise + SMB. Tag every quote with segment metadata; synthesizer must not merge across segments without an explicit "shared opportunity" check.
- Quote duplication: the same customer interviewed twice produces two quote_ids that look like two data points. Dedup by participant_id at the synthesizer.
- Roadmap-mapper recency bias: opus over-weights last week. Force it to use rolling-90d evidence count, not raw recency.
- Trio-prep meeting padding: agent will hedge with "depends on team capacity" boilerplate; constrain to specific recommendations + tradeoffs.
- Outcome-metric drift: PM rewords the outcome between quarters and the OST orphan their evidence chain. Pin outcome_id; new wording = new outcome = new tree.
- Privacy: customer recordings often contain SSN, contract terms, internal company info. Run a PII scrubber pre-coding; never feed raw recordings to a remote LLM without redaction.
- Calendar contention: agents auto-book interviews into PM's deep-work blocks; require a "discovery zone" calendar block as the only legal slot.
- Memory creep across weeks: agents fed last-week's "decisions" treat them as immutable, blocking re-litigation. Always include a `revisited_ok: true` flag in the prompt for opportunities older than 30 days.
- Synthesis hallucination: opus will manufacture cross-cutting themes from 3 unrelated quotes. Require N>=5 quotes from >=3 participants before emitting a theme.

## References

- Teresa Torres — *Continuous Discovery Habits* (2021), the canonical source. producttalk.org/continuous-discovery-habits.
- Product Talk podcast + community templates (OST examples, interview snapshot, assumption test cards).
- Marty Cagan — *Inspired* (2017), *Empowered* (2020) — Product Trio framing.
- Sibling: `solo/product/product-planning/continuous-discovery/README.md` — discovery cadence in agile delivery.
- Sibling: `pro/research/researcher/continuous-discovery/agent-integration.md` — research-side coding/synthesis depth.
- Sibling: `pro/product/product-operations/experimentation-at-scale/agent-integration.md` — quantitative loop that consumes OST hypotheses.
- Sibling: `pro/product/product-manager/portfolio-strategy/`, `roadmap-design/`, `okr-setting/` — downstream artifacts of the weekly readout.
- Anthropic Claude Agent SDK — structured outputs, scheduled triggers (`schedule` skill in this repo).
- Spotify, CarMax, Tesco public talks (2022–2025) on continuous discovery in practice.
