# Agent Integration — Continuous Discovery (Teresa Torres)

## When to use

- Live products with active users where signal volume (analytics, tickets, sessions, NPS, churn events) exceeds what a human PM can review unaided.
- Product Trio (PM + designer + engineer) workflows that need a weekly cadence of customer touchpoints and assumption tests.
- Markets with 6-month half-life on user-need validity (AI tools, fintech, dev tooling, consumer social).
- Pre-launch teams that need to convert a one-time research phase into an always-on opportunity backlog feeding an Opportunity Solution Tree (OST).
- Solopreneur stacks where one operator must simulate trio coverage via specialized subagents.
- After a launch, when growth slows and the team needs to detect "the solution that worked 6 months ago no longer works" pattern.

## When NOT to use

- Pre-PMF zero-to-one with no users yet — start with `customer-development` or `jobs-to-be-done`, not continuous loops.
- Compliance-bound enterprise sales where contract cycles are 6–18 months — interview cadence cannot be weekly.
- Hardware/regulated medical where each iteration ships in months, not weeks; cadence must match release rhythm.
- Crisis mode (active outage, security incident, churn cliff) — switch to focused root-cause work, resume discovery after stabilization.
- When stakeholders demand "validated" answers from a single interview — Torres explicitly rejects "validation theater"; do not fake the practice.

## Where it fails / limitations

- Recruiting fatigue: weekly interviews require a recurring source (in-app prompt, customer panel, Userinterviews.com) — without infrastructure the cadence collapses by week 4.
- Curse-of-knowledge bias persists if the same trio interprets every interview — rotate observers, use Looppanel/Dovetail tagging across team members.
- Assumption testing is often skipped because it feels slower than shipping — without an explicit weekly slot it disappears.
- AI synthesis hallucinates patterns from small N — never let an LLM declare an "insight" from <5 interviews without human cross-tag.
- OSTs rot when not pruned — opportunities accumulate; require monthly archival of stale branches.
- Discovery output without delivery linkage becomes a research graveyard — every opportunity must trace to either a tested assumption or a deliberate "park" decision.

## Agentic workflow

```
Daily   → analytics-watcher (haiku)   → insight-log.md
Daily   → support-triage (haiku)      → ticket-themes.md
Weekly  → interview-scheduler (sonnet) → upcoming-interviews.md
Weekly  → interview-synthesizer (sonnet, post-call) → interview-notes/<date>.md
Weekly  → competitor-monitor (haiku) → competitor-changes.md
Weekly  → assumption-tester (sonnet) → assumption-results.md
Bi-week → discovery-synthesizer (opus) → opportunity-solution-tree.md
Monthly → research-reviewer (opus)   → research-report.md, archived-opportunities.md
```

All agents write to `.aidocs/product_docs/discovery/`. The synthesizer reads the full week's outputs and updates the OST.

### Recommended subagents

| Subagent | Model | Cadence | Inputs | Outputs |
|----------|-------|---------|--------|---------|
| `analytics-watcher` | haiku | Daily | PostHog/Amplitude exports, GA4 anomalies | `insight-log.md` daily entry |
| `support-triage` | haiku | Daily | Intercom/Zendesk/Linear tickets last 24h | Theme cluster + count + severity |
| `competitor-monitor` | haiku | Weekly | RSS, changelog scrapes, ProductHunt, G2 reviews | `competitor-changes.md` diff |
| `interview-scheduler` | sonnet | Weekly | User segment criteria, recruit pool | Recruit list + outreach drafts |
| `interview-synthesizer` | sonnet | Per call | Transcript (Otter/Fireflies/Looppanel) | Tagged notes, JTBD pulls, quotes |
| `assumption-tester` | sonnet | Weekly | Open assumptions list, OST leaves | Test design (smoke test, fake door, prototype) + result rubric |
| `discovery-synthesizer` | opus | Bi-weekly | All weekly outputs | Updated OST, opportunity scores |
| `research-reviewer` | opus | Monthly | All synthesis outputs | Strategic memo, kill list, doubled-down list |

Key principle: cheap models for collection, sonnet for structured synthesis, opus only for bi-weekly+ pattern recognition. Never invert this — opus on daily ticket triage burns tokens for no marginal value.

### Prompt pattern

```
<role>You are the {agent}. Continuous Discovery (Torres) practitioner.</role>

<inputs>
  <since>{ISO8601 last-run timestamp}</since>
  <signals>{paths to analytics/tickets/transcripts}</signals>
  <ost>{path to opportunity-solution-tree.md}</ost>
  <assumptions>{path to open-assumptions.md}</assumptions>
</inputs>

<rules>
  - Tag every observation with: source, user_segment, frequency, severity (1-5).
  - Distinguish OPPORTUNITY (unmet need) from SOLUTION (proposed feature). Reject solution-shaped input.
  - Never declare "validated" from a single signal. Require N>=5 across >=2 sources.
  - Surface curse-of-knowledge risk: flag claims that assume internal jargon.
  - Output JSON matching schema {schema_path}, plus a markdown digest <= 60 lines.
</rules>

<task>{cadence-specific instruction}</task>
```

Wire this through Claude Agent SDK with structured outputs (Pydantic/Zod schema enforced) — see `feedback_agent_output` in NERO memory.

## CLI tools

- `claude` (Claude Code) — orchestrate subagents via Task tool; one slash command per cadence (`/discovery-daily`, `/discovery-weekly`, `/discovery-synth`).
- `gh` — pull GitHub issue feedback as a signal source; `gh issue list --label feedback --json` feeds support-triage.
- `posthog` CLI / `amplitude-cli` — pull funnel + retention deltas; pipe into analytics-watcher.
- `linear` CLI — query bug+feature requests; tag against OST opportunity nodes.
- `otter`/`fireflies`/`tldv` API — fetch transcripts of completed interviews; auto-feed interview-synthesizer.
- `dovetail` API (`/v1/notes`, `/v1/tags`) — push tagged quotes from synthesizer; central source of truth.
- `notion` API — write OST + research-report entries to product team's space.
- `userinterviews.com` API — automate weekly recruit batches.
- `slack` CLI / webhook — post weekly synthesis digest to product channel.
- `cron` / `systemd timers` / `launchd` — run cadence agents on schedule; on NERO use `loop` skill or `schedule` skill for managed triggers.

## Services & apps

| Service | Role | API | Notes |
|---------|------|-----|-------|
| Dovetail | Research repo | REST + webhooks | Best for tagging at scale; Magic AI summaries 2025+ |
| Looppanel | AI interview analysis | REST | Auto-tagging of transcripts, JTBD extraction |
| Condens | Synthesis | REST | Lighter than Dovetail; good for solo PMs |
| EnjoyHQ (acquired by Userinterviews) | Research ops | REST | Repository + recruit unification |
| Userinterviews.com | Recruitment | REST | Panel access, scheduling, incentives |
| Userlytics / UserTesting | Moderated/unmoderated | REST | For weekly assumption tests via prototypes |
| Maze | Unmoderated prototype tests | REST | Fast assumption tests, quant + qual |
| Notion | Knowledge base | REST | OST + opportunity backlog home |
| Airtable | Insight tracking | REST | Lightweight insight DB if not on Dovetail |
| PostHog | Product analytics | REST + SQL | Self-hostable; feeds analytics-watcher |
| Amplitude | Product analytics | REST | Hypothesis-aligned cohorts |
| Intercom / Zendesk / HelpScout | Support ticket source | REST | Daily theme clustering input |
| Otter / Fireflies / tl;dv | Transcription | REST | Required for async interview synthesis |
| ProductBoard | Insight → opportunity linkage | REST | Optional; OSTs duplicate most of its value |

## Templates & scripts

Daily analytics digest agent (Claude Agent SDK pseudocode, ~40 lines):

```python
from claude_agent_sdk import Agent, tool
from datetime import datetime, timedelta

@tool
def fetch_posthog(since: str) -> dict: ...
@tool
def fetch_tickets(since: str) -> list: ...
@tool
def append_insight_log(entry: dict) -> None: ...

watcher = Agent(
    model="claude-haiku-4-7",
    system=open("prompts/analytics-watcher.xml").read(),
    tools=[fetch_posthog, fetch_tickets, append_insight_log],
    output_schema=InsightLogEntry,  # Pydantic
)

since = (datetime.utcnow() - timedelta(hours=24)).isoformat()
result = watcher.run(f"Summarize signals since {since}. Tag by OST node id.")
append_insight_log(result.model_dump())
```

OST node schema (JSON, drop into `.aidocs/product_docs/discovery/ost-schema.json`):

```json
{
  "id": "opp_xxx",
  "type": "outcome|opportunity|solution|assumption_test",
  "parent_id": "opp_yyy",
  "title": "string",
  "evidence": [{"source": "interview|ticket|analytics", "ref": "url", "date": "ISO"}],
  "n_signals": 0,
  "status": "open|tested|parked|killed",
  "last_touched": "ISO",
  "owner": "trio|pm|design|eng"
}
```

Cron schedule (`crontab -e`):

```
0 7 * * *   /usr/local/bin/claude run /discovery-daily
0 8 * * 1   /usr/local/bin/claude run /discovery-weekly
0 9 1,15 * * /usr/local/bin/claude run /discovery-synth
0 10 1 * *  /usr/local/bin/claude run /discovery-monthly
```

## Best practices

- Pin one Outcome at the OST root before any opportunity work — without it agents drift into solution mining.
- Force "opportunity vs solution" classification at intake; reject any item phrased as a feature ("add filter X") and re-prompt for the underlying need.
- Maintain an `open-assumptions.md` register; every opportunity branched into a solution must spawn at least one assumption with a falsifiable test.
- Rotate the human reviewer of synthesis output weekly — agents anchor on patterns; humans catch curse-of-knowledge.
- Cap interview synthesis to 5 themes per session; more = noise. Discovery-synthesizer aggregates across sessions.
- Record interview consent + retention policy alongside transcripts; agents must read the consent flag before quoting.
- Score opportunities on (frequency × severity × addressability), not gut feel; have agents emit numeric scores and surface deltas week-over-week.
- Every research-reviewer monthly pass must produce a "kill list" (parked/dead opportunities) — without pruning, OSTs collapse under their own weight.
- Tie discovery output to delivery: reference opportunity IDs in PR titles and SDD specs (`spec.md` cites `opp_xxx`).
- Token budget: cap weekly synth at ~30k tokens, monthly at ~80k; otherwise opus costs balloon.

## AI-agent gotchas

- LLMs love to invent "insights" from thin signal — enforce N>=5 rule in the schema and reject completions that violate it.
- Transcription tools mis-attribute speakers; agents will conflate interviewer leading questions with user statements. Strip interviewer turns before synthesis.
- "Validation" is a banned word in prompts — Torres framework deliberately uses "test assumptions"; agents trained on generic UX content will drift into validation theater otherwise.
- Models hallucinate competitor changelog entries when scraping fails; require explicit URL + fetched-at timestamp in every competitor-monitor row.
- Daily haiku watchers will overwrite the insight log if not append-only — use atomic append + lock file, never `Write`.
- Bi-weekly synthesizer with full week's context can exceed context window — pre-summarize per-day with haiku, feed summaries to opus.
- Subagents that write to Dovetail/Notion via API can create duplicate notes if retried; require idempotency keys (hash of source URL + date).
- Curse-of-knowledge: agents trained on internal docs will use jargon. Add an explicit lint step that flags any term not present in the last 20 interview transcripts.
- Recruitment automation can violate panel ToS (Userinterviews limits weekly batch); rate-limit at agent level.
- Privacy: never feed raw PII transcripts to a non-zero-retention model. Use Anthropic ZDR-eligible endpoints or strip PII pre-prompt.
- Assumption-tester will propose "ship and measure" as a test — that's delivery, not discovery. Constrain to: smoke test, fake door, prototype, Wizard of Oz, concierge.
- Long-running cron agents accumulate state drift; have research-reviewer run a monthly schema-validation pass over OST + assumptions register.

## References

- Teresa Torres, *Continuous Discovery Habits* (2021) — canonical text.
- producttalk.org/podcast — 2025–2026 episodes on AI in discovery, Claude Code integration.
- Torres' "Opportunity Solution Tree" deep dives on producttalk.org.
- Sibling methodology: `../opportunity-solution-trees/README.md`.
- Sibling methodology: `../user-research-at-scale/README.md`.
- Sibling methodology: `../persona-building/README.md`.
- Anthropic Claude Agent SDK docs — agents, structured outputs, scheduled triggers.
- Looppanel + Dovetail blogs (2025) on AI-assisted synthesis pipelines.
- "Continuous Discovery in the Age of AI" — Torres + Hubert Palan, 2025 conference talks.
- Marty Cagan, *Inspired* / *Empowered* — adjacent product-trio practices.
