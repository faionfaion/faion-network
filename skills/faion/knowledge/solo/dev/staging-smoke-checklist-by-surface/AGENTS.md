---
slug: staging-smoke-checklist-by-surface
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Daily-use staging smoke checklist organised by surface ("top-3 surfaces, what to click, what to verify"), produced once per surface and re-run before every promotion to production.
content_id: "070a5956e788e119"
tags: [software-developer, smoke-test, staging, deploy, sign-off, solo-dev, checklist]
---
# Staging Smoke Checklist by Surface

## Summary

**One-sentence:** A per-surface smoke checklist — "top 3 surfaces, what to click, what to verify" — that lives next to the deploy script and gates every promotion from staging to production.

**One-paragraph:** Continuous-delivery methodology talks about smoke testing in the abstract, but solo developers actually need a concrete daily artefact: a short markdown file listing the three highest-impact surfaces of the system, with the exact clicks and the exact verifications to perform after deploying to staging. This methodology defines the shape: surfaces ranked by user impact, one checklist per surface, each item phrased as `click → expect`, signed off by writing your initials and a timestamp into the file. The file is checked into the repo next to the deploy script and re-run *every* time staging gets a new build. Replaces the "I'll just click around" pattern that silently misses regressions in the parts of the app the dev did not touch.

## Applies If (ALL must hold)

- Project has a distinct staging environment with the same shape as production.
- Promotion from staging to production is a deliberate action (script or manual approval), not auto-promote.
- Dev is the sole owner of staging sign-off (no separate QA gate).
- Repo has at least one user-facing surface (web UI, API, CLI) with observable behaviour.

## Skip If (ANY kills it)

- Trunk-based deploys directly to prod without staging — there is nothing to smoke.
- Library or pure backend with no UI/API surface — use unit/contract testing instead.
- System has full E2E automation covering the high-impact surfaces — smoke checklist is redundant.
- Pre-launch project with <2 surfaces — write inline test notes; no checklist overhead.

## Prerequisites

- Working staging URL/credentials.
- Identified top-3 surfaces by user/business impact (collected once, reviewed quarterly).
- Place to commit the checklist file (repo root or `ops/` folder).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `free/dev/software-developer/` | Baseline developer workflow conventions. |
| `solo/dev/deploy-notes-template-with-rollback` | Deploy-time artefact this checklist links into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Five rules: top-3 cap, click→expect format, sign-off line, file-in-repo, abort-on-fail. | ~900 |

## Related

- parent skill: `solo/dev/software-developer/`
- peer: `deploy-notes-template-with-rollback`, `qa-rc-smoke-pack-template`, `qa-rollback-trigger-canon`
- external: Continuous Delivery (Humble & Farley) §Smoke Testing
