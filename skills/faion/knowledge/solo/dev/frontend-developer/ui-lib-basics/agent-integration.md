# Agent Integration — UI Component Library Basics

## When to use
- Multiple apps or features share UI primitives and you keep re-implementing buttons, modals, and inputs.
- Team or agent fleet is producing inconsistent patterns; centralized library forces a standard.
- You need accessibility baked in once (focus rings, ARIA wiring) instead of audited per-PR.
- Onboarding new agents/devs faster by reducing decisions on every component.

## When NOT to use
- Single small app where YAGNI applies; a `components/` folder is enough.
- Fast-evolving product still finding its visual language; abstraction freezes premature decisions.
- You can adopt shadcn/ui or an existing library — building from scratch rarely pays off solo.
- Marketing site with brochure pages; library overhead exceeds reuse.

## Where it fails / limitations
- Premature abstraction kills velocity; over-genericized props become a worse API than copy-paste.
- Versioning across consumer apps is hard without monorepo + workspace tooling.
- Theming via CSS variables is portable; theming via JS context locks consumers into a stack.
- Bundle size grows when consumers import the whole library; barrel files defeat tree-shaking unless `sideEffects: false` is set and imports are deep.
- Storybook drift: components ship without stories, agents cannot inspect, library decays.

## Agentic workflow
Three roles: (1) **architect** decides structure (`primitives/`, `composite/`, `patterns/`), (2) **author** implements components paired with stories + tests, (3) **integrator** lifts useful patterns from product code into the library. Force agents to write the story before the component (story-first development); the story doubles as the agent's understanding check. Gate releases on Storybook visual regression + axe scan + bundle-size budget.

### Recommended subagents
- `faion-frontend-component-agent` — author primitive + composite components.
- `faion-storybook-agent` — write stories first, MDX docs, args matrix.
- `faion-sdd-executor-agent` — typecheck, axe, bundle-size budget, semver bump.

### Prompt pattern
```
Add a <Tooltip> to packages/ui/primitives/Tooltip/.
Deliver: Tooltip.tsx, Tooltip.stories.tsx (args matrix: side, align, delay), Tooltip.test.tsx,
index.ts (named export only). API: ({content, side, align, children}). Use Radix Popper or Floating UI.
Forbid: default exports, side-effecting imports, inline styles. Story before component.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `storybook` | Component sandbox, MDX docs | `npx storybook@latest init` |
| `tsup` / `tsc` / `vite build --mode lib` | Build dist with ESM + CJS + dts | `npm i -D tsup` |
| `changesets` | Versioning + changelogs | `npm i -D @changesets/cli` |
| `size-limit` | Bundle-size budget per export | `npm i -D size-limit` |
| `@axe-core/playwright` | A11y in CI | `npm i -D @axe-core/playwright` |
| `playwright` | Visual + interaction tests | `npm init playwright@latest` |
| `pnpm` / `nx` / `turbo` | Monorepo orchestration | `npm i -g pnpm` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chromatic | SaaS | Yes | Visual regression + Storybook hosting |
| Storybook Cloud | SaaS | Yes | Storybook hosting, sharing |
| npmjs.com / GitHub Packages | SaaS | Yes | Publish private/public lib |
| Verdaccio | OSS | Yes | Self-hosted npm proxy |
| Bit.dev | SaaS | Yes | Component-level versioning |
| Backstage TechDocs | OSS | Yes | Internal portal for the library |

## Templates & scripts
See `templates.md` and `examples.md`. Bundle-size budget config:

```json
// .size-limit.json
[
  { "name": "Button", "path": "dist/index.js", "import": "{ Button }", "limit": "2 kB" },
  { "name": "Modal",  "path": "dist/index.js", "import": "{ Modal }",  "limit": "5 kB" }
]
```

Story-first scaffold helper:

```bash
#!/usr/bin/env bash
# scripts/new-component.sh <name>
set -euo pipefail
name="${1:?name required}"
dir="src/primitives/${name}"
mkdir -p "$dir"
cat > "$dir/${name}.stories.tsx" <<EOF
import type { Meta, StoryObj } from '@storybook/react';
import { ${name} } from './${name}';
const meta: Meta<typeof ${name}> = { title: 'Primitives/${name}', component: ${name} };
export default meta;
type Story = StoryObj<typeof ${name}>;
export const Default: Story = { args: {} };
EOF
echo "// TODO implement after story" > "$dir/${name}.tsx"
echo "export * from './${name}';" > "$dir/index.ts"
```

## Best practices
- One named export per file; barrel files only at package root with `sideEffects: false`.
- Polymorphic `as` prop kept simple; complex generics confuse both humans and agents — prefer composition.
- Ship `dist/` with ESM + CJS + `.d.ts`; consumers should not transpile your sources.
- Use CSS variables for theme, never theme via React Context inside the library — locks consumers.
- Keep primitives behavior-only when possible (Radix/Headless UI under the hood) and apply visual styles in a higher layer.
- Document accessibility per component (keyboard map, ARIA roles, focus trap behavior). Stories show, MDX explains.

## AI-agent gotchas
- Agents over-abstract; force a "rule of three" — extract only after three duplicates exist.
- LLMs love prop explosion (`<Button leftIcon={...} rightIcon={...} loading={...} block={...} round={...}`); mandate `cva()` variants instead.
- Default exports break refactoring; lint rule `import/no-default-export` saves hours.
- Agents skip stories and tests under deadline; CI must reject components without `*.stories.tsx` + `*.test.tsx`.
- Bundle size regressions sneak in via `lodash` and date libs; `size-limit` budget per primitive prevents drift.
- Polymorphic `as` typed in TS often regresses on agent edits — pin a working `PolymorphicProps` helper and forbid agents from rewriting it.

## References
- https://storybook.js.org/docs
- https://www.radix-ui.com/primitives
- https://floating-ui.com/
- https://github.com/changesets/changesets
- https://github.com/ai/size-limit
