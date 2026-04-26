# Agent Integration — Mobile Responsive

## When to use
- Building any web UI agent-side: the default starting point is mobile-first CSS, viewport meta, fluid type via `clamp()`.
- Auditing an existing site for mobile parity (e.g., regression after redesign), where an agent runs Lighthouse + Playwright in multiple viewports.
- Generating Tailwind configs, Storybook stories, or component libraries that must render correctly from 320px to 1920px.
- Producing email/embed snippets where viewport meta and fluid units are non-negotiable.

## When NOT to use
- Internal admin tooling targeting fixed-resolution kiosks or desktop-only ops dashboards — adding breakpoints adds drag without payoff.
- Embedded WebViews where the host app forces a known viewport (e.g., a Telegram WebApp pinned to mobile only) — design for one width.
- Print stylesheets, PDF generators, or static reports — different rendering model entirely.
- Native mobile (React Native, Flutter, SwiftUI) — different layout primitives; this methodology is web-CSS-specific.

## Where it fails / limitations
- Pure breakpoint design ignores container queries; modern UIs need `@container` for self-aware components.
- `100vh` on iOS Safari includes the URL bar height — leads to hidden bottom UI; use `100dvh` (dynamic viewport) or `svh`/`lvh`.
- Touch targets <44px violate Apple HIG and WCAG 2.5.5 — easy to miss when an agent is just translating Figma px to CSS.
- Hover-based UI breaks on touch; agents that translate `:hover` patterns from desktop demos produce broken mobile UX.
- Performance regressions hide on dev machines: a `<picture>` with 4 sources can still ship a 2 MB image to a 4G phone if the agent forgot `loading="lazy"` and `srcset` widths.

## Agentic workflow
A frontend subagent generates the markup + Tailwind classes (or vanilla CSS), then a verification subagent runs headless Chromium at 360×640, 768×1024, 1280×800, 1920×1080 and screenshots each. Layout-shift, scroll-overflow, and tap-target size are checked programmatically. A11y checks run in the same pass. The agent never accepts a UI as "responsive" without three viewport screenshots and a Lighthouse mobile score above an agreed threshold (e.g., perf > 85, a11y > 95).

### Recommended subagents
- `faion-sdd-executor-agent` — owns the UI task and reads acceptance criteria including viewport list.
- A purpose-built `responsive-auditor` subagent (Playwright + axe-core + Lighthouse) — runs the verification pass.
- For component libraries, drive Storybook viewport addon via the same agent so each story is checked in `mobile1`/`tablet`/`desktop`.

### Prompt pattern
```
Implement <component> mobile-first. No fixed widths. Use rem/em/%, clamp()
for type, and CSS Grid for layout. Tap targets >= 44x44px. Test at
360, 768, 1280 widths. Output the full CSS plus the Playwright assertions.
```
```
Audit <file>. Find: (1) px values that should be rem, (2) hover-only
interactions, (3) missing viewport meta, (4) 100vh usages, (5) tap
targets under 44px. Return a JSON list of findings with line numbers.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Headless multi-viewport screenshots & assertions | `npm i -D @playwright/test` · https://playwright.dev/ |
| `lighthouse` | Mobile perf/a11y audits | `npm i -g lighthouse` · https://developer.chrome.com/docs/lighthouse/ |
| `axe-core` / `@axe-core/cli` | Accessibility checks (touch target, contrast) | `npm i -g @axe-core/cli` |
| `pa11y` | Single-URL a11y CI runner | `npm i -g pa11y` |
| `puppeteer` + `puppeteer-cluster` | Bulk screenshot diffing | `npm i puppeteer puppeteer-cluster` |
| `responsively-app` | Multi-device live preview during dev | https://responsively.app/ |
| `tailwindcss` | Mobile-first utility classes (sm/md/lg/xl/2xl) | `npm i -D tailwindcss` |
| `polypane` | Multi-device preview + a11y; CLI exists for screenshots | https://polypane.app/ |
| `unlighthouse` | Site-wide Lighthouse crawl | `npx unlighthouse --site <url>` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BrowserStack | SaaS | Yes (REST API) | Real-device testing across iOS/Android matrix. |
| Sauce Labs | SaaS | Yes (REST API) | Same niche; integrates with Playwright/WebDriver. |
| LambdaTest | SaaS | Yes | API + Playwright-cloud runners. |
| Percy / Chromatic | SaaS | Yes | Visual diffing across breakpoints; agent-driven baselines. |
| Web.dev / PageSpeed Insights | SaaS | Yes | Programmatic via `psi` API for CI. |
| Storybook + Viewport addon | OSS | Yes | Per-story breakpoint tests. |

## Templates & scripts
See `templates.md` for full mobile-first CSS scaffolds. Inline Playwright assertion helper:

```ts
// scripts/responsive-check.ts
import { chromium, devices } from "@playwright/test";

const viewports = [
  { name: "iphone-se", ...devices["iPhone SE"] },
  { name: "ipad",      ...devices["iPad Pro 11"] },
  { name: "desktop",   viewport: { width: 1280, height: 800 } },
];

const url = process.argv[2] ?? "http://localhost:3000";
const browser = await chromium.launch();
for (const v of viewports) {
  const ctx = await browser.newContext(v);
  const page = await ctx.newPage();
  await page.goto(url);
  await page.screenshot({ path: `out/${v.name}.png`, fullPage: true });
  const overflow = await page.evaluate(
    () => document.body.scrollWidth > window.innerWidth,
  );
  if (overflow) console.error(`HORIZONTAL SCROLL at ${v.name}`);
  await ctx.close();
}
await browser.close();
```

## Best practices
- Always start with the viewport meta tag and `box-sizing: border-box` global rule; agent UI templates that omit these regress on day one.
- Use `clamp(min, fluid, max)` for both type and spacing — eliminates most breakpoint-specific font rules.
- Prefer CSS Grid for top-level layout (auto responsive via `grid-template-columns: repeat(auto-fit, minmax(...))`), Flexbox inside cells.
- Use container queries (`@container`) for components reused at different widths inside the same page.
- Replace `100vh` with `100dvh` (or `min(100vh, 100dvh)` for older browsers) to fix iOS bottom-bar bugs.
- Touch target rule: every interactive element ≥44×44 CSS px, with non-zero padding around small icons.
- Use `<picture>` + `srcset` + `sizes` for hero images; never ship a desktop-resolution PNG to a 360px viewport.
- Add a `prefers-reduced-motion` media query and gate all animations.
- Lock-in via Tailwind: enable `screens` config, ditch arbitrary breakpoints, use `min-h-dvh` once available.

## AI-agent gotchas
- LLMs default to `px` units when generating CSS because training data is full of legacy px examples. Prompt explicitly: "no fixed pixel widths above 1px borders".
- Agents copying Figma exports often invert mobile-first into desktop-first (`@media (max-width: ...)`); add a lint rule rejecting `max-width` media queries except for print/dark-mode overrides.
- LLMs frequently emit `<meta name="viewport" content="width=device-width">` without `initial-scale=1.0`, which breaks iOS Safari rotation. Verify both attributes are present.
- When asked to "make this responsive," LLMs often only add breakpoints to width and forget grid columns, font sizes, and touch targets. Provide a checklist explicitly.
- Auto-screenshot diffs need locked fonts/clock. Without `await page.evaluate(() => document.fonts.ready)` and freezing time, agents will report false-positive diffs every run.
- iOS-specific: agents miss `-webkit-tap-highlight-color: transparent`, momentum scrolling (`-webkit-overflow-scrolling: touch`) — flag these in PR review.
- A "passing" Lighthouse mobile run on localhost lies (no throttling). Always force `--throttling-method=devtools --preset=mobile` so the agent sees real perf budgets.
- Container queries land at different times in Safari/Firefox — agent must check support matrix before generating `@container` rules; provide a fallback or polyfill.

## References
- https://web.dev/articles/responsive-web-design-basics — Google's canonical guide
- https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_container_queries — container queries reference
- https://www.w3.org/WAI/WCAG21/Understanding/target-size.html — WCAG target size rule
- https://css-tricks.com/the-large-small-and-dynamic-viewport-units/ — dvh/svh/lvh explainer
- https://utopia.fyi/ — fluid type/space calculator producing clamp() values
- https://every-layout.dev/ — patterns for resilient component layouts
- https://playwright.dev/docs/emulation — device emulation reference
