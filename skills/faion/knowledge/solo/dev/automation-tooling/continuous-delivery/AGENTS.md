# Continuous Delivery (Index)

## Summary

Router file for the CD knowledge cluster. Dispatches to `cd-basics/` for principles, prerequisites, expand-contract migrations, and phased adoption roadmap; dispatches to `cd-pipelines/` for YAML, deployment strategies (blue-green, canary, rolling), health checks, and monitoring. Reading this index alone is insufficient — always fan out to the correct child.

## Why

CD topics cluster into two distinct concern layers: the conceptual/process layer (what CD is, when it applies, how to adopt it) and the implementation layer (concrete pipeline YAML, rollout strategies, rollback wiring). Merging them produces a file too large to auto-load and too broad to act on. This index keeps routing cheap and lets agents load exactly one focused child.

## When To Use

- Routing: a task mentions "continuous delivery" without specifying whether it needs principles or pipeline YAML.
- Producing an executive summary of CD for stakeholders using only the Quick Reference and CD vs CI matrix.
- Cross-linking from other knowledge bases (trunk-based-dev, feature-flags) into a single CD landing page.

## When NOT To Use

- Implementation work — always open `cd-basics/` or `cd-pipelines/` directly.
- Continuous Deployment safety nets (canary analysis, SLO-based rollout gates) — not covered here.
- Team-process change management — Accelerate and The DevOps Handbook are referenced but not unpacked.

## Content

| File | What's inside |
|------|---------------|
| `content/01-overview.xml` | Quick Reference, CD vs CI vs Continuous Deployment matrix, DORA elite targets, deployment strategy summary, routing table. |

## Templates

none
