# Diary Study Basics

## Summary

A longitudinal research method where participants self-record behaviors, thoughts, and contexts in the moment or shortly after, over days or weeks. Three variants: interval-contingent (fixed schedule), event-contingent (triggered by occurrence), and signal-contingent (random prompts). Each entry captures when, where, what happened, how the participant felt, and their interpretation.

## Why

Lab studies capture a single snapshot; diary studies reveal how behavior evolves over time, what context shapes usage, and when habits form. The method produces in-the-moment data that retrospective interviews cannot recover — participants' recall of "typical" behavior is systematically inaccurate after 48 hours.

## When To Use

- Studying behavior that unfolds over days or weeks (onboarding journeys, habit formation, multi-device patterns).
- Capturing real-world context (location, mood, environment) that lab conditions eliminate.
- Tracking how user understanding evolves from novice to proficient.
- Pre-purchase or high-consideration journeys where each touchpoint matters.
- Validating retention drop-off hypotheses by following individual usage trajectories.

## When NOT To Use

- Need findings in under two weeks — minimum useful diary period is 7-14 days.
- Single isolated event with no context dependency — a post-event interview is faster and cheaper.
- Sensitive personal contexts (mental health, finances) without ethics review — continuous self-documentation feels surveillance-like.
- Behaviors already covered by product analytics — diary adds self-report noise without incremental signal.
- Rare events (less than once per week) — participants miss too many triggers to form useful patterns.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | What diary studies are, three study types, when-to/not-to use, study design decisions. |
| `content/02-planning.xml` | Planning steps: research questions, design decisions, entry template design, recruitment and onboarding rules. |
| `content/03-examples.xml` | Two worked examples (new-user onboarding 14-day study; cross-device 30-day study) with findings and insights. |

## Templates

| File | Purpose |
|------|---------|
| `templates/study-plan.md` | Full study plan skeleton: research questions, participants, design, diary entry structure, timeline, engagement plan. |
| `templates/entry-daily.md` | Daily diary entry template with location, rating, problems, surprises fields. |
| `templates/entry-event.md` | Event-contingent entry template: trigger, goal, outcome, rating, optional photo. |
| `templates/diary-bot.py` | Minimal Telegram-bot intake skeleton for text + photo + voice entries → JSONL. |
