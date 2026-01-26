---
id: llm-observability-checklist
name: "LLM Observability Implementation Checklist"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Implementation Checklist

## Phase 1: Foundation

### Platform Selection

- [ ] Define requirements (self-hosted vs SaaS, budget, team size)
- [ ] Evaluate platforms against criteria:
  - [ ] Open source requirement (Langfuse, Phoenix, LangWatch)
  - [ ] LangChain integration (LangSmith preferred)
  - [ ] Cost optimization focus (Helicone)
  - [ ] Multi-provider routing (Portkey)
- [ ] Set up free tier / proof of concept
- [ ] Validate data residency requirements (GDPR, SOC2)

### Basic Integration

- [ ] Install SDK (Python/JavaScript)
- [ ] Configure API keys and endpoints
- [ ] Instrument first LLM call
- [ ] Verify trace appears in dashboard
- [ ] Test error handling and logging

## Phase 2: Tracing Setup

### Core Tracing

- [ ] Trace all LLM calls (generations)
- [ ] Add spans for business logic operations
- [ ] Configure session tracking for conversations
- [ ] Set up user identification (userId metadata)
- [ ] Add relevant metadata (tags, labels, version)

### Trace Enrichment

- [ ] Add custom attributes to traces
- [ ] Configure trace sampling for high-volume workloads (10-20%)
- [ ] Set up PII masking / data sanitization
- [ ] Add cost tracking per trace
- [ ] Configure TTFT (Time to First Token) measurement

### Agent/RAG Specific

- [ ] Trace retrieval operations (context, scores)
- [ ] Track tool/function call invocations
- [ ] Instrument multi-step agent workflows
- [ ] Add embedding generation traces
- [ ] Track reranking operations

## Phase 3: Cost Monitoring

### Token Tracking

- [ ] Configure automatic token counting
- [ ] Set up cost calculation per model
- [ ] Track input vs output tokens separately
- [ ] Monitor cached vs non-cached requests
- [ ] Aggregate costs by user/team/project

### Budgets and Alerts

- [ ] Define cost budgets (daily/weekly/monthly)
- [ ] Set up alert thresholds (70%, 90%, 100%)
- [ ] Configure notification channels (email, Slack, PagerDuty)
- [ ] Create cost anomaly detection rules
- [ ] Set up automatic rate limiting (optional)

### Cost Optimization

- [ ] Enable response caching (Helicone: 20-30% savings)
- [ ] Implement prompt optimization (shorter prompts)
- [ ] Configure model fallbacks (expensive → cheaper)
- [ ] Track cost per feature/endpoint
- [ ] Review and optimize high-cost traces weekly

## Phase 4: Quality Evaluation

### Automated Evaluations

- [ ] Set up LLM-as-judge evaluators
- [ ] Configure built-in criteria (helpfulness, coherence, safety)
- [ ] Add custom evaluation prompts
- [ ] Run evaluations on production traces (sampled)
- [ ] Store evaluation scores with traces

### Quality Metrics

- [ ] Track response relevance scores
- [ ] Monitor hallucination detection
- [ ] Measure user feedback (thumbs up/down)
- [ ] Track format/structure compliance
- [ ] Monitor safety/toxicity scores

### Testing Datasets

- [ ] Create reference dataset from production traces
- [ ] Define expected outputs for regression testing
- [ ] Set up CI/CD evaluation pipeline
- [ ] Compare prompt/model versions
- [ ] Automate regression detection

## Phase 5: Prompt Management

### Version Control

- [ ] Centralize prompts in prompt registry
- [ ] Enable versioning for all prompts
- [ ] Link traces to prompt versions
- [ ] Set up rollback capability
- [ ] Document prompt changes

### Prompt Testing

- [ ] Create prompt playground environment
- [ ] Set up A/B testing framework
- [ ] Define prompt performance metrics
- [ ] Automate prompt comparison
- [ ] Document winning variants

## Phase 6: Dashboards and Alerts

### Key Dashboards

- [ ] Executive dashboard (cost, quality, usage)
- [ ] Engineering dashboard (latency, errors, traces)
- [ ] Model performance comparison
- [ ] User/session analytics
- [ ] Prompt performance tracking

### Alert Configuration

| Alert Type | Threshold | Priority |
|------------|-----------|----------|
| Error rate spike | >5% (5min window) | High |
| Latency P99 | >5s | Medium |
| Cost anomaly | >150% daily average | High |
| Quality drop | <3.5/5 avg score | Medium |
| Token limit | >80% budget | Medium |

- [ ] Configure all critical alerts
- [ ] Set up escalation policies
- [ ] Test alert delivery
- [ ] Document runbooks for each alert

## Phase 7: Operations

### Maintenance

- [ ] Set up data retention policies (30/90/365 days)
- [ ] Configure log rotation
- [ ] Plan capacity for trace storage
- [ ] Schedule regular dashboard reviews
- [ ] Automate weekly cost reports

### Documentation

- [ ] Document observability architecture
- [ ] Create onboarding guide for new developers
- [ ] Write troubleshooting runbook
- [ ] Document evaluation criteria
- [ ] Maintain integration changelog

### Security

- [ ] Audit API key management
- [ ] Review PII masking configuration
- [ ] Validate data encryption (at rest, in transit)
- [ ] Check access controls and permissions
- [ ] Schedule security reviews

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

## Rollout Strategy

1. **Week 1**: Platform setup, basic tracing
2. **Week 2**: Cost monitoring, alerts
3. **Week 3**: Quality evaluations, prompt registry
4. **Week 4**: Dashboards, documentation, go-live

## Success Metrics

| Metric | Target |
|--------|--------|
| Trace coverage | 100% of LLM calls |
| Alert response time | <15 min for critical |
| Cost visibility | Real-time by user/team |
| Quality score tracking | All production traces |
| Mean time to debug | <30 min with traces |
