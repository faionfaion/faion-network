# Reliability Architecture

## Summary

Designing systems that maintain availability targets, recover from failures, and degrade gracefully under stress. Core outputs: SLO/SLI/error-budget definitions, fault-tolerance pattern selection (circuit breaker, retry with jitter, bulkhead, timeout), graceful degradation tiers, health check endpoints, chaos engineering plan, and DR strategy (RPO/RTO, 3-2-1 backups).

## Why

Without explicit reliability design, every component failure becomes a user-facing incident. Error budgets translate business uptime goals (99.9% = 43 min/month downtime) into actionable engineering constraints. Patterns like circuit breakers prevent cascading failures; bulkheads stop one failing dependency from exhausting shared resources.

## When To Use

- Defining SLOs before a new service goes to production
- Conducting an architecture review where availability targets exceed 99.9%
- Adding fault tolerance after an outage revealed cascading failure modes
- Designing health check endpoints for Kubernetes probes
- Planning a chaos engineering programme or DR drill

## When NOT To Use

- MVP or internal tool where 99% availability (3.65 days/year downtime) is acceptable — over-engineering adds cost
- Single-service monolith without external dependencies — most patterns target distributed call paths
- When the bottleneck is a business/product problem, not an infrastructure one

## Content

| File | What's inside |
|------|---------------|
| `content/01-slo-sli-error-budget.xml` | SLI types by service, SLO targets by tier, error budget calculation, policy triggers |
| `content/02-fault-tolerance-patterns.xml` | Circuit breaker states/config, retry with exponential backoff + jitter, bulkhead types, timeout management |
| `content/03-graceful-degradation.xml` | Feature criticality matrix (P0-P3), degradation patterns, load shedding priority levels |
| `content/04-health-checks-dr.xml` | Kubernetes probe types, health endpoint design, RPO/RTO strategies, 3-2-1 backup rule, chaos engineering maturity model |

## Templates

| File | Purpose |
|------|---------|
| `templates/slo-definition.yaml` | SLO document template with SLI expression, target, window, and error budget |
| `templates/circuit-breaker.py` | Python circuit breaker implementation with decorator usage |
| `templates/retry-config.py` | tenacity-based retry decorator factory with jitter |
| `templates/health-endpoint.py` | FastAPI liveness/readiness/startup endpoints with structured response |
