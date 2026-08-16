# AI Cost Attribution Schema

## Summary

**One-sentence:** Produces a JSON Schema + middleware spec that tags every LLM call with tenant, feature, route, model, prompt-cache-hit so cost reports are sliceable per dimension.

**One-paragraph:** A raw vendor invoice is a single number ("$8,431 this month"). Without an attribution schema the team cannot answer "which feature caused the increase?", "which tenant cost us money?", "did the prompt-cache rollout pay off?". This methodology defines the mandatory call-side metadata (tenant_id, feature, route, model, prompt_cache_hit, input_tokens, output_tokens, latency_ms, request_id), the middleware that stamps it on every request, and a daily aggregator producing a sliceable table. The schema is shared between the app, the FinOps team, and the cost dashboard.

**Ефективно для:** multi-tenant SaaS, internal AI tools shared across teams, agents with parallel tool calls, model-routing pipelines that need ROI evidence.

## Applies If (ALL must hold)

- Monthly LLM bill exceeds the threshold where slicing matters (≥ $1k/mo typical).
- Application has ≥2 features or tenants that should be attributable.
- A telemetry pipeline (logs, OTel, ClickHouse, etc.) can ingest structured records.
- A FinOps or engineering owner consumes the resulting report.

## Skip If (ANY kills it)

- Single-feature single-tenant prototype — attribution overhead exceeds insight.
- LLM bill below $100/mo — slicing doesn't unlock budget decisions.
- No telemetry pipeline yet — fix that first; this methodology assumes ingestion exists.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of features calling LLMs | YAML | engineering wiki |
| Tenant model (multi/single) | doc | architecture |
| Telemetry ingest endpoint | URL + creds | observability stack |
| Vendor pricing per model | table | finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `[[latency-vs-quality-decision-grid]]` | Routing config consumes the cost column. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: 8 required tags, middleware-stamped, no-blank-tenant, cost computed at write, daily aggregator, dashboard | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for per-call record + aggregated daily table | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: optional tags, tenant-as-string, cost-at-read-time, sampled-not-full, no-aggregator | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: list features → define schema → wire middleware → ingest → aggregate → dashboard | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "monthly bill > $1k AND ≥2 attribution dimensions matter?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Inventory feature list | sonnet | Mechanical extraction from code. |
| Author middleware sketch | opus | Cross-language reasoning. |
| Aggregate SQL drafted | haiku | Pure SQL template. |
| Dashboard layout | sonnet | UX-light. |

## Templates

| File | Purpose |
|---|---|
| `templates/attribution.schema.json` | JSON Schema for per-call attribution record. |
| `templates/middleware.py` | Python middleware reference (FastAPI/Django shape). |
| `templates/middleware.ts` | TypeScript middleware reference (Express/Next shape). |
| `templates/daily-aggregator.sql` | SQL aggregator producing the daily attribution table. |
| `templates/_smoke-test.json` | Single valid attribution record. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-cost-attribution-schema.py` | Validates a JSONL of attribution records against the schema and asserts no records have blank/generic tenant or feature. | Pre-commit on test fixtures; CI on dashboard data sources. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/llm-integration/`
- `[[latency-vs-quality-decision-grid]]` — consumes the per-call cost
- `[[llm-drift-daily-triage]]` — references cost deltas

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether attribution is worth the wiring: skip when bill or feature count is tiny; route to baseline-instrumentation-first when telemetry pipe is missing.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/attribution.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/ai-cost-attribution-record",
  "_purpose": "Schema for one attribution record emitted per LLM call by the middleware.",
  "_consumes": "middleware.py / middleware.ts",
  "_produces": "validation verdict + reject decision",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator/ingest only",
  "type": "object",
  "required": [
    "request_id",
    "ts",
    "tenant_id",
    "feature",
    "route",
    "model",
    "prompt_cache_hit",
    "input_tokens",
    "output_tokens",
    "latency_ms",
    "cost_usd"
  ],
  "properties": {
    "request_id": {
      "type": "string"
    },
    "ts": {
      "type": "string"
    },
    "tenant_id": {
      "type": "string",
      "pattern": "^(?!team$|us$|unknown$|tbd$|n/a$).+"
    },
    "feature": {
      "type": "string",
      "minLength": 1
    },
    "route": {
      "type": "string"
    },
    "model": {
      "type": "string"
    },
    "prompt_cache_hit": {
      "type": "boolean"
    },
    "input_tokens": {
      "type": "integer",
      "minimum": 0
    },
    "output_tokens": {
      "type": "integer",
      "minimum": 0
    },
    "latency_ms": {
      "type": "integer",
      "minimum": 0
    },
    "cost_usd": {
      "type": "number",
      "minimum": 0
    },
    "pricing_snapshot_id": {
      "type": "string"
    }
  }
}
```

### `templates/middleware.py`

```python
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Callable, Any

# In production import the real pricing table + sink.
PRICING: dict[str, dict[str, float]] = {
    "claude-haiku-4": {"in_per_1k": 0.00025, "out_per_1k": 0.00125, "snapshot": "anthropic-2026-05-22"},
    "claude-sonnet-4-5": {"in_per_1k": 0.003, "out_per_1k": 0.015, "snapshot": "anthropic-2026-05-22"},
    "claude-opus-4-5": {"in_per_1k": 0.015, "out_per_1k": 0.075, "snapshot": "anthropic-2026-05-22"},
}


@dataclass
class CallContext:
    tenant_id: str
    feature: str
    route: str


def compute_cost(model: str, input_tokens: int, output_tokens: int) -> tuple[float, str]:
    p = PRICING.get(model)
    if not p:
        return (0.0, "unknown")
    cost = (input_tokens / 1000) * p["in_per_1k"] + (output_tokens / 1000) * p["out_per_1k"]
    return (round(cost, 6), p["snapshot"])


def with_attribution(client_call: Callable[..., Any], ctx: CallContext, sink: Callable[[dict], None]):
    def wrapper(*args, **kwargs):
        rid = str(uuid.uuid4())
        t0 = time.perf_counter()
        resp = client_call(*args, **kwargs)
        latency_ms = int((time.perf_counter() - t0) * 1000)
        # Adapt the next two lines to the real SDK shape (anthropic / openai / gemini).
        usage = getattr(resp, "usage", None) or {}
        model = getattr(resp, "model", kwargs.get("model", "unknown"))
        in_tok = usage.get("input_tokens", 0) if isinstance(usage, dict) else getattr(usage, "input_tokens", 0)
        out_tok = usage.get("output_tokens", 0) if isinstance(usage, dict) else getattr(usage, "output_tokens", 0)
        cache_hit = bool(getattr(resp, "prompt_cache_hit", False) or (isinstance(usage, dict) and usage.get("cache_read_input_tokens", 0) > 0))
        cost, snap = compute_cost(model, in_tok, out_tok)
        record = {
            "request_id": rid,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "tenant_id": ctx.tenant_id or f"anon_session_{rid[:8]}",
            "feature": ctx.feature,
            "route": ctx.route,
            "model": model,
            "prompt_cache_hit": cache_hit,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "latency_ms": latency_ms,
            "cost_usd": cost,
            "pricing_snapshot_id": snap,
        }
        sink(record)
        return resp
    return wrapper
```

### `templates/middleware.ts`

```typescript
 */

type Pricing = { in_per_1k: number; out_per_1k: number; snapshot: string };
const PRICING: Record<string, Pricing> = {
  "claude-haiku-4": { in_per_1k: 0.00025, out_per_1k: 0.00125, snapshot: "anthropic-2026-05-22" },
  "claude-sonnet-4-5": { in_per_1k: 0.003, out_per_1k: 0.015, snapshot: "anthropic-2026-05-22" },
  "claude-opus-4-5": { in_per_1k: 0.015, out_per_1k: 0.075, snapshot: "anthropic-2026-05-22" },
};

export type CallContext = { tenant_id: string; feature: string; route: string };
export type AttributionRecord = {
  request_id: string;
  ts: string;
  tenant_id: string;
  feature: string;
  route: string;
  model: string;
  prompt_cache_hit: boolean;
  input_tokens: number;
  output_tokens: number;
  latency_ms: number;
  cost_usd: number;
  pricing_snapshot_id: string;
};

function computeCost(model: string, inTok: number, outTok: number): [number, string] {
  const p = PRICING[model];
  if (!p) return [0, "unknown"];
  const cost = (inTok / 1000) * p.in_per_1k + (outTok / 1000) * p.out_per_1k;
  return [Math.round(cost * 1_000_000) / 1_000_000, p.snapshot];
}

export function withAttribution<T extends (...args: any[]) => Promise<any>>(
  clientCall: T,
  ctx: CallContext,
  sink: (rec: AttributionRecord) => void
): T {
  const wrapper = async (...args: Parameters<T>) => {
    const rid = crypto.randomUUID();
    const t0 = performance.now();
    const resp = await clientCall(...args);
    const latencyMs = Math.round(performance.now() - t0);
    const usage = resp.usage ?? {};
    const model = resp.model ?? (args[0]?.model ?? "unknown");
    const inTok = usage.input_tokens ?? 0;
    const outTok = usage.output_tokens ?? 0;
    const cacheHit = Boolean(resp.prompt_cache_hit ?? (usage.cache_read_input_tokens ?? 0) > 0);
    const [cost, snap] = computeCost(model, inTok, outTok);
    sink({
      request_id: rid,
      ts: new Date().toISOString(),
      tenant_id: ctx.tenant_id || `anon_session_${rid.slice(0, 8)}`,
      feature: ctx.feature,
      route: ctx.route,
      model,
      prompt_cache_hit: cacheHit,
      input_tokens: inTok,
      output_tokens: outTok,
      latency_ms: latencyMs,
      cost_usd: cost,
      pricing_snapshot_id: snap,
    });
    return resp;
  };
  return wrapper as T;
}
```

### `templates/daily-aggregator.sql`

```sql
INSERT INTO daily_attribution (date, tenant_id, feature, model, calls, input_tokens, output_tokens, cache_hits, cost_usd)
SELECT
  CAST(ts AS DATE) AS date,
  tenant_id,
  feature,
  model,
  COUNT(*) AS calls,
  SUM(input_tokens) AS input_tokens,
  SUM(output_tokens) AS output_tokens,
  SUM(CASE WHEN prompt_cache_hit THEN 1 ELSE 0 END) AS cache_hits,
  ROUND(SUM(cost_usd), 4) AS cost_usd
FROM raw_attribution
WHERE ts >= CURRENT_DATE - INTERVAL '1' DAY
  AND ts <  CURRENT_DATE
GROUP BY 1, 2, 3, 4
ON CONFLICT (date, tenant_id, feature, model) DO UPDATE
SET calls = EXCLUDED.calls,
    input_tokens = EXCLUDED.input_tokens,
    output_tokens = EXCLUDED.output_tokens,
    cache_hits = EXCLUDED.cache_hits,
    cost_usd = EXCLUDED.cost_usd;
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Single valid attribution record for the validator smoke loop.",
  "_consumes": "validate-ai-cost-attribution-schema.py",
  "_produces": "ok verdict",
  "_depends_on": "templates/attribution.schema.json",
  "_token_budget_impact": "docs-only",
  "request_id": "01HXYZ-SMOKE",
  "ts": "2026-05-22T10:00:00Z",
  "tenant_id": "tnt_smoke",
  "feature": "chat",
  "route": "/api/chat",
  "model": "claude-sonnet-4-5",
  "prompt_cache_hit": true,
  "input_tokens": 1200,
  "output_tokens": 350,
  "latency_ms": 1800,
  "cost_usd": 0.0125,
  "pricing_snapshot_id": "anthropic-2026-05-22"
}
```
