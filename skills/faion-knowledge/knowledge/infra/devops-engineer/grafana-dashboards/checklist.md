# Grafana Dashboard Checklist

Pre-flight checklist for creating production-ready Grafana dashboards.

## Pre-Design Phase

### Strategy

- [ ] Identify target audience (SRE, developers, management)
- [ ] Define specific questions dashboard should answer
- [ ] Choose observability framework (USE, RED, Golden Signals)
- [ ] Check for existing dashboards to avoid duplication
- [ ] Plan dashboard hierarchy (overview -> detail)

### Data Source Verification

- [ ] Verify data source connectivity
- [ ] Confirm metrics/logs availability
- [ ] Test query performance for expected time ranges
- [ ] Identify cardinality issues in labels

## Design Phase

### Structure

- [ ] Dashboard has clear, descriptive title
- [ ] Dashboard description explains purpose
- [ ] Panels organized in logical rows/tabs
- [ ] Information flows from general to specific
- [ ] Related metrics grouped together

### Variables

- [ ] Namespace/environment variable configured
- [ ] Pod/service/instance variable configured
- [ ] Time interval variable for aggregation
- [ ] Variables use appropriate refresh settings
- [ ] Include "All" option where appropriate
- [ ] Variables have sensible defaults

### Panels

- [ ] Each panel has descriptive title
- [ ] Panel descriptions explain metric meaning
- [ ] Appropriate visualization type selected
- [ ] Units configured correctly (bytes, percent, etc.)
- [ ] Thresholds set for visual indicators
- [ ] Legend positioned appropriately
- [ ] Null values handled (connect, show as zero, etc.)

### Colors and Thresholds

- [ ] Green = healthy, Yellow = warning, Red = critical
- [ ] Consistent color scheme across panels
- [ ] Thresholds aligned with SLO targets
- [ ] Color-blind friendly palette considered

### Queries

- [ ] Queries use recording rules for heavy computations
- [ ] Variables used in queries (`$namespace`, `$pod`)
- [ ] Appropriate aggregation intervals
- [ ] Label matchers are specific (avoid `.*`)
- [ ] Queries tested at 24h, 7d, 30d ranges

## Alerting Integration

### Alert Rules

- [ ] Alerts defined for critical metrics
- [ ] Alert on symptoms, not causes
- [ ] Alert thresholds match dashboard thresholds
- [ ] Runbook links included in alert annotations
- [ ] Alert grouping configured appropriately

### Contact Points

- [ ] Notification channels configured
- [ ] Alert routing rules defined
- [ ] Silence rules documented

## Provisioning

### Version Control

- [ ] Dashboard JSON exported and committed
- [ ] Provisioning YAML configured
- [ ] Folder structure matches Git structure
- [ ] Dashboard UID is stable and meaningful

### GitOps

- [ ] Dashboard uses provisioning API
- [ ] Changes deploy through CI/CD
- [ ] Rollback procedure documented
- [ ] Test dashboards in staging first

## Performance

### Query Optimization

- [ ] Avoid `rate()` over large time ranges without step
- [ ] Use `topk()` to limit series count
- [ ] Prefer instant queries for tables
- [ ] Recording rules for expensive queries
- [ ] Query inspector shows acceptable load times

### Dashboard Settings

- [ ] Refresh rate matches data granularity
- [ ] Time range appropriate for use case
- [ ] Avoid auto-refresh on historical dashboards
- [ ] Panel data caching enabled where appropriate

## Documentation

### In-Dashboard

- [ ] Text panel with dashboard overview
- [ ] Panel descriptions for complex metrics
- [ ] Links to related dashboards
- [ ] Links to runbooks/documentation

### External

- [ ] Dashboard purpose documented in README
- [ ] Query explanations for custom metrics
- [ ] Ownership/team information included
- [ ] Update procedure documented

## Pre-Production Validation

### Functional Testing

- [ ] Dashboard loads without errors
- [ ] All variables populate correctly
- [ ] Variable changes update all panels
- [ ] Time range changes work correctly
- [ ] Drill-down links function properly

### Load Testing

- [ ] Dashboard tested with production data volume
- [ ] Query performance acceptable (< 5s per panel)
- [ ] Browser memory usage acceptable
- [ ] No infinite loops in variable queries

### Cross-Browser

- [ ] Dashboard displays correctly in Chrome
- [ ] Dashboard displays correctly in Firefox
- [ ] Mobile/tablet responsiveness (if needed)

## Post-Deployment

### Monitoring

- [ ] Dashboard usage tracked (Grafana analytics)
- [ ] Query performance monitored
- [ ] Error rates from dashboard queries tracked

### Maintenance

- [ ] Regular review scheduled (quarterly)
- [ ] Unused dashboards archived/deleted
- [ ] Metrics deprecation handled
- [ ] Version updates applied

## Common Issues Checklist

| Issue | Resolution |
|-------|------------|
| Slow dashboard | Add recording rules, reduce time range |
| Missing data | Check data source, verify metric names |
| Variable not updating | Check refresh settings, query syntax |
| Inconsistent colors | Use field overrides consistently |
| Dashboard sprawl | Use variables instead of copies |
| Lost changes | Enable provisioning, use version control |
