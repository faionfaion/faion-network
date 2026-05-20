---
slug: shift-log-template
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5a55fbd86d40a24c"
summary: Per-shift operational log template DevOps engineers fill at start, mid, and end of every on-call shift — capturing context that incident runbooks cannot — so handovers are deterministic and the next shift starts informed.
tags: [devops, on-call, shift-log, handoff, sre]
---

# Shift Log Template

## Summary

**One-sentence:** Per-shift operational log template DevOps engineers fill at start, mid, and end of every on-call shift, capturing context (active investigations, deferred work, watch items, environmental quirks) that incident runbooks do not, so handovers happen in writing not in tribal lore.

**One-paragraph:** Incident runbooks cover what to do when a specific alert fires. They do not cover the operational state of "the morning of": ongoing investigations from the previous shift, deferred maintenance, known-flaky systems being watched, scheduled jobs that should fire, vendor maintenance windows, customer escalations in flight, things-that-are-weird-but-not-yet-broken. Without a structured shift log, each on-call hands over via a 5-minute call (or worse, a Slack DM) and 30% of the operational context evaporates. This methodology pins a markdown shift-log template with five named sections (Carry-over, Active investigations, Watch items, Deferred work, Customer escalations), filled at shift start (read previous), mid-shift (update active items), and end (write next), committed to a `shifts/` directory in the ops repo so each entry is permanent and searchable. Mechanism: structured-write at three checkpoints + read-from-previous at handover. Primary output: a per-shift `YYYY-MM-DD-shift-N.md` log + a searchable archive.

## Applies If (ALL must hold)

- on-call rotation with ≥2 people (single-operator may use a simplified version)
- production system with active alerting (Sentry, Datadog, Grafana, Pingdom)
- the team has a shared repository or Notion / Confluence space for the logs
- shifts have defined start/end (8h, 12h, or 24h)

## Skip If (ANY kills it)

- single solo operator — they remember their own context; this overhead is excessive
- batch-mode operations (no real-time on-call) — use a maintenance log instead
- the team explicitly uses an incident management platform (incident.io, FireHydrant) that already supports shift logs — extend that, do not build parallel

## Prerequisites

- shared repo or page for logs (`shifts/`, `ops/shifts/`, or similar)
- shift-rotation schedule visible to all engineers
- handover ritual at shift change (5-15 minutes)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/inc-runbook-as-markdown-tagged-steps` | Runbooks the shift log references but does not duplicate |
| `pro/infra/devops-engineer/oncall-handoff-template` | Generic handoff pattern; this is the per-shift complement |
| `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` | Postmortem drafting; shift log feeds postmortem timeline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: three-checkpoint discipline, structured sections, read-previous-as-start, searchable archive, no-blame framing | ~1000 |
| `content/02-output-contract.xml` | essential | Shift-log markdown frontmatter + sections schema, archive layout | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: end-of-shift skipped, free-form drift, handover-by-DM, blame-leak, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `shift_log_draft_from_chat_and_alerts` | sonnet | Compose end-of-shift entry from Slack + alert history |
| `handover_summary_for_next_shift` | sonnet | Compact previous log into the active-priority view |
| `archive_search` | n/a | Plain grep / search index |

## Templates

| File | Purpose |
|------|---------|
| `templates/shift-log.md` | The five-section template |
| `templates/handover-checklist.md` | 5-minute handover meeting checklist |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/new-shift.py` | Scaffold a new shift log, copy carry-over from previous | Start of each shift |
| `scripts/lint-shift-log.py` | Ensure all five sections present and frontmatter valid | Pre-commit hook |

## Related

- parent skill: `pro/sdlc-ai/`
- peer methodologies: `inc-runbook-as-markdown-tagged-steps`, `oncall-handoff-template`, `inc-postmortem-auto-draft-no-publish`
- external: [Google SRE Workbook — On-call](https://sre.google/workbook/on-call/) · [PagerDuty Incident Response](https://response.pagerduty.com/) · [Atlassian Incident Handbook](https://www.atlassian.com/incident-management/handbook)
