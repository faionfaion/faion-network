# AIOps Checklists

## Anomaly Detection Checklist

### Data Foundation

- [ ] **Metrics coverage**: CPU, memory, disk, network, latency, error rates
- [ ] **Log aggregation**: Centralized logging with structured format
- [ ] **Trace collection**: Distributed tracing enabled across services
- [ ] **Baseline establishment**: 2+ weeks of normal behavior data
- [ ] **Seasonality mapping**: Weekly, monthly, release-day patterns identified

### Model Configuration

- [ ] **Algorithm selection**: Isolation Forest, Prophet, or LSTM based on data
- [ ] **Threshold tuning**: Dynamic thresholds vs static (prefer dynamic)
- [ ] **Multi-signal correlation**: Combine latency + error rate + saturation
- [ ] **SLO integration**: Alerts based on error budget burn rate
- [ ] **False positive baseline**: <20% false positive rate target

### Operational Readiness

- [ ] **Alert routing**: Severity-based routing to appropriate teams
- [ ] **Escalation paths**: Defined escalation for unacknowledged alerts
- [ ] **Suppression rules**: Maintenance windows, known issues
- [ ] **Dashboard visibility**: Anomaly trends visible to all stakeholders
- [ ] **Feedback loop**: Process to mark false positives for model improvement

---

## Root Cause Analysis Checklist

### Data Requirements

- [ ] **Service topology**: Up-to-date service dependency graph
- [ ] **Change events**: Deployment, config, feature flag changes tracked
- [ ] **Infrastructure events**: Scale events, node failures, network changes
- [ ] **Correlation window**: Appropriate time window for event correlation
- [ ] **Blast radius mapping**: Impact scope for each service

### Analysis Capabilities

- [ ] **Causal graph**: Directed graph of service dependencies
- [ ] **Correlation engine**: Events from multiple sources correlated
- [ ] **Timeline reconstruction**: Ordered sequence of related events
- [ ] **Change awareness**: Recent changes highlighted in RCA
- [ ] **Confidence scoring**: Ranked probable causes with confidence %

### Integration Points

- [ ] **APM integration**: Traces linked to RCA findings
- [ ] **Log correlation**: Relevant logs attached to incidents
- [ ] **Metric context**: Anomalous metrics shown alongside RCA
- [ ] **Runbook linking**: Suggested remediation based on cause
- [ ] **Postmortem export**: RCA data exportable for review

---

## Incident Management Checklist

### Detection & Triage

- [ ] **Multi-channel detection**: Metrics, logs, traces, synthetic monitors
- [ ] **Severity classification**: P1-P4 based on impact and urgency
- [ ] **Auto-assignment**: Routing based on service ownership
- [ ] **Deduplication**: Related alerts grouped into single incident
- [ ] **Noise reduction**: >80% alert correlation achieved

### Response Workflow

- [ ] **War room automation**: Slack/Teams channel created automatically
- [ ] **Stakeholder notification**: Business stakeholders informed for P1/P2
- [ ] **Status page integration**: External communication automated
- [ ] **Runbook access**: Relevant runbooks surfaced during incident
- [ ] **Timeline tracking**: All actions logged with timestamps

### Remediation

- [ ] **Auto-remediation policies**: Defined actions for known issues
- [ ] **Human approval gates**: P1/P2 require human confirmation
- [ ] **Rollback capability**: One-click rollback for deployments
- [ ] **Scale actions**: Auto-scale triggers for resource issues
- [ ] **Restart policies**: Pod/service restart automation

### Post-Incident

- [ ] **Postmortem template**: Standardized format for all P1/P2
- [ ] **Action item tracking**: Follow-ups assigned and tracked
- [ ] **Pattern identification**: Recurring issues flagged
- [ ] **Model feedback**: Incident data fed back to ML models
- [ ] **Metrics review**: MTTR, MTTD tracked and improved

---

## Auto-Remediation Checklist

### Policy Definition

- [ ] **Scope boundaries**: Clear limits on what can be auto-remediated
- [ ] **Risk classification**: Actions categorized by risk level
- [ ] **Approval matrix**: Which actions need human approval
- [ ] **Blast radius limits**: Max impact of any auto-action
- [ ] **Rollback triggers**: Conditions to reverse auto-actions

### Common Patterns

| Pattern | Trigger | Action | Risk |
|---------|---------|--------|------|
| Pod restart | CrashLoopBackOff | kubectl rollout restart | Low |
| Node drain | Node unhealthy | kubectl drain | Medium |
| HPA scale | CPU >80% | Increase replicas | Low |
| Deployment rollback | Error rate spike post-deploy | kubectl rollout undo | Medium |
| Cache flush | Memory pressure | Clear application cache | Low |
| Circuit breaker | Upstream errors >50% | Enable fallback | Low |

### Safety Controls

- [ ] **Rate limiting**: Max actions per time window
- [ ] **Cooldown periods**: Minimum time between same actions
- [ ] **Health verification**: Confirm improvement after action
- [ ] **Audit logging**: All actions logged with context
- [ ] **Manual override**: Ability to disable auto-remediation

---

## AIOps Platform Selection Checklist

### Must-Have Capabilities

- [ ] **OpenTelemetry native**: Full OTel support (metrics, logs, traces)
- [ ] **SLO-aware detection**: Error budget-based alerting
- [ ] **Change correlation**: Deployment and config change awareness
- [ ] **Service topology**: Automatic dependency discovery
- [ ] **LLM integration**: AI-powered summaries and runbooks

### Data Management

- [ ] **Data retention**: Meets compliance requirements (30-90 days hot)
- [ ] **Cost model**: Predictable pricing at scale
- [ ] **Data governance**: GDPR/SOC2 compliance
- [ ] **Multi-tenancy**: Team/service isolation
- [ ] **Export capability**: Data portability

### Integration

- [ ] **IaC support**: Terraform/Pulumi providers
- [ ] **ChatOps**: Slack/Teams integration
- [ ] **ITSM**: ServiceNow/Jira integration
- [ ] **CI/CD**: GitHub Actions/GitLab CI webhooks
- [ ] **SIEM**: Security event correlation

### Operational

- [ ] **SLA**: Vendor SLA meets requirements
- [ ] **Support**: 24/7 support for P1 issues
- [ ] **Documentation**: Comprehensive docs and examples
- [ ] **Training**: Onboarding resources available
- [ ] **Community**: Active user community/forums

---

## Audit Checklist (Quarterly Review)

### Performance Review

- [ ] **MTTR trend**: Improving quarter-over-quarter
- [ ] **False positive rate**: Decreasing or stable
- [ ] **Auto-remediation rate**: Increasing coverage
- [ ] **Noise reduction**: >80% maintained
- [ ] **Anomaly precision**: >60% maintained

### Model Health

- [ ] **Training data**: Recent data included in models
- [ ] **Concept drift**: Models retrained if drift detected
- [ ] **Feature relevance**: Features still predictive
- [ ] **Threshold review**: Thresholds still appropriate
- [ ] **New patterns**: Recently discovered patterns added

### Process Review

- [ ] **Runbook accuracy**: Runbooks match current systems
- [ ] **Escalation effectiveness**: Escalations reaching right people
- [ ] **Feedback loop**: Teams providing model feedback
- [ ] **Tool adoption**: Teams using AIOps capabilities
- [ ] **Training needs**: Knowledge gaps addressed
