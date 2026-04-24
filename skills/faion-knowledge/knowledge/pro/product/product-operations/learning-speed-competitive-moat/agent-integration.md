# Agent Integration — Learning Speed as Competitive Moat

## When to use
- AI-replicable product surface where feature parity is reachable in weeks (most B2B SaaS, content tools, vertical AI wrappers).
- Org has 3+ teams and signal latency between customer/market/team measured in weeks rather than days.
- Strategy reviews are quarterly but competitor and customer behavior changes weekly.
- Founders/PM-leads need a defensible operational artefact that is not a feature list (board, GTM, fundraising narrative).
- Post-PMF stage where the bottleneck is "what do we ship next" not "does anyone want this".

## When NOT to use
- Pre-PMF / 1–5 person team — speed of one founder beats any process; "rituals" become theater.
- Truly defensible moats already in place (network effects, regulated licenses, hardware, dataset lock-in) — focus there, not on meta-process.
- Markets with 6–12 month sales cycles and slow regulatory cadence (defense, medical devices) — weekly belief updates produce noise.
- Teams that will not act on signals — building Insight Repository without a decision owner = dashboard graveyard.
- Burned-out teams — adding "weekly rituals" on top of broken delivery makes velocity worse, not better.

## Where it fails / limitations
- Vanity loops: teams measure "insights captured" instead of "decisions changed" — looks great, predicts nothing.
- Belief inertia: leadership says "weekly review" but never overrides last quarter's roadmap; the ritual exists, the moat does not.
- Signal drowning: AI dumps thousands of mentions; no signal-to-decision ratio. Without scoring + action owner this becomes worse than human curation.
- Recency bias: weekly cadence over-weights last 7 days, kills strategic patience on bets that need 90 days to play out.
- "Learning velocity" is unmeasurable directly — proxies (cycle time, decision count, prediction accuracy) drift; teams game them.
- Cross-team write-amplification: shared insight repo without curation produces 50 "insights/day" nobody reads.
- Tooling sprawl: Notion + Slack + Linear + Looker + Zoom transcripts ⇒ no single source of belief; agents lose the thread across contexts.

## Agentic workflow
Drive this as a daily/weekly belief-update pipeline, not a methodology. A daily collector agent (Haiku) ingests signals from product analytics, customer calls, support tickets, competitor watchlist, market news. A daily classifier (Haiku) tags each signal as `evidence-for | evidence-against | new-hypothesis | noise` against the current belief registry. A weekly synthesizer (Sonnet) updates a versioned `beliefs.yaml`, flags any belief whose evidence flipped, and generates a Monday digest. An Opus "strategy-reviewer" agent runs once per week against `beliefs.yaml` + ongoing experiments + roadmap and proposes which roadmap items to keep, kill, or re-prioritise. Humans own only two checkpoints: kill/keep decisions and any belief change that affects pricing or positioning.

### Recommended subagents
- `signal-collector` — Haiku. Pulls deltas from analytics (PostHog/Amplitude), CRM (Hubspot/Salesforce), support (Intercom/Zendesk), call transcripts (Gong/Fireflies), competitor watchlist. Emits normalized JSON events to `events.ndjson`.
- `signal-classifier` — Haiku/Sonnet. Tags each event against current `beliefs.yaml`: `evidence-for | evidence-against | new-hypothesis | noise`. Drops noise.
- `belief-updater` — Sonnet. Versioned `beliefs.yaml` write. Diff-aware: only changes a belief when ≥3 independent events agree, or 1 high-severity contradicting event. Emits a per-belief audit trail.
- `weekly-synthesizer` — Sonnet. Monday digest: which beliefs changed, which experiments concluded, which competitor moves matter, recommended discussion topics. Cite event_id per claim.
- `strategy-reviewer` — Opus. Friday roadmap pass: for each in-flight item, "still bet on this? evidence?". Outputs keep/kill/reframe with named decision owner.
- `decision-logger` — Haiku. Records every decision with prediction + check-back date. Quarterly calibration job grades prediction accuracy → feeds back into belief-updater confidence weights.
- `faion-research-agent` (this repo) — runs market/competitor mode on demand to refresh the signal corpus the collector sees.
- `faion-brainstorm` (this repo) — diverge/converge on `new-hypothesis` events before they enter belief registry.

### Prompt pattern
Belief updater (XML, structured output, Jinja2-style):
```
<role>belief-updater</role>
<current_beliefs>{{ beliefs_yaml }}</current_beliefs>
<new_events>{{ events_jsonl }}</new_events>
<rules>
  Only mutate a belief if (a) ≥3 independent event_ids agree, OR
  (b) 1 high-severity event directly contradicts current claim with cited URL/transcript.
  Never invent beliefs. Cite event_id for every change.
</rules>
<output_schema>
  {changed:[{belief_id, before, after, evidence:[event_id], confidence_delta}],
   unchanged_with_pressure:[{belief_id, opposing_evidence:[event_id]}]}
</output_schema>
```

Strategy reviewer (Opus, neutral framing):
```
<role>strategy-reviewer</role>
<beliefs>{{ beliefs_yaml }}</beliefs>
<roadmap>{{ roadmap_md }}</roadmap>
<experiments>{{ experiments_yaml }}</experiments>
<deliverable>For each roadmap item: keep|kill|reframe, cited evidence,
decision_owner, check_back_date.</deliverable>
<constraint>Default to "kill" if evidence_for_keeping &lt; 3 cited events
in last 30 days. Never reuse last week's recommendation without re-citing.</constraint>
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog` API / CLI | Product analytics events, feature flag results | posthog.com/docs/api |
| `amplitude` API | Behavioural cohorts, retention deltas | developers.amplitude.com |
| `metabase` / `cube` | SQL-based metric layer agents can query | metabase.com, cube.dev |
| `gong` / `chorus` API | Sales call transcripts, deal signals | app.gong.io/api |
| `fireflies.ai` API | Meeting transcripts → searchable corpus | docs.fireflies.ai |
| `intercom` / `zendesk` API | Support tickets, conversation tags | developers.intercom.com |
| `linear` / `jira` API | Decision log, experiment status | developers.linear.app |
| `notion` / `confluence` API | Belief registry storage, audit trail | developers.notion.com |
| `langfuse` / `helicone` | LLM-call observability (your own agents) | langfuse.com |
| `firecrawl` / `jina reader` | Competitor page extraction | firecrawl.dev, r.jina.ai |
| `dbt` | Transform raw signals → metric tables | docs.getdbt.com |
| `dagster` / `prefect` / `airflow` | Schedule the daily/weekly agent loops | dagster.io, prefect.io |
| `git` + `yamllint` | Version `beliefs.yaml`, diff weekly | trivial |
| `claude` (Anthropic SDK) | All synthesizer / reviewer agents | docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Partial — REST API | Insight repo + roadmap; rigid taxonomy. |
| Maze | SaaS | Yes — API | Continuous discovery experiments at scale. |
| Dovetail | SaaS | Yes — API + AI tags | Customer-research repo; auto-tagging quality varies. |
| Notion AI | SaaS | Limited (no eventing) | Cheap belief registry; weak as system of record. |
| Linear | SaaS | Yes — GraphQL | Strong for decision log + experiment status. |
| Hex / Hex Magic | SaaS | Yes — API | Notebooks agents can run as jobs. |
| Statsig | SaaS | Yes — REST | Experimentation + feature flags + warehouse export. |
| Eppo | SaaS | Yes — REST | Warehouse-native experiment platform. |
| GrowthBook | OSS + SaaS | Yes — REST + DB | Self-host belief experiments. |
| Pendo / Heap | SaaS | Partial API | Behavioural signal layer. |
| Productlane | SaaS | Yes — API | Customer-feedback → product loop. |
| Glean | SaaS | Yes — API | Cross-tool semantic search; "AI-indexed knowledge" layer. |
| Hebbia / Glean Assistant | SaaS | Yes — agent layer | Enterprise insight surfacing. |
| OpenAI / Anthropic Claude API | SaaS | Native | Belief updater / strategy reviewer brains. |
| Postgres + pgvector | OSS | Yes | Belief registry + event store; cheap and ownable. |

## Templates & scripts
Inline weekly belief-update loop (Python, ≤50 lines):

```python
# belief_update.py — schedule weekly via Dagster/cron
import json, pathlib, yaml, datetime, anthropic

EVENTS = pathlib.Path("events.ndjson")     # 7-day rolling window
BELIEFS = pathlib.Path("beliefs.yaml")     # versioned via git
HISTORY = pathlib.Path("beliefs.history.ndjson")
client = anthropic.Anthropic()

def load_window(days: int = 7) -> list[dict]:
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    out = []
    for line in EVENTS.read_text().splitlines():
        ev = json.loads(line)
        if datetime.datetime.fromisoformat(ev["ts"].rstrip("Z")) >= cutoff:
            out.append(ev)
    return out

prompt = f"""<role>belief-updater</role>
<current_beliefs>{BELIEFS.read_text()}</current_beliefs>
<events>{json.dumps(load_window(), indent=2)}</events>
<rules>Mutate a belief only if >=3 independent events agree OR 1 high-severity
contradicting event with cited source. Cite event_id per change. JSON only.</rules>
"""

resp = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=8000,
    messages=[{"role": "user", "content": prompt}],
)
delta = json.loads(resp.content[0].text)
beliefs = yaml.safe_load(BELIEFS.read_text())
for change in delta.get("changed", []):
    beliefs[change["belief_id"]] = change["after"]
    HISTORY.open("a").write(json.dumps({**change, "ts": datetime.datetime.utcnow().isoformat()+"Z"}) + "\n")
BELIEFS.write_text(yaml.safe_dump(beliefs, sort_keys=True))
print(f"changed={len(delta.get('changed', []))} pressure={len(delta.get('unchanged_with_pressure', []))}")
```

`beliefs.yaml` is the single source of truth. Commit it weekly; `git log` is your belief audit trail.

## Best practices
- Treat `beliefs.yaml` as code: versioned, reviewed, diffable. PR-reviewed belief changes beat Slack-thread consensus.
- Measure decisions, not insights. Track `(decisions made / week) × (decisions reversed within 30 days)` — high reversal = noisy loop, low decisions = inert org.
- Pair every belief with a kill criterion + check-back date. Beliefs without falsifiers rot into dogma.
- Quarterly calibration: grade past predictions vs outcomes; recalibrate confidence weights and prompt scoring rubrics.
- Separate "what changed" (Haiku, mechanical) from "what to do" (Opus, judgment). Mixing cost 10x and biases.
- One belief registry per product line, not per team. Cross-team write access; PM-lead has merge rights.
- Time-box rituals: Monday 30 min digest, Friday 45 min strategy — drift past that and people skip.
- Decision logs > meeting notes. A logged decision with prediction + owner + check-back is worth 10 retro pages.
- Force red-team passes: every belief change must survive a "what would have to be true for this to be wrong?" prompt.
- Limit watchlist: 3–5 competitors, 1 macro trend, 1 customer segment. Broader scope = noise.
- Bias to kill on Friday review. Default for evidence-thin items is "kill or reframe", not "keep".
- Keep the human in the loop on pricing, positioning, hiring — anything irreversible. Agents propose, humans dispose.

## AI-agent gotchas
- Memory rot: belief-updater pulled into context-window compaction loses last week's reasoning. Mitigation: persist `beliefs.yaml` + `beliefs.history.ndjson` outside the LLM and re-inject every run.
- Evidence laundering: Sonnet rewrites the same event into 3 different "independent" supports for a belief. Mitigation: dedupe by event_id hash before counting.
- Prompt bias: "summarise this week's competitor wins" yields wins. Use neutral framing: "score evidence-based threat 1-5, default 1".
- Hallucinated event_ids: model invents `event_42` that does not exist. Fact-checker pass that lookups every cited id in `events.ndjson` before publishing.
- Belief drift via summarisation: digest-of-digest-of-digest loses original wording. Always re-ground synthesizer on raw `events.ndjson`, never on previous digest.
- Recency over-weighting: cluster by week-of-year, not "last 7 days from now"; otherwise Friday digest weights different events than Monday digest of the same period.
- Confirmation loop: if the same Slack channel feeds events AND classification, you measure your own opinion velocity, not the market. Ingest at least one external corpus (analytics or competitor scrape).
- Token blow-up: dumping 10k events into Opus weekly is wasteful. Pre-cluster with Haiku, hand 50–100 archetypal events to Opus.
- Action-less insight loop: agent surfaces 200 insights/week, no decision_owner, nobody acts. Force schema field `decision_owner` or drop the event.
- Auto-publishing risk: an agent-generated digest claiming a competitor is "in trouble" leaks via Slack screenshot. Add a human review gate before any cross-org distribution.
- Calibration neglect: nobody scores last quarter's predictions, confidence weights become superstition. Quarterly grading job is not optional.

## References
- Reforge — "Speed of learning as a moat" (https://www.reforge.com/blog/learning-velocity)
- Teresa Torres — Continuous Discovery Habits (book + producttalk.org)
- Eric Ries — The Lean Startup (build-measure-learn loop)
- Annie Duke — How to Decide (decision logging, prediction calibration)
- Marty Cagan — Inspired / Empowered (product-team learning loops)
- Ben Thompson — Aggregation theory and learning-rate moats (stratechery.com)
- Andy Grove — High Output Management (decision-making cadence)
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://www.producttalk.org/opportunity-solution-tree/
- https://posthog.com/docs/api
- https://docs.gong.io
- https://eppo.cloud/docs
- https://www.statsig.com/docs
