---
slug: indie-postmortem-template
tier: solo
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Structured postmortem template for indie hackers and small-team founders to turn failed launches into public consumption — narrative arc, learning extraction, metrics, opt-in privacy.
content_id: "45ebbb7305e91a53"
tags: [product, indie-hacker, postmortem, failed-launch, public-narrative, content-marketing]
---

# Indie Postmortem Template

## Summary

**One-sentence:** A 7-section postmortem template (narrative / what we tried / metrics / what we learned / what we'd do differently / what comes next / opt-in privacy) for indie hackers turning failed launches into shareable content.

**One-paragraph:** SRE-style internal incident postmortems exist in faion (`inc-postmortem-auto-draft-no-publish`); they target ops audiences and stay private. Indie hackers face a different need: turning a failed product / failed launch into PUBLIC content that drives community trust, audience growth, and learning capture. Mechanism: narrative-arc structure (setup → attempt → outcome → reflection), explicit metrics (visitors, signups, churn, MRR trajectory, time-spent, cost), separation of "what we learned" from "what we'd do differently" (different lessons), opt-in privacy section (what about customers / co-founders / financials gets shared), and a "what comes next" section that closes the loop. Primary output: a publishable postmortem post + a private debrief log paired with it.

## Applies If (ALL must hold)

- product / launch / experiment has been shut down OR has been declared "failed" (not "we'll come back to it someday")
- founder is willing to publish AT LEAST the public-safe version of the postmortem
- some metrics are available (even if "0 paying customers" — that's a number)
- failure is recent enough (&lt; 12 months) that lessons are still actionable

## Skip If (ANY kills it)

- product is still alive and pivoting — write a pivot retrospective, not a postmortem
- founder is in active emotional processing of the failure (write the private debrief first, public post later)
- legal / NDA constraints prevent meaningful disclosure (write private only)
- audience is enterprise B2B with public-postmortem risk (write differently-framed "lessons" content instead)

## Prerequisites

- raw timeline of the launch / product life (dates, decisions, releases)
- metrics dump (analytics, billing, support volume, time-spent)
- a list of "what surprised us" — the highest-value section content
- review by a trusted second reader before publishing (catches blame, ambiguity, emotional leak)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` | SRE postmortem methodology; this methodology is its public-narrative counterpart |
| `pro/marketing/growth-marketer/launch-week-orchestration` | If the failure is launch-week-shaped, consume the orchestration's "what was attempted" |
| `solo/marketing/content-marketer/personal-narrative-content` | Public postmortems are a content artifact; consume the narrative-content rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: narrative arc, metrics with numbers (not feelings), what-we-learned vs what-we'd-do-differently split, opt-in privacy, no-blame-framing | ~1000 |
| `content/02-output-contract.xml` | essential | Public-post structure + private-debrief structure + forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (vague metrics, victim narrative, lesson-as-platitude, etc.) with detector + repair | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `timeline_assembly` | sonnet | From raw events, build the chronological narrative arc |
| `metrics_table_population` | haiku | Mechanical: extract numbers from analytics / billing exports |
| `lesson_extraction` | opus | Cross-event synthesis — what is the actual learning vs the surface explanation |
| `privacy_filter_pass` | sonnet | Strip PII / NDA-sensitive content from the public version |

## Templates

| File | Purpose |
|------|---------|
| `templates/public-postmortem.md` | 7-section public-facing post template |
| `templates/private-debrief.md` | Internal debrief paired with public post |
| `templates/metrics-table.md` | Standard numbers table (visitors, signups, MRR, churn, costs) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/privacy-scan.py` | Scans public draft for PII / NDA flags (named co-founders, customer names, raw financial figures) | Before publishing |
| `scripts/blame-scan.py` | Scans for blame-language patterns and victim framing | Before publishing |

## Related

- parent skill: `solo/product/product-operations/`
- peer methodologies: `failed-experiment-debrief`, `personal-narrative-content`, `pivot-retrospective`
- external: [Indie Hackers shutdown posts (corpus)](https://www.indiehackers.com/) · [Y Combinator startup-failure essays](https://www.ycombinator.com/) · [Patrick McKenzie — Reflective Writing on Failure](https://www.kalzumeus.com/)
