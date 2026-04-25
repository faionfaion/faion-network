# Agent Integration — UI Component Library

## When to use
- Building a reusable component set across multiple apps in a monorepo (web, admin, mobile-web).
- Standardizing variants, tokens, and a11y across product surfaces so agents have a single source of truth.
- Need versioned, semver-controlled UI exports (npm or workspace packages) — distinct from shadcn's copy-paste model.
- Enforcing accessibility, theming, and prop API consistency through code review and automated audits.

## When NOT to use
- A single small app with no plans to share components — premature library extraction adds cost.
- Heavy bespoke styling per-page where compositional reuse is low (marketing sites, one-off campaigns).
- Replacing well-maintained external libraries (MUI, Chakra, Mantine) without a clear extension story.
- When the team can't commit to maintaining stories, tests, and tokens — the library will rot fast.

## Where it fails / limitations
- Prop explosion: API surface grows uncontrollably as agents add `isRound`, `hasIcon`, `tone`, etc. Hard to deprecate later.
- Accessibility regression: hand-rolled primitives without Radix/React Aria miss focus traps, roving tabindex, IME handling.
- CSS leakage: Module CSS or styled-components can break when agents bulk-rename selectors.
- Bundle size: every consumer pays for unused code if tree-shaking metadata is missing (`sideEffects: false`, ESM exports).
- Cross-version drift: app A pins v2, app B pins v5; bug fixes never reach v2 consumers.
- "Tight coupling" to parent layout (e.g., a Modal that assumes specific portal root) appears subtly and explodes in tests.

## Agentic workflow
Use a subagent to (1) draft the component spec (props, variants, a11y notes) before writing code, (2) implement primitive + tests + Storybook story atomically, (3) run a11y + visual regression checks, (4) update the public barrel. Library work is naturally three-phase — spec → impl → review — so route each phase to a different agent role with clear handoffs. Keep the design-token JSON outside any single component to allow theme edits without touching component source.

### Recommended subagents
- `component-architect` (Sonnet) — proposes API surface, variant set, a11y model from a one-line brief.
- `component-implementer` (Sonnet/Haiku) — writes the `.tsx` + CSS + Story + test scaffold.
- `a11y-auditor` (Haiku) — runs axe-core, keyboard tab tests, ARIA attribute review.
- `bundle-watcher` (Haiku) — runs `size-limit` / `bundlewatch` and refuses PRs that bloat exports.
- `storybook-story-writer` (Haiku) — generates stories covering all variants × states (loading, disabled, error).

### Prompt pattern
```
Brief: Add a Toast component to packages/ui.
Inputs: variants=[info, success, warning, error], dismissible, autoClose ms.
Constraints:
- Use @radix-ui/react-toast under the hood.
- Prop API mirrors existing Button/Input naming (variant, size, isLoading).
- forwardRef, displayName, "use client" directive (Next).
- Must export from packages/ui/src/index.ts.
Deliverables: Toast.tsx + Toast.module.css + Toast.test.tsx + Toast.stories.tsx + barrel update.
```

```
Audit: components/primitives/Dropdown.
Run: keyboard (Tab/Esc/Arrow), focus trap, aria-* on trigger and menu, screen reader labels.
Output: pass/fail per check, patch plan if any fail.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Storybook 8 | Component dev + docs | `npx storybook@latest init` |
| `tsup` / `tsc --build` | Library bundling with d.ts | `npm i -D tsup` |
| `@size-limit/preset-small-lib` | Enforce bundle budgets per export | https://github.com/ai/size-limit |
| `@axe-core/playwright` | A11y in e2e | `npm i -D @axe-core/playwright` |
| Chromatic CLI | Visual regression on stories | `npm i -D chromatic` |
| `react-docgen` / `typedoc` | Auto-generate prop docs | https://react-docgen.dev |
| `changesets` | Versioning + changelogs in monorepo | `npm i -D @changesets/cli` |
| `eslint-plugin-jsx-a11y` | Lint-level a11y enforcement | `npm i -D eslint-plugin-jsx-a11y` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Storybook | OSS | Yes (CLI + MDX) | Stories are agent-writable; ship alongside components |
| Chromatic | SaaS | Yes via CLI | Visual diff PR comments — agents trigger via `chromatic --exit-zero-on-changes` |
| Bit.dev | SaaS / OSS | Yes via Bit CLI | Component-as-a-package model with isolated workspaces |
| Radix Primitives | OSS | Yes (just code) | Use under the hood for any interactive primitive |
| React Aria (Adobe) | OSS | Yes | Hooks-based a11y primitives — alternative to Radix |
| Figma + Tokens Studio | SaaS | Partial | Token export to JSON/CSS; agents consume the JSON |
| Style Dictionary | OSS | Yes | Compile token JSON → CSS/JS/iOS/Android |
| Verdaccio / GitHub Packages | OSS / SaaS | Yes | Private registry for library distribution |

## Templates & scripts
See `templates.md` for the per-component skeleton. Useful generator script:

```bash
#!/usr/bin/env bash
# Usage: ./new-component.sh primitives Toast
set -euo pipefail
LAYER=$1; NAME=$2
DIR="src/components/$LAYER/$NAME"
mkdir -p "$DIR"
cat > "$DIR/$NAME.tsx" <<EOF
import { forwardRef } from 'react';
import { clsx } from 'clsx';
import styles from './$NAME.module.css';
export interface ${NAME}Props extends React.HTMLAttributes<HTMLDivElement> {}
export const $NAME = forwardRef<HTMLDivElement, ${NAME}Props>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={clsx(styles.root, className)} {...props} />
  )
);
$NAME.displayName = '$NAME';
EOF
cat > "$DIR/$NAME.module.css" <<EOF
.root { display: block; }
EOF
cat > "$DIR/$NAME.stories.tsx" <<EOF
import type { Meta, StoryObj } from '@storybook/react';
import { $NAME } from './$NAME';
const meta: Meta<typeof $NAME> = { component: $NAME, title: '$LAYER/$NAME' };
export default meta;
export const Default: StoryObj<typeof $NAME> = { args: {} };
EOF
echo "export * from './$NAME/$NAME';" >> "src/components/$LAYER/index.ts"
```

## Best practices
- Lock the public API: barrel exports only — never `import { foo } from '@org/ui/dist/internal/...'`.
- Use design tokens (CSS variables or Style Dictionary) for all colors, radii, spacing — components reference tokens, never literals.
- Co-locate test + story + source per component; agents touching one usually need to touch all three.
- Define a "prop-API doctrine": same name = same meaning across components (`variant`, `size`, `isLoading`, `leftIcon`, `rightIcon`, `asChild`, `fullWidth`).
- Ban prop names that imply layout in primitives (`marginBottom`, `paddingX`) — those belong on layout components (Stack, Box).
- Add a11y assertions to every test (axe-core) — not optional.
- Maintain an `/migrations.md` doc that agents append to whenever they break a public API.
- Use `peerDependencies` for `react`, `react-dom`, never `dependencies`.

## AI-agent gotchas
- Agents reinvent primitives (custom dropdown menu) instead of wrapping Radix; require a "use Radix or React Aria" rule for interactive primitives.
- API drift: agents add `colorScheme` here, `tone` there. Enforce with a static check that all components expose the same `variant` enum names where applicable.
- "Helpful" defaults: agents set defaults that hide bugs (`isLoading={false}` is fine; `onClose={() => {}}` masks missing wiring).
- Storybook control mismatch: agents forget `argTypes`, leaving controls broken — require lint rule that every prop has a control or `control: { disable: true }`.
- Forgetting `"use client"` (Next.js) or `import 'client-only'` — components break SSR silently.
- Treating CSS modules as global: agents add `:global(.foo)` selectors that leak. Hook lints for `:global` outside specific files.
- Human-in-loop checkpoint: any change to public barrel (`src/index.ts`) is a semver event — require human approval and a changeset.

## References
- https://www.radix-ui.com/primitives
- https://react-spectrum.adobe.com/react-aria/
- https://storybook.js.org/docs
- https://www.chromatic.com/docs
- https://github.com/changesets/changesets
- https://amzn.eu/d/bound-react-design-systems (Brad Frost, Atomic Design)
- https://design-system-checklist.com
- https://amzn.eu/d/ant-design-philosophy (https://ant.design/docs/spec/values)
