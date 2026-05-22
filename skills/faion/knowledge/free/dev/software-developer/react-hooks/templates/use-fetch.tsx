// purpose: TBD-template-header
// consumes: input from methodology
// produces: output artefact
// depends-on: 01-core-rules.xml
// token-budget-impact: small

// use-fetch.tsx — Strict-Mode-safe useFetch with typed status states.
// For production apps prefer TanStack Query. This is a teaching example
// showing correct cleanup and Strict-Mode-safe behavior.
import { useEffect, useState } from "react";

type State<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

export function useFetch<T>(url: string): State<T> {
  const [state, setState] = useState<State<T>>({ status: "idle" });

  useEffect(() => {
    const ctrl = new AbortController();
    setState({ status: "loading" });

    fetch(url, { signal: ctrl.signal })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        const data = (await r.json()) as T;
        setState({ status: "success", data });
      })
      .catch((err: Error) => {
        if (err.name === "AbortError") return; // Strict Mode or url change — ignore
        setState({ status: "error", error: err });
      });

    return () => ctrl.abort();
  }, [url]);

  return state;
}
