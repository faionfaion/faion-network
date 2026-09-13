<!-- purpose: Unit-economics report skeleton — one section per block of content/02-output-contract.xml -->
<!-- consumes: Per-call usage log, pinned price sheet, success events, revenue attribution (AGENTS.md Prerequisites) -->
<!-- produces: artefact conforming to content/02-output-contract.xml for produces=report -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~500 tokens when loaded as context -->

# Inference Unit Economics Report

_Skeleton for the `inference-cost-unit-economics` report. The JSON sidecar (`templates/cost-decomposition.json`) is the validated artefact; this document is its readable form. Fill every section; do not leave a heading empty._

## Report

- report_id / as_of / author
- Window: start, end, days (at least 7 days of production traffic)
- Token source: provider `usage` object per call; monthly sum reconciled against the invoice on (date), gap (%)
- Headline metric: cost per successful outcome

## Price sheet

| Provider | Model id (dated snapshot) | Sheet date / URL | Input per 1M | Output per 1M | Cached input per 1M | Discount (kind, %) |
|----------|---------------------------|------------------|--------------|---------------|---------------------|--------------------|

## Per feature

### (feature_id)

- Success definition: (observable outcome, time bound, source event)
- Successful outcomes in window: (count)
- Cost lines per outcome: input tokens / output tokens / cached input / retrieval / tools
- Cost per outcome: p50 / p95 / mean; tail-dominated (p95 > 5 x p50)? driver
- Cost per call (supporting figure only)
- Retry share of cost: (%) — cause named and first action = retry policy when above 15%
- Revenue basis: attributed revenue | allocation rule (key) | value proxy (derivation)
- Revenue per outcome, gross margin, target margin
- Cost ceiling per outcome = revenue x (1 - target margin); daily spend alert (kind, threshold, where wired)

## Features over ceiling

| Feature | Mean cost per outcome | Ceiling | Gap | Action owner |
|---------|-----------------------|---------|-----|--------------|

## First actions

- Per feature, in order: retry policy where retry share > 15%, then the dominant cost line.

## Provenance

- Author, reviewer, date
- Validator run: `python scripts/validate-inference-cost-unit-economics.py --file report.json`
- Next refresh scheduled: (date)
