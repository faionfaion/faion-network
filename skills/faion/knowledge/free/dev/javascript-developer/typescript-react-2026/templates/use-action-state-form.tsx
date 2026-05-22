// purpose: client form using React 19 useActionState + useFormStatus
// consumes: a Server Action conforming to (prev, formData) => Promise<ActionResult>
// produces: a thin form component; pending state via SubmitButton
// depends-on: react, react-dom, ../actions
// token-budget-impact: ~260 tokens

'use client';

import { useActionState } from 'react';
import { useFormStatus } from 'react-dom';
import { createInvoice, type ActionResult } from './actions';

function SubmitButton(): React.ReactElement {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Saving…' : 'Create invoice'}
    </button>
  );
}

export interface InvoiceFormProps {
  customerId: string;
}

export function InvoiceForm({ customerId }: InvoiceFormProps): React.ReactElement {
  const initial: ActionResult = { success: false };
  const [state, formAction] = useActionState(createInvoice, initial);

  return (
    <form action={formAction}>
      <input type="hidden" name="customerId" value={customerId} />
      <label>
        Amount
        <input name="amount" type="number" step="0.01" required />
      </label>
      <label>
        Due date
        <input name="dueDate" type="date" required />
      </label>
      {!state.success && state.fieldErrors ? (
        <ul role="alert">
          {Object.entries(state.fieldErrors).map(([field, errs]) => (
            <li key={field}>
              {field}: {errs?.join(', ')}
            </li>
          ))}
        </ul>
      ) : null}
      <SubmitButton />
    </form>
  );
}
