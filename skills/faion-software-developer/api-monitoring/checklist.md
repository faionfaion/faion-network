# Checklist

## Planning Phase

- [ ] Define SLOs (service level objectives)
- [ ] Define key metrics (availability, latency, errors)
- [ ] Plan alert thresholds (p50, p95, p99 latency)
- [ ] Identify critical endpoints to monitor
- [ ] Plan dashboards (team, management, operations)
- [ ] Define on-call rotation and escalation

## Health Check Implementation Phase

- [ ] Create /health endpoint (liveness probe)
- [ ] Create /health/ready endpoint (readiness probe)
- [ ] Check database connectivity
- [ ] Check Redis/cache connectivity
- [ ] Check external service dependencies
- [ ] Return proper status codes (200 vs 503)
- [ ] Test health checks manually

## Metrics Collection Phase

- [ ] Set up Prometheus/metrics collection
- [ ] Implement request counter metric
- [ ] Implement request latency histogram
- [ ] Implement error rate counter
- [ ] Add labels (method, endpoint, status)
- [ ] Implement custom business metrics
- [ ] Expose /metrics endpoint
- [ ] Configure scraping interval

## Structured Logging Phase

- [ ] Add request ID to all logs
- [ ] Log request start with metadata
- [ ] Log request completion with status/latency
- [ ] Log errors with full context
- [ ] Use structured logging format (JSON)
- [ ] Avoid logging sensitive data
- [ ] Configure log level appropriately

## Alerting Phase

- [ ] Define alert rules for high error rate
- [ ] Define alert for slow responses (p95/p99)
- [ ] Define alert for service unavailability
- [ ] Define alert for dependency failures
- [ ] Set appropriate alert thresholds
- [ ] Configure alert routing/escalation
- [ ] Create runbooks for each alert

## Dashboard Setup Phase

- [ ] Create operational dashboard (requests, errors, latency)
- [ ] Create business dashboard (revenue, conversions)
- [ ] Add graphs for key metrics
- [ ] Add status indicators
- [ ] Create SLO burn down chart
- [ ] Make dashboards accessible to team

## Testing Phase

- [ ] Test health checks work correctly
- [ ] Test metrics are collected and exposed
- [ ] Test log aggregation works
- [ ] Test alerts trigger correctly
- [ ] Test alert routing works
- [ ] Load test monitoring overhead

## Integration Phase

- [ ] Integrate metrics with alerting system
- [ ] Integrate logs with log aggregation platform
- [ ] Connect dashboards to data sources
- [ ] Configure data retention policies
- [ ] Test end-to-end monitoring flow

## Deployment

- [ ] Deploy monitoring infrastructure
- [ ] Configure service to emit metrics/logs
- [ ] Set up SLO tracking
- [ ] Train team on dashboards
- [ ] Create documentation for metrics/alerts