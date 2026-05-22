// purpose:   Reference custom hook with abort cleanup, exhaustive deps, no sync-via-effect
// consumes:  url string, optional fetch options
// produces:  {data, error, loading} state slot
// depends-on: React 18+
// token-budget-impact: ~120 tokens when referenced from a component

import {useEffect, useState} from 'react';

export function useFetch<T>(url: string, init?: RequestInit) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    fetch(url, {...init, signal: controller.signal})
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<T>;
      })
      .then(j => setData(j))
      .catch(e => {
        if (e.name !== 'AbortError') setError(e);
      })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [url, init]);

  return {data, error, loading};
}
