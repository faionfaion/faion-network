# Agent Integration — Accessibility (WCAG)

## When to use
- Every web project — accessibility is a default, not an opt-in.
- Public-facing apps subject to ADA, EAA (June 2025 EU mandate), Section 508, AODA.
- Enterprise/government RFPs that require WCAG 2.1 AA or 2.2 AA conformance.
- E-commerce and fintech where assistive-tech failures convert directly into lost revenue + lawsuits.
- Any agent-generated UI: LLMs systematically under-deliver on a11y unless forced.

## When NOT to use
- Internal CLI/server-only tools with no UI surface (still apply for any web admin panel).
- Throwaway experiments — but even then, accessible markup is rarely more expensive than div soup.

## Where it fails / limitations
- Automated tools (axe, Lighthouse) catch ~30–40% of WCAG issues; manual + assistive-tech testing is non-negotiable.
- Agent-generated ARIA is often *wrong* and worse than no ARIA (e.g., `role="button"` on a `<div>` without keyboard handlers).
- Color-contrast checks pass on token sheets but fail in real composition (text over images, gradients).
- Focus management in SPAs is invisible to crawlers; route changes silently break screen readers.
- Translated content (i18n) breaks alt text, ARIA labels, and live-region politeness if not checked per locale.

## Agentic workflow
Bake a11y into three gates: (1) **author-time** — agents must use semantic HTML + reach for native elements first; (2) **commit-time** — `eslint-plugin-jsx-a11y` + `axe` Playwright sweep on changed pages; (3) **release-time** — manual screen-reader pass (NVDA on Win, VoiceOver on macOS/iOS, TalkBack on Android) on top user journeys. Never let an agent ship `role="button"` on a `<div>` without a paired keyboard handler test.

### Recommended subagents
- `faion-frontend-component-agent` — author with semantic HTML + ARIA where required.
- `faion-sdd-executor-agent` — run axe, jsx-a11y, focus-trap tests as gates.
- `faion-storybook-agent` — generate `@storybook/addon-a11y` reports per story.

### Prompt pattern
```
Build <DropdownMenu> meeting WCAG 2.2 AA. Constraints:
- Use Radix or @headlessui/react primitive (do not hand-roll).
- Keyboard map: Tab focus, Enter/Space open, Esc close, ↑/↓ navigate, type-ahead.
- aria-expanded, aria-controls, role=menu/menuitem wired correctly.
- Visible focus indicator at 3:1 contrast against adjacent color.
- Test: axe violations==0, keyboard-only walkthrough, focus restoration on close.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `eslint-plugin-jsx-a11y` | Static a11y lint for JSX | `npm i -D eslint-plugin-jsx-a11y` |
| `@axe-core/cli` / `axe-core` | Audit deployed pages | `npm i -D @axe-core/cli` |
| `@axe-core/playwright` | Per-test a11y check | `npm i -D @axe-core/playwright` |
| `pa11y` / `pa11y-ci` | Batch a11y CI runs | `npm i -D pa11y-ci` |
| `lighthouse` | A11y score in CI | `npm i -D lighthouse` |
| `@storybook/addon-a11y` | Per-story a11y panel | `npm i -D @storybook/addon-a11y` |
| `nvda` (Windows) / VoiceOver (macOS) / TalkBack (Android) | Manual SR testing | OS-native |
| Color contrast checkers | WCAG contrast | `axe`, Stark, Chrome DevTools |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevHub / axe Monitor | SaaS | Yes (CLI + API) | Industry-standard automated audit |
| WAVE (WebAIM) | SaaS | Partial | Visual report; API limited |
| AssistivLabs | SaaS | Yes | Cloud-hosted screen readers |
| Siteimprove | SaaS | Yes (REST API) | Enterprise governance |
| Stark | SaaS | Yes (Figma plugin + CLI) | Design-time contrast + simulation |
| Pa11y Dashboard | OSS | Yes | Self-hosted CI dashboards |
| Chromatic + a11y addon | SaaS | Yes | Story-level a11y in PR review |

## Templates & scripts
See `templates.md` and `checklist.md`. Quick Playwright + axe gate:

```ts
// tests/a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const routes = ['/', '/pricing', '/login', '/dashboard'];

for (const r of routes) {
  test(`a11y: ${r}`, async ({ page }) => {
    await page.goto(r);
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'])
      .analyze();
    expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });
}
```

ESLint quick-add:

```bash
npm i -D eslint-plugin-jsx-a11y
# .eslintrc append
# "extends": ["plugin:jsx-a11y/strict"]
```

## Best practices
- Semantic HTML first; reach for `<button>`, `<a>`, `<nav>`, `<main>` before any `role=`.
- One `<h1>` per page; outline must be hierarchical (no `h2 → h4` jumps).
- Keyboard-only walkthrough is the cheapest sanity check; if Tab/Shift-Tab traverses logically and Esc dismisses overlays, you are 80% there.
- Focus management on route change: move focus to `<main>` heading or a skip-link target; announce via aria-live on SPA navigations.
- All interactive elements: ≥44×44 CSS px touch target (WCAG 2.5.5).
- Respect `prefers-reduced-motion` and `prefers-color-scheme`; do not autoplay or auto-rotate.
- Form inputs must have programmatic labels (`<label for>` or `aria-labelledby`); placeholder is not a label.
- Provide visible error messaging linked via `aria-describedby` and `aria-invalid`.

## AI-agent gotchas
- Agents reach for `role="button"` and ARIA before considering native elements; require a "why not native?" justification in PR description.
- Generated `aria-label` strings are often duplicated, English-only, or contain Tailwind tokens (`aria-label="bg-blue-600"`); add a regex lint.
- Focus trap inside modals is frequently missing; require an integration test that Tab cycles inside the modal and Esc returns focus to opener.
- Live-region (`aria-live`) misuse: `assertive` for everything spams screen readers. Default to `polite`.
- Skip links and landmark regions disappear after refactors; pa11y or axe in CI catches regressions agents introduced.
- Color-contrast tokens that pass on white may fail on the secondary surface; test contrast in context, not in isolation.
- i18n: agents copy ARIA labels literally; long German/Ukrainian translations break truncated labels and tooltips.

## References
- https://www.w3.org/WAI/WCAG22/quickref/
- https://www.deque.com/axe/
- https://www.a11yproject.com/checklist/
- https://inclusive-components.design/
- https://webaim.org/resources/contrastchecker/
- https://accessibility.huit.harvard.edu/screen-reader-testing
