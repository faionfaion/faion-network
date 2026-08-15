# Agent Integration — Feedback Management

## When to use
- Feedback is arriving from 3+ channels (support, in-app, app stores, social, sales) and a human can no longer triage in real time.
- You want a periodic (daily / weekly) digest with categorized, deduplicated, prioritized requests linked to backlog items.
- You need automated "close-the-loop" emails when a requested feature ships.
- Sentiment tracking against a release or pricing change is required.

## When NOT to use
- < 20 feedback items per week — manual handling beats pipeline overhead.
- High-stakes B2B accounts where every quote requires named-customer context — keep human in the loop end-to-end.
- Regulated industries (medical, finance) where verbatim handling has compliance constraints (PII redaction first, then categorize).

## Where it fails / limitations
- LLM categorization drifts when the taxonomy is fuzzy; lock taxonomy in code, treat changes as schema migrations.
- Sentiment models misread sarcasm and Ukrainian/mixed-language text — calibrate per locale.
- Volume bias: loud users post 10 tickets, quiet ones post zero. Weighting by user/segment matters more than raw counts.
- Closing the loop at scale via email risks spam complaints — segment by recency of request.
- Feature-request "votes" inside tools like Canny correlate poorly with retention impact; never use vote count alone for prioritization.

## Agentic workflow
Run a triage subagent on every new feedback item: it outputs `{type, topic, sentiment, segment, dedup_id, severity, suggested_backlog_link}` as structured JSON, never free text. A weekly aggregator subagent groups by `topic + dedup_id`, surfaces top requests with mention counts and segment breakdown, and proposes 1–3 backlog candidates with draft RICE Reach numbers. A close-loop subagent watches the deploy pipeline and, when a backlog item linked to ≥ N feedback rows ships, drafts personalized "you asked, we built" emails for human approval before send.

### Recommended subagents
- `faion-mlp-gap-finder-agent` — feedback analysis agent named in this methodology's metadata.
- `faion-mlp-feature-proposer-agent` — converts top feedback clusters into RICE-ready candidates.
- `password-scrubber-agent` (already in `agents/`) — strip secrets/PII from raw feedback before storing.
- General-purpose `researcher` — pulls competitor patterns when feedback hints at a category gap.

### Prompt pattern
```
Triage one feedback item. Output JSON only:
{
  "type": "bug|request|enhancement|confusion|praise|complaint",
  "topic": "<one of [taxonomy ids]>",
  "sentiment": "positive|neutral|negative",
  "segment": "<plan or persona>",
  "severity": 1-5,
  "dedup_hash": "<sha1 of normalized verbatim>",
  "suggested_backlog_link": "<existing issue id or null>",
  "rationale": "<<= 240 chars>"
}
Reject if you would invent a topic outside the supplied taxonomy.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `intercom-cli` / Intercom REST API | Pull conversations, tag, push notes | https://developers.intercom.com |
| Zendesk API + `zendesk` Python SDK | Tickets, satisfaction, macros | https://developer.zendesk.com |
| Front API | Unified inbox feedback ingestion | https://dev.frontapp.com |
| Canny API | Feature requests + votes + status | https://developers.canny.io |
| Productboard API | Insights + linkage to features | https://developer.productboard.com |
| Slack API + `slack-cli` | Pull #feedback channels, post digests | https://api.slack.com |
| Telegram Bot API | Ingest feedback from TG channels (NERO uses this) | https://core.telegram.org/bots/api |
| `app_store_connect_api` (Python) / RSS | App Store / Play Store reviews | https://developer.apple.com/documentation/appstoreconnectapi |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Canny | SaaS | Yes (REST + webhooks) | Public boards, votes, status changes ideal for agent close-loop |
| Productboard | SaaS | Yes (REST) | Insights → features → roadmap; native prioritization |
| Savio | SaaS | Yes (REST) | Aggregates from Intercom/Zendesk/Slack |
| Olvy | SaaS | Yes (REST) | Combines feedback + changelog (close-loop in one tool) |
| Frill | SaaS | Yes (REST) | Lightweight Canny alternative |
| Fider | OSS (self-host) | Yes (REST) | Free Canny-style board |
| Featurebase | SaaS | Yes (REST) | Roadmap + feedback + changelog combo |
| Dovetail | SaaS | Partial | Research repo with API for tags/highlights |

## Templates & scripts
See `templates.md` for the feedback log and response email templates. Pipeline skeleton (Python pseudo-code, ≤ 50 lines):

```python
# triage.py — one new item -> structured row
import json, hashlib, sys
TAXONOMY = ["onboarding","billing","integrations","perf","auth","mobile","other"]

def normalize(text: str) -> str:
    return " ".join(text.lower().split())

def dedup(text: str) -> str:
    return hashlib.sha1(normalize(text).encode()).hexdigest()[:10]

def triage_via_llm(text: str) -> dict:
    # call Claude with strict JSON schema, validate
    raise NotImplementedError

def main():
    item = json.load(sys.stdin)  # {source, user_id, segment, text}
    out = triage_via_llm(item["text"])
    out["dedup_hash"] = dedup(item["text"])
    out["source"] = item["source"]
    out["user_id"] = item["user_id"]
    if out["topic"] not in TAXONOMY:
        out["topic"] = "other"
    json.dump(out, sys.stdout)

if __name__ == "__main__":
    main()
```

## Best practices
- Lock the taxonomy in a versioned file; require a migration script + re-tag run when it changes.
- Always store the verbatim alongside structured fields — never lose the original quote.
- Weight feedback by ARR / segment, not raw mention count. One enterprise complaint can outweigh 50 free-tier votes.
- Run a quarterly "drift audit" — sample 50 LLM-categorized items, have a human re-tag, measure agreement.
- Close the loop within 30 days of ship — agents can draft, humans approve, system sends.
- Track "feedback → roadmap" conversion rate as an internal KPI; if < 5%, the funnel is decorative.

## AI-agent gotchas
- Strip PII before sending raw feedback to the LLM (emails, phone numbers, account IDs). Use `password-scrubber-agent` or a regex pre-pass.
- Auto-responding without human review is a brand risk. Default agentic mode = "draft and queue", human approves send.
- LLMs over-categorize as "enhancement" (catch-all). Force the model to pick "bug" when a verb like "broken / can't / fails" appears.
- Dedup naively on full text misses paraphrases; use embedding similarity (e.g., text-embedding-3-small with cosine ≥ 0.85) for true clustering.
- Sentiment ≠ priority. A polite "would be nice" can mask a churn-driver; cross-reference with retention data.
- Human-in-loop checkpoints: (a) before any outbound message, (b) before promoting a feedback cluster to a roadmap item, (c) before changing taxonomy.

## References
- Teresa Torres, "Continuous Discovery Habits" — feedback-to-opportunity tree pattern.
- Productboard "Insights" framework https://www.productboard.com/glossary/customer-feedback/
- Intercom blog — "How we triage product feedback" https://www.intercom.com/blog/
- Lenny's Newsletter — "How top PMs handle customer feedback at scale" https://www.lennysnewsletter.com/
