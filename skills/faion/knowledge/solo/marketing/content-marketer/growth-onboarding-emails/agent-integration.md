# Agent Integration — Onboarding Email Sequences

## When to use
- SaaS or app with a free trial or freemium model and measurable activation steps
- Onboarding activation rate below 50% and no behavioral trigger emails in place
- Redesigning an existing time-based sequence to add behavior-triggered branches
- New product launch where the first-week user journey has been mapped but not automated
- Post-signup flow where the product has identifiable "aha moment" milestones

## When NOT to use
- Product analytics not set up — behavioral triggers require event tracking (Segment, Mixpanel, Amplitude); without data, you can only use time-based sequences
- Transactional product with no recurring engagement cycle (one-time purchase, no return usage pattern)
- User base is extremely homogeneous with a single known path to activation — a simple 3-email linear sequence may outperform complex branching
- No ESP with automation capability — behavioral triggers require Customer.io, ActiveCampaign, or Intercom, not basic Mailchimp

## Where it fails / limitations
- Trigger logic misconfiguration silently fires wrong emails to wrong segments — staging environment testing is non-negotiable
- High email frequency during onboarding (more than 1/day) causes unsubscribe spikes that hurt overall deliverability
- Personalization tokens ("You created your first project!") break when product analytics events are not reliably firing
- The "stuck user" escalation path (offer a call on Day 10) rarely scales beyond 200 new signups/month without a dedicated success team
- Onboarding emails cannot substitute for in-app guidance — they are a reminder layer, not an education layer

## Agentic workflow
Claude agents excel at drafting the full email sequence copy given a user journey map and product activation milestones. Sonnet is the right model for individual email drafting and CTA writing; Opus for designing the full branching trigger logic and segment definitions. Agents cannot configure automations inside Customer.io or ActiveCampaign — that is always a human-in-loop step. The output from agents should be: email copy per trigger event, subject line variants (3 per email), and a plain-English description of trigger conditions that a human then configures in the ESP.

### Recommended subagents
- `faion-sdd-executor-agent` — for managing the onboarding sequence build as an SDD task with QA gates
- General Claude Sonnet subagent — for drafting email copy per trigger (welcome, nudge, celebration, escalation, trial-end)

### Prompt pattern
```
Write onboarding email copy for [Product].
Trigger: user signed up but did not [action] within 24 hours.
Segment: [new + stuck]. Goal: remove blockers and drive [action].
Format: subject line, preview text (≤55 chars), body (≤120 words), one CTA button text.
Tone: helpful, personal, non-salesy.
```

```
Design the trigger logic for an 8-email onboarding sequence for [Product].
Activation milestone: [user completes X].
For each email: trigger condition, delay, goal, escalation if no action.
Output as a table: # | Trigger | Delay | Email goal | If no action.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `curl` | Customer.io, Intercom, ActiveCampaign REST APIs | Standard |
| `customerio-cli` | Official Customer.io CLI for campaign management | github.com/customerio/customerio-cli |
| `segment-cli` | Trigger test events to Segment for testing trigger logic | `npm install -g @segment/analytics-node` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Customer.io | SaaS | Yes — REST API | Best behavioral trigger engine for SaaS; event-driven campaigns |
| Intercom | SaaS | Yes — REST API | In-app + email; strong for hybrid onboarding |
| ActiveCampaign | SaaS | Yes — REST API | Powerful automation builder; steeper setup |
| Drip | SaaS | Yes — REST API | E-commerce focused but works for SaaS |
| Userpilot | SaaS | Partial | In-app + email; native onboarding flows |
| Appcues | SaaS | Partial | In-app guidance primary; email secondary |
| Postmark | SaaS | Yes — REST API | Transactional delivery layer; pair with Customer.io for reliability |
| Segment | SaaS | Yes — REST API | Event source for behavioral triggers; feeds Customer.io |

## Templates & scripts
See `templates.md` for welcome, celebration, nudge, personal-outreach, and trial-end email templates.

Minimal Python script to send a Customer.io trigger event:
```python
import requests
import json

SITE_ID = "your_site_id"
API_KEY = "your_api_key"

def trigger_event(customer_id: str, event_name: str, data: dict = None):
    url = "https://track.customer.io/api/v1/events"
    payload = {
        "name": event_name,
        "data": data or {},
        "id": customer_id,
    }
    resp = requests.post(
        url,
        auth=(SITE_ID, API_KEY),
        json=payload
    )
    return resp.status_code

# Example: fire "completed_first_action" for a user
status = trigger_event("user_123", "completed_first_action", {"action": "project_created"})
print(f"Event sent: HTTP {status}")
```

## Best practices
- Map the user journey before writing a single email — know the 3-5 milestones between signup and activation, and which one is the "aha moment"
- One email, one action: every onboarding email should have exactly one CTA; multiple CTAs split attention and reduce completion
- Behavior-triggered emails outperform time-based by 15-40% in activation rate — invest in event tracking setup before worrying about copy
- Personal tone (from a named founder or CS rep) outperforms branded templates in onboarding; plain text often outperforms HTML
- For high-value signups (enterprise domain, large company), trigger the personal outreach email (Day 10) as a human-reviewed Slack notification to a CS rep rather than fully automated
- A/B test subject lines in the first 4 hours post-send; onboarding email recency is critical — stale subject line tests are not representative
- Track "email received → action completed" conversion per email, not just open/click rate — this is the real activation metric

## AI-agent gotchas
- Trigger conditions described by agents in natural language must be translated into ESP-specific automation logic by a human — never deploy agent-described conditions directly
- Agents tend to produce overly long onboarding emails; specify ≤120 words per email in every prompt
- Personalization tokens vary by ESP (`{{customer.first_name}}` in Customer.io vs `{{subscriber.first_name}}` in ConvertKit) — always specify the ESP in the prompt
- Escalation paths (Day 10 personal outreach) require human involvement; agents should flag this as a human checkpoint in their output
- Multiple email copy variants produced by agents should be evaluated against real open/click data, not agent self-assessment of quality

## References
- https://customer.io/blog/
- https://www.intercom.com/blog
- https://reallygoodemails.com/category/onboarding/
- https://www.useronboard.com/
- https://www.appcues.com/blog
