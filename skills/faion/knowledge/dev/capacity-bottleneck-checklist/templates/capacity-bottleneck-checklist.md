<!-- purpose: Markdown skeleton naming the checklist sections. | consumes: see content/02-output-contract.xml inputs | produces: artefact conforming to content/02-output-contract.xml (capacity-bottleneck-checklist) | depends-on: content/01-core-rules.xml | token-budget-impact: small (template is loaded only when an artefact is being authored) -->
# Capacity Bottleneck Checklist — <artefact_id>

**Owner:** <@handle>
**Version:** 1.0.0
**Last reviewed:** 2026-05-23
**Headroom:** <pct>%

## Decision

<one-line decision>

## Rationale

Cites inputs by path. ≥2 sentences referencing measured values.

## Bottleneck candidates

- [ ] DB connections (pool size, saturation)
- [ ] Queue throughput (consumer lag, ack rate)
- [ ] Gateway TLS handshakes / connection reuse
- [ ] Autoscale lag (scale-out time to first-served-request)
- [ ] Hot keys / shard imbalance
- [ ] Fan-out limits (downstream backpressure)

## Inputs used

| Path | Type |
|------|------|
| observability/load-test-2026-05-22.html | report |
| observability/web-cpu-p95.json | metric |
