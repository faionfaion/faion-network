---
id: llm-observability-stack-checklist
name: "LLM Observability Stack Setup Checklist"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Stack Setup Checklist

## Phase 1: Stack Planning

### Requirements Analysis

- [ ] Define data residency requirements (GDPR, SOC2, HIPAA)
- [ ] Identify self-hosting vs SaaS preference
- [ ] Assess existing observability infrastructure (APM, logging)
- [ ] Determine budget constraints (monthly spend limit)
- [ ] Map AI workloads (RAG, agents, chat, embeddings)
- [ ] Identify integration requirements (LangChain, LlamaIndex, custom)

### Platform Selection

- [ ] Evaluate platforms against requirements:
  - [ ] **Langfuse** - self-hosted, MIT, full-stack
  - [ ] **LangSmith** - LangChain native, debugging
  - [ ] **Helicone** - proxy-based, cost optimization
  - [ ] **Portkey** - multi-provider, gateway
  - [ ] **Phoenix** - embeddings, evaluation
  - [ ] **OpenLLMetry** - OTEL-native, existing APM
- [ ] Set up free tier / POC environment
- [ ] Test integration with one LLM endpoint
- [ ] Validate trace data appears in dashboard

## Phase 2: Core Stack Setup

### Tracing Layer

- [ ] Install primary SDK (Langfuse/LangSmith/Phoenix)
- [ ] Configure API keys and endpoints
- [ ] Instrument all LLM calls (generations)
- [ ] Add spans for business logic operations
- [ ] Set up session tracking for conversations
- [ ] Configure user identification (userId, sessionId)
- [ ] Add relevant metadata (tags, version, environment)

### OpenTelemetry Integration

- [ ] Install OpenTelemetry SDK
- [ ] Configure OTEL collector (if using)
- [ ] Set up span processors for LLM traces
- [ ] Configure exporters:
  - [ ] Primary platform (Langfuse/Phoenix)
  - [ ] Secondary APM (Datadog/New Relic/Grafana)
- [ ] Verify trace correlation across systems
- [ ] Set up sampling for high-volume workloads

### Analytics Gateway (Optional)

- [ ] Choose gateway (Helicone or Portkey)
- [ ] Configure proxy integration
- [ ] Set up caching (Helicone: 20-30% savings)
- [ ] Configure rate limiting policies
- [ ] Set up fallback routing (multi-provider)
- [ ] Enable retry policies

## Phase 3: Cost Monitoring

### Token Tracking

- [ ] Configure automatic token counting
- [ ] Set up cost calculation per model
- [ ] Track input vs output tokens separately
- [ ] Monitor cached vs non-cached requests
- [ ] Aggregate costs by:
  - [ ] User/team
  - [ ] Project/feature
  - [ ] Environment (prod/staging/dev)
  - [ ] Model

### Budget Management

- [ ] Define cost budgets (daily/weekly/monthly)
- [ ] Set up alert thresholds:
  - [ ] 70% of budget - warning
  - [ ] 90% of budget - critical
  - [ ] 100% of budget - alert on-call
- [ ] Configure notification channels (Slack, PagerDuty, email)
- [ ] Create cost anomaly detection rules
- [ ] Set up automatic rate limiting (optional)

### Cost Optimization

- [ ] Enable response caching
- [ ] Implement prompt optimization (shorter prompts)
- [ ] Configure model fallbacks (expensive to cheaper)
- [ ] Track cost per feature/endpoint
- [ ] Schedule weekly cost review

## Phase 4: Quality Evaluation

### LLM-as-Judge Setup

- [ ] Choose evaluator model (GPT-4o, Claude)
- [ ] Configure evaluation prompts:
  - [ ] Relevance scoring
  - [ ] Accuracy/hallucination detection
  - [ ] Completeness
  - [ ] Safety/toxicity
- [ ] Set up async evaluation pipeline
- [ ] Configure sampling rate (10-20% of production)

### Quality Metrics

- [ ] Track response relevance scores
- [ ] Monitor hallucination detection
- [ ] Measure user feedback (thumbs up/down)
- [ ] Track format/structure compliance
- [ ] Monitor safety/toxicity scores
- [ ] Set up quality degradation alerts

### Testing Datasets

- [ ] Create reference dataset from production traces
- [ ] Define expected outputs for regression testing
- [ ] Set up CI/CD evaluation pipeline
- [ ] Configure A/B test framework for prompts
- [ ] Automate regression detection

## Phase 5: Agent-Specific Monitoring

### Tool Use Tracking

- [ ] Trace function/tool calls
- [ ] Monitor tool call success rates
- [ ] Track tool execution latency
- [ ] Identify failing tool patterns
- [ ] Set up tool error alerts

### Multi-Step Workflow Monitoring

- [ ] Configure nested span tracing
- [ ] Track reasoning step count
- [ ] Monitor iteration/loop counts
- [ ] Detect infinite loop patterns
- [ ] Track workflow completion rates

### Agent Debugging

- [ ] Enable full prompt/response logging
- [ ] Configure intermediate state capture
- [ ] Set up replay capability
- [ ] Create agent-specific dashboards
- [ ] Document common failure patterns

## Phase 6: Alerting and Dashboards

### Alert Configuration

| Alert | Threshold | Priority |
|-------|-----------|----------|
| Error rate spike | >5% (5min) | Critical |
| Latency P99 | >10s | Warning |
| TTFT P95 | >2s | Warning |
| Cost anomaly | >150% daily avg | High |
| Quality drop | <3.5/5 avg | Medium |
| Budget threshold | >80% | Medium |
| Hallucination rate | >10% | High |

- [ ] Configure all critical alerts
- [ ] Set up escalation policies
- [ ] Test alert delivery
- [ ] Document runbooks for each alert

### Dashboard Setup

- [ ] **Executive Dashboard**
  - [ ] Total cost (MTD)
  - [ ] Cost trend (daily)
  - [ ] Cost by model/team
  - [ ] Quality score average
  - [ ] Request volume
- [ ] **Engineering Dashboard**
  - [ ] Latency distributions (P50/P95/P99)
  - [ ] TTFT metrics
  - [ ] Error rates by type
  - [ ] Trace explorer
  - [ ] Token usage trends
- [ ] **Agent Dashboard**
  - [ ] Tool call success rates
  - [ ] Iteration counts
  - [ ] Workflow completion
  - [ ] Loop detection alerts

## Phase 7: Security and Compliance

### Data Protection

- [ ] Configure PII masking/sanitization
- [ ] Validate data encryption (at rest, in transit)
- [ ] Set up audit logging
- [ ] Review API key management
- [ ] Configure access controls and permissions

### Compliance

- [ ] Document data retention policies
- [ ] Configure log rotation
- [ ] Plan capacity for trace storage
- [ ] Schedule security reviews
- [ ] Document compliance requirements

## Phase 8: Operations

### Maintenance

- [ ] Set up data retention policies (30/90/365 days)
- [ ] Configure backup procedures
- [ ] Plan capacity scaling
- [ ] Schedule regular dashboard reviews
- [ ] Automate weekly cost reports

### Documentation

- [ ] Document observability architecture
- [ ] Create onboarding guide for developers
- [ ] Write troubleshooting runbook
- [ ] Document evaluation criteria
- [ ] Maintain integration changelog

## Verification Checklist

Before going to production:

- [ ] All LLM calls are traced
- [ ] Cost tracking is accurate
- [ ] Alerts are configured and tested
- [ ] Dashboards show correct data
- [ ] PII masking is verified
- [ ] Team has dashboard access
- [ ] Runbooks are documented
- [ ] Retention policies are set

## Rollout Phases

| Phase | Focus | Deliverables |
|-------|-------|--------------|
| Week 1 | Platform setup | Basic tracing, SDK integration |
| Week 2 | Cost monitoring | Token tracking, budget alerts |
| Week 3 | Quality evaluation | LLM-as-judge, quality scores |
| Week 4 | Dashboards/alerts | Unified dashboard, alert runbooks |
| Week 5 | Agent monitoring | Tool tracking, workflow tracing |
| Week 6 | Go-live | Full production deployment |

## Success Metrics

| Metric | Target |
|--------|--------|
| Trace coverage | 100% of LLM calls |
| Alert response time | <15 min for critical |
| Cost visibility | Real-time by user/team |
| Quality score tracking | All production traces |
| Mean time to debug | <30 min with traces |
| Cache hit rate | >25% |
| Cost reduction | 20-30% with optimization |
