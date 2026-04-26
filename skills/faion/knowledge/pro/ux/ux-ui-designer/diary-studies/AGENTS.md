# Diary Studies

## Summary

A longitudinal UX research method where participants self-record experiences in the moment over days or weeks. Three types: interval-contingent (fixed schedule), event-contingent (on trigger), signal-contingent (random prompt). Cap entry time at 5 minutes; entries exceeding that spike attrition. Recruit 30% over target to absorb 20–40% dropout. Run a 3-day pilot with 2 participants before launch.

## Why

Lab studies capture a moment; diary studies capture behavior change over time — habit formation, onboarding progression, context switching, churn precursors. These patterns are invisible to any single-session method. The 5-minute entry cap and varied prompts are the two most important mechanical controls: drop either and data quality collapses after day 4.

## When To Use

- Studying longitudinal behavior: onboarding, habit formation, churn precursors.
- Multi-device or context-switching usage scattered across days.
- Pre-redesign discovery for products with dispersed usage (fitness, journaling, sleep, medication).
- Validating retention drivers — what triggers re-engagement vs. abandonment.
- B2B day-in-the-life research where workflows span weeks.

## When NOT To Use

- Quick directional input on a feature — use intercept survey or unmoderated test instead.
- One-time or rare events unlikely to surface within study duration.
- Fully synchronous tasks where in-context observation is more valuable (use contextual inquiry).
- Highly regulated domains where ongoing self-reporting risks PII/PHI leak.

## Content

| File | What's inside |
|------|---------------|
| `content/01-study-design.xml` | Study types, design decisions, planning checklist, entry format rules. |
| `content/02-antipatterns-and-workflow.xml` | Common failure modes, attrition safeguards, agentic workflow, coding schema. |

## Templates

| File | Purpose |
|------|---------|
| `templates/study-plan.md` | Full study plan template: objectives, participants, design, timeline, quality measures. |
| `templates/entry-daily.md` | Daily diary entry template (context, rating, issues, media). |
| `templates/entry-event.md` | Event-contingent entry template (trigger, goal, outcome, sentiment). |
| `templates/diary-reminders.py` | Script: emit per-participant reminder schedule with early-study weighting. |
