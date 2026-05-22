/**
 * purpose: TypeScript middleware that stamps attribution metadata on every LLM call.
 * consumes: request ctx (tenant_id, feature, route) + LLM client response
 * produces: one attribution record per call, emitted to sink
 * depends-on: content/02-output-contract.xml; templates/attribution.schema.json
 * token-budget-impact: runtime overhead ~1ms per call
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
