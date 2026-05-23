<!-- purpose: HA Architecture Decision Record skeleton with SLA + topology + failure modes -->
<!-- consumes: see content/02-output-contract.xml inputs (sla_target, lb_instances, azs_used, gslb_kind, drain_on_sigterm) -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml (two-lb-min, two-az-min, anycast-over-dns-for-9999, drain-on-sigterm) -->
<!-- token-budget-impact: ~400 tokens when loaded as context -->

# HA Decision: <service-name>

## Context

- **Service:** <service-name>
- **SLA target:** 99.99% (~52 min/year)
- **Customer geography:** US + EU
- **Current state:** <describe>

## Decision

| Tier | Choice | Rationale |
|------|--------|-----------|
| LB instances | 2 (managed ALB in each region) | rule two-lb-min |
| AZs used per region | 3 | rule two-az-min |
| Backends per AZ | 2 | rule two-az-min |
| GSLB | AWS Global Accelerator (anycast) | rule anycast-over-dns-for-9999 |
| Drain on SIGTERM | yes, deregistration_delay = 30 s | rule drain-on-sigterm |

## Failure-domain analysis

| Failure | Blast radius | Mitigation |
|---------|--------------|------------|
| Process crash | 1 instance | managed LB removes via health-check |
| Host failure | 1 instance | AZ-level spread absorbs |
| AZ failure | 1/3 of one region | 2 AZ remain with capacity |
| Region failure | 1 region | Global Accelerator fails over to peer region |
| BGP route flap | edge PoP | client retry; anycast reroutes within ~30 s |

## Operational requirements

- Chaos drill: monthly LB-instance kill + quarterly region failover.
- SIGTERM handler: see [sigterm-drain.py](sigterm-drain.py).
- Alert on healthy-target-count &lt; 2 in any AZ.

## Status

- [ ] Approved
- [ ] Deployed
- [ ] Drill passed
