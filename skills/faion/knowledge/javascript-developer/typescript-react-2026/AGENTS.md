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
