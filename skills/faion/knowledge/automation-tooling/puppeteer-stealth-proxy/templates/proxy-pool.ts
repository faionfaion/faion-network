// purpose: Small proxy pool with health-check + circuit breaker
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-stealth-proxy
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import fetch from 'node-fetch';

export interface Proxy { host: string; auth?: { user: string; pass: string } }

export async function healthy(pool: Proxy[], probeUrl: string, timeoutMs = 5000): Promise<Proxy[]> {
  const out: Proxy[] = [];
  for (const p of pool) {
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), timeoutMs);
      const res = await fetch(probeUrl, { signal: ctrl.signal });
      clearTimeout(t);
      if (res.ok) out.push(p);
    } catch { /* dead proxy */ }
  }
  return out;
}

export class CircuitBreaker {
  private fails = 0;
  constructor(private threshold = 5) {}
  recordFail() { this.fails++; }
  reset() { this.fails = 0; }
  open(): boolean { return this.fails >= this.threshold; }
}
