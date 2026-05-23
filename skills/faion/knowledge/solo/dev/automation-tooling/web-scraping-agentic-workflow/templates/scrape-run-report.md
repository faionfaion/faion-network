<!--
purpose: Per-run scrape report skeleton authors emit at end of run.
consumes: nothing — this IS the artefact.
produces: report.md → JSON via scorer; JSON is the schema-validated form.
depends-on: scrape run completed; robots/render/tool/drift fields populated.
token-budget-impact: ~150 tokens when copied.
-->

# Scrape run — &lt;source&gt; — &lt;run_id&gt;

## Identity
- artefact_id: wsr-&lt;slug&gt;
- source:
- run_id: YYYY-MM-DDTHHMMZ-&lt;random&gt;
- user_agent: faion-network/1.0 (+mailto:contact@domain)

## Robots
- fetched_at:
- allowed:

## Tool selection
- render_mode: ssr | js | managed
- tool: httpx-selectolax | playwright | firecrawl | jina-reader

## Rows
- rows_seen:
- rows_valid:
- raw_path: raw/YYYY-MM-DD/&lt;source&gt;.jsonl

## Drift
- drift_score (%):
- drift_fields_disappeared:

## Verdict
- [ ] promote
- [ ] block-validation-low
- [ ] block-drift-high
- [ ] block-tool-mismatch
- [ ] block-robots-disallow

## Versioning
- version: 1.0.0
- last_reviewed: YYYY-MM-DD
