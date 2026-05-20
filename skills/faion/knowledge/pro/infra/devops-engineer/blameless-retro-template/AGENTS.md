---
slug: blameless-retro-template
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Human facilitation template for a post-incident blameless retrospective: agenda, time-boxing, language rules, and action-item capture that complements automated postmortem draft generation.
content_id: "01a39d8809482090"
tags: [infra, devops, sre, postmortem, retrospective, blameless, incident-response]
---

# Blameless Retro Template (Human Facilitation)

## Summary

**One-sentence:** A 60-90 minute blameless retrospective template with explicit agenda blocks, language rules ("the system did X" not "Bob did X"), and a forcing function that prevents the team from skipping contributing-factors analysis.

**One-paragraph:** Auto-drafted postmortems (e.g., faion's `inc-postmortem-auto-draft-no-publish`) produce solid factual reconstruction but cannot facilitate human conversation. Blameless retros are where teams convert incidents into systemic learning — and they fail predictably when facilitation is improvised. Mechanism: a 4-block agenda (timeline review / contributing factors / generative discussion / action items) with named language rules, explicit time-box per block, and a final round that surfaces "what we ALMOST learned but didn't" — the meta question that catches superficial retros. Primary output: a retro record with contributing factors, action items with owners + dates, and meta-notes for the facilitator's next retro.

## Applies If (ALL must hold)

- incident has been declared and resolved (or partially-resolved with stable workaround)
- auto-draft postmortem exists OR will be drafted in parallel (this template is for the FACILITATION layer)
- team includes >= 3 people involved (responders, sub-system owners, downstream consumers)
- facilitator is named and is NOT a direct responder of the incident (to maintain blameless framing)

## Skip If (ANY kills it)

- solo founder with no team to retro with — write a personal incident journal instead (different format)
- incident was a known recurring issue with an existing action item still in flight — re-open the existing AI, don't double-retro
- multi-party incident where root cause is external (cloud provider outage with no internal mitigation gap) — short retro, focus on detection / comms only
- team is in crisis-burnout mode and cannot give 90 min of attention — postpone 1-2 weeks, run an async-async retro instead

## Prerequisites

- incident timeline data assembled (alert times, comms timestamps, deploy events) — from auto-draft if available
- facilitator has read the auto-draft AND timeline in advance (not reading it during the retro)
- participants list confirmed; meeting scheduled within 5 working days of incident resolution
- agreed psychological-safety norms (sometimes called "Norvig's prime directive": everyone did the best they could with what they knew at the time)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` | This methodology layers on top of the auto-draft; consume the draft as input |
| `pro/infra/devops-engineer/incident-response-rotation` | Defines responder roles; retro participants derive from that rotation |
| `pro/comms/hr-recruiter/feedback-protocol` | Language rules for blame-free framing borrow from this |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: language-rule-enforcement, contributing-factors-min-3, action-items-with-owner-and-date, meta-round-required, retro-record-published | ~1000 |
| `content/02-output-contract.xml` | essential | Retro record schema + action-item contract + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 facilitation failure modes (root-cause-fixation, name-leak, action-item-overflow, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `timeline_pre_read_summary` | sonnet | Compress auto-draft into a 1-page pre-read for participants |
| `language_flag_review` | haiku | Post-retro: scan transcript for blame-language patterns and flag for facilitator coaching |
| `action_item_clustering` | sonnet | Group similar action items proposed in retro to avoid AI overflow |
| `meta_learning_extraction` | opus | Extract "what we almost learned" — cross-incident pattern synthesis |

## Templates

| File | Purpose |
|------|---------|
| `templates/retro-agenda.md` | 4-block agenda with time-boxes and facilitator prompts |
| `templates/retro-record.json` | JSON Schema for the retro output |
| `templates/language-rules-card.md` | Printable card with do / do-not phrasing examples |
| `templates/action-item.json` | Schema for one action item |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/scan-transcript-for-blame.py` | NLP scan of retro transcript for blame-language patterns | Post-retro, before publishing the record |
| `scripts/action-item-tracker.py` | Tracks action-item completion across retros; flags chronic uncompleted items | Monthly review of retro outputs |

## Related

- parent skill: `pro/infra/devops-engineer/`
- peer methodologies: `incident-response-rotation`, `runbook-as-markdown`, `postmortem-publish-cadence`
- external: [Google SRE Workbook ch. 9: Incident Response](https://sre.google/workbook/incident-response/) · [Etsy Debriefing Facilitation Guide](https://www.etsy.com/codeascraft/blameless-postmortems) · [PagerDuty Postmortem Open Source Doc](https://postmortems.pagerduty.com/)
