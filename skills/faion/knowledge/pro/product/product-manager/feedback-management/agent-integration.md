# Agent Integration — Feedback Management

## When to use

- Inbound feedback volume exceeds human triage capacity (>20 items/day across channels).
- Multiple disconnected sources (support tickets, app store reviews, in-app widget, social, sales notes) need a single canonical store.
- Recurring monthly review cycle exists where patterns must be surfaced, ranked by segment + revenue, and linked to backlog items.
- Closing-the-loop emails to specific requesters are repetitive but high-leverage and must reference the original verbatim quote.
- Pre-roadmap sessions where PM needs "top 10 themes from last 90 days, with verbatim citations and segment breakdown."

## When NOT to use

- Pre-PMF, when total feedback volume is low (<5 items/week) — direct human reading is faster and richer.
- High-stakes strategic decisions (pivot, kill) where the verbatim nuance matters more than the count.
- Compliance-bound feedback (HIPAA, GDPR DSAR text) where LLM ingestion needs DPA review first.
- Sentiment-only loops with no commitment to act — automation amplifies noise without closing the loop.
- Single-channel products where the channel tool's native AI (Intercom Fin, Zendesk QA) already does the categorization.

## Where it fails / limitations

- LLM categorization drifts: same feedback labelled "billing" on Monday and "pricing" on Friday unless the taxonomy is pinned in the prompt and validated.
- Duplicate detection on embeddings is fragile for short messages ("doesn't work", "broken") — needs context window from the source thread.
- Aggregation by mention count rewards the loud minority; weight by segment ARR + retention risk or it just reproduces the squeaky-wheel bias.
- Auto-generated "you asked, we built" emails sound robotic and erode trust if the user's verbatim is paraphrased away — keep the original quote in the email body.
- Feedback from prospects (sales calls) and churned users cannot be replied to via the same close-the-loop flow; agents conflate them unless lifecycle stage is a required tag.

## Agentic workflow

Drive feedback management as a five-stage pipeline (ingest → dedupe → tag → aggregate → close-loop), each stage a discrete subagent invocation with structured I/O. Use one agent per stage rather than a monolithic "feedback agent" so failures are isolated and prompts stay short. Persist state as JSON in the feedback store (Productboard/Canny/Linear/Notion) — never trust a single agent run's in-memory state. The PM stays human-in-the-loop on prioritization decisions and all outbound user replies.

### Recommended subagents

- `faion-mlp-gap-finder-agent` — already referenced in the README; consume aggregated feedback to surface gaps between current MLP and user requests.
- `faion-sdd-executor-agent` — once a feedback theme becomes a backlog item, hand to this agent for spec/design generation in `.aidocs/backlog/`.
- Custom `feedback-triage-agent` (Haiku) — categorize one item at a time against a fixed taxonomy. Cheap, fast, parallelizable.
- Custom `feedback-aggregator-agent` (Sonnet) — weekly/monthly: cluster, count, weight by segment, output ranked themes with verbatim citations.
- `faion-brainstorm` skill — for open-ended "what does this batch of confused-onboarding feedback really mean?" diverge-converge.

### Prompt pattern

```
You are a feedback triage agent. Taxonomy (FIXED, do not invent new tags):
TYPE: [bug|request|enhancement|confusion|praise|complaint]
TOPIC: [onboarding|core-A|core-B|billing|integrations|performance|other]
SEGMENT: [free|solo|pro|geek|unknown]
SENTIMENT: [positive|neutral|negative]

Input: {verbatim} from {source} by user {user_id} on {date}.
Output JSON: {type, topic, segment, sentiment, duplicate_of?, confidence_0_1, action_required: [build|wont_do|need_info|already_planned]}
If confidence < 0.7 OR topic == "other", set action_required = "need_info" and stop.
```

```
You are a close-the-loop drafter. Input: shipped feature X, list of N feedback items that requested it (with verbatim, user_id, date).
Output: N personalized emails. Each MUST quote the user's original verbatim verbatim (not paraphrased), reference the date, and link to the changelog. Do not send — return drafts for human review.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear-cli` (`@linear/cli`) | Create/update issues from feedback themes via Linear API | `npm i -g @linear/cli`; docs.linear.app |
| `gh` | Mine GitHub Issues + Discussions for feedback signal | preinstalled; `gh issue list --label feedback` |
| `jq` | Parse triage agent JSON output before piping to issue tracker | apt/brew |
| `intercom-cli` (community) | Pull conversations tagged `feedback` for batch ingest | github.com/intercom/intercom-node |
| `zendesk` (`zcli`) | Pull tickets, push macros for close-loop replies | developer.zendesk.com/zcli |
| `discourse_api` | Pull community forum posts as feedback source | discourse-api gem / pip pkg |
| `play-scraper` / `app-store-scraper` | Pull app-store reviews in JSON | npm packages |
| `slack-cli` | Pull `#feedback` channel messages, react with status emoji | api.slack.com/automation/cli |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Productboard | SaaS | Yes (REST API, webhooks) | Strongest object model: Insights → Features → Releases. AI add-on $20/maker/mo. Ideal central store. |
| Canny | SaaS | Yes (REST API, Autopilot ingest from Intercom/Slack/email) | Public boards + voting. Native AI categorization on higher tiers. Best for public-facing feedback. |
| FeatureOS | SaaS | Yes | AI categorization + sentiment + duplicate detection on Starter tier. Cheaper Canny alternative. |
| Featurebase | SaaS | Yes | Lightweight, public roadmap + voting + API. |
| UserJot, Quackback, Heedback | SaaS | Partial | Smaller players; APIs vary, check before committing. |
| Linear | SaaS | Excellent (GraphQL API, webhook events) | Use as backlog destination, not feedback store; link insights via custom field. |
| Notion | SaaS | OK (API, but rate-limited) | Cheap MVP for <500 items/month; outgrows fast. |
| Fider | OSS, self-host | Yes (REST API) | Open-source Canny-equivalent; run on faion-net for free tier. |
| Astuto | OSS, self-host | Yes (REST API) | OSS feature voting; Postgres + Rails. |
| Dovetail | SaaS | Yes (API + AI tags) | Strongest for qualitative interview transcripts, not real-time feedback. |

## Templates & scripts

Inline triage helper (≤50 lines, Bash + Anthropic API). Pipes any feedback file to a Haiku triage agent and emits one JSON line per item. Use as the first stage before pushing to Productboard/Linear.

```bash
#!/usr/bin/env bash
# triage-feedback.sh — categorize feedback items via Claude Haiku
# Usage: cat feedback.txt | ./triage-feedback.sh > triaged.jsonl
# Each input line: ISO_DATE\tSOURCE\tUSER_ID\tVERBATIM
set -euo pipefail
: "${ANTHROPIC_API_KEY:?set ANTHROPIC_API_KEY}"

SYSTEM='You are a feedback triage agent. Output ONLY one JSON object, no prose.
Schema: {"type":"bug|request|enhancement|confusion|praise|complaint",
"topic":"onboarding|core-A|core-B|billing|integrations|performance|other",
"segment":"free|solo|pro|geek|unknown",
"sentiment":"positive|neutral|negative",
"confidence":0.0,
"action_required":"build|wont_do|need_info|already_planned"}
If confidence<0.7 set action_required="need_info".'

while IFS=$'\t' read -r date source user verbatim; do
  body=$(jq -nc --arg s "$SYSTEM" --arg u "Date:$date Source:$source User:$user Verbatim:$verbatim" \
    '{model:"claude-haiku-4-5", max_tokens:300, system:$s, messages:[{role:"user", content:$u}]}')
  resp=$(curl -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "$body" | jq -r '.content[0].text')
  jq -nc --argjson t "$resp" --arg d "$date" --arg s "$source" --arg u "$user" --arg v "$verbatim" \
    '{date:$d, source:$s, user:$u, verbatim:$v} + $t'
done
```

Beyond this, see `templates.md` for the Feedback Log table and the three close-loop email skeletons (shipped / not-planned / more-info).

## Best practices

- Pin the taxonomy in the system prompt and in a JSON schema; reject any agent output with tags outside the enum. Drift kills aggregation.
- Always store the original verbatim alongside tags. Never let the agent rewrite the user's words — re-tagging later is impossible without the source string.
- Weight aggregations by ARR / retention risk / segment, not raw mention count. A loud free-tier user is not the same signal as a silent enterprise account.
- Run the triage agent at single-item granularity, not in batches. Batch prompts hide per-item confidence scores and cause the model to over-cluster.
- Require a `confidence` field; route low-confidence items to a human queue, not to auto-action.
- Keep close-loop emails as *drafts* in the human's inbox, never auto-send. Trust collapses fast if a generated reply misquotes the user.
- Link every backlog item back to its source feedback IDs (foreign key, not free-text). Lets you re-contact requesters when shipped.
- Re-run categorization quarterly on the historical corpus when the taxonomy evolves — agents make this cheap, humans don't.
- Keep a "rejected suggestions" log with the honest reason. Builds trust and prevents the same idea recurring through the funnel.

## AI-agent gotchas

- LLMs invent new tags ("UI/UX", "minor bug") even when given an enum — enforce with JSON schema validation, not prompt politeness.
- Embedding-based dedup gives false positives on short generic complaints ("slow", "broken"); always require a length floor (~30 chars) or include thread context.
- Sentiment models read sarcasm wrong ~20% of the time; never use sentiment alone to gate priority.
- Agents conflate prospects, active users, and churned users. Lifecycle stage must be a required input field, not optional.
- "Top requests by mention count" output flatters the agent and the loud minority simultaneously. Force a segment-weighted secondary ranking.
- Close-loop drafts hallucinate dates ("you mentioned this last quarter") if the source date isn't passed in. Pass it; verify it.
- Auto-creating Linear/Productboard items on every feedback-tagged ticket floods the backlog. Require a clustering step (≥3 mentions same theme) before issue creation.
- Long agent context windows tempt "load all 6 months of feedback at once" — accuracy drops sharply past ~100 items per call. Chunk and reduce.
- Pre-commit hook in this repo blocks agent-generated content if `print()` statements or T20 violations leak from a Python triage script — keep scripts clean.

## References

- Productboard API — developer.productboard.com
- Canny API + Autopilot — developers.canny.io
- Marty Cagan, *Inspired* (2017) — feedback as discovery input, not roadmap fuel
- Teresa Torres, *Continuous Discovery Habits* (2021) — opportunity solution trees from feedback
- Intercom, *Intercom on Customer Engagement* — close-loop messaging patterns
- Linear API GraphQL reference — linear.app/docs/api
- Anthropic, *Building effective agents* (2024) — chained vs. orchestrated agents pattern
- Featurebase, ProductLift 2026 comparisons — current SaaS landscape (search: "Canny vs Productboard 2026")
