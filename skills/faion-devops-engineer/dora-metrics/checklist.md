# DORA Metrics Implementation Checklist

Comprehensive checklist for implementing and measuring DORA metrics (2025-2026).

---

## Pre-Implementation Checklist

### Organizational Readiness

- [ ] Executive sponsorship secured
- [ ] Team buy-in obtained (no punishment culture)
- [ ] Metric definitions documented and agreed
- [ ] Baseline measurement period defined
- [ ] Improvement targets set (realistic, incremental)
- [ ] Review cadence established (weekly/bi-weekly/monthly)

### Technical Prerequisites

- [ ] CI/CD pipeline instrumented
- [ ] Deployment tracking automated
- [ ] Incident management system configured
- [ ] Monitoring and alerting in place
- [ ] Version control metadata accessible
- [ ] Data aggregation infrastructure ready

---

## Metric 1: Deployment Frequency

### Data Collection

- [ ] Define what constitutes a "deployment"
- [ ] Track deployments to production only (not staging)
- [ ] Capture deployment timestamp
- [ ] Associate deployment with service/application
- [ ] Track deployment initiator (automated vs manual)
- [ ] Exclude rollbacks from frequency count

### Measurement Points

- [ ] CI/CD pipeline completion events
- [ ] Container registry pushes
- [ ] Kubernetes deployment events
- [ ] Cloud deployment logs (AWS CodeDeploy, GCP Deploy, etc.)
- [ ] Feature flag activations (if applicable)

### Improvement Actions

- [ ] Reduce batch sizes
- [ ] Implement trunk-based development
- [ ] Automate deployment pipeline
- [ ] Remove manual approval gates (where safe)
- [ ] Enable feature flags for decoupled deploys

---

## Metric 2: Lead Time for Changes

### Data Collection

- [ ] Track commit timestamp
- [ ] Track PR creation timestamp
- [ ] Track PR merge timestamp
- [ ] Track deployment timestamp
- [ ] Calculate end-to-end duration
- [ ] Handle multi-commit PRs (first commit vs last)

### Pipeline Stages to Measure

- [ ] Code commit to PR creation
- [ ] PR creation to first review
- [ ] First review to approval
- [ ] Approval to merge
- [ ] Merge to build completion
- [ ] Build to deployment
- [ ] **Total: Commit to Production**

### Improvement Actions

- [ ] Reduce PR size (target <200 lines)
- [ ] Automate code reviews (linting, security scans)
- [ ] Set PR review SLAs
- [ ] Improve test execution time
- [ ] Implement parallel testing
- [ ] Optimize build pipelines

---

## Metric 3: Change Failure Rate

### Data Collection

- [ ] Define "failure" criteria clearly
- [ ] Track failed deployments (immediate issues)
- [ ] Track incidents caused by changes
- [ ] Track hotfixes deployed
- [ ] Track rollbacks performed
- [ ] Associate incidents with causative deployments

### Failure Categories

- [ ] Deployment failures (pipeline breaks)
- [ ] Runtime failures (crashes after deploy)
- [ ] Performance degradation (latency increase)
- [ ] Functional bugs (user-facing issues)
- [ ] Security incidents (vulnerabilities exploited)

### Improvement Actions

- [ ] Increase test coverage
- [ ] Implement canary deployments
- [ ] Add progressive rollouts
- [ ] Improve staging environment parity
- [ ] Enhance pre-deployment validation
- [ ] Implement feature flags for safer releases

---

## Metric 4: Time to Restore Service (MTTR)

### Data Collection

- [ ] Track incident detection time
- [ ] Track incident acknowledgment time
- [ ] Track incident resolution time
- [ ] Calculate total downtime
- [ ] Categorize by severity level
- [ ] Track resolution method (rollback, fix-forward, etc.)

### Recovery Milestones

- [ ] Time to detect (monitoring alert)
- [ ] Time to acknowledge (on-call response)
- [ ] Time to diagnose (root cause identified)
- [ ] Time to mitigate (service restored)
- [ ] Time to resolve (permanent fix deployed)

### Improvement Actions

- [ ] Improve monitoring coverage
- [ ] Reduce alert noise (only actionable alerts)
- [ ] Create runbooks for common issues
- [ ] Practice incident response (game days)
- [ ] Implement automated rollback
- [ ] Improve observability (logs, traces, metrics)

---

## Metric 5: Reliability

### Data Collection

- [ ] Define SLOs for each service
- [ ] Track availability (uptime percentage)
- [ ] Track error rates (5xx responses)
- [ ] Track latency (P50, P95, P99)
- [ ] Calculate MTBF (Mean Time Between Failures)
- [ ] Track SLO compliance over time

### Reliability Indicators

- [ ] Availability: >= 99.9% (target)
- [ ] Error rate: < 1% (5xx responses)
- [ ] Latency P99: < defined threshold
- [ ] MTBF: increasing trend
- [ ] User-facing incidents: decreasing trend

### Improvement Actions

- [ ] Implement SLO-based alerting
- [ ] Create error budgets
- [ ] Improve architecture resilience
- [ ] Add circuit breakers
- [ ] Implement graceful degradation
- [ ] Enhance capacity planning

---

## Tooling Checklist

### Data Sources

- [ ] Version control (GitHub, GitLab, Bitbucket)
- [ ] CI/CD (GitHub Actions, GitLab CI, Jenkins)
- [ ] Deployment (Kubernetes, ArgoCD, AWS CodeDeploy)
- [ ] Incident management (PagerDuty, Opsgenie, ServiceNow)
- [ ] Monitoring (Prometheus, Datadog, New Relic)

### Integration Points

- [ ] Webhooks configured
- [ ] API access tokens secured
- [ ] Data sync frequency defined
- [ ] Historical data imported
- [ ] Real-time updates working

### Dashboard Requirements

- [ ] All five metrics visible
- [ ] Trend lines over time
- [ ] Team/service breakdown
- [ ] Comparison to benchmarks
- [ ] Drill-down capability

---

## Reporting Checklist

### Weekly Review

- [ ] Deployment count reviewed
- [ ] Failed deployments identified
- [ ] Open incidents tracked
- [ ] Blockers discussed
- [ ] Quick wins identified

### Monthly Review

- [ ] All five metrics calculated
- [ ] Trends analyzed
- [ ] Bottlenecks identified
- [ ] Improvement actions prioritized
- [ ] Progress towards targets reviewed

### Quarterly Review

- [ ] Performance tier assessed (Elite/High/Medium/Low)
- [ ] Comparison to industry benchmarks
- [ ] Strategic improvements planned
- [ ] Targets adjusted if needed
- [ ] Success stories documented

---

## Anti-Patterns Checklist

### Avoid These Practices

- [ ] Using metrics for individual performance reviews
- [ ] Comparing teams without context
- [ ] Focusing on single metric in isolation
- [ ] Gaming metrics (deploy empty commits)
- [ ] Setting unrealistic targets
- [ ] Ignoring qualitative feedback

### Warning Signs

- [ ] Metrics improving but incidents increasing
- [ ] High deployment frequency but low customer satisfaction
- [ ] Fast MTTR but same incidents recurring
- [ ] Low CFR but missing real failures in counting
- [ ] Reliability targets met but error budget unused

---

## Maturity Assessment

### Level 1: Basic

- [ ] Manual tracking of some metrics
- [ ] Inconsistent definitions
- [ ] Reactive improvement

### Level 2: Developing

- [ ] Automated tracking of all five metrics
- [ ] Consistent definitions across teams
- [ ] Regular reviews and discussions

### Level 3: Defined

- [ ] Integrated dashboards
- [ ] Team-level accountability
- [ ] Improvement experiments running

### Level 4: Managed

- [ ] Predictive analysis
- [ ] Continuous improvement culture
- [ ] Industry benchmark comparison

### Level 5: Optimized

- [ ] Elite performance sustained
- [ ] Innovation in measurement
- [ ] Thought leadership

---

## Quick Validation Commands

```bash
# GitHub: Deployment frequency (last 30 days)
gh api repos/{owner}/{repo}/deployments \
  --jq '[.[] | select(.created_at > (now - 2592000 | todate))] | length'

# GitHub: Recent deployments with status
gh api repos/{owner}/{repo}/deployments \
  --jq '.[] | {id, ref, created_at, description}'

# GitLab: Deployment frequency
curl --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.com/api/v4/projects/{id}/deployments?per_page=100"

# Kubernetes: Recent deployments
kubectl get deployments -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.creationTimestamp}{"\n"}{end}'

# Prometheus: Error rate query
curl -s "http://prometheus:9090/api/v1/query?query=sum(rate(http_requests_total{status=~\"5..\"}[1h]))/sum(rate(http_requests_total[1h]))"
```

---

## Sources

- [DORA Official Guide](https://dora.dev/guides/dora-metrics-four-keys/)
- [DORA Metrics 2025 Best Practices | Oobeya](https://www.oobeya.io/blog/dora-metrics-2025-best-practices)
- [DevOps Metrics 2025 | Checkmarx](https://checkmarx.com/learn/appsec/devops-metrics-2025-the-complete-guide-to-successfully-measuring-dev-operations/)
- [Your Practical Guide to DORA Metrics | Swarmia](https://www.swarmia.com/blog/dora-metrics/)
