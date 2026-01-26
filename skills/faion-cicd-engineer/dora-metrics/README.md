# DORA Metrics

DORA (DevOps Research and Assessment) metrics measure software delivery performance and organizational effectiveness.

## Overview

DORA metrics originated from research led by Dr. Nicole Forsgren, Jez Humble, and Gene Kim, published in "Accelerate" (2018). These metrics are now the industry standard for measuring DevOps performance.

## The Four Key Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | Multiple/day | Weekly-monthly | Monthly-6mo | 6mo+ |
| **Lead Time for Changes** | <1 hour | 1 day-1 week | 1-6 months | 6mo+ |
| **Change Failure Rate** | 0-15% | 16-30% | 31-45% | 46%+ |
| **Mean Time to Restore (MTTR)** | <1 hour | <1 day | 1 day-1 week | 1 week-1 month |

## Metric Definitions

### 1. Deployment Frequency (DF)

How often code is successfully deployed to production.

**What it measures:** Team agility and delivery cadence
**Data sources:** CI/CD pipelines, deployment logs, release management tools

### 2. Lead Time for Changes (LT)

Time from code commit to successful production deployment.

**What it measures:** Pipeline efficiency and process overhead
**Data sources:** Git commits, CI/CD timestamps, deployment records

### 3. Change Failure Rate (CFR)

Percentage of deployments causing production failures requiring remediation.

**What it measures:** Code quality, testing effectiveness, deployment reliability
**Data sources:** Incident tracking, rollback records, hotfix deployments

### 4. Mean Time to Restore (MTTR)

Average time to recover from production incidents.

**What it measures:** Incident response capability, system resilience
**Data sources:** Incident management systems, monitoring alerts, resolution logs

## 2025-2026 Evolution

### Fifth Metric: Reliability

DORA research now emphasizes **Reliability** as a fifth metric, measuring operational performance beyond deployment:

- Service Level Objectives (SLOs) achievement
- Error budgets
- System availability

### AI Impact on DORA Metrics

Research findings (2025):
- 7.2% reduction in delivery stability with increased AI adoption
- 1.5% reduction in delivery throughput
- AI-generated code encourages larger batch sizes, violating small-batch principles

**Recommendation:** Monitor batch size when using AI code generation tools.

### Business Outcome Mapping

Modern DORA implementations connect metrics to:
- Revenue impact
- User satisfaction scores
- Team well-being indicators
- Customer churn rates

## Why DORA Metrics Matter

| Finding | Impact |
|---------|--------|
| Elite performers | 2x more likely to exceed organizational goals |
| Deployment frequency | 208x higher in elite vs low performers |
| Lead time | 106x faster in elite teams |
| Recovery time | 2,604x faster in elite performers |

## Implementation Approach

1. **Establish baseline** - Measure current state without targets
2. **Automate collection** - Integrate with CI/CD, Git, incident tools
3. **Focus on trends** - Track improvement over absolute numbers
4. **Team-level ownership** - Metrics for improvement, not punishment
5. **Weekly reviews** - Regular team retrospectives on metrics

## Tooling Ecosystem

| Tool | Integration Focus |
|------|-------------------|
| [Sleuth](https://www.sleuth.io/) | GitHub, GitLab, Jira, PagerDuty |
| [LinearB](https://linearb.io/) | Git, Jira, CI/CD, incidents |
| [Swarmia](https://www.swarmia.com/) | Engineering analytics |
| [Jellyfish](https://jellyfish.co/) | Multi-platform aggregation |
| [Four Keys](https://github.com/GoogleCloudPlatform/fourkeys) | Open source, GCP native |
| [GitLab DORA](https://docs.gitlab.com/user/analytics/dora_metrics/) | Native GitLab integration |

## Data Sources Mapping

| Metric | Primary Source | Secondary Source |
|--------|----------------|------------------|
| Deployment Frequency | CI/CD pipelines | Release management |
| Lead Time | Git + CI/CD timestamps | Project management |
| Change Failure Rate | Incident tracking | Rollback logs |
| MTTR | Incident management | Monitoring systems |

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview and concepts (this file) |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Real-world configurations |
| [templates.md](templates.md) | Reusable templates |
| [llm-prompts.md](llm-prompts.md) | AI assistance prompts |

## References

- [DORA State of DevOps Report](https://dora.dev/research/)
- [Google Cloud DORA Guide](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [Accelerate Book](https://itrevolution.com/product/accelerate/)
- [DORA 5 Metrics](https://cd.foundation/blog/2025/10/16/dora-5-metrics/)
- [Atlassian DORA Guide](https://www.atlassian.com/devops/frameworks/dora-metrics)
- [GitLab DORA Docs](https://docs.gitlab.com/user/analytics/dora_metrics/)

---

*faion-cicd-engineer / dora-metrics*
