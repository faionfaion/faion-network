# Postmortem: <Incident Title>

> incident_id: <INC-YYYY-MMDD-NNN>
> severity: <SEV1 | SEV2 | SEV3>
> services: <comma-separated>
> commander: <@handle>
> status: draft           <!-- agent fills as draft; human flips to published -->
> tone: blameless

## Summary

One paragraph in plain language. Customer-visible behavior. Duration. Whether data was lost.

## Timeline (UTC)

<!-- Each line MUST end with a citation: [slack:...] [alert:...] [deploy:...] [pr:...] -->

- HH:MM <event> [source-id]
- HH:MM <event> [source-id]

## Impact

- Affected services and surfaces.
- Estimated user-minutes / requests / revenue.
- SLO budget consumed.

## Root Cause Hypothesis

<!-- Agent-writable. Mark each non-quoted claim with `(hypothesis)`. -->

- The change in deploy `<sha>` reduced X (hypothesis); when load Y arrived, Z saturated (hypothesis).

## Contributing Factors

- Process / design / monitoring gaps that allowed the incident to grow. Mark `(hypothesis)` where uncertain.

## Action Items

<!-- One row per item; owner is a human handle, not the agent. -->

| ID  | Action                       | Owner    | Due       | Status |
|-----|------------------------------|----------|-----------|--------|
| AI-1| Add p99-pool-saturation alert| @teamA   | 2026-MM-DD| open   |
| AI-2| Document pool-size change    | @teamA   | 2026-MM-DD| open   |

## Root Cause (HUMAN-WRITTEN)

<!--
Filled by the incident commander before publishing.
The agent must NOT fill this section.
-->

- (left blank for human review)
