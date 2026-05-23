<!-- purpose: AcceptanceRecord skeleton -->
<!-- consumes: impact data + cost-curve + tier options -->
<!-- produces: scaffold consumed by capture-acceptance step -->
<!-- depends-on: content/01-core-rules.xml#r3-tier-banded-options -->
<!-- token-budget-impact: ~150 tokens -->

# RPO/RTO Acceptance Record — [system_id]

**Owner:** [architect] / [person]
**Version:** [semver]

## Impact basis

[$/hr revenue loss + historical outage hours/year]

## Options presented (≥ 3)

| tier_name | rpo | rto | annual_cost_delta | operational_impact |
|-----------|-----|-----|-------------------|--------------------|
| tier-0    | 24h | 8h  | +$0               | current baseline |
| tier-1    | 1h  | 4h  | +$11k/yr          | hourly snapshots; warm standby |
| tier-2    | 15min | 1h | +$28k/yr          | streaming replication; cross-region failover |
| tier-3    | <1min | <15min | +$140k/yr     | active-active |

## Chosen

- tier_name: ...
- rpo: ...
- rto: ...
- stakeholder_echo: "..." (verbatim quote)

## Audit

- stakeholder_handle: @cfo
- evidence_link: meet://transcripts/YYYY-MM-DD
- decided_at: YYYY-MM-DD
- refresh_due: YYYY-MM-DD (≤ 12 months from decided_at)
