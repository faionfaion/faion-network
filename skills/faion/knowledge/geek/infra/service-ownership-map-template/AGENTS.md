---
slug: service-ownership-map-template
tier: geek
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Service Ownership Map Template — a versioned service→owner artefact that powers triage routing for Sentry / Datadog alerts in product-dev teams.
content_id: "4348da368aff0d9a"
tags: [service-ownership-map-template, infra, geek]
---
# Service Ownership Map Template

## Summary

**One-sentence:** A canonical service→owner map that lets in-hours alert triage (Sentry, Datadog) route incidents to a named human within seconds, with no tribal-knowledge lookups.

**One-paragraph:** Every P6 product-dev team rebuilds the same artefact from scratch — a list of services, each tagged with primary on-call, escalation owner, slack channel, and runbook link. This methodology codifies the artefact: schema, generation source (service registry / IaC tags), update cadence, and the contract triage tools consume. Without it, alerts land in shared channels, response times balloon, and the team relearns ownership every quarter.

## Applies If (ALL must hold)

- the team operates ≥3 production services with on-call coverage
- alert tooling (Sentry, Datadog, PagerDuty) supports per-service routing via tags or webhooks
- the team accepts a single source-of-truth file checked into version control
- tier == geek (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- only one service exists — a wiki line suffices
- ownership is already encoded inside the observability tool's UI and stays current automatically
- the team has zero on-call rotation (alerts go nowhere regardless)

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | 5 testable rules covering schema, source-of-truth, refresh cadence, escalation chain, and tool-side enforcement |

## Related

- upstream playbook: `p6-product-dev-team/Sentry / Datadog alert triage (in-hours)`
- parent skill: `geek/infra/`
