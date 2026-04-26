# Microservices Architecture

## Summary

Methodology for decomposing applications into independently deployable services organised around business capabilities. Covers the decision framework (microservices vs modular monolith), prerequisites, decomposition strategies (business capability, DDD subdomains, volatility, Strangler Fig), communication patterns (REST/gRPC/GraphQL vs async messaging), database-per-service, and anti-patterns.

## Why

Microservices enable independent deployment and scaling per service, and team autonomy aligned with Conway's Law — but only when prerequisites are met. Skipping domain analysis leads to a distributed monolith: services that must be deployed together and share databases, combining all the complexity of microservices with none of the benefits. The decision framework prevents premature decomposition.

## When To Use

- Team size exceeds 30 developers with clear sub-team ownership per domain
- Domain boundaries are well-understood via DDD or business capability mapping
- Mature CI/CD, container orchestration, and observability are already in place
- Different services have genuinely different scaling profiles (catalogue vs checkout)
- Strangler Fig migration: extracting bounded contexts from an existing monolith

## When NOT To Use

- Team smaller than 10 developers — operational overhead outweighs autonomy benefits
- MVP or early-stage product where domain boundaries are not yet understood
- Limited DevOps maturity — microservices require automation to be operational
- Simple CRUD application — a monolith or modular monolith is cheaper and faster
- Tight budget — microservices multiply infrastructure and observability costs

## Content

| File | What's inside |
|------|---------------|
| `content/01-decision-and-decomposition.xml` | Decision framework tree, prerequisites table, decomposition strategies (business capability, DDD subdomains, volatility, Strangler Fig phases) |
| `content/02-communication-patterns.xml` | REST vs gRPC vs GraphQL trade-offs, async messaging options (queues vs event streaming vs pub/sub), communication decision tree, database-per-service rationale |
| `content/03-antipatterns-and-resilience.xml` | Distributed monolith, shared database, chatty communication, no API versioning antipatterns; Circuit Breaker + Retry + Bulkhead + Timeout resilience patterns; Kubernetes sidecar/ambassador/init container patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/service-dockerfile` | Minimal multi-stage Dockerfile for a Python/Go microservice with non-root user |
| `templates/k8s-service-deployment.yaml` | Deployment + Service + HPA manifest with health probes and resource limits |
