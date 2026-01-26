# DORA Metrics Implementation Checklist

## Pre-Implementation

- [ ] Identify current CI/CD tools in use
- [ ] Map existing deployment workflow
- [ ] Identify incident management system
- [ ] Document current deployment frequency (baseline)
- [ ] Get stakeholder buy-in (metrics for improvement, not punishment)

## Data Collection Setup

### Deployment Frequency

- [ ] Configure CI/CD to emit deployment events
- [ ] Tag deployments with environment (prod, staging, dev)
- [ ] Distinguish between full deployments and hotfixes
- [ ] Set up deployment counter/aggregator
- [ ] Define "successful deployment" criteria

### Lead Time for Changes

- [ ] Enable Git commit timestamps tracking
- [ ] Configure deployment timestamp capture
- [ ] Link commits to deployments (merge commit or tag)
- [ ] Account for timezone differences
- [ ] Handle multi-commit deployments

### Change Failure Rate

- [ ] Define "failure" criteria (rollback, hotfix, incident)
- [ ] Link incidents to deployments
- [ ] Track rollback events
- [ ] Track hotfix deployments separately
- [ ] Set up failure/total deployment ratio calculation

### Mean Time to Restore (MTTR)

- [ ] Configure incident detection timestamps
- [ ] Configure incident resolution timestamps
- [ ] Define "resolved" criteria
- [ ] Link incidents to affected services
- [ ] Set up MTTR aggregation (mean, median, p95)

## Tool Integration

### GitHub Actions

- [ ] Add deployment tracking step to workflows
- [ ] Configure GitHub Environments
- [ ] Set up deployment status API calls
- [ ] Enable GitHub deployment events

### GitLab CI

- [ ] Enable DORA analytics (Premium/Ultimate)
- [ ] Configure environments in `.gitlab-ci.yml`
- [ ] Set up deployment tracking jobs
- [ ] Link issues to merge requests

### Incident Management

- [ ] Integrate PagerDuty/Opsgenie/VictorOps
- [ ] Configure incident severity levels
- [ ] Set up incident-to-deployment linking
- [ ] Enable automated incident creation from alerts

### Monitoring

- [ ] Export metrics to Prometheus
- [ ] Create Grafana dashboards
- [ ] Set up alerting for metric degradation
- [ ] Configure data retention policy

## Dashboard Setup

- [ ] Deployment frequency chart (daily/weekly/monthly)
- [ ] Lead time histogram with percentiles
- [ ] Change failure rate gauge with threshold
- [ ] MTTR trend line with SLO target
- [ ] Team/service breakdown views
- [ ] Historical comparison (week-over-week, month-over-month)

## Process Integration

- [ ] Add DORA review to sprint retrospectives
- [ ] Create weekly metrics report automation
- [ ] Set up Slack/Teams notifications for significant changes
- [ ] Document metrics collection methodology
- [ ] Train team on interpreting metrics

## Quality Assurance

- [ ] Validate data accuracy (spot check)
- [ ] Test edge cases (partial deployments, cancelled releases)
- [ ] Verify timezone handling
- [ ] Confirm incident-deployment linking accuracy
- [ ] Set up data quality alerts

## Advanced (2025-2026 Practices)

- [ ] Add reliability metric (SLO achievement)
- [ ] Implement AI-assisted bottleneck detection
- [ ] Connect metrics to business outcomes
- [ ] Set up cross-team comparisons (normalized)
- [ ] Enable predictive analytics for metric trends
- [ ] Monitor batch size when using AI code generation
- [ ] Track team well-being indicators

## Ongoing Maintenance

- [ ] Review and adjust "elite" thresholds quarterly
- [ ] Update tool integrations as stack evolves
- [ ] Archive historical data appropriately
- [ ] Conduct quarterly metrics methodology review
- [ ] Update dashboards based on team feedback

---

*Use this checklist when implementing DORA metrics tracking for a new project or team.*
