<!-- purpose: Markdown skeleton for the IDP spec -->
<!-- consumes: inputs declared in AGENTS.md `## Prerequisites` -->
<!-- produces: artefact conforming to content/02-output-contract.xml (spec) -->
<!-- depends-on: content/01-core-rules.xml + content/02-output-contract.xml -->
<!-- token-budget-impact: ~500 tokens when loaded -->

# Internal Developer Platform Spec

- **Org:** 
- **Author:** 
- **Date:** 
- **Sponsor:** 

## Current state

- DevOps ticket volume / month: 
- Onboarding TTFD (time-to-first-deploy): 
- Dev NPS: 
- Service count: 
- Compliance scope: 

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Service catalogue / portal | Backstage / Port / Cortex / none-yet | |
| Orchestration backend | Crossplane / Humanitec / Kratix / homegrown | |
| IaC engine | Terraform / Pulumi / both | |
| Golden path #1 | Go microservice / Node API / Python data pipeline / other | |
| RBAC model | groups + roles + AI-agent identity | |

## Metrics dashboard

- DORA: DF / LT / MTTR / CFR
- Platform: self-service adoption rate, TTFD for new devs, ticket trend, NPS

## Explicit non-goals (year 1)

- (e.g.) multi-cloud abstraction; left to year 2.
- (e.g.) database self-service; left to year 2.
