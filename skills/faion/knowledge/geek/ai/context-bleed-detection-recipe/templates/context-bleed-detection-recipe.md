<!--
purpose: Markdown skeleton for a context-bleed incident record.
consumes: probe_signal payload from the detector run.
produces: a Markdown incident record for the on-call timeline.
depends-on: content/02-output-contract.xml schema.
token-budget-impact: ~180 tokens.
-->

# Context Bleed Incident — &lt;incident_id&gt;

- **incident_id**: cbi-2026-05-22-001
- **owner**: &lt;handle or pager — single named human, never "team"&gt;
- **bleed_type**: cross-tenant | prior-turn | system-drift | clean
- **detected_at**: 2026-05-22T10:32:11Z
- **version**: 1.0.0

## Probe signal

- canary_hit: true
- embedding_distance: 0.08
- snapshot_diff: none

## Affected sessions

- a1b2c3d4e5f60718
- f9e8d7c6b5a40392

## Threshold

cosine 0.15 (default)

## Kill switch

- scope: worker-pool
- target: pool-3
- human_approval: false

## Notes

&lt;e.g., "false positive ruled out via canary lineage", "supersedes cbi-2026-05-21-007".&gt;
