// purpose: custom-hook skeleton extracted from a React component
// consumes: component logic identified by decomposition-react decision tree
// produces: reusable, testable hook isolated from JSX
// depends-on: React 18+; project's I/O service module
// token-budget-impact: ~200 tokens when loaded as context
import { useCallback, useEffect, useState } from 'react'

export interface UseFeatureOptions {
  initial?: unknown
  serviceFetch?: (id: string) => Promise<unknown>
}

export function useFeature(id: string, opts: UseFeatureOptions = {}) {
  const [data, setData] = useState(opts.initial ?? null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const reload = useCallback(async () => {
    if (!opts.serviceFetch) return
    setLoading(true); setError(null)
    try { setData(await opts.serviceFetch(id)) }
    catch (e) { setError(e as Error) }
    finally { setLoading(false) }
  }, [id, opts])

  useEffect(() => { reload() }, [reload])
  return { data, loading, error, reload }
}
