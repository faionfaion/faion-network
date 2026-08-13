# TypeScript & React 2026

## Summary

**One-sentence:** Produces an App-Router scaffold spec for a Next.js 15 + React 19 + TS 5.x project, naming the server/client component boundary, the useActionState form wiring, the revalidate strategy, and the strict-mode tsconfig flags.

**Ефективно для:** Greenfield Next.js 15 app or a focused App-Router migration where the team must decide per-component server-vs-client, per-mutation revalidatePath, and per-form useActionState wiring without re-arguing every PR.

**One-paragraph:** The 2026 stack (TS 5.x strict + React 19 + Next 15 App Router) shifts defaults from React 18 in three ways: server components by default, Server Actions replace bespoke API routes, useActionState replaces useFormState. This methodology produces an auditable spec naming for every page/segment whether it is a Server Component or Client Component, what 'use server' actions it exposes, what revalidatePath/revalidateTag calls fire after mutation, and which strict tsconfig flags are enabled. Forbids: `useFormState` (legacy), `'use client'` on layouts, missing revalidate after mutation, `array[0]!` to suppress noUncheckedIndexedAccess.

## Applies If (ALL must hold)

- Target stack is Next.js ≥ 15.0 + React ≥ 19.0 + TypeScript ≥ 5.0 with App Router.
- The app deploys to a Node-capable runtime (Vercel Node, AWS Lambda, self-hosted) — not edge-only with limited Node APIs.
- The team commits to RSC-by-default with thin `'use client'` boundaries.
- Forms use Server Actions, not bespoke `/api/*` routes + client fetch.
- Output drives codegen and PR review on every route segment.

## Skip If (ANY kills it)

- React Native / Expo — RSC for native is not stable.
- Static-only marketing sites — Astro / Gatsby produce smaller bundles.
- Pages Router project intended to remain on Pages Router.
- Library / SDK package — verbatimModuleSyntax complicates dual-publish.
- Edge-only runtime without robust Node.js APIs (some Cloudflare Workers tiers).

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| Page / route map | tree | feature brief |
| Per-page state needs | bullets | UX analysis |
| Mutation list (action name, affected paths) | YAML | feature brief |
| Current tsconfig.json | JSON | repo root |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[typescript-strict-mode]]` | Strict tsconfig baseline this spec extends. |
| `[[react-hooks]]` | useActionState / useFormStatus shape consumed by the form wiring. |
| `[[react-patterns]]` | Feature folder layout this spec annotates. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 7 testable rules: server-default, 'use client' boundary, server-only import guard, useActionState, revalidate after mutation, no-bang on indexed access, parallel Promise.all loading | ~1200 |
| `content/02-output-contract.xml` | essential | JSON schema for app-router spec | ~1000 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: layout-wide 'use client', useFormState, missing revalidate, array[0]! | ~800 |
| `content/04-procedure.xml` | deep | 6 steps: map → boundary classify → actions → revalidate → tsconfig → validate | ~700 |
| `content/05-examples.xml` | deep | Worked example: /dashboard with client sidebar + Server Action createInvoice + revalidatePath | ~600 |
| `content/06-decision-tree.xml` | essential | Per-component: server-default vs client; per-mutation: revalidatePath vs revalidateTag | ~200 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `map_routes` | haiku | Mechanical expansion of app/ tree from the brief. |
| `classify_boundary` | sonnet | Per-component server/client decision with reasoning. |
| `audit_security` | opus | server-only imports + secret leakage + boundary inversions. |

## Templates

| File | Purpose |
|---|---|
| `templates/server-action.ts` | Reference `'use server'` action with Zod parse + revalidatePath. |
| `templates/use-action-state-form.tsx` | Client form using useActionState + useFormStatus. |
| `templates/tsconfig.strict-2026.json` | TS 5.x strict baseline tsconfig. |
| `templates/app-router-spec.json` | Reference output document. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-typescript-react-2026.py` | Validate an app-router spec JSON against the contract. | After the agent emits the spec, before codegen runs. |

## Related

- [[typescript-strict-mode]] — tsconfig flags this spec assumes are enabled.
- [[react-hooks]] — useActionState / useFormStatus form wiring.
- [[react-patterns]] — feature folder layout.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates per-component: does the component use a hook, browser API, or event handler? → 'use client'. Otherwise → server-default. For mutations: does the revalidation target a known path? → revalidatePath. Tag-keyed cache? → revalidateTag.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/server-action.ts`

```typescript
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
```

### `templates/use-action-state-form.tsx`

```tsx
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
```

### `templates/tsconfig.strict-2026.json`

```json
{
  "_purpose": "TypeScript 5.x strict baseline for Next.js 15 + React 19 in 2026.",
  "_consumes": "nothing \u2014 copy and adapt.",
  "_produces": "tsconfig.json baseline.",
  "_depends-on": "typescript >= 5.0; Next.js >= 15.",
  "_token-budget-impact": "~120 tokens.",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "target": "ES2023",
    "lib": [
      "ES2023",
      "DOM",
      "DOM.Iterable"
    ],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "allowImportingTsExtensions": true,
    "resolvePackageJsonExports": true,
    "resolvePackageJsonImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": [
        "./src/*"
      ]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts"
  ],
  "exclude": [
    "node_modules"
  ]
}
```

### `templates/app-router-spec.json`

```json
{
  "_purpose": "Reference App-Router scaffold spec output.",
  "_consumes": "Page map + per-page state + mutation list + tsconfig.",
  "_produces": "JSON for codegen / review.",
  "_depends-on": "content/02-output-contract.xml.",
  "_token-budget-impact": "~180 tokens.",
  "artefact_id": "billing-app-router",
  "owner": "ruslan@faion.net",
  "app_name": "billing",
  "next_version": "^15.0.0",
  "react_version": "^19.0.0",
  "ts_version": "^5.4.0",
  "routes": [
    {
      "path": "/dashboard",
      "files": [
        {
          "file": "app/dashboard/layout.tsx",
          "boundary": "server-default"
        },
        {
          "file": "app/dashboard/page.tsx",
          "boundary": "server-default"
        },
        {
          "file": "app/dashboard/loading.tsx",
          "boundary": "server-default"
        },
        {
          "file": "app/dashboard/Sidebar.tsx",
          "boundary": "use-client",
          "uses_hooks": true
        },
        {
          "file": "app/dashboard/InvoiceForm.tsx",
          "boundary": "use-client",
          "uses_hooks": true
        },
        {
          "file": "app/dashboard/actions.ts",
          "boundary": "use-server"
        }
      ]
    }
  ],
  "actions": [
    {
      "name": "createInvoice",
      "mutates": true,
      "revalidate": {
        "kind": "path",
        "target": "/dashboard"
      },
      "input_schema": "CreateInvoiceSchema"
    }
  ],
  "tsconfig_flags": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true
  },
  "version": "1.0.0",
  "last_reviewed": "2026-05-22"
}
```
