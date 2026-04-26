# Social Media Strategy

## Summary

The PACE framework (Platform → Audience → Content → Engagement) for solopreneurs building
an audience on social media. Master one platform before adding another; commit to six months
before evaluating results. Track engagement rate, not follower count, as the primary KPI.

## Why

Most social media failures stem from platform sprawl, inconsistent cadence, and treating posts
as broadcasts. The PACE framework forces sequencing: pick the platform where your ICP already
spends time, define 3-5 content pillars, post on a fixed schedule, and spend daily time engaging.
Engagement rate (likes + comments + shares / impressions) predicts content quality; follower count
is a lagging indicator that follows engagement, not the other way around.

## When To Use

- Choosing which platform(s) to invest in for a new product or personal brand
- Designing a content calendar with pillar distribution and posting frequency
- Batch-generating post drafts (threads, carousels, text posts) for a defined platform
- Running a monthly strategy review: what to double down on, what to cut
- Briefing an agent to produce a 4-week content calendar in JSON format

## When NOT To Use

- Real-time trend hijacking — requires human judgment on brand safety and timing
- Community management and comment responses — relationship quality requires a human
- Generating content for all platforms simultaneously from one prompt — quality degrades
- Accounts under 1 month old with no ICP data — build ICP clarity first
- When the goal is paid acquisition; use ppc-manager methodology instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-pace-framework.xml` | Platform selection scorecard, content pillar definitions, posting frequency targets |
| `content/02-engagement-and-metrics.xml` | 5-5-5 daily engagement method, engagement rate formula, KPI targets, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-calendar.md` | Monthly content calendar with pillar distribution and weekly plan |
| `templates/prompt-content-calendar.txt` | Agent prompt: 4-week calendar in JSON |
| `templates/engagement-tracker.py` | Parse platform analytics CSV → avg/median engagement rate |
