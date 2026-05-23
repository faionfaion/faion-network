// purpose: Feature folder skeleton: components/, hooks/, lib/, index.ts barrel.
// consumes: see content/02-output-contract.xml inputs for react-component-architecture
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// src/features/checkout/components/CheckoutForm.tsx
'use client';
import { Button } from '@/components/ui/button';
import { useCheckoutStore } from '../store';

export function CheckoutForm() {
  const { total, submit } = useCheckoutStore((s) => ({ total: s.total, submit: s.submit }));
  return (
    <form onSubmit={submit}>
      <Button type='submit'>Pay {total}</Button>
    </form>
  );
}
