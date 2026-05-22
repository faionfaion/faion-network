---
slug: aiops
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: # AIOps AI-powered operations for automated incident detection, root cause analysis, and remediation.
content_id: "fa4838d8ad1a0cbb"
tags: [[]]
---
# AIOps

## Summary

**One-sentence:** # AIOps AI-powered operations for automated incident detection, root cause analysis, and remediation.

**One-paragraph:** # AIOps AI-powered operations for automated incident detection, root cause analysis, and remediation. ## Overview AIOps (Artificial Intelligence for IT Operations) applies machine learning and data analytics to automate and enhance IT operations. Key focus areas: - **Anomaly Detection** - Pattern recognition to detect subtle deviations - **Automated Remediation** - Self-healing systems with human-in-the-loop - **Predictive Analytics** - Forecast failures before production impact ## Core Capabilities | Area | AI Application | |------|----------------| | Anomaly detection | Multi-signal pattern recognition, seasonality-aware baselines | | Root cause analysis | Topology-driven correlation across systems | | Predictive alerts | Forecast failures, capacity bottlenecks | | Auto-remediation | Self-healing: restarts, scaling, rollbacks | | Capacity planning | Demand forecasting, resource optimization | ## 2025-2026 Best Practices ### Anomaly Detection - **Historical baselines** - Establish "normal" behavior patterns - **Multi-signal detection** - Promote only convergent anomalies (2+ signals) to incidents - **Change-aware weighting** - Anomalies after deploys/config changes get higher priority - **Seasonality-aware** - Understand business patterns and SLOs ### Automated Remediation - **Trust levels** - Recommend-only, human-approved, fully autonomous (low-risk) - **GenAI runbooks** - Step-by-step remediation with guardrails and HITL - **Cross-tool integration** - ITSM, CI/CD, cloud management, chat tools - **Target metrics** - Start at >15% auto-remediation rate, grow to >40% ### Predictive Analytics - **Historical + real-time data** - Combine for accurate forecasting - **Proactive capacity** - Scale before demand spikes - **Performance degradation** - Detect trends before user impact ## Key Metrics | Metric | Description | Target | |--------|-------------|--------| | Anomaly precision | True incidents / anomalies promoted | >60% after tuning | | Auto-remediation rate | Incidents resolved without human commands | >40% mature | | MTTR reduction | Time to resolve incidents | -50% with AIOps | | Availability improvement | Revenue-generating app uptime | +15% | ## Tool Ecosystem | Tool | Key Capability | |------|----------------| | Splunk ITSI | ML on logs/metrics, prioritize incidents | | Datadog AIOps | Native CI/CD integration, early anomaly detection | | Dynatrace Davis AI | Real-time infrastructure monitoring | | ServiceNow | Predictive AIOps, pre-built remediation | | Moogsoft | Noise reduction, ML-powered detection | | BigPanda | AI incident management, situational awareness | | Coralogix | AI log monitoring, security detection | | Site24x7 | Advanced anomaly detection, metric monitoring | ## Implementation Roadmap | Phase | Focus | Key Activities | |-------|-------|----------------| | Phase 1 | Baseline Setup | Prometheus + Fluent Bit, Isolation Forest anomaly detection | | Phase 2 | Automation Layer | AWS Lambda/Jenkins for automated restarts/rollba

## Applies If (ALL must hold)

- TBD — populate from v1 when-to-use list

## Skip If (ANY kills it)

- TBD — populate from v1 when-not-to-use list

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
