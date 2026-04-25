# Agent Integration — Storybook Setup

## When to use
- Bootstrapping a component library or design system in a React / Vue / Svelte / Angular codebase.
- Adding `*.stories.tsx` files alongside new components as part of a feature delivery.
- Generating MDX docs from existing components for non-developer stakeholders.
- Wiring visual regression (Chromatic / Percy) and a11y checks (`addon-a11y`) into CI.
- Building a sandbox for components that need to be reviewed before they are wired into the app.

## When NOT to use
- Single-page apps with fewer than ~10 components — overhead exceeds value.
- Framework-tightly-coupled components (e.g., relying on Next.js `app/` server components) where Storybook context is hard to fake.
- Pure backend / CLI projects.
- Internal-only "throwaway" admin UIs that won't be redesigned.
- When the team will not maintain stories — outdated stories are worse than none.

## Where it fails / limitations
- Storybook v8/v9 configuration churn breaks agent-generated `main.ts` from older training data; addons get renamed (`@storybook/addon-essentials` was unbundled into per-feature addons in v9).
- Decorators that depend on a real router/store/i18n context are easy to forget and surface later as runtime errors only when a story is opened.
- `play` functions look like Jest but use `@storybook/test`; agents conflate the two and import the wrong helpers.
- Visual diffs depend on deterministic rendering — animations, dates, network calls cause false positives.
- MDX has its own pitfalls: importing components inside MDX and using them inside `<Canvas>` requires them to also exist as a story.

## Agentic workflow
A scaffolding subagent runs `npx storybook@latest init`, commits the baseline, then a per-component generator subagent emits `<Component>.stories.tsx` from the component's prop types (TypeScript or PropTypes). A reviewer subagent checks each story for: tags includes `'autodocs'`, `args` covers all required props, at least one variant per visually distinct state, and no duplicated decorators with `preview.tsx`. CI runs `build-storybook` and Chromatic on every PR; the agent reads Chromatic's accept/reject delta to flag visual regressions for human review.

### Recommended subagents
- `faion-feature-executor` — sequential delivery: component → story → MDX → visual baseline.
- A `story-generator` subagent (custom) — input: component file path; output: `*.stories.tsx` + minimal MDX with all variants from prop union types.
- A `chromatic-triage` subagent — reads Chromatic API, classifies diffs as intentional vs regression, posts comment on PR.

### Prompt pattern
```
Generate <Component>.stories.tsx for <path>. Constraints:
1. Use CSF3 (default-export Meta + named StoryObj exports).
2. tags: ['autodocs'].
3. One named export per visual variant of every prop in the union types.
4. argTypes for every prop: control type matches prop type; description from JSDoc.
5. Include a `play` function asserting basic interaction for any prop named `on*`.
```

```
Review story file. Block if: missing autodocs tag, missing args for required props, decorators duplicate preview.tsx, hard-coded date/locale that breaks visual diff, or imports from `@storybook/jest` (must be `@storybook/test`).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `storybook` CLI | Init, dev, build, upgrade | `npx storybook@latest init` — https://storybook.js.org/docs/get-started/install |
| `@storybook/test-runner` | Headless runner that executes `play` functions | https://storybook.js.org/docs/writing-tests/test-runner |
| `chromatic` CLI | Publish to Chromatic for visual review | https://www.chromatic.com/docs/cli |
| `@storybook/addon-a11y` | axe-core inside the panel | https://storybook.js.org/docs/writing-tests/accessibility-testing |
| `@storybook/addon-coverage` | Code coverage from interaction tests | https://github.com/storybookjs/test-runner |
| `storycap` | Screenshot all stories for self-hosted visual diff | https://github.com/reg-viz/storycap |
| `loki` (`@loki/runner`) | OSS visual regression alternative to Chromatic | https://loki.js.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chromatic | SaaS | yes | First-party visual review; agents read PR-level review URLs and accept/deny via API token. |
| Percy (BrowserStack) | SaaS | yes | Alternative visual review with multi-browser. |
| Vercel / Netlify / GitHub Pages | SaaS | yes | Static `storybook-static/` hosting for stakeholders. |
| Argos CI | SaaS | yes | Lighter-weight visual diff, OSS-friendly pricing. |
| Figma + Storybook Connect | SaaS | partial | Maps stories to Figma frames; useful for designer review but agents can't drive Figma directly. |

## Templates & scripts
See `templates.md` for full `main.ts`, `preview.ts`, story, and MDX templates. Inline auto-detection helper for an agent generating stories from prop types:

```ts
// scripts/derive-variants.ts
// Emits a list of variant names from a TS union type via the TS compiler API.
import { Project, SyntaxKind } from "ts-morph";
const project = new Project();
const sf = project.addSourceFileAtPath(process.argv[2]);
const iface = sf.getInterfaceOrThrow("ButtonProps");
for (const prop of iface.getProperties()) {
  const type = prop.getType();
  if (type.isUnion()) {
    const names = type.getUnionTypes().map((t) => t.getText());
    console.log(`${prop.getName()}: ${names.join(", ")}`);
  }
}
```

The agent feeds output into a story-generator prompt to ensure no variant is missed.

## Best practices
- Pin Storybook version in `package.json` and run `npx storybook upgrade` deliberately, not via Renovate auto-merge — minor releases break configs.
- One `preview.tsx` global decorator per cross-cutting context (Theme, Router, Query, i18n). Per-story decorators only for story-specific overrides.
- Use `args` and `argTypes` so Controls panel works; agents skip `argTypes` and the panel becomes useless.
- For network-dependent components, use MSW (`msw-storybook-addon`) instead of mocking inside the component.
- Pair every story with at least one `play` function for primary interaction — turns Storybook into a free interaction-test suite.
- Give stories deterministic data: fixed dates with `MockDate`, fixed UUIDs, suppressed animations (`parameters.chromatic.pauseAnimationAtEnd: true`).
- Title hierarchy is documentation: `Foundation/*`, `Components/*`, `Patterns/*`, `Pages/*` keeps the sidebar navigable for designers.

## AI-agent gotchas
- Agents copy v6 `argTypes: { ..., control: { type: 'select' } }` syntax into v8/v9 which expects `control: 'select'` (or both, but inconsistently). Anchor prompts to "Storybook v8.x CSF3".
- `@storybook/test` (`fn`, `expect`, `userEvent`, `within`) replaced `@storybook/jest` and `@storybook/testing-library`. Old training data still imports from removed packages.
- `autodocs` tag: agents add it to the meta but forget the `tags: ['autodocs']` is also needed at the story level for some addons; check Storybook output.
- For Next.js, agents forget `@storybook/nextjs` framework; they'll use `@storybook/react-vite` and `next/image` will explode.
- Human-in-loop: visual regression baselines must be approved by a human first time; agents accepting their own baselines defeats the purpose.
- Agents add `parameters.docs.description` with the same string as the component JSDoc — duplication and drift. Source-of-truth should be JSDoc only; let `react-docgen-typescript` extract it.
- When stories live in `src/`, ensure `tsconfig.json` exclude does NOT cover `*.stories.tsx`, otherwise type-checking misses them.

## References
- https://storybook.js.org/docs — official docs (v8/v9)
- https://storybook.js.org/docs/api/csf — Component Story Format reference
- https://www.chromatic.com/docs — Chromatic
- https://storybook.js.org/docs/writing-tests/accessibility-testing — a11y addon
- https://storybook.js.org/docs/writing-tests/test-runner — test-runner setup
- https://storybook.js.org/recipes — framework-specific recipes (Next.js, Remix, Vite, Astro)
