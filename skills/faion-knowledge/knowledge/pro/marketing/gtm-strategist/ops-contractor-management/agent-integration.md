# Agent Integration — Contractor Management

## When to use
- Onboarding a freshly-hired contractor: build doc pack, provision tooling, schedule check-ins.
- Running weekly/monthly check-ins where status reports must be aggregated across multiple contractors.
- Drafting structured feedback (SBI-R format) from observed work output.
- Performance evaluation cycles: synthesize a review from logged tasks, time entries, and quality signals.
- Standardizing communication rhythm across an async, multi-timezone roster.

## When NOT to use
- Pre-hire screening — use `ops-contractor-basics` for sourcing, ROI, paid-test design.
- Conflict resolution / termination conversations — human-only; agents can prep facts but never deliver.
- Performance issues that may signal misclassification — escalate to legal before adjusting management cadence.
- Managing a team of W-2 employees — different feedback frameworks (1:1s, OKRs, comp reviews).

## Where it fails / limitations
- Source README assumes single-PM single-contractor; doesn't cover contractor-managing-contractor or pod structures.
- SBI feedback framework is helpful as scaffolding but cannot capture nuance of repeated underperformance — human judgment required.
- Time tracking metrics are vulnerable to gaming; the methodology trusts self-reported hours.
- No guidance on contractor-to-employee conversion (visa, comp, equity) — out of scope.
- Cross-cultural feedback norms differ widely; the SBI template reads as US/Western-direct and may need softening for some markets.

## Agentic workflow
Treat the agent as a contractor ops layer: it ingests Slack/Loom transcripts, time-tracker exports, and PR/asset deliverables, then emits weekly status digests, missed-deadline alerts, and draft feedback notes. The principal reviews and personalizes before sending. Pair with `ops-contractor-basics` (pre-hire) and `ops-legal-basics` (contracts, IP assignment). For payment workflows, drive Deel/Wise/Stripe Connect via their REST APIs.

### Recommended subagents
- `faion-growth-agent` (source README) — owns the management loop; drafts check-in notes, evaluations.
- `faion-feature-executor` — when contractor work is dev-tracked in SDD tasks, sequence and gate task acceptance.
- `faion-improver` — quarterly: identify recurring blockers across contractor pool and propose process fixes.
- General-purpose Claude subagent for SBI feedback drafting: prompt with situation/behavior/impact triples, generate request.

### Prompt pattern
```
You have <contractor>'s last 4 weekly check-ins (attached) and the original SOW.
Output: (1) trend summary 3 bullets, (2) one risk to flag, (3) draft monthly review
using the framework Quality/Communication/Reliability/Speed/Proactiveness, 1-5 + notes.
Stay neutral; do not recommend continue/end — that's the human's call.
```

```
Convert this raw observation into SBI-R feedback (max 100 words):
"<contractor> shipped pricing-page redesign 2 days late, but the design lifted conv from 2% to 3.4% per Friday A/B test"
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` | Track contractor PRs, review diffs, gate merges | `brew install gh` |
| `slack-cli` (rtmbot or slack-sdk) | Pull thread history for status digests | pypi.org/project/slack-sdk |
| `toggl` API client | Pull time entries by user/project | github.com/toggl/toggl_api_docs |
| `harvest` CLI | Pull invoiced hours, project budgets | help.getharvest.com/api-v2 |
| `linear` CLI | Sync contractor task list, priorities | developers.linear.app |
| `loom` API | Pull async-video update transcripts | loom.com/developers |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deel | SaaS | Yes | API: contracts, time, milestones, payments. End-to-end agent-drivable. |
| Remote.com | SaaS | Yes | Similar to Deel; stronger in EU. |
| Bonsai | SaaS | Yes | Solo-friendly: contracts + time + invoicing in one API. |
| Notion | SaaS | Yes | Source of truth for SOWs, playbooks, onboarding docs. Strong API. |
| Linear | SaaS | Yes | Best-in-class API for task assignment + status. |
| Asana | SaaS | Yes | API for project tracking; weaker than Linear for dev work. |
| Slack | SaaS | Yes | API for digests, async standups, alerts. |
| Loom | SaaS | Partial | Transcripts via API (paid plan); video content not parseable. |
| Toggl / Harvest / Clockify | SaaS | Yes | All have time-tracking APIs; pick one and stick. |
| DocuSign / HelloSign | SaaS | Yes | E-sign new SOW addenda programmatically. |

## Templates & scripts
See `templates.md` for weekly check-in, evaluation, and SOW addendum templates. Inline status-digest aggregator:

```python
# Weekly contractor status digest from Slack channel
import os
from slack_sdk import WebClient

def weekly_digest(channel_id, contractor_user_id, days=7):
    cli = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    import time
    oldest = time.time() - days * 86400
    history = cli.conversations_history(channel=channel_id, oldest=oldest)
    msgs = [m for m in history["messages"] if m.get("user") == contractor_user_id]
    return {
        "msg_count": len(msgs),
        "first": msgs[-1]["text"] if msgs else None,
        "last": msgs[0]["text"] if msgs else None,
        "raw": [m["text"] for m in msgs],
    }
```

## Best practices
- Front-load documentation: a complete onboarding pack pays back within the first deliverable cycle.
- Define "done" with examples, not adjectives. "Match this past piece" beats "high quality."
- Use async-first communication (Slack threads + Loom) and reserve sync calls for ambiguous problems only.
- Run a structured monthly review even when nothing's wrong — small frictions surface only when prompted.
- Log feedback the same week the behavior happens; SBI loses signal at one-month delay.
- Treat the contractor like a contractor: avoid setting fixed working hours, providing all tools, or branding them as your team to clients (misclassification flags).
- Maintain a "contractor onboarding kit" repo (Notion or git) that ships intact to every new contractor — versioned, reviewed quarterly.

## AI-agent gotchas
- LLM-generated feedback drifts towards mealy-mouthed praise. Force the SBI structure and require the agent to include at least one concrete behavior + measurable impact.
- Agents over-trust time-tracker self-reports; cross-check against PR/commit/asset volume before passing through to evaluations.
- When digesting Slack, agents lose tone — sarcasm and friction signals are flattened. Flag any thread with >5 back-and-forth messages for human read.
- Do not let agent auto-pay invoices. Mandatory human approval per invoice; misissuance vs disputed work is hard to claw back across borders.
- Confidentiality leakage: agents pulling Slack/Notion may surface sensitive customer data into LLM context. Use redaction step before any external-API LLM call.
- Auto-generated SOW addenda often re-introduce default IP/confidentiality clauses that may conflict with the master agreement. Always diff against the signed master before sending.
- Token economics: ingesting 4 weeks of Slack history per contractor is multi-100k tokens. Pre-summarize daily, cache, then reduce.

## References
- April Dunford on operating cadence — https://www.aprildunford.com/
- SBI feedback model (CCL) — https://www.ccl.org/articles/leading-effectively-articles/closing-the-gap-between-intention-and-action-with-sbi/
- Deel contractor management — https://www.deel.com/resources/contractor-management
- Loom async communication guide — https://www.loom.com/blog/async-communication
- Sibling methodology: `ops-contractor-basics/README.md`
- Sibling methodology: `ops-legal-basics/README.md` (contractor agreement + IP clauses)
