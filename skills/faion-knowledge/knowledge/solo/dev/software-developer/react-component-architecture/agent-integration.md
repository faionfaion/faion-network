# Agent Integration — React Component Architecture

## When to use
- Bootstrapping a new React/Next.js codebase and you need a defensible directory + component layout from day one.
- Refactoring a sprawling `components/` folder into feature-modules + shared UI primitives.
- Building or extending a design system (Button, Card, Input) where compound + polymorphic patterns matter.
- Establishing team coding standards that an LLM agent will follow when generating new components.
- Migrating from Pages Router to App Router and re-deciding what is a server vs client boundary.

## When NOT to use
- One-off React prototypes / spikes — full architecture is overhead.
- Pure logic libraries (no JSX) — use module-architecture guidance instead.
- React Native projects with platform-specific structure (`*.ios.tsx` / `*.android.tsx`) — adapt, do not copy.
- When the project already mandates a different convention (e.g. Bulletproof React, Nx workspace generators) — follow that and skip this.

## Where it fails / limitations
- Compound components (`Card.Header`) break tree-shaking in some bundlers and confuse codemods that expect named exports only.
- Polymorphic `as` props with full TS inference are heavy on the type-checker; LLMs often emit subtly wrong generic constraints.
- `forwardRef` boilerplate is being deprecated in React 19 (refs are now props on function components) — patterns in the README still target React 18.
- "Container/Presenter" can degenerate into prop-drilling once data deps multiply; not a substitute for proper data-fetching colocation.
- Feature-module boundaries are nominal — there is no enforcement; without an ESLint boundary plugin, modules leak into each other.

## Agentic workflow
Drive React component architecture as a planning + scaffold + verify loop. A planner subagent decides whether the new piece is a UI primitive (`components/ui/`), a feature component (`features/<X>/components/`), or a layout. A scaffolder subagent emits the 4-5 file folder (`Component.tsx` + tests + stories + `index.ts`). A reviewer subagent runs ESLint, TS, and a11y checks plus hunts for prop-drilling, oversized components, and client/server boundary mistakes.

### Recommended subagents
- `faion-sdd-executor-agent` — own the spec → scaffold → tests → review loop for any new component.
- `password-scrubber-agent` — sweep generated files before commit (catches accidental tokens in stories/fixtures).
- A user-defined `frontend-reviewer` (model: sonnet) — checks Server vs Client component placement, RSC-safety of imports, and `'use client'` correctness.

### Prompt pattern
- "You are scaffolding a `<Name>` component under `<path>`. Read `react-component-architecture/README.md`. Decide: ui primitive | feature component | layout. Emit `<Name>.tsx`, `<Name>.test.tsx`, `<Name>.stories.tsx`, `index.ts`. Use `cva` for variants only if >=2 variants exist. No `forwardRef` if React 19. Output unified diffs only."
- "Audit `src/features/<X>/` against `react-component-architecture/README.md`. Flag: prop-drilling >2 levels, files >300 lines, business logic inside components, default exports, and missing `index.ts` barrels."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `plop` | Scaffold component folders from a template | `npm i -D plop` — https://plopjs.com |
| `hygen` | Same idea, faster + zero-deps templates | `npm i -g hygen` — https://hygen.io |
| `eslint-plugin-react` + `eslint-plugin-jsx-a11y` | Enforce JSX patterns, a11y baseline | `npm i -D eslint-plugin-react eslint-plugin-jsx-a11y` |
| `eslint-plugin-boundaries` | Enforce feature-module isolation (`features/A` cannot import `features/B/internal/*`) | `npm i -D eslint-plugin-boundaries` |
| `madge` | Detect circular deps between feature modules | `npx madge --circular src/` |
| `knip` | Find unused exports inside feature `index.ts` barrels | `npx knip` |
| `Storybook` CLI | Story-driven dev for primitives | `npx storybook@latest init` |
| `tsc --noEmit` | Type-check polymorphic + generic components | bundled |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Storybook | OSS | Yes | Stories double as agent-readable docs + visual fixtures. |
| Chromatic | SaaS | Yes (REST/CLI) | Visual regression for component diffs in CI. |
| Vercel v0 | SaaS | Partial | LLM emits shadcn-style components; useful as an idea source, not the final commit. |
| shadcn/ui registry | OSS | Yes (CLI) | `npx shadcn@latest add <comp>` — agents can drive component installation; the patterns in the README map directly. |
| Bit.dev | SaaS/OSS | Limited | Component-as-package — heavy for solo, useful for multi-app monorepos. |

## Templates & scripts
See `templates.md` for component skeletons. Minimal `plop` generator the agent can invoke:

```js
// plopfile.cjs
module.exports = (plop) => {
  plop.setGenerator('component', {
    description: 'UI primitive or feature component',
    prompts: [
      { type: 'input', name: 'name', message: 'PascalCase name' },
      { type: 'list', name: 'kind', choices: ['ui', 'feature'], message: 'Kind' },
      { type: 'input', name: 'feature', message: 'Feature slug (if feature)', when: (a) => a.kind === 'feature' },
    ],
    actions: (data) => {
      const base = data.kind === 'ui'
        ? `src/components/ui/{{name}}`
        : `src/features/${data.feature}/components/{{name}}`;
      return [
        { type: 'add', path: `${base}/{{name}}.tsx`, templateFile: 'plop-templates/Component.tsx.hbs' },
        { type: 'add', path: `${base}/{{name}}.test.tsx`, templateFile: 'plop-templates/Component.test.tsx.hbs' },
        { type: 'add', path: `${base}/{{name}}.stories.tsx`, templateFile: 'plop-templates/Component.stories.tsx.hbs' },
        { type: 'add', path: `${base}/index.ts`, template: "export * from './{{name}}';\n" },
      ];
    },
  });
};
```

## Best practices
- One folder per component, even for tiny primitives — keeps tests/stories/types colocated and makes future renames mechanical.
- Default to **named exports** only; default exports break refactor tools and create ambiguous imports.
- Cap component file size at ~250 lines; past that, force-extract subcomponents or hooks.
- Put **all** data fetching in feature `hooks/` (or RSC), never inside leaf components — this is what makes Container/Presenter actually pay off.
- For React 19 codebases, drop `forwardRef`; for React 18, keep it on every primitive that may need a ref (Button, Input, Combobox triggers, Radix primitives).
- Use `cva` only when variants ≥2 — single-variant `cva` calls are noise.
- Compound components: keep child components as **named exports too** (`export function CardHeader`) and assign `Card.Header = CardHeader` only as ergonomic alias, so tree-shaking still works.
- Add an `eslint-plugin-boundaries` config so `features/auth` cannot reach into `features/billing/internal`; agents will respect the boundary if the linter screams.

## AI-agent gotchas
- LLMs love to emit `'use client'` defensively at the top of every component — review server-component candidates and strip it.
- LLMs frequently mix React 18 `forwardRef` with React 19 ref-as-prop syntax in the same file. Pin the React version in the prompt.
- Polymorphic component generics: agents often produce `as: T extends ElementType = 'div'` but forget to spread `ComponentPropsWithoutRef<T>` correctly — TS will compile but `href` won't be typed for `<Box as="a">`. Always include a typed usage test.
- Compound components break when an agent adds a new subcomponent (`Card.Action`) but forgets to also export it from `index.ts` — barrel drift is the #1 LLM bug here.
- Agents tend to import from deep paths (`'@/components/ui/Button/Button'`) instead of the barrel (`'@/components/ui/Button'`). Add an ESLint rule against deep imports inside `components/ui/*/`.
- Human-in-loop checkpoint: after agent generates a new feature module, manually verify there is no `import` from `features/<other>/` — circular feature deps are a long-tail trap.
- When refactoring an existing big component, run the agent in **two passes**: (1) extract subcomponents only, no logic change; (2) move logic into hooks. Combining the two in one pass produces silent regressions.

## References
- React docs — https://react.dev/learn/thinking-in-react
- Bulletproof React — https://github.com/alan2207/bulletproof-react
- patterns.dev — https://www.patterns.dev/react
- Class Variance Authority — https://cva.style/docs
- shadcn/ui — https://ui.shadcn.com
- React 19 ref-as-prop — https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop
