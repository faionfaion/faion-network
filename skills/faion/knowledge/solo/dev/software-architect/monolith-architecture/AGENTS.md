# Monolith Architecture

## Summary

A monolith is a single deployable unit containing all application functionality. It is the correct starting architecture for teams of fewer than 10, unvalidated business models, and domains whose boundaries are not yet understood. The "Monolith First" principle (Fowler) holds: start simple, add complexity only when scaling data proves you need it. Modern monoliths use vertical slice organization or modular structure — not the traditional layered anti-pattern that causes anemic domain models.

## Why

Almost every successful microservices migration started from a well-structured monolith. Systems decomposed into microservices prematurely (before domain boundaries are understood) become distributed monoliths — the worst of both worlds. A monolith provides ACID transactions, in-process communication with zero network latency, a single deployment pipeline, and simpler debugging. Shopify, GitHub, Basecamp, and Stack Overflow run monoliths at massive scale with the right internal organization.

## When To Use

- Team size is fewer than 10 developers
- MVP or startup: speed to market matters more than scalability
- Domain boundaries are unclear or evolving
- Limited DevOps maturity: no Kubernetes/distributed systems expertise
- Budget constraints: single server, simpler infrastructure
- Rapid iteration phase where all code in one place accelerates changes
- Building the foundation for a future modular monolith or selective microservices extraction

## When NOT To Use

- Independent per-feature scaling is already needed (measurably different traffic profiles)
- 10+ developers with independent release cadences causing merge conflicts and deploy bottlenecks
- Different modules have fundamentally different tech stack requirements
- Deployment frequency is already high and feature teams are blocking each other — switch to modular-monolith first
- Module build and test time exceeds 30 minutes — a sign the monolith has grown past the modular-monolith extraction threshold

## Content

| File | What's inside |
|------|---------------|
| `content/01-architecture-styles.xml` | Layered, Vertical Slice, and Modular Monolith internal organization — trade-offs and when to use each |
| `content/02-scaling-and-deployment.xml` | Vertical vs horizontal scaling; stateless requirements; blue-green and canary deployments; feature flags |
| `content/03-migration-signals.xml` | Warning signs the monolith has outgrown itself; migration path: Monolith → Modular Monolith → Selective Microservices; Strangler Fig pattern |

## Templates

| File | Purpose |
|------|---------|
| `templates/vertical-slice-layout.txt` | Directory layout for vertical slice architecture in Python/Django |
| `templates/structured-logging.py` | structlog structured logging example with JSON output |
