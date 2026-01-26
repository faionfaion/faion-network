# Prometheus Monitoring Checklists

## Initial Setup Checklist

### Infrastructure

- [ ] Prometheus server deployed with appropriate resources
  - [ ] CPU: 500m-2000m (based on scrape targets)
  - [ ] Memory: 2Gi-8Gi (based on time series count)
  - [ ] Storage: 100Gi+ persistent volume
- [ ] Alertmanager deployed (3 replicas for HA)
- [ ] Grafana deployed with Prometheus datasource
- [ ] Persistent storage configured for all components
- [ ] Resource limits and requests defined
- [ ] Pod disruption budgets configured

### Configuration

- [ ] Retention period set (recommended: 15-30 days)
- [ ] Retention size set (prevents disk full)
- [ ] Scrape interval configured (15-30s default)
- [ ] Scrape timeout set (< scrape interval)
- [ ] External labels configured for federation
- [ ] Service discovery configured

### Security

- [ ] TLS enabled for all endpoints
- [ ] Authentication configured (if exposed)
- [ ] Network policies applied
- [ ] RBAC permissions limited to necessary
- [ ] Secrets managed securely (not in ConfigMaps)

---

## Application Instrumentation Checklist

### Metrics Endpoint

- [ ] `/metrics` endpoint exposed
- [ ] Appropriate port configured (e.g., 9090)
- [ ] Health check endpoints separate from metrics
- [ ] Metrics endpoint secured if needed

### Metric Design

- [ ] Counter for request counts
- [ ] Histogram for latency measurements
- [ ] Gauge for current state (connections, queue size)
- [ ] Info metric for application metadata (version, env)
- [ ] Appropriate bucket boundaries for histograms

### Labels

- [ ] Labels have bounded cardinality
- [ ] No user IDs, request IDs, or UUIDs as labels
- [ ] Consistent label naming across services
- [ ] All required dimensions included
- [ ] Label names follow snake_case convention

### Naming

- [ ] Metrics follow naming convention: `namespace_name_unit_suffix`
- [ ] Counters end with `_total`
- [ ] Units included in metric name (seconds, bytes)
- [ ] HELP strings provided for all metrics
- [ ] TYPE annotation correct for each metric

---

## ServiceMonitor/PodMonitor Checklist

### Configuration

- [ ] Correct label selector matches target service/pods
- [ ] Namespace selector configured
- [ ] Metrics port name matches service/pod port
- [ ] Path correct (default: `/metrics`)
- [ ] Scrape interval appropriate for target

### Relabeling

- [ ] Source labels correctly specified
- [ ] Drop unnecessary labels to reduce cardinality
- [ ] Keep only relevant metrics if needed
- [ ] Pod/namespace labels preserved for debugging

### Verification

- [ ] Target appears in Prometheus UI targets
- [ ] No scrape errors in Prometheus logs
- [ ] Metrics visible in Prometheus expression browser
- [ ] Labels correct in scraped metrics

---

## Alerting Rules Checklist

### Alert Design

- [ ] Alert on symptoms, not causes
- [ ] `for` duration set to avoid flapping (5m minimum)
- [ ] Severity label assigned (critical/warning/info)
- [ ] Team label assigned for routing
- [ ] Description template uses `{{ $value }}`

### Annotations

- [ ] Summary provides concise description
- [ ] Description includes relevant details and values
- [ ] Runbook URL points to remediation docs
- [ ] Dashboard URL for investigation

### Testing

- [ ] Alert fires correctly in test environment
- [ ] Alert resolves when condition clears
- [ ] Notification reaches correct channel
- [ ] Alert is actionable (not noise)

---

## Recording Rules Checklist

### Design

- [ ] Pre-computes expensive aggregations
- [ ] Follows naming: `level:metric:operation`
- [ ] Evaluation interval appropriate
- [ ] Rule group logically organized

### Performance

- [ ] Reduces query time for dashboards
- [ ] Covers common aggregation patterns
- [ ] Avoids redundant calculations
- [ ] Memory impact acceptable

---

## Alertmanager Configuration Checklist

### Routing

- [ ] Default receiver configured
- [ ] Critical alerts route to PagerDuty/on-call
- [ ] Warning alerts route to Slack/email
- [ ] Team-specific routing configured
- [ ] `continue: true` set where needed

### Receivers

- [ ] Slack webhooks configured and tested
- [ ] PagerDuty integration keys set
- [ ] Email SMTP configured (if used)
- [ ] Webhook URLs secured

### Grouping

- [ ] `group_by` includes relevant labels
- [ ] `group_wait` set (30s default)
- [ ] `group_interval` set (5m default)
- [ ] `repeat_interval` set (4h default)

### Templates

- [ ] Custom templates render correctly
- [ ] Template syntax validated
- [ ] Templates include relevant context
- [ ] Templates tested with sample alerts

---

## Dashboard Checklist

### Design

- [ ] Uses recording rules for expensive queries
- [ ] Appropriate time ranges and intervals
- [ ] Variables for namespace/pod filtering
- [ ] Consistent color scheme

### Performance

- [ ] Queries optimized with appropriate aggregations
- [ ] Uses `$__rate_interval` variable
- [ ] Avoids high-cardinality queries
- [ ] Dashboard loads in < 5 seconds

### Content

- [ ] Request rate panel
- [ ] Error rate panel
- [ ] Latency percentiles (P50, P90, P99)
- [ ] Resource usage (CPU, memory)
- [ ] Pod/container status

---

## Scaling Checklist

### Vertical Scaling

- [ ] Memory increased for more time series
- [ ] CPU increased for more scrape targets
- [ ] Storage increased for longer retention
- [ ] Monitoring Prometheus resource usage

### Horizontal Scaling (Federation)

- [ ] Global Prometheus deployed
- [ ] Federation scrape jobs configured
- [ ] Only aggregated metrics federated
- [ ] External labels distinguish sources

### Remote Write

- [ ] Remote write endpoint configured
- [ ] Write relabeling drops unnecessary metrics
- [ ] Queue configuration tuned
- [ ] Long-term storage operational

---

## Operational Checklist

### Daily

- [ ] Check Prometheus targets health
- [ ] Review new alerts and silences
- [ ] Verify Alertmanager receiving alerts

### Weekly

- [ ] Review dashboard performance
- [ ] Check storage usage trends
- [ ] Audit high-cardinality metrics
- [ ] Review alert noise and tune

### Monthly

- [ ] Remove unused metrics/rules
- [ ] Update recording rules for new patterns
- [ ] Review and update runbooks
- [ ] Capacity planning review

---

## Migration/Upgrade Checklist

### Pre-upgrade

- [ ] Backup Prometheus data (if needed)
- [ ] Backup Alertmanager configuration
- [ ] Review release notes for breaking changes
- [ ] Test upgrade in staging environment

### During Upgrade

- [ ] Maintain at least one healthy replica
- [ ] Monitor scrape success during rollout
- [ ] Verify alert delivery continues

### Post-upgrade

- [ ] Verify all targets healthy
- [ ] Confirm dashboards load correctly
- [ ] Test alert routing
- [ ] Check for deprecation warnings

---

## Troubleshooting Checklist

### Prometheus Not Scraping

- [ ] Target endpoint accessible from Prometheus
- [ ] ServiceMonitor labels match service
- [ ] Port name matches in ServiceMonitor
- [ ] Network policy allows traffic
- [ ] RBAC allows scraping

### High Cardinality

- [ ] Identify high-cardinality metrics: `count by (__name__)({__name__=~".+"})`
- [ ] Find labels causing explosion
- [ ] Add metric relabeling to drop
- [ ] Fix application instrumentation

### Memory Issues

- [ ] Check time series count
- [ ] Reduce retention period
- [ ] Drop high-cardinality metrics
- [ ] Increase memory limits
- [ ] Consider sharding

### Query Performance

- [ ] Create recording rules for slow queries
- [ ] Optimize PromQL (avoid regex where possible)
- [ ] Reduce time range
- [ ] Add aggregation to reduce data
