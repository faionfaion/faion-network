# AI Latency Waterfall Template

## Summary

**One-sentence:** Reusable latency waterfall template for an LLM call — token-by-token segments (ttfb, prefill, decode, tool round-trip, post-process) with budget and observed values, surfacing where time actually goes.

**One-paragraph:** Engineers debug AI latency with single end-to-end timer, see "the LLM is slow", and try a smaller model — missing that 60% of the time was prefill on uncached prefix, or that a tool round-trip blew the budget. This methodology produces one filled waterfall report per latency investigation, with segments (ttfb, prefill, decode tps, per-tool round-trip, post-process serialisation) plus a budget per segment and an observed value. Output is a versioned report engineers use to direct optimisation effort to the actual bottleneck.

**Ефективно для:** Команд, у яких p95 latency повзе вгору і ніхто не знає, де; за годину waterfall показує «prefill 1.2s, decode 800ms, tool round-trip 400ms», і питання стає «чи кешувати prefix, чи паралелити tool calls» — замість «давайте візьмемо Haiku».

## Applies If (ALL must hold)

- LLM-based feature is in production with measurable end-to-end latency.
- Tracing infrastructure (OTel, LangSmith, Datadog) records per-call timing.
- A target SLA exists (e.g. p95 < 5s).
- Owner can run controlled measurements (no live production traffic mutation needed).
- At least one bottleneck candidate is identifiable a priori (else use chaos-eval first).

## Skip If (ANY kills it)

- No tracing instrumentation — instrument before measuring.
- Single-call workload with no segmentation (model exposed as one black box).
- Latency is within SLA and no regression — no investigation needed.
- Prototype with no SLA target.

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Trace logs | jsonl / OTel span dump | Observability |
| SLA target | p95 ≤ X s | Product / SRE |
| Per-segment budget | s per segment | Tech lead |
| Tool latency baselines | per-tool p50/p95 | Tool catalogue |
| Named owner | handle | Engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/agent-trajectory-eval-method/AGENTS.md` | Trajectory metrics include system_efficiency.latency_ms; waterfall drills into it. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: segment-not-aggregate, budget per segment, ≥30 samples, p50+p95, cached vs cold | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the waterfall report | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure: instrument → sample → segment → diff vs budget → recommend | ~900 |
| `content/05-examples.xml` | medium | Worked example: support-agent latency waterfall | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: instrumented? → ≥30 samples? → biggest segment over budget? → optimise/escalate | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `parse_traces_to_segments` | haiku | Mechanical extraction. |
| `compute_percentiles` | haiku | Mechanical stats. |
| `diff_vs_budget_and_recommend` | sonnet | Per-segment judgment. |
| `executive_review` | opus | For SLA breach with customer impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the waterfall report. |
| `templates/output.example.json` | Filled example. |
| `templates/waterfall.md` | Markdown skeleton with the segment table. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the report. | After authoring, before forwarding to engineering. |

## Related

- parent skill: `geek/ai/ai-agents/`
- peer: [[agent-trajectory-eval-method]] — trajectory eval surfaces latency_ms; waterfall drills into it.
- peer: [[batch-cache-stack]] — prompt-caching is the typical fix for prefill bottlenecks.

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is tracing instrumented? (2) are there ≥30 samples? (3) which segment exceeds budget? Leaves point to "optimise that segment", "instrument missing dimension", or "escalate SLA renegotiation".

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ai-latency-waterfall-template/output.json",
  "title": "Ai Latency Waterfall Template Output",
  "description": "purpose=schema; consumes=brief+context; produces=artefact; depends-on=01-core-rules.xml; token-budget-impact=low",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "version",
    "version_stamp",
    "produced_at",
    "rationale",
    "inputs_used"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "minLength": 3
    },
    "owner": {
      "type": "string",
      "minLength": 1
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "version_stamp": {
      "type": "string"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "fields": {
      "type": "object"
    },
    "rationale": {
      "type": "string",
      "minLength": 20
    },
    "inputs_used": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    }
  }
}
```

### `templates/output.example.json`

```json
{
  "artefact_id": "ai-latency-waterfall-template-example-001",
  "owner": "alex@faion.net",
  "version": "1.0.0",
  "version_stamp": "ai-latency-waterfall-template@1.0.0",
  "produced_at": "2026-05-22T12:00:00Z",
  "fields": {
    "placeholder_field": "filled-by-author"
  },
  "rationale": "Example output for Ai Latency Waterfall Template; references at least one named input.",
  "inputs_used": [
    "docs/brief.md"
  ]
}
```
