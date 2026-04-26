# Agent Integration — Storybook Setup

## When to use
- Initial Storybook 8.x install on a Vite/Webpack/Next.js project (`storybook init` + framework adapter).
- Wiring `.storybook/main.ts` and `.storybook/preview.ts` for theming, viewports, backgrounds, a11y addon.
- Adding visual + a11y + interaction testing (Chromatic / `@storybook/test-runner` / `@storybook/addon-a11y`).
- Setting up CSF 3 stories convention and `tags: ['autodocs']` for a typed component library.

## When NOT to use
- The project ships only one or two pages — Ladle or `vite-plugin-storybook-lite` boots faster with less config.
- No design system / no shared component library yet — Storybook's value lives in component reuse; without it, it's overhead.
- The team commits to `playground/`-style Next.js dev pages — Storybook duplicates that effort.

## Where it fails / limitations
- Storybook 8 dropped Webpack 4 and Babel-only setups; legacy Create React App projects need a Vite migration first.
- `react-docgen-typescript` chokes on generic components (`<T>`) and emits empty prop tables in autodocs — needs `propFilter` + sometimes a manual `argTypes` block.
- Tailwind v4 + Storybook 8 needs the `@tailwindcss/postcss` plugin loaded via `viteFinal` / `webpackFinal`; the `init` command does not configure it.
- Theme switching via `globalTypes.toolbar` only flips a CSS class — agents often forget to actually consume it in `decorators` and the toggle does nothing.
- Storybook 8 changed the `argTypesRegex` action behavior; agents copying older snippets get console warnings on startup.

## Agentic workflow
First action: run `npx storybook@latest init` in the target repo and let it auto-detect the framework. Then have a subagent fill `main.ts`, `preview.ts`, and a starter `Button.stories.tsx` from the README skeleton. Add `@storybook/addon-a11y` and Chromatic in a second pass — small commits avoid blowing up the initial setup. Use a Playwright + `@storybook/test-runner` smoke test as the oracle ("storybook builds and every story renders without console errors").

### Recommended subagents
- `faion-feature-executor` — Storybook setup is naturally task-decomposed: install → main.ts → preview.ts → first story → a11y → CI.
- `faion-sdd-executor-agent` — only if the work is part of a larger design-system rollout with spec/design.

### Prompt pattern
- "Initialize Storybook 8 in this Vite + React + TS project. Generate `.storybook/main.ts` and `.storybook/preview.ts` per `storybook-setup/README.md`. Add a11y addon and a `Button.stories.tsx` smoke story. Run `pnpm storybook build` and report errors."
- "Convert `Card.tsx` props into CSF 3 stories. Each variant gets a story, `tags: ['autodocs']`, and `argTypes` for select/boolean controls. Write a `play` function that asserts the rendered DOM."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx storybook@latest init` | Bootstrap with framework auto-detect | https://storybook.js.org/docs/get-started/install |
| `npx storybook@latest upgrade` | Major-version upgrade with codemods | https://storybook.js.org/docs/configure/upgrading |
| `npx storybook@latest doctor` | Diagnose plugin/version mismatches | https://storybook.js.org/docs/api/cli-options |
| `pnpm dlx @storybook/test-runner` | Headless Playwright runner over all stories | https://storybook.js.org/docs/writing-tests/test-runner |
| `npx chromatic --project-token=$T` | Visual review + Storybook hosting | https://www.chromatic.com/docs/cli |
| `pnpm dlx storybook build` | Static export for hosting (`storybook-static/`) | https://storybook.js.org/docs/sharing/publish-storybook |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Chromatic | SaaS | Yes (CLI + GH Action + REST) | Default for visual testing; agents read PR-status checks and capture baselines. |
| Storybook hosting on faion-net | OSS (self-host) | Yes | `storybook-static/` rsynced to `storybook.faion.net` (see workspace `AGENTS.md`). |
| Vercel/Netlify static deploy | SaaS | Yes | Drop `storybook-static` for previews. |
| Percy | SaaS | Yes | Alternative to Chromatic; same agent flow. |
| Lost Pixel | OSS | Yes | Self-hosted visual regression; agents can drive via CLI. |

## Templates & scripts
See `templates.md` for `main.ts`, `preview.ts`, and a CSF 3 story scaffold. Minimal CI build check:

```yaml
# .github/workflows/storybook.yml
name: storybook
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm storybook build
      - run: pnpm dlx @storybook/test-runner --url file://$(pwd)/storybook-static
```

## Best practices
- Pick CSF 3 (`Meta<typeof Component>`, `StoryObj`) for new stories; CSF 2 still works but autodocs and controls are weaker.
- Co-locate stories with components (`Button.tsx` + `Button.stories.tsx`) — ergonomics over global `stories/` folder.
- Keep `preview.ts` small: globals (theme, locale), decorators, parameters. Avoid app-wide providers unless strictly needed.
- Use `argTypes` + `parameters: { controls: { exclude: [...] } }` to hide noise from autodocs; default tables are full of HTML attribute leaks.
- Run `@storybook/test-runner` in CI on every PR — catches "story renders but throws" regressions cheaply.
- Treat the deployed Storybook URL as a design-review artifact for non-engineers; commit messages should reference story IDs.

## AI-agent gotchas
- Agents emit `Meta<typeof Button>` but forget `tags: ['autodocs']`, then wonder why no docs page appears.
- LLMs add a duplicate `addons` entry when re-running setup → Storybook starts but addon panels are empty; dedupe `main.ts` after multi-pass edits.
- `actions: { argTypesRegex }` is logged as deprecated in Storybook 8 — agents copying 6.x snippets cause CI warnings; use `@storybook/addon-actions` decorators instead.
- For Next.js App Router, agents forget `@storybook/nextjs` framework adapter and hit "useRouter is null" in stories.
- Tailwind: missing `import '../src/styles/globals.css'` in `preview.ts` is the #1 "my classes don't work in Storybook" cause.
- Generated `play` functions skip `await` on `userEvent.click` — assertions fire before React updates.

## References
- Storybook 8 docs — https://storybook.js.org/docs
- CSF 3 spec — https://storybook.js.org/docs/api/csf
- `@storybook/addon-a11y` — https://storybook.js.org/addons/@storybook/addon-a11y
- Test runner — https://storybook.js.org/docs/writing-tests/test-runner
- Chromatic — https://www.chromatic.com/docs/
