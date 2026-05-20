---
slug: ba-onboarding-week-one-template
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "30b1e1ecc35a9745"
summary: Week-one onboarding checklist for a BA joining a new project — artefact pull, stakeholder discovery script, glossary intake, tooling setup — collapsed to a single five-day plan.
tags: [business-analyst, onboarding, p4-outsource, discovery, requirements-baseline]
---
# BA Week-One Onboarding Template

## Summary

**One-sentence:** A five-day, artefact-driven onboarding plan that gets a BA from "first commit to project" to "ready to write requirements" without improvising the discovery sequence each time.

**One-paragraph:** P4 outsource BAs rotate across projects every few weeks; the cost of starting from a blank page is paid every time. This methodology fixes the sequence — Day 1 artefact pull, Day 2 stakeholder map and interview script, Day 3 glossary intake, Day 4 process baseline, Day 5 risk register and gap memo — and pins each step to a concrete output committed to the project workspace. The deliverable is a `week-one-pack/` folder the BA can hand to a PM or successor without verbal context. Replaces the abstract `ba-planning` methodology with day-level execution rules.

## Applies If (ALL must hold)

- BA is joining a project they have not previously worked on (or has been away >60 days).
- Project has a paying client and an existing scope document (SOW, contract, brief).
- BA has >=20% capacity for the first 5 working days (cannot run the pack at 5h/week).
- At least one product/business owner is reachable within the first three days.

## Skip If (ANY kills it)

- Project lifetime <2 weeks — the pack costs more than it saves on micro-engagements.
- BA is replacing an in-flight BA mid-sprint — use a hand-off checklist instead, not a fresh discovery.
- Pre-sales or estimation engagement — use `ops-pre-sales-discovery` methodology, scope is different.
- Internal product where the BA is also the founder — much of the discovery has already happened informally.

## Prerequisites

- Read access to the existing project workspace (Confluence/Notion/Drive/Jira).
- The signed SOW or brief (PDF or markdown) — written contract, not just a Slack thread.
- Calendar slot booked for a 60-minute kickoff with the engagement manager or PM within 48h.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst/elicitation-techniques` | Day-2 interviews lean on standard elicitation; this methodology does not re-teach it. |
| `pro/ba/business-analyst/requirements-documentation` | Output of week one feeds the requirements doc; format is assumed familiar. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: artefact-first pull, named stakeholder map, written glossary, process baseline diagram, risk memo | ~900 |
| `content/02-output-contract.xml` | essential | Shape of `week-one-pack/` folder, required files, naming, sign-off field | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: stakeholder-by-Slack, copy-paste glossary, missing process diagram, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `artefact-inventory-from-workspace` | haiku | Mechanical listing of files + metadata |
| `stakeholder-map-extraction` | sonnet | Reads SOW / kickoff transcript, infers roles + influence — bounded judgment |
| `gap-memo-synthesis` | opus | Cross-artefact reasoning: what is missing, what conflicts |

## Templates

| File | Purpose |
|------|---------|
| `templates/week-one-pack-skeleton/` | Folder skeleton with empty README, stakeholders.md, glossary.md, processes.md, risks.md |
| `templates/kickoff-interview-script.md` | 12 standard kickoff questions + recording-consent prompt |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pack.py` | Confirm all required files present in `week-one-pack/` before declaring D5 complete | End of Day 5 |

## Related

- parent skill: `pro/ba/business-analyst/`
- peer methodology: `ba-planning`, `requirements-lifecycle`, `stakeholder-analysis`
- external: [BABOK Guide v3 §3.1](https://www.iiba.org/career-resources/babok/) (planning & monitoring KA)
