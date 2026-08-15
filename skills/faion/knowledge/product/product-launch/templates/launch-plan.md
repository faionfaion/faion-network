<!--
purpose: Launch plan skeleton — timeline, asset checklist, channels, metrics, rollback narrative
consumes: positioning doc + asset owners + channel inventory
produces: Markdown artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml
token-budget-impact: ~400-1200 tokens when loaded as context
variables:
  - name: product_name
    type: string
    required: true
    description: What is launching, as customers will see it. If it is a feature rather than a product, name the feature - a launch plan for "the platform" has no audience and no message.
  - name: launch_type
    type: enum
    required: true
    options: [soft, beta, full, major-release]
    description: How loudly this goes out. Be honest: a soft launch announced as a full one burns the list you would need for the real launch, and you only get to send that email once.
  - name: target_date
    type: string
    required: true
    description: Launch day, ISO. Mid-week and mid-month unless you have a reason - every T-minus row below counts back from here, so pick a date engineering has already agreed to.
  - name: launch_dri
    type: string
    required: true
    description: The one person who can call the launch off on the day. Not a committee - the rollback decision has a window measured in minutes and consensus does not fit inside it.
  - name: goal_metric
    type: text
    required: true
    description: The number that makes this launch a success, with its target and window - "500 signups in the first 24 hours". Decide before, not after; after, every number is a success.
  - name: primary_audience
    type: text
    required: true
    description: Who this is aimed at, specifically enough to pick channels from - "solo consultants who already pay for a scheduling tool". "Everyone" means you will buy the wrong ads.
  - name: key_message
    type: text
    required: true
    description: One sentence saying what problem this solves for that audience, in their words. Every asset below is a translation of it, so if it is vague here it is vague nine times over.
-->
# Launch Plan: {{product_name}}

## Launch Overview
- **Product:** {{product_name}}
- **Launch type:** {{launch_type}}
- **Target date:** {{target_date}}
- **Launch DRI:** {{launch_dri}}
- **Goal:** {{goal_metric}}

## Target Audience
- **Primary:** {{primary_audience}}
- **Key message:** {{key_message}}

## Timeline

| Week | Date | Deliverable | Owner | Done When |
|------|------|-------------|-------|-----------|
| T-8 | [Date] | Strategy and messaging finalized | [Name] | Positioning doc approved |
| T-6 | [Date] | Asset creation begins | [Name] | All owners assigned |
| T-4 | [Date] | Audience building (waitlist, social) | [Name] | [X] signups or followers |
| T-2 | [Date] | All assets complete and reviewed | [Name] | Asset checklist 100% |
| T-1 | [Date] | Final staging test, team briefed | [Name] | Core flow verified |
| T-Day | {{target_date}} | Launch | {{launch_dri}} | Metrics dashboard live |
| T+1 | [Date] | Monitor and respond | [Name] | Triage queue cleared |
| T+2 | [Date] | Retrospective | [Name] | Learnings documented |

## Asset Checklist

| Asset | Owner | Status | Due |
|-------|-------|--------|-----|
| Landing page | [Name] | [ ] | [Date] |
| Announcement email | [Name] | [ ] | [Date] |
| Demo video or screenshots | [Name] | [ ] | [Date] |
| Social posts | [Name] | [ ] | [Date] |
| Press kit | [Name] | [ ] | [Date] |
| Documentation / onboarding | [Name] | [ ] | [Date] |
| Rollback narrative (200 words) | [Name] | [ ] | [Date] |

## Channel Strategy

| Channel | Timing | Content | Owner |
|---------|--------|---------|-------|
| Email list | T-Day 9am | Announcement | [Name] |
| Twitter/X | T-Day 10am | Thread | [Name] |
| LinkedIn | T-Day 10am | Article | [Name] |
| Product Hunt | T-Day 12:01am PT | Full listing | [Name] |
| Communities | T-Day 11am | Direct post | [Name] |

## Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Primary goal | {{goal_metric}} | |
| Signups week 1 | [X] | |
| Product Hunt rank | Top [X] | |
| Email open rate | [X]% | |

## Risk Mitigation

| Risk | Mitigation | Owner |
|------|------------|-------|
| Server overload | Pre-scale infrastructure T-1 | Eng |
| Critical bug on launch day | Rollback plan ready, kill switch with the DRI | {{launch_dri}} |
| No press pickup | Double down on community channels | Marketing |

## Rollback Narrative
[Pre-written 200-word post explaining why the launch was paused. Fill in before T-Day.]
