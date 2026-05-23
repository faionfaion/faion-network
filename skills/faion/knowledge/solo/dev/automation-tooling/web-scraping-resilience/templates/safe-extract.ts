// purpose: safeExtract + retryWithBackoff helpers wrapping the unsafe extraction primitives.
// consumes: Playwright Page handle; resilience config object.
// produces: hardened extraction + retry that never throws to the row loop.
// depends-on: playwright >= 1.40.
// token-budget-impact: ~250 tokens when loaded as context.

export interface ResilienceConfig {
  delay_ms_min: number;
  delay_ms_max: number;
  max_retries: number;
  base_delay_ms: number;
  safe_extract_timeout_ms: number;
}

export async function safeExtract<T>(
  fn: () => Promise<T>,
  defaultValue: T,
  timeoutMs: number = 5000
): Promise<T> {
  try {
    const timeout = new Promise<T>((_, rej) =>
      setTimeout(() => rej(new Error("safe-extract-timeout")), timeoutMs)
    );
    return await Promise.race([fn(), timeout]);
  } catch (_) {
    return defaultValue;
  }
}

export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  cfg: Pick<ResilienceConfig, "max_retries" | "base_delay_ms">
): Promise<T> {
  let lastErr: unknown;
  for (let attempt = 0; attempt <= cfg.max_retries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastErr = err;
      if (attempt === cfg.max_retries) break;
      const delay = cfg.base_delay_ms * 2 ** attempt + Math.floor(Math.random() * 1000);
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw lastErr;
}

export async function jitteredSleep(min: number, max: number): Promise<void> {
  const ms = min + Math.floor(Math.random() * (max - min));
  return new Promise(r => setTimeout(r, ms));
}
