---
slug: launch-retro-template
tier: solo
group: marketing
domain: content-marketer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: A marketing-specific launch retrospective template that feeds lessons back into messaging, creative, and channel mix — distinct from engineering retros.
content_id: "2c8c510cb9ce1984"
tags: [launch,retro,marketing,messaging,creative,channel-mix]
---
# Launch Retro Template

## Summary

**One-sentence:** A marketing-specific launch retrospective template that feeds lessons back into messaging, creative, and channel mix — distinct from engineering retros.

**One-paragraph:** Engineering retros (what shipped, what broke) miss the marketing dimensions of a launch: which message resonated, which creative converted, which channel delivered against expectation, which audience segment surprised, which CTA missed. This methodology defines a 90-minute retro structure with five marketing-anchored sections (Audience reaction, Messaging fit, Creative performance, Channel ROI, Lessons), explicit before/after metric comparison, a "what we'd keep / change / drop" output, and one committed change for the next launch. Mechanism: data pull (channels, conversion, comments), facilitated session, written output, and decision-rights for committing the change. Primary output: a launch-retro doc with three named owners on the committed change.

## Applies If (ALL must hold)

- launch happened in the last 14 days (memory fresh)
- launch had measurable metrics (signups, revenue, engagement, channel reach)
- launch involved ≥ 2 channels OR ≥ 2 contributors on marketing side
- team has bandwidth for a 60-90 min retro session
- another launch is planned within 90 days (lessons must compound)

## Skip If (ANY kills it)

- &gt; 30 days since launch — memory decay invalidates anecdotal data
- launch with single-channel single-asset (post and pray) — too thin for retro
- launch was a soft / rolling release with no fixed metric window
- team has no next-launch plan within 90 days — lessons evaporate without forward use
- regulated launch where retros require legal sign-off process

## Prerequisites (must be true before starting)

- channel data exported (PH ranking, email open/click, social impressions, signups)
- comments / community feedback collected
- pre-launch goal sheet (what the team committed to before launch)
- launch-day warroom logs OR contemporaneous notes
- facilitator named (not the launch director — bias risk)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/launch-day-warroom-template` | Source of contemporaneous launch-day notes |
| `solo/marketing/content-marketer/messaging-house-template` | Receives messaging lessons for next launch |
| `pro/marketing/growth-marketer/aarrr-pirate-metrics` | Optional framework for channel ROI math |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: marketing-not-eng focus, data-first, blameless tone, keep/change/drop, one committed change | ~1000 |
| `content/02-output-contract.xml` | essential | Retro doc schema, five sections required, committed-change owners | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (rebrand-the-launch, no committed change, vibes-only retro, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `data_pull_normalizer` | haiku | Format channel data into standard table |
| `comment_sentiment_synth` | sonnet | Categorize comments (positive, negative, confusion, request) |
| `keep_change_drop_classifier` | sonnet | Classify proposed lessons into 3 buckets |
| `committed_change_writeup` | sonnet | Format the one committed change into spec form |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro-doc.md` | Master retro template |
| `templates/keep-change-drop.md` | Three-bucket worksheet |
| `templates/committed-change-spec.md` | Format for the one next-launch change |
| `templates/data-pull-checklist.md` | List of metrics + sources to gather |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/channel-rollup.py` | Aggregate per-channel data into one table | Pre-retro |
| `scripts/committed-change-tracker.py` | Track whether the change was applied in next launch | Next launch prep |

## Related

- parent skill: `solo/marketing/content-marketer/`
- peer methodology: `launch-day-warroom-template`, `messaging-house-template`
- external: [Norm Kerth, Project Retrospectives](https://www.amazon.com/Project-Retrospectives-Handbook-Team-Reviews/dp/0932633447) · [Atlassian retro playbook](https://www.atlassian.com/team-playbook/plays/retrospective)
