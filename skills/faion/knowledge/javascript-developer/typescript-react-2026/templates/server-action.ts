// purpose: canonical 'use server' Server Action with Zod parse + revalidatePath
// consumes: prevState + FormData from useActionState
// produces: ActionResult discriminated union (success | error with fieldErrors)
// depends-on: zod, next/cache, ./db (server-only)
// token-budget-impact: ~280 tokens

'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';
// import 'server-only' would normally be added in the imported DB module, not here.

export const CreateInvoiceSchema = z.object({
  customerId: z.string().uuid(),
  amount: z.coerce.number().positive(),
  dueDate: z.coerce.date(),
});

export type CreateInvoiceInput = z.infer<typeof CreateInvoiceSchema>;

export type ActionResult =
  | { success: true }
  | { success: false; fieldErrors?: Record<string, string[]>; message?: string };

export async function createInvoice(
  _prevState: ActionResult | undefined,
  formData: FormData,
): Promise<ActionResult> {
  const parsed = CreateInvoiceSchema.safeParse({
    customerId: formData.get('customerId'),
    amount: formData.get('amount'),
    dueDate: formData.get('dueDate'),
  });

  if (!parsed.success) {
    return { success: false, fieldErrors: parsed.error.flatten().fieldErrors };
  }

  // await db.invoices.create(parsed.data);

  // Mandatory: invalidate the cached fetch behind /dashboard so the list refreshes.
  revalidatePath('/dashboard');

  return { success: true };
}
