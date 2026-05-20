---
slug: launch-readiness-review
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "85fd712c1280235d"
summary: A cross-functional pre-launch readiness review covering 8 gates (security, performance, observability, runbooks, on-call, legal, support enablement, comms tree) that turns implicit launch knowledge into a hard go/no-go decision.
tags: [launch, readiness, sre, runbook, cross-functional]
---

# Launch Readiness Review

## Summary

**One-sentence:** A cross-functional pre-launch readiness review covering 8 gates (security, performance, observability, runbooks, on-call, legal, support enablement, comms tree) that turns implicit launch knowledge into a hard go/no-go decision.

**One-paragraph:** Product-launch methodology covers go-to-market; SRE-launch covers reliability; legal handles ToS — but no single methodology assembles all of them into one review before a P6 product-team ships. The result: legal forgotten, runbooks missing, on-call rotation undefined, comms tree out-of-date. This methodology defines 8 gates, each with explicit pass criteria and an owner. Output: `LaunchReadiness` JSON with per-gate status + go/no-go decision + remediation list. Built on Google SRE Production Readiness Review (PRR), AWS Well-Architected, and Marty Cagan launch-readiness essays.

## Applies If (ALL must hold)

- net-new product or service launch (not a bugfix release)
- launch will hit external customers (not internal beta)
- team size ≥ 3 (cross-functional gates are realistic)
- launch date within next 4-12 weeks

## Skip If (ANY kills it)

- shipping a hotfix or minor feature — overhead exceeds value
- internal-only launch (no external customers) — only security + observability gates apply
- solo SaaS — use the lighter `solo` launch checklist
- launch already shipped — this is pre-launch; for post-mortem use launch-retro methodology

## Prerequisites

- launch date set (not "soon")
- product owner + tech lead + 1 stakeholder per gate identified
- service-level objectives (SLOs) drafted
- ToS / Privacy Policy reviewed by counsel (or affirmative skip with reason)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/sdlc-ai/sre-production-readiness` | Google SRE PRR source for security / performance / observability gates |
| `pro/comms/communicator/launch-comms-tree` | Provides the comms-tree gate's structure |
| `pro/infra/devops-engineer/us-uk-eu-compliance-matrix` | Legal gate consumes its matrix output |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 8-gate coverage, named owners, hard criteria, sign-off discipline, blocker veto | ~1000 |
| `content/02-output-contract.xml` | essential | `LaunchReadiness` schema with per-gate fields | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: rubber-stamp, missing owner, partial sign-off | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gate_owner_identification` | haiku | Lookup against org chart |
| `criterion_evaluation` | sonnet | Bounded judgment per gate |
| `blocker_diff_assembly` | sonnet | Cross-gate aggregation |
| `go_no_go_synthesis` | opus | Final cross-team decision needs careful reasoning |

## Templates

| File | Purpose |
|------|---------|
| `templates/launch-readiness.json` | Output schema |
| `templates/gate-criteria.yaml` | Pass criteria per gate |
| `templates/comms-tree.md` | Comms tree template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/run-readiness.py` | Pulls gate status from owners; assembles report | T-7d, T-3d, T-1d |
| `scripts/runbook-presence-check.py` | Verifies runbook URLs return 200 OK | Pre-launch |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodologies: `launch-comms-tree`, `sre-production-readiness`, `us-uk-eu-compliance-matrix`
- external: [Google SRE Book — Production Readiness Review](https://sre.google/sre-book/evolving-sre-engagement-model/) · [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) · [Marty Cagan — Inspired](https://svpg.com/) · [Lenny Rachitsky — Launch checklists](https://www.lennyspodcast.com/)
