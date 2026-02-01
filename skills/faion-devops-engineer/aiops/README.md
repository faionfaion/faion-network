---
id: aiops
name: "AIOps"
domain: OPS
skill: faion-devops-engineer
category: "best-practices-2026"
---

# AIOps (AI for IT Operations)

## Overview

AIOps applies machine learning and big data analytics to automate IT operations, including anomaly detection, root cause analysis, and incident management. By 2026, 60%+ of large enterprises will adopt self-healing systems powered by AIOps (Gartner).

## Problem Statement

| Challenge | Impact |
|-----------|--------|
| Alert fatigue | Teams overwhelmed by noise, miss critical issues |
| Slow incident response | MTTR measured in hours, not minutes |
| Manual root cause analysis | Engineers spend 50%+ time on diagnosis |
| Reactive operations | Incidents reach production before detection |
| Data silos | Logs, metrics, traces in separate tools |

## Core Capabilities

| Capability | Description | AI Application |
|------------|-------------|----------------|
| **Anomaly Detection** | Identify deviations from normal behavior | Pattern recognition, statistical models, ML |
| **Root Cause Analysis** | Determine failure origin across systems | Event correlation, causal graphs, topology analysis |
| **Predictive Alerts** | Forecast failures before impact | Time-series forecasting, trend analysis |
| **Auto-Remediation** | Self-healing actions | Runbook automation, policy-driven responses |
| **Capacity Planning** | Resource demand forecasting | Regression models, seasonal decomposition |

## Architecture

```
Data Sources          Ingestion           Analysis            Action
─────────────────────────────────────────────────────────────────────
Metrics (Prometheus)    │                    │                    │
Logs (Fluent Bit)       │     OpenTelemetry  │    ML Models       │   Auto-Remediation
Traces (Jaeger)         │ ──► Collector ────►│ ──► Engine ───────►│ ──► Scripts
Events (K8s)            │                    │    LLM Analysis    │   Human Approval
Changes (Git/CD)        │     Normalization  │                    │   Notifications
                        │                    │                    │
                        ▼                    ▼                    ▼
                   Data Lake            Alert Engine         SOAR/ChatOps
```

## 2025-2026 Evolution

| Trend | Description |
|-------|-------------|
| **LLM Integration** | Natural language incident summaries, GenAI runbooks |
| **Predictive Operations** | Failures predicted and prevented before production impact |
| **Hybrid Workflows** | AI recommends → humans approve → systems execute |
| **Explainable AI** | Every decision logged with reasoning (audit trail) |
| **SLO-Aware Detection** | Alerts based on error budget burn, not static thresholds |
| **Change-Aware Correlation** | RCA considers recent deployments, config changes |

## Tool Landscape

| Tool | Key Capability | Best For |
|------|----------------|----------|
| **Splunk ITSI** | ML on logs/metrics, incident prioritization | Enterprise observability |
| **Dynatrace Davis AI** | Real-time anomaly detection, topology mapping | Full-stack monitoring |
| **ServiceNow ITOM** | Predictive AIOps, pre-built remediation | ITSM integration |
| **Moogsoft** | Noise reduction, alert correlation | Alert management |
| **BigPanda** | Incident management, situational awareness | Event correlation |
| **Datadog** | Watchdog AI, unified observability | Cloud-native |
| **New Relic AIOps** | Applied Intelligence, error tracking | APM-focused |
| **PagerDuty AIOps** | Event Intelligence, smart routing | Incident response |

## Minimum Requirements (2026)

| Requirement | Why |
|-------------|-----|
| Native OpenTelemetry support | Unified telemetry collection |
| SLO-aware detection | Business impact awareness |
| Change-aware correlation | RCA accuracy |
| Topology/RCA with traces | Service dependency understanding |
| LLM/RAG for runbooks | Intelligent remediation |

## Success Metrics

| Metric | Target | Formula |
|--------|--------|---------|
| Anomaly Precision | >60% after tuning | True incidents / Anomalies promoted |
| Auto-Remediation Rate | Start >15%, grow to >40% | Incidents resolved without humans |
| MTTR Reduction | >50% improvement | Average resolution time |
| False Positive Rate | <20% | False alerts / Total alerts |
| Noise Reduction | >80% | Correlated alerts / Raw alerts |

## Implementation Roadmap

| Phase | Focus | Deliverables |
|-------|-------|--------------|
| **Phase 1** | Observability Foundation | Prometheus + Fluent Bit + Jaeger, OpenTelemetry |
| **Phase 2** | Anomaly Detection | Isolation Forest, Prophet for time-series |
| **Phase 3** | Auto-Remediation | Lambda/Jenkins jobs, restart/scale/rollback |
| **Phase 4** | Human-in-the-Loop | Slack/Teams approvals, SOAR integration |
| **Phase 5** | Continuous Improvement | Automated postmortems, feedback to models |

## Folder Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation and audit checklists |
| [examples.md](examples.md) | Real-world patterns and code samples |
| [templates.md](templates.md) | Configuration and runbook templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for AIOps tasks |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-cicd-engineer](../../faion-cicd-engineer/CLAUDE.md) | CI/CD and monitoring integration |
| [faion-infrastructure-engineer](../../faion-infrastructure-engineer/CLAUDE.md) | Infrastructure for AIOps tools |
| [faion-ml-engineer](../../faion-ml-engineer/CLAUDE.md) | ML model development |
| [faion-rag-engineer](../../faion-rag-engineer/CLAUDE.md) | RAG for intelligent runbooks |

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |

---

## Sources

- [AIOps Survey in the Era of LLMs - ACM](https://dl.acm.org/doi/10.1145/3746635)
- [AIOps in 2025: Components and Capabilities - Selector](https://www.selector.ai/learning-center/aiops-in-2025-4-components-and-4-key-capabilities/)
- [Autonomous IT Operations 2026 - Ennetix](https://ennetix.com/the-rise-of-autonomous-it-operations-what-aiops-platforms-must-enable-by-2026/)
- [AIOps for Modern IT - Medium](https://medium.com/@iambivash.bn/aiops-for-modern-it-anomaly-detection-root-cause-and-genai-runbooks-what-works-in-2025-by-ba4b4ccc0c21)
- [How Log Data Powers AIOps for RCA - Eyer](https://www.eyer.ai/blog/how-log-data-powers-aiops-for-root-cause-analysis/)
