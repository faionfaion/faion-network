// purpose: useFetch hook demonstrating AbortController cleanup + Result discriminated union
// consumes: a URL string
// produces: { state: 'idle' | 'loading' | 'ok' | 'error'; data?; error? }
// depends-on: react; native fetch + AbortController
// token-budget-impact: ~280 tokens

import { useEffect, useState } from 'react';

type FetchState<T> =
  | { state: 'idle' }
  | { state: 'loading' }
  | { state: 'ok'; data: T }
  | { state: 'error'; error: Error };

export function useFetch<T>(url: string): FetchState<T> {
  const [result, setResult] = useState<FetchState<T>>({ state: 'idle' });

  useEffect(() => {
    const controller = new AbortController();
    setResult({ state: 'loading' });

    async function run(): Promise<void> {
      try {
        const res = await fetch(url, { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as T;
        setResult({ state: 'ok', data });
      } catch (err) {
        if (err instanceof Error && err.name !== 'AbortError') {
          setResult({ state: 'error', error: err });
        }
      }
    }

    void run();
    // Cancels the in-flight fetch on unmount or url change. Required by r2 + r3.
    return () => controller.abort();
  }, [url]);

  return result;
}
