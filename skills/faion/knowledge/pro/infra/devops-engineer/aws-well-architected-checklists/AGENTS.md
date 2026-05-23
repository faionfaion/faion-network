---
slug: aws-well-architected-checklists
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a binary pass/fail Well-Architected checklist across the 6 pillars (OpEx, Security, Reliability, Performance, Cost, Sustainability), used as a pre-launch gate or quarterly review.
content_id: "25519959f6ca12ac"
complexity: medium
produces: checklist
est_tokens: 4200
tags: [aws, well-architected, checklist, security, cost-optimization]
---

# AWS Well-Architected Framework Checklists (2025-2026)

## Summary

**One-sentence:** Produces a binary pass/fail Well-Architected checklist across the 6 pillars (OpEx, Security, Reliability, Performance, Cost, Sustainability), used as a pre-launch gate or quarterly review.

**One-paragraph:** The AWS Well-Architected Framework encodes lessons from thousands of production reviews; the abstract pillars only become useful when translated into concrete pass/fail items wired into CI gates, pre-launch reviews, and quarterly audits. This methodology produces that checklist for a target workload — every item is binary, every item names an AWS CLI / Config rule that verifies it, and the output includes per-pillar gap severity (HIGH/MED/LOW) so remediation can be prioritised. Without the structured checklist, security and reliability gaps stay hidden until an incident.

**Ефективно для:**

- Pre-launch review нового AWS workload до production traffic.
- Quarterly Well-Architected review для існуючого prod environment.
- New AWS account baseline setup (security + cost management).
- Post-incident review — які чек-айтеми були відсутні.
- Agent-driven environment audit — кожен айтем має verifiable CLI check.

## Applies If (ALL must hold)

- Workload runs on AWS (any combination of EC2 / Lambda / RDS / S3 / etc.).
- Production launch OR audit deadline is named.
- AWS Config (or CLI access) is available to verify the items programmatically.

## Skip If (ANY kills it)

- Throwaway sandbox account — overhead exceeds value.
- Replacing the formal AWS Well-Architected Tool review for compliance — use this as a working checklist alongside the tool.
- Non-AWS workload — apply the corresponding cloud framework (Azure WAF, GCP WAF).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload inventory | list of AWS services + accounts in scope | AWS Organizations / tags |
| Pillar priority | ranking of pillars by business priority (Security first by default) | leadership / GRC |
| Compliance scope | SOC2 / PCI / HIPAA / FedRAMP applicable controls | GRC |
| AWS CLI access | read-only role or AWS Config aggregator | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[devops-aws-service-selection]] | Pillar evaluation depends on service choices made earlier |
| [[finops-cloud-cost-optimization]] | Cost-pillar items depend on FinOps practice |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: all-6-pillars-evaluated, binary-items-only, cli-verifiable, gap-severity-ranked, skip-this-methodology | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for checklist artefact + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: skip-pillars, non-binary-items, no-cli-check, no-severity | 800 |
| `content/04-procedure.xml` | essential | 5 steps: inventory → per-pillar checklist → CLI map → run → score | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree on workload type → pillar priority | 800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compose-checklist` | sonnet | Assemble pillar-by-pillar item list from the canonical bank. |
| `map-to-cli` | haiku | Deterministic CLI command per item. |
| `score-gaps` | sonnet | Severity assignment based on workload + compliance scope. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wa-checklist.md` | Markdown skeleton of the 6-pillar checklist |
| `templates/wa-checklist.json` | JSON checklist artefact (validator target) |
| `templates/_smoke-test.json` | Minimum checklist artefact used by validate-aws-well-architected-checklists.py --self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aws-well-architected-checklists.py` | Validate the checklist artefact against the schema in `content/02-output-contract.xml` | CI on every artefact change + pre-commit hook |

## Related

- [[devops-aws-service-selection]]
- [[finops-cloud-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals on the input to a conclusion that points back to a rule from `01-core-rules.xml`. Use it whenever scoping a launch review or quarterly WA audit.
