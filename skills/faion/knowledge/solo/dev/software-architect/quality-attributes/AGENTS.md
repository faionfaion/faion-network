# Quality Attributes

## Summary

Quality attributes (non-functional requirements, "-ilities") are measurable properties that determine whether a system succeeds in production: Performance, Scalability, Availability, Reliability, Security, Maintainability, Testability, Observability. Every quality requirement must be expressed as a 6-part scenario (Source, Stimulus, Environment, Artifact, Response, Response Measure) with a concrete, testable threshold — vague requirements like "the system should be fast" are not actionable.

## Why

Functional requirements describe what a system does; quality attributes describe whether it survives real-world conditions. Systems that meet all functional requirements but fail on latency, availability, or security invariably fail in production. Quality attributes also conflict: improving security adds latency, improving scalability adds complexity. Explicit, prioritized, measurable QA scenarios let architects make informed trade-offs instead of implicit ones.

## When To Use

- System design phase: establishing measurable NFRs before selecting architecture style
- Architecture review: evaluating an existing system against business SLOs
- Trade-off analysis: choosing between architecture options when they affect different attributes differently
- SLO definition: setting error budgets and reliability targets for SRE teams
- ATAM (Architecture Tradeoff Analysis Method): formal utility tree + scenario prioritization
- Writing ADRs: NFR context is required in the Decision Drivers section

## When NOT To Use

- When performance/security requirements are already well-defined and being tested — this methodology is for defining and prioritizing, not for implementation
- For pure functional requirements (what the system does) — use spec.md / SDD methodology instead
- When the system is a throwaway prototype where NFRs are irrelevant
- After architecture is locked and no trade-off decisions remain — at that point use the specific architecture methodology (observability-architecture, security-architecture, etc.)

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-attributes.xml` | Performance (latency p50/p95/p99, throughput), Scalability (vertical/horizontal/elastic), Availability (SLA table), Reliability (MTBF/MTTR) — definitions, metrics, tactics |
| `content/02-secondary-attributes.xml` | Security (CIA + auth), Maintainability (SOLID, modularity), Testability (levels), Observability (logs/metrics/traces) — definitions and architectural tactics |
| `content/03-tradeoffs-and-slo.xml` | Common QA trade-off pairs; SLI/SLO/SLA framework; error budget calculation; 6-part scenario format (Source/Stimulus/Environment/Artifact/Response/Measure) |

## Templates

| File | Purpose |
|------|---------|
| `templates/qa-scenario.md` | 6-part quality attribute scenario template with example filled in |
| `templates/slo-doc.md` | SLO definition document: SLI, target, error budget, alerting thresholds |
