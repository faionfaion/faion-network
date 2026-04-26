# Agent Integration — Product Hunt Launch

## When to use
- Product is polished and launch-ready; need to prepare all listing assets (copy, images, first comment)
- Need to evaluate launch readiness against the 4-week checklist before committing to a date
- Drafting the launch day email sequence and social media posts in bulk
- Post-launch: generating a retrospective/learnings document from metrics and comment threads
- Building a hunter outreach message or a "coming soon" waitlist page copy

## When NOT to use
- Product is not yet functional or requires major UX fixes — a launch will surface the problems publicly and damage credibility permanently
- No email list or community presence exists yet (< 200 warm contacts) — launch preparation matters more than the launch itself at this stage
- Planning to launch on a weekend or during a major tech event — timing is not negotiable and an agent cannot override this constraint
- Expecting an agent to upvote, comment as fake users, or coordinate inauthentic support — TOS violation and easily detected

## Where it fails / limitations
- Agents cannot post to Product Hunt or monitor the listing in real-time; human presence is mandatory on launch day
- Image and video assets require human design or dedicated design tools — agents can specify requirements but cannot generate compliant visuals
- Upvote velocity is a social phenomenon; agent-generated copy improves conversion but cannot guarantee ranking
- HN and Reddit cross-posts are separate tactics; PH launch alone does not guarantee sustained traffic after day 1
- Product Hunt's algorithm changes; guidance in the README may lag current ranking factors

## Agentic workflow
An agent is best used in two phases: (1) pre-launch asset generation — given product description, target audience, and key differentiators, produce the tagline, gallery descriptions, first comment, launch email, and social posts; (2) post-launch analysis — given the comment thread export and traffic/signup metrics, produce a retrospective with lessons learned and follow-up actions. On launch day itself, the agent can draft real-time comment responses if given the incoming comment text, but a human must post them. Allow at least 2 hours of human availability on launch day for comment moderation.

### Recommended subagents
- `faion-content-agent` (referenced in README) — asset drafting, tagline variants, first comment, email copy
- A `launch-readiness-agent` could systematically check each item in the 4-week checklist against provided context and output a gap report

### Prompt pattern
```
You are preparing a Product Hunt launch for [Product].
Product: [one-paragraph description]
Target audience: [persona]
Key differentiators: [list]
Task: Generate 5 tagline variants (each < 60 chars, benefit-focused, no jargon),
      a first comment following the PH template, and a launch day email (< 150 words).
Output: structured markdown with labeled sections.
```

```
Here is the Product Hunt comment thread export for our launch: [text].
Metrics: [upvotes, ranking, signups, traffic].
Task: (1) Identify top 3 themes in feedback.
      (2) List questions that went unanswered.
      (3) Draft a retrospective post for IndieHackers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `ph` (unofficial PH CLI) | Scrape listing data, monitor position | https://github.com/hunt-cli/ph (community) |
| Buffer CLI / API | Schedule social media posts for launch day | https://buffer.com/developers/api |
| ConvertKit API | Segment and send launch email to waitlist | https://developers.convertkit.com |
| Typefully API | Schedule and publish Twitter/X threads | https://typefully.com/developers |
| `curl` + PH API | Fetch upvote count for monitoring | https://api.producthunt.com/v2/docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Product Hunt Ship | SaaS | Partial — manual UI | Pre-launch subscriber collection; no API |
| ConvertKit | SaaS | Yes — REST API | Email list segmentation and launch send |
| Mailchimp | SaaS | Yes — REST API | Alternative to ConvertKit |
| Buffer | SaaS | Yes — REST API | Schedule all launch-day social posts in advance |
| Typefully | SaaS | Yes — API | Twitter/X thread scheduling |
| Figma | SaaS | Partial — export API | Gallery image creation (requires design work) |
| Loom / Screen Studio | SaaS | No — manual recording | Demo video; agent can script narration |

## Templates & scripts
See templates.md for: first comment template, launch day email, social media post.

Inline script — check launch day timing (is it optimal?):

```python
from datetime import datetime
import pytz

def check_launch_timing(iso_datetime_str: str) -> dict:
    """Evaluate a proposed PH launch time."""
    pt = pytz.timezone("America/Los_Angeles")
    dt = datetime.fromisoformat(iso_datetime_str).astimezone(pt)
    issues = []

    if dt.hour != 0 or dt.minute != 1:
        issues.append(f"Not 12:01 AM PT — launches lose ranking hours (got {dt.strftime('%H:%M')} PT)")
    if dt.weekday() not in (1, 2, 3):  # Tue, Wed, Thu
        issues.append(f"Not Tue-Thu — weekends/Mondays have lower traffic (got {dt.strftime('%A')})")

    return {"ok": len(issues) == 0, "issues": issues, "local_time_pt": dt.isoformat()}

# Example usage:
print(check_launch_timing("2025-06-04T00:01:00-07:00"))
```

## Best practices
- Write the first comment before launch day and have it ready to paste within 60 seconds of the post going live — early velocity is critical
- Request the hunt from a hunter with 1,000+ followers in the same niche; hunter audience overlap with your product category matters more than raw follower count
- Prepare canned responses for the 5 most likely comment types (how does X work, what's the pricing, is there a free trial, how does it compare to Y, can I use it for Z) — agent can draft these in advance
- Do not use launch day to announce unfinished features; HN/PH commenters will test everything mentioned and negative comments compound fast
- Add a dedicated landing page URL for PH traffic (e.g., `/welcome-producthunters`) with a custom offer and tracking — measure conversion separately from organic traffic
- Post the retrospective on IndieHackers within 48 hours while the launch is fresh — it doubles as marketing and community building

## AI-agent gotchas
- Agents may generate taglines that exceed the 60-character limit; always validate length programmatically after generation
- First comment drafts often sound too polished/corporate — instruct agent to write in first-person casual voice and review for authenticity before posting
- Agents cannot monitor real-time upvote velocity or detect if the post is being flagged — human must watch the dashboard
- Human-in-loop checkpoint: agent drafts responses to comments; human reviews and posts — never allow fully automated comment posting on a public platform
- Launch day email timing is critical; agent-generated send schedules should be validated against the subscriber timezone distribution before execution
- Agents may include calls to action that violate PH TOS ("upvote us", "share with your network") — explicitly forbid this in the system prompt

## References
- https://www.producthunt.com/launch — Official PH launch checklist and guidelines
- https://www.ycombinator.com/library/6f-a-guide-to-product-hunt — YC's PH strategy guide
- https://api.producthunt.com/v2/docs — Product Hunt GraphQL API (monitoring, listing data)
- https://www.producthunt.com/ship — Pre-launch subscriber collection tool
- https://makermag.com/ — Real launch retrospectives and case studies
