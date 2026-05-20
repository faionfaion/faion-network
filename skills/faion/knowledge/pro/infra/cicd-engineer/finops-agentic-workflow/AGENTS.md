---
slug: finops-agentic-workflow
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: FinOps with agents is continuous-loop optimization: a daily billing-snapshot agent ingests cost data, a tag-auditor flags untagged resources, an idle-hunter files tickets for waste candidates, and a weekly RI/SP-advisor proposes commitment adjustments.
content_id: "62ed513d7c686fb1"
tags: [finops, agentic, cost-automation, human-in-loop, idle-detection]
---
# FinOps with AI Agents: Continuous-Loop Cost Automation

## Summary

**One-sentence:** FinOps with agents is continuous-loop optimization: a daily billing-snapshot agent ingests cost data, a tag-auditor flags untagged resources, an idle-hunter files tickets for waste candidates, and a weekly RI/SP-advisor proposes commitment adjustments.

**One-paragraph:** FinOps with agents is continuous-loop optimization: a daily billing-snapshot agent ingests cost data, a tag-auditor flags untagged resources, an idle-hunter files tickets for waste candidates, and a weekly RI/SP-advisor proposes commitment adjustments. All write-actions require human approval — agents never auto-delete or auto-terminate. Split detection (read-only) from remediation (write, gated) to prevent runaway savings loops.

## Applies If (ALL must hold)

- Cloud bill above $10k/month and growing — manual weekly review misses too many anomalies.
- Multiple teams deploying independently — no single human has visibility across all accounts.
- Commitment (RI/SP) renewals require analysis of 30-90 day usage patterns — tedious for humans, trivial for agents.
- Tagging compliance below 95% — tag-auditor agent closes the gap without manual resource-by-resource review.

## Skip If (ANY kills it)

- Cloud bill below $5k/month — agent setup cost exceeds value; manual weekly review is sufficient.
- Strictly regulated environments where all changes require formal change control — agent-generated tickets still need human workflow before approval.
- No human owner available to review agent recommendations — agents without a human approver accumulate unreviewed backlogs that become stale and misleading.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/cicd-engineer/`
