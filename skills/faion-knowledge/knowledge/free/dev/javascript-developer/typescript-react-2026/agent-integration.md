# Agent Integration — TypeScript & React 2026

## When to use
- Greenfield Next.js 15 + React 19 app where Server Components, Server Actions, and the App Router are the default.
- Migrating a CRA/Vite SPA to Next.js App Router with a clear server/client split.
- Tightening an existing TS project's `tsconfig.json` to 2026 strict baseline (`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `verbatimModuleSyntax`).
- Adding form mutations via Server Actions instead of bespoke API routes + client fetch wrappers.

## When NOT to use
- React Native / Expo — Server Components RFC for native is not stable; this README is web-only.
- Static-only marketing sites where Astro/Gatsby produce smaller output. Next 15 RSC adds runtime weight you don't need.
- Pages Router projects you intend to keep — most patterns here assume App Router and would break Pages-Router data fetching.
- Library/SDK packages — `verbatimModuleSyntax` and `allowImportingTsExtensions` complicate dual-publish (CJS+ESM); use a library-tuned tsconfig instead.

## Where it fails / limitations
- `exactOptionalPropertyTypes` breaks most existing component prop spreads — agents that flip it on a mature codebase generate hundreds of errors and tend to "fix" by adding `| undefined` everywhere, hiding real bugs.
- `'use client'` and `'use server'` directives are easy to misplace; the README does not enumerate the failure modes (e.g., importing a server-only module from a client tree leaks secrets).
- Server Actions silently fall back to plain POST without progressive enhancement when JS is disabled and the form has client-side state — agents copy `useFormState` examples without testing the no-JS path.
- `useFormState` was renamed to `useActionState` in React 19.0+; the README's snippet is already drifting.
- `revalidatePath` only works inside Next.js — agents that copy the pattern into a non-Next RSC framework (e.g., Waku) get runtime errors.
- The "38% faster" benchmark is not reproducible on data-heavy dashboards; uncritical agents quote it as universal truth.

## Agentic workflow
Use a planner agent to classify each component as server-default vs client-leaf, then a coder agent to add `'use client'` only at the boundary. A type-tightener agent runs `tsc --noEmit` after every file change to catch directive errors early. For Server Actions, pair a Zod-schema agent (defines validated input) with a UI agent that wires `useActionState` and a `<SubmitButton>` using `useFormStatus`. Keep one agent per tsconfig flag flip — bundling flag changes with feature work makes review impossible.

### Recommended subagents
- `faion-sdd-executor-agent` — disciplined, gated migration of files with `tsc` + lint + test on each step.
- `faion-feature-executor` — for adding a new route (`page.tsx` + `loading.tsx` + `error.tsx` + action + form).
- A custom `rsc-boundary-auditor` (sonnet) — scans imports across `'use client'`/`'use server'` boundaries and flags leaks.
- A custom `tsconfig-tightener` (sonnet) — turns on one strict flag, fixes errors, opens a single-flag PR.

### Prompt pattern
```
Read skills/faion-knowledge/knowledge/free/dev/javascript-developer/typescript-react-2026/README.md.
Convert app/dashboard/page.tsx to a Server Component. Move only the interactive widgets to
'use client' files. Validate: no client component imports from a server-only module.
```

```
Add Server Action createUser with Zod validation. Use useActionState (React 19) — NOT
useFormState. Wrap submit in <SubmitButton> using useFormStatus. Provide a no-JS test
plan for the form.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `create-next-app` | Bootstrap Next 15 + RSC | `npx create-next-app@latest` · https://nextjs.org/docs/app/api-reference/cli/create-next-app |
| `tsc --noEmit` | Type-check only | https://www.typescriptlang.org/docs/handbook/compiler-options.html |
| `next lint` | App-Router-aware ESLint | https://nextjs.org/docs/app/api-reference/cli/next#next-lint |
| `eslint-plugin-react-server-components` | Boundary lint | https://github.com/facebook/react/tree/main/packages/eslint-plugin-react-hooks |
| `@next/codemod` | Next 14→15 migration codemods | `npx @next/codemod@canary upgrade latest` |
| `madge` | Detect circular imports across server/client | `npx madge --circular --extensions ts,tsx src` |
| `tsr` (ts-reset) | Library-quality lib.d.ts overrides | `npm i -D @total-typescript/ts-reset` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Vercel | SaaS | Yes | First-class RSC + Server Actions hosting; preview deployments per PR. |
| Cloudflare Pages (Next on Workers) | SaaS | Partial | Limited Node APIs; agents must check `runtime = 'edge'` compatibility per route. |
| Netlify | SaaS | Yes | Has Next runtime; Server Actions supported via `@netlify/next`. |
| Sentry | SaaS | Yes | First-class Next 15 SDK with Server Component traces. |
| Vercel Toolbar / Speed Insights | SaaS | Yes | Auto-injected with `@vercel/speed-insights`. |
| Drizzle ORM / Prisma | OSS | Yes | Direct DB access from RSC matches the README's pattern. |
| Clerk / Auth.js | SaaS/OSS | Yes | Both ship App-Router-native helpers (`auth()` in Server Components). |

## Templates & scripts
See `templates.md` for tsconfig and component templates. Inline a `'use client'` boundary auditor (drop in `scripts/audit-rsc.ts`):

```typescript
import { Project, SyntaxKind } from 'ts-morph';
const project = new Project({ tsConfigFilePath: 'tsconfig.json' });
const violations: string[] = [];
for (const sf of project.getSourceFiles('src/**/*.{ts,tsx}')) {
  const isClient = sf.getFullText().startsWith("'use client'");
  if (!isClient) continue;
  for (const imp of sf.getImportDeclarations()) {
    const target = imp.getModuleSpecifierSourceFile();
    if (!target) continue;
    const targetText = target.getFullText();
    if (targetText.includes("'server-only'") || targetText.startsWith("'use server'")) {
      violations.push(`${sf.getFilePath()} imports server module ${target.getFilePath()}`);
    }
  }
}
if (violations.length) { console.error(violations.join('\n')); process.exit(1); }
```

Run in CI to fail PRs that punch through the RSC boundary.

## Best practices
- Default every component to a Server Component. Add `'use client'` only when the component uses hooks, browser APIs, or event handlers.
- Put DB/SDK calls behind `import 'server-only'`; importing them from a client file errors at build time, not in production.
- Use `useActionState` (React 19) — `useFormState` is the React 18 name and will be removed.
- Co-locate Server Actions next to their consumers (`actions.ts` in the route folder), not in a global `lib/actions/`. Easier to delete features.
- For TS strict flags, flip one at a time across the whole repo; never per-file `// @ts-expect-error` to suppress.
- Prefer `satisfies` over type annotations for config objects (preserves literal types — see the README).
- Replace `Capitalize<string>` template-literal patterns with finite unions whenever possible — the wide form defeats autocomplete.
- For data-loading patterns, use parallel `Promise.all` in Server Components. Sequential `await` chains kill TTFB.

## AI-agent gotchas
- LLMs trained on React 18 emit `useFormState`, class components, and `useEffect`-based fetching even in App Router projects. Pin the model context with explicit "React 19" reminders or a custom prompt prefix.
- Agents add `'use client'` to entire layouts to "make hooks work" — that flips the whole tree to client. Require boundary justifications.
- `noUncheckedIndexedAccess` makes `array[0]` `T | undefined`; agents reflexively `!`-assert away the union and reintroduce runtime crashes. Forbid `!` on indexed access in lint.
- Server Actions throw HTTP redirects via `redirect()` — caught by a generic `try/catch` they look like errors. Document and lint for this.
- Decorators (still proposal-based) and the README's example use the new TC39 form, not legacy `experimentalDecorators`. Mixing the two in one repo confuses agents and breaks the build.
- Human checkpoint: any new `'use server'` file should be reviewed for input validation before merge — Zod schema must cover every form field. Server Actions are public RPC endpoints.
- Caching: agents forget `revalidatePath`/`revalidateTag` after mutations; UI shows stale data. Add an integration test that mutates then re-fetches.

## References
- https://react.dev/blog/2024/12/05/react-19
- https://react.dev/reference/rsc/server-components
- https://react.dev/reference/react/useActionState
- https://nextjs.org/docs/app
- https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-0.html
- https://www.joshwcomeau.com/react/server-components/
- https://vercel.com/blog/whats-new-in-react-19
