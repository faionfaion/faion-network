// purpose: Bounded retry helper with exponential backoff
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-stealth-proxy
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

export async function retry<T>(fn: () => Promise<T>, max = 2, baseMs = 500): Promise<T> {
  let lastErr: unknown;
  for (let i = 0; i <= max; i++) {
    try { return await fn(); }
    catch (e) {
      lastErr = e;
      if (i === max) break;
      await new Promise((r) => setTimeout(r, baseMs * 2 ** i));
    }
  }
  throw lastErr;
}
