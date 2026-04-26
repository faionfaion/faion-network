# Agent Integration — Customer Support

## When to use
- Setting up the first support system (self-serve docs, email SLAs, templates)
- Ticket volume is growing and responses are ad-hoc; need templates and triage
- Conducting weekly support review: pattern extraction, FAQ gap identification
- Drafting or updating a support policy document
- Mining support tickets for product insight (recurring pain points → roadmap)

## When NOT to use
- Real-time live chat or voice support — requires a human in the loop, not an agent
- Legal or financial issues raised via support — escalate to counsel/accountant immediately
- Incidents affecting all users (outages, data loss) — use a dedicated incident response process, not a support agent
- Highly sensitive topics (account termination disputes, fraud) — human judgment required

## Where it fails / limitations
- Agents cannot access live ticket data without integration to Intercom, Zendesk, or Help Scout APIs
- Automated responses risk sounding generic; personalization requires injecting customer context (plan, history)
- CSAT measurement requires a survey tool; agents cannot measure satisfaction directly
- Pattern detection from tickets requires a structured export — agents cannot browse a ticketing UI
- Agents must not promise specific fixes or timelines without human confirmation of feasibility

## Agentic workflow
An agent can own the weekly support review cycle end-to-end if given a structured ticket export:
ingest the export, categorize tickets by type (bug / how-to / feature request / billing), count
patterns, flag the top three recurring issues, and generate a draft review document with suggested
FAQ additions. A second agent pass can draft template responses for the top recurring questions.
Human review is required before publishing any new FAQ article or sending templated responses.

### Recommended subagents
- `faion-growth-agent` (referenced in README) — support process design, template generation, review reports
- A `support-triage-agent` could auto-categorize incoming tickets and draft first-response acknowledgments from a ticket queue export

### Prompt pattern
```
You are a customer support agent for [Product].
Ticket: """[raw ticket text]"""
Customer plan: [Free/Pro/Enterprise].
Task: (1) Categorize this ticket (bug/how-to/feature/billing).
      (2) Draft a resolution response using the templates in context.
      (3) If the issue is a bug, flag it with severity (critical/high/medium).
Output: JSON with fields: category, severity, draft_response.
```

```
Here is a CSV export of this week's support tickets: [data].
Task: (1) Count tickets by category.
      (2) Identify top 3 recurring issues (5+ similar tickets).
      (3) For each recurring issue, suggest a FAQ article title and one-sentence summary.
Output: markdown report matching the Weekly Support Review template.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `zendesk-cli` (unofficial) | Export tickets, update statuses | https://github.com/zendesk/zendesk_apps_tools |
| Intercom CLI / `intercom-python` | Pull conversations via API | https://github.com/intercom/intercom-python |
| Help Scout API (REST) | List conversations, post replies | https://developer.helpscout.com |
| `jq` | Parse JSON ticket exports for pattern counting | stdlib on most systems |
| `miller` (`mlr`) | Aggregate CSV ticket exports by category | https://miller.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Intercom | SaaS | Yes — REST API | Conversations, notes, tags; webhook for new tickets |
| Zendesk | SaaS | Yes — REST API | Full ticket lifecycle; bulk export available |
| Help Scout | SaaS | Yes — REST API | Simpler than Zendesk; good for solopreneurs |
| Crisp | SaaS | Yes — REST API | Affordable; includes knowledge base and chat |
| Tawk.to | SaaS (free tier) | Partial — webhook only | No outbound API for replies |
| Linear | SaaS | Yes — REST/GraphQL | Convert bug tickets to issues automatically |

## Templates & scripts
See templates.md for full response templates (acknowledgment, resolution, review doc).

Inline script — weekly ticket pattern summary from a CSV export:

```python
import csv, sys
from collections import Counter

# Expects CSV with columns: id, category, subject
tickets = list(csv.DictReader(open(sys.argv[1])))
counts = Counter(t["category"] for t in tickets)

print("## Weekly Support Volume")
for cat, n in counts.most_common():
    print(f"- {cat}: {n} ({100*n/len(tickets):.0f}%)")

print(f"\nTotal: {len(tickets)}")
```

## Best practices
- Build self-serve (FAQ, knowledge base) before adding any async support channel — agents can draft articles from existing ticket data
- Respond to the first support ticket from any paying customer within 4 hours regardless of SLA tier; first impressions determine churn risk
- Keep response templates in a structured format (YAML or JSON) so agents can select and fill them programmatically without reformatting
- Use ticket categories as product signals: if how-to tickets for a specific feature exceed 20% of volume, that feature needs UX work, not more documentation
- Set explicit support hours in the product UI and auto-reply; an agent can generate the out-of-hours message automatically
- Never let an agent send a response with a specific commit, deadline, or "we will fix this by [date]" — those require human sign-off

## AI-agent gotchas
- Agents may hallucinate product behavior if given only the ticket text without current product documentation as context
- Sensitive tickets (billing disputes, data deletion requests) must never be handled automatically — build a hard filter to route these to human queue
- GDPR/data privacy: ticket data often contains PII; agents processing it must run in an environment with appropriate data handling controls
- Tone calibration: agents default to neutral-formal; for consumer products, inject explicit tone guidelines ("friendly, empathetic, first-person")
- Human-in-loop checkpoint: any response that includes a refund, credit, or plan change must be queued for human approval before sending
- Agents should not mark tickets as resolved automatically — only draft the response; resolution confirmation requires human action

## References
- https://www.zendesk.com/resources/customer-service-best-practices/ — Industry benchmarks and SLA guidance
- https://www.helpscout.com/blog/customer-service/ — Practical support management for small teams
- https://www.intercom.com/resources/customer-support — Modern support strategy with automation
- https://developer.helpscout.com — Help Scout API reference for agent integration
- https://www.crisp.chat/docs/api/v1/ — Crisp REST API docs (affordable alternative for solopreneurs)
