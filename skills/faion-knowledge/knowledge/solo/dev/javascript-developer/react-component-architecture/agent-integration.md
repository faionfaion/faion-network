# Agent Integration — React Component Architecture

## When to use
- Setting up a new React or Next.js project and deciding folder structure before writing any components
- Refactoring a flat `components/` folder that has grown beyond 20 files into feature-based modules
- Reviewing a component for single-responsibility violations before merging a PR
- Generating a new UI primitive (Button, Input, Card) following the codebase's established variant system

## When NOT to use
- Very small apps (1-3 pages, <10 components) where the structure overhead exceeds the benefit
- Pure server-rendered applications with minimal interactivity (use Next.js server components pattern instead)
- Component libraries that are consumed externally — those have different export and versioning constraints

## Where it fails / limitations
- Feature-based module structure requires discipline: agents tend to place new components in `components/` by default unless explicitly told otherwise
- Compound component pattern (Card.Header, Card.Content, etc.) breaks tree-shaking in some bundlers if sub-components are added to the root export object
- `forwardRef` boilerplate becomes verbose at scale; React 19 removes the need for it but most codebases are not yet on React 19
- Context used for cross-feature communication rather than within a feature scope re-introduces the coupling it was meant to avoid

## Agentic workflow
An agent scaffolds a new component by reading the existing Button or Card implementation to infer the project's variant system (CVA, Tailwind tokens), then generating the new component file, test file, Storybook story, and index.ts in one pass. The agent must check for an existing `index.ts` barrel before adding exports to avoid duplicate entries. For container/presenter splits, the agent generates both files and wires them before adding route imports.

### Recommended subagents
- `faion-sdd-executor-agent` — drives sequential component creation tasks from SDD task files with quality gates

### Prompt pattern
```
Create a <ComponentName> component following the existing Button pattern in src/components/ui/Button/.
Stack: React 18, TypeScript strict, Tailwind, CVA for variants.
Variants needed: <list variants>.
Include: ComponentName.tsx, ComponentName.test.tsx, ComponentName.stories.tsx, index.ts.
Read Button/Button.tsx first to match token and CVA conventions.
```

```
Split <ComponentName> into a container (data/logic) and presenter (UI only).
Container: <ComponentName>Container.tsx — uses hook <hookName>.
Presenter: <ComponentName>.tsx — pure props, no hooks.
Output both files with explicit prop interfaces.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `storybook` | Component development and visual testing in isolation | `npx storybook@latest init` / https://storybook.js.org |
| `@testing-library/react` | DOM-based component unit testing | `npm i -D @testing-library/react @testing-library/jest-dom` |
| `class-variance-authority` | Type-safe variant system for Tailwind components | `npm i class-variance-authority` / https://cva.style/docs |
| `clsx` / `cn` utility | Conditional class merging | `npm i clsx tailwind-merge` |
| `eslint-plugin-react-hooks` | Enforce hooks rules statically | Bundled with CRA/Next; `npm i -D eslint-plugin-react-hooks` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Storybook | OSS | Yes | Agent can generate `.stories.tsx` files from component prop types; visual review still needs human |
| Chromatic | SaaS | Partial | Automated visual regression testing for Storybook; CI integration is automated, baseline approval needs human |
| Radix UI | OSS | Yes | Headless accessible primitives; agent can wrap Radix with Tailwind variants following established patterns |
| shadcn/ui | OSS | Yes | CLI adds components to your codebase; agent can run `npx shadcn-ui@latest add <component>` |
| Figma Tokens | SaaS | Partial | Design token sync; agent can read exported JSON, human must manage Figma side |

## Templates & scripts
See `templates.md` for full component file templates including CVA variant setup and forwardRef pattern.

Component scaffold script (runs in project root):
```bash
#!/bin/bash
# Usage: ./scaffold-component.sh ComponentName ui
NAME=$1
GROUP=${2:-ui}
DIR="src/components/$GROUP/$NAME"
mkdir -p "$DIR"
touch "$DIR/$NAME.tsx" "$DIR/$NAME.test.tsx" "$DIR/$NAME.stories.tsx" "$DIR/index.ts"
echo "export { $NAME } from './$NAME';" > "$DIR/index.ts"
echo "Scaffolded $DIR"
```

## Best practices
- Establish the CVA/variant pattern in one reference component (Button) before generating others — agents copy existing patterns reliably when a reference exists
- Barrel files (`index.ts`) must export types alongside components: `export type { ButtonProps }` — agents omit type exports by default
- Keep feature module boundaries strict: `features/auth/` components must not import from `features/dashboard/` — cross-feature data goes through shared hooks or context at the app level
- Container components must not contain any JSX beyond rendering the presenter and handling loading/error states
- `displayName` must be set on components created with `forwardRef` for React DevTools readability; agents frequently omit this

## AI-agent gotchas
- Agents default to `'use client'` on everything in Next.js projects — explicitly specify "Server Component" or "Client Component" in each prompt
- When generating polymorphic components (`Box as={...}`), agents may produce incorrect TypeScript generics that pass compilation but lose type safety on the `as` prop
- Storybook story generation works well but agents produce `@storybook/react` v6 syntax when the project uses v7/v8 — always specify the Storybook version
- Human checkpoint needed when moving components between `components/` (shared) and `features/` (scoped), as imports across the codebase must be updated
- Agents regenerating index.ts barrel files tend to overwrite rather than append — read the file first and edit only missing lines

## References
- https://react.dev/
- https://www.patterns.dev/react
- https://github.com/alan2207/bulletproof-react
- https://www.patterns.dev/posts/compound-pattern
- https://cva.style/docs
