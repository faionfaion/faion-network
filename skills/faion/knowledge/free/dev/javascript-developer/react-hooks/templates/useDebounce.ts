// purpose: canonical useDebounce custom hook with explicit return type + cleanup
// consumes: a value of type T and a delay in ms
// produces: the debounced value of the same type
// depends-on: react (useState, useEffect)
// token-budget-impact: ~150 tokens

import { useEffect, useState } from 'react';

export function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    // Mandatory cleanup: cancels the previous timer when value or delayMs changes,
    // or when the component unmounts. Required by rule r2-effect-cleanup.
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}
