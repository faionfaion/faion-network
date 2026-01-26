# Grafana Implementation Checklist

## Dashboard Setup

### Initial Configuration

- [ ] Define dashboard purpose and audience
- [ ] Choose appropriate time range default
- [ ] Set refresh interval based on data update frequency
- [ ] Create folder structure for organization
- [ ] Add dashboard tags for searchability

### Variables

- [ ] Add namespace/environment variable
- [ ] Add pod/service filter variable
- [ ] Add time interval variable
- [ ] Configure variable refresh settings
- [ ] Test variable cascading dependencies

### Panel Organization

- [ ] Group related panels into rows
- [ ] Place most important metrics at top
- [ ] Use consistent grid positioning
- [ ] Add row titles for sections
- [ ] Ensure logical flow (overview → details)

## Panel Configuration

### Query Optimization

- [ ] Use recording rules for complex queries
- [ ] Set appropriate `$__rate_interval` or custom interval
- [ ] Limit label cardinality in queries
- [ ] Use instant queries for tables where appropriate
- [ ] Test query performance with large time ranges

### Visualization Settings

- [ ] Select appropriate visualization type
- [ ] Set correct unit (bytes, seconds, percent)
- [ ] Configure legend display and placement
- [ ] Set axis labels and ranges
- [ ] Add value mappings where needed

### Thresholds

- [ ] Define green/yellow/red thresholds
- [ ] Align thresholds with SLO targets
- [ ] Use consistent threshold colors across dashboards
- [ ] Set appropriate min/max for gauges
- [ ] Test threshold visibility at different values

### Documentation

- [ ] Add panel title (clear, concise)
- [ ] Write panel description (hover info)
- [ ] Add Text panel for dashboard instructions
- [ ] Document data source requirements
- [ ] Include query explanations in comments

## Alerting Setup

### Alert Rule Configuration

- [ ] Define symptom-based alert conditions
- [ ] Set evaluation interval
- [ ] Configure pending period (avoid flapping)
- [ ] Add meaningful alert name
- [ ] Write actionable alert summary

### Notification Routing

- [ ] Configure contact points (Slack, email, PagerDuty)
- [ ] Set up notification policies
- [ ] Define severity levels (critical, warning, info)
- [ ] Configure silence and mute timings
- [ ] Test notification delivery

### Alert Best Practices

- [ ] Link alerts to relevant panels
- [ ] Include runbook URLs in annotations
- [ ] Set appropriate severity based on user impact
- [ ] Avoid infrastructure-only alerts for paging
- [ ] Group related alerts to reduce noise

## Data Source Setup

### Prometheus

- [ ] Configure scrape endpoint
- [ ] Set HTTP method (POST recommended)
- [ ] Configure default time interval
- [ ] Test connectivity
- [ ] Verify metrics availability

### Loki

- [ ] Configure Loki endpoint
- [ ] Set max lines limit
- [ ] Configure derived fields (if needed)
- [ ] Test log queries
- [ ] Verify label indexing

## Maintenance

### Version Control

- [ ] Export dashboard JSON
- [ ] Store in Git repository
- [ ] Use provisioning for deployment
- [ ] Document schema version
- [ ] Test import/export cycle

### Performance

- [ ] Review panel query load
- [ ] Optimize expensive queries
- [ ] Set appropriate caching
- [ ] Monitor dashboard load time
- [ ] Reduce unnecessary panels

### Regular Review

- [ ] Audit unused dashboards quarterly
- [ ] Update deprecated queries
- [ ] Review alert thresholds against actuals
- [ ] Remove redundant panels
- [ ] Update documentation

## Quality Gates

### Before Publishing

- [ ] All panels load without errors
- [ ] Variables filter correctly
- [ ] Thresholds display properly
- [ ] Mobile responsiveness checked
- [ ] Documentation complete

### After Publishing

- [ ] Share with team for feedback
- [ ] Monitor usage in dashboard analytics
- [ ] Track alert noise levels
- [ ] Gather user improvement suggestions
- [ ] Schedule periodic review

---

*Grafana Implementation Checklist | faion-cicd-engineer*
