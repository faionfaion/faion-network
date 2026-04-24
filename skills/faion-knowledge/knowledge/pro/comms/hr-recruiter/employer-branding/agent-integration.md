# Agent Integration — Employer Branding

## When to use
- Running an annual or quarterly employer-brand audit: scrape Glassdoor + LinkedIn + Comparably, summarize themes, benchmark against competitors.
- Producing the employer-brand content calendar (4-week or 12-week) across LinkedIn, Instagram, careers blog, and YouTube.
- Drafting and rotating employee testimonials, day-in-the-life posts, and culture-moment content from employee-supplied raw material.
- Monitoring and responding to Glassdoor / Indeed / Comparably reviews within 48h SLA, with consistent tone and approved language.
- Onboarding a talent community (rejected-but-strong candidates) into a monthly newsletter pipeline.

## When NOT to use
- The company has no EVP or culture document — branding work without those produces inauthentic output. Do `employee-value-proposition` first.
- Crisis comms (layoffs, PR incident) — switch to `crisis-communication` and `legal-review` workflow; brand agents will produce tone-deaf copy.
- Highly regulated industries (defense, financial services) where every external post needs compliance review — agents can draft but cannot publish.
- Sub-30-employee companies — the founder's voice is the brand; structured content calendars are overkill.

## Where it fails / limitations
- Glassdoor and Indeed terms of service prohibit automated scraping; agent should use official APIs (Glassdoor for Employers) or human-driven exports.
- LLMs generate sycophantic testimonials that read AI-written; require employee-supplied raw quotes and editorial oversight.
- Content calendars degrade after 4–6 weeks of mechanical execution; humans must inject novelty (events, milestones, real moments).
- DEI content without internal lived experience produces tokenism; agents should never invent ERG names, programs, or diversity stats.
- Cross-platform tone is hard: the same post in LinkedIn voice vs. TikTok voice needs different drafts; agents trained on one channel produce flat copy on others.
- Glassdoor responses must be carefully worded — over-defensive reactions go viral. Always human approval before submission.

## Agentic workflow
A recurring agent (cron-driven via `schedule` skill) ingests review feeds, extracts themes, and drafts response options for human approval. A separate "content calendar" agent generates 4 weeks of posts from EVP pillars, rotates content types, and produces channel-specific drafts. A third agent runs the testimonial intake pipeline: employee fills a short form (Typeform/Notion), agent drafts polished version, human + employee approve, then publish via Buffer/Hootsuite.

### Recommended subagents
- `faion-employer-brand-agent` (referenced in README) — owns the brand domain.
- `faion-marketing-manager` knowledge — for content calendar structure and channel best practices.
- A custom `glassdoor-monitor` agent (sonnet) on a daily `schedule` — pulls new reviews, drafts responses, posts to Slack for human approval.
- `faion-recruiter-agent` — outbound recruiter messages aligned to brand pillars.
- `faion-improver` — quarterly retrospective on what brand content drove applications vs. flopped.

### Prompt pattern
```
Given EVP pillars <pillars.md> and last 4 weeks of LinkedIn analytics
<analytics.csv>, draft a 4-week content calendar:
- Week 1: employee spotlight (request quote from <employee_name>)
- Week 2: behind-the-scenes (Instagram-friendly, ≤90s video brief)
- Week 3: culture moment (LinkedIn long-form, ≤300 words)
- Week 4: open role promo (LinkedIn + Indeed)
For each, output: hook, body, CTA, hashtags, asset brief.
```

```
New Glassdoor review at <url>. Sentiment <pos|neg|mixed>.
Draft a response in <company> voice:
- thank reviewer
- acknowledge specific feedback (no defensiveness)
- describe action taken or planned (only if true)
- ≤80 words, no "We are committed to..." cliché
- mark UNVERIFIED any claim that cannot be substantiated
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI | Push careers-page content to repo | https://cli.github.com |
| `playwright` | Headless browser for review scraping (where ToS-allowed) | `npm i -D @playwright/test` |
| `pandoc` | Convert briefs MD ↔ DOCX for stakeholder review | OS package |
| `csvkit` | Slice analytics exports | `pip install csvkit` |
| `ffmpeg` / `ffprobe` | Process testimonial videos (cut, normalize, captions) | OS package |
| `whisper.cpp` | Transcribe video testimonials → captions | https://github.com/ggerganov/whisper.cpp |
| `op` | Pull API tokens (Buffer, Glassdoor, LinkedIn) | https://developer.1password.com/docs/cli |
| `jq` | Parse Glassdoor / LinkedIn JSON responses | OS package |
| `imagemagick` | Resize / watermark testimonial images | OS package |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Glassdoor for Employers | SaaS | Partial | Reviews API for enterprise tiers; otherwise read via dashboard. |
| Indeed Employer / Comparably | SaaS | Partial | Limited APIs; mostly UI-driven. |
| LinkedIn Talent Solutions | SaaS | Yes | Career pages, sponsored posts, follower analytics via API. |
| Buffer / Hootsuite / Sprout Social | SaaS | Yes | Schedule posts via API; agent drafts, human approves queue. |
| Canva / Figma | App | Partial | Brand assets; agent can request via Canva API for templated graphics. |
| The Muse / Built In / Otta | SaaS | Yes | Branded employer pages; content syndication via API or feed. |
| Typeform / Tally | SaaS | Yes | Testimonial intake forms; webhook into agent. |
| Loom / Wistia / YouTube | SaaS | Yes | Video hosting; agent retrieves URLs and embed codes. |
| Reputation.com / ReviewTrackers | SaaS | Yes | Aggregate review monitoring + response API. |
| Mailchimp / Customer.io / Beehiiv | SaaS | Yes | Talent community newsletter delivery. |

## Templates & scripts
See `templates.md` for content calendar, testimonial brief, and Glassdoor response templates. Inline review-monitor cron script:

```bash
#!/usr/bin/env bash
# review-monitor.sh - scheduled hourly, drafts Slack approvals
set -euo pipefail
source ~/bin/op_unlock.sh
TOKEN=$(op item get "Glassdoor API" --vault "Faion Personal" --fields token)
SINCE=$(date -d '1 hour ago' --iso-8601=seconds)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.glassdoor.com/api/employer/<id>/reviews?since=$SINCE" \
  | jq -c '.reviews[]' | while read -r r; do
    rating=$(echo "$r" | jq -r '.rating')
    body=$(echo "$r" | jq -r '.body')
    # Hand off to LLM for drafted response, then post to Slack #brand-approvals
    claude -p "Draft Glassdoor response per brand voice: rating=$rating body='$body'" \
      | tee >(curl -X POST -H 'Content-Type: application/json' \
        -d "{\"text\":\"$(cat)\"}" "$SLACK_WEBHOOK")
  done
```

## Best practices
- Audit perception (external) vs. reality (internal surveys) annually; gap > 1.0 on 5-pt scale = repositioning needed.
- Respond to every Glassdoor review within 48h, including positive ones; pattern-match, don't templatize.
- Employee testimonials: get written consent + image release before publication; store in HRIS.
- Use UTM-tagged careers page links per channel for source attribution; agents must add UTMs by default.
- Diversity content: lead with employee voices, never with leadership claims; metrics only when published quarterly internally.
- Pair every "we're hiring" post with a "what we're building" post — applications follow trust, not job listings.
- Repurpose: one long-form testimonial → 5 LinkedIn quotes → 1 video → 1 newsletter feature. Agents excel at this fan-out.

## AI-agent gotchas
- Cliché injection: "we're committed to", "our amazing team", "passionate professionals" — strip in post-pass; train agent to avoid.
- Fake testimonial risk: agent invents employee names or quotes when source data is missing; require explicit `[EMPLOYEE_NAME] [QUOTE]` tokens with no auto-fill.
- Glassdoor responses that contradict employee experience escalate. Always human approval, no auto-publish.
- Hashtag stuffing: LLMs add 15+ hashtags; LinkedIn best practice is 3–5 per post.
- Image rights: agents pull stock images that may be unlicensed; use whitelisted libraries (Unsplash, company DAM).
- Localization mishap: a US-positive phrase ("crushing it") translates poorly; agent must localize per market, not direct-translate.
- ToS violation: scraping Glassdoor without API access can get the company account banned. Bake ToS check into the agent's pre-flight.
- Human-in-loop checkpoints: any external publication (LinkedIn, Glassdoor response, Instagram), any DEI claim, any compensation/benefit claim.
- Brand voice drift: agents handed the brand guide once will drift after 50 generations; re-anchor by including 3 approved sample posts in every prompt.

## References
- LinkedIn Talent Solutions Employer Brand Playbook: https://business.linkedin.com/talent-solutions/employer-brand
- Glassdoor Employer Branding Guide: https://www.glassdoor.com/employers/employer-branding/
- Indeed Employer Branding: https://www.indeed.com/hire/c/info/employer-branding
- Brett Minchington, "Employer Brand Leadership"
- LinkedIn Global Talent Trends (annual)
- Universum World's Most Attractive Employers (annual benchmark)
- Built In employer-branding playbook
- Reputation.com / ReviewTrackers research reports
