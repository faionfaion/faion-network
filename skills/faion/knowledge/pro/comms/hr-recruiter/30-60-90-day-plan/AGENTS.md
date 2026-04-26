# 30-60-90 Day Plan

## Summary

A three-phase new-hire ramp framework based on Michael Watkins's Learn / Contribute / Execute cadence. Each phase has observable milestones anchored to real team work (a release, a quota slice, a shipped doc), not generic verbs like "understand". The plan is co-authored with the hiring manager and the new hire on Day 1; plans written by HR alone become checkboxes nobody reads.

## Why

Without a structured ramp plan, new hires and managers operate on implicit, mismatched expectations. The 30-day review is the first moment misalignment surfaces — too late for easy correction. Observable artifacts per phase (PR merged, deal closed, doc published) give the manager a defensible basis for the day-30, day-60, and day-90 reviews and give the hire a clear contract for what success looks like.

## When To Use

- New hire onboarding for any role with measurable project deliverables (engineer, sales rep, PM, marketer).
- Internal transfers and promotions where role scope changes substantially.
- Re-orgs where leaders need a structured first quarter against new mandates.
- Drafting role-specific milestones during offer close to set explicit expectations.

## When NOT To Use

- Hourly or shift roles where competency comes from training scripts, not project ownership.
- Sub-30-day contracts where the three-phase cadence does not fit.
- Roles where outcomes depend wholly on team output — use team-level OKRs instead.
- Externally mandated apprenticeship curricula (medical residency, regulated trades).

## Content

| File | What's inside |
|------|---------------|
| `content/01-phases.xml` | Learn/Contribute/Execute phase definitions, milestone types, success criteria per phase, check-in cadence. |
| `content/02-role-examples.xml` | Role-specific milestone examples for software engineer and sales representative. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plan-scaffold.sh` | Bash scaffold: given a role slug and JD file, generates a markdown plan skeleton with the three phases. |

## Scripts

none
