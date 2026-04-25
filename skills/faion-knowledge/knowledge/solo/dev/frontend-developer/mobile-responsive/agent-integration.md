# Agent Integration — Mobile Responsive

## When to use
- Greenfield site/app — set viewport meta, mobile-first base CSS, container queries from the first commit.
- Auditing an existing layout for breakpoint regressions, touch-target sizes, and CLS on small screens.
- Migrating from media-query-based responsive design to container queries for component-driven layouts.
- Configuring Tailwind / vanilla CSS breakpoints to match real content breakpoints (not iPhone vs iPad widths).

## When NOT to use
- App is locked to a single device class (e.g., kiosk, internal tablet-only tool) — fixed layout is simpler.
- The framework already enforces mobile-first (Tailwind default, Material UI Grid) and the current site passes Lighthouse mobile — adding more breakpoints is busywork.

## Where it fails / limitations
- iOS Safari `100vh` includes the URL bar, causing layout jump when it hides; use `100dvh` or `--vh` JS shim.
- `meta name="viewport"` with `user-scalable=no` violates WCAG 1.4.4; agents copy this from old templates and break a11y silently.
- Container queries (`@container`) require `container-type: inline-size` on the parent — without it, queries silently never match.
- Touch-target rule (44×44 CSS px from WCAG 2.5.8) is regularly violated by icon-only buttons; visual review hides this.
- `srcset`/`sizes` is verbose and easy to miswrite — wrong `sizes` makes the browser fetch the largest image regardless.

## Agentic workflow
Run a subagent that (1) inventories every fixed-width / `min-width` value in CSS, (2) regenerates them from a tokenized breakpoint set, (3) snapshots the page at mobile/tablet/desktop with Playwright + visual diff. Use Lighthouse mobile + the Chrome DevTools device emulation script as oracles. The agent should not pick breakpoints from device sizes; pin them to content (e.g., "two-column when card row exceeds 640px").

### Recommended subagents
- `faion-feature-executor` — page-by-page audit + fix loop with visual-test gate.
- `faion-sdd-executor-agent` — when responsive work ties into a redesign with explicit AC.

### Prompt pattern
- "Audit `src/app/**/page.tsx` for fixed widths and missing breakpoints. Output a table: file, offending rule, proposed mobile-first replacement. Do NOT edit files yet."
- "Refactor `Card.module.css` to use container queries: `Card` reads its parent width via `container-type: inline-size`. Provide before/after screenshots at 320, 480, 720, 1024 px."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `npx lighthouse <url> --preset=mobile --only-categories=performance,accessibility,seo` | Mobile audit | https://developer.chrome.com/docs/lighthouse/ |
| `pnpm dlx @lhci/cli autorun` | Lighthouse CI in PRs | https://github.com/GoogleChrome/lighthouse-ci |
| `npx playwright test --project=mobile-chrome` | Run Playwright with mobile emulation devices | https://playwright.dev/docs/emulation |
| `npx pa11y-ci --config .pa11yci` | A11y audit (touch targets, contrast) | https://github.com/pa11y/pa11y-ci |
| `npx browser-sync start --server --files "**/*"` | Multi-device live-reload during manual checks | https://browsersync.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BrowserStack / Sauce Labs | SaaS | Yes (REST + Playwright integration) | Real-device testing; agents drive via Playwright cloud connection. |
| LambdaTest | SaaS | Yes | Cheaper alternative; same agent flow. |
| Chromatic | SaaS | Yes | Visual regression at multiple viewports; pair with Storybook stories per breakpoint. |
| WebPageTest | SaaS + OSS | Yes (REST API) | Mobile + 3G throttled testing for CWV; agent fetches JSON results. |

## Templates & scripts
See `templates.md` for the mobile-first CSS / Tailwind config / image responsive snippets. Snippet for a 100dvh fix:

```css
/* iOS-safe full-height; falls back to vh on browsers without dvh */
.full-screen {
  min-height: 100vh;
  min-height: 100dvh;
}

/* Touch-target floor: every interactive element */
button, a, [role="button"], input[type="button"] {
  min-height: 44px;
  min-width: 44px;
}
```

```ts
// playwright.config.ts (extract)
import { devices, defineConfig } from '@playwright/test';
export default defineConfig({
  projects: [
    { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 14'] } },
    { name: 'tablet',         use: { ...devices['iPad (gen 7) landscape'] } },
    { name: 'desktop',        use: { viewport: { width: 1440, height: 900 } } },
  ],
});
```

## Best practices
- Mobile-first: base styles unconditional, `min-width` queries layer up. Never `max-width` first — it leaks desktop assumptions.
- Pick breakpoints from content, not device. Common content-driven set: 480 / 640 / 768 / 1024 / 1280.
- Use `clamp(min, fluid, max)` for typography and spacing instead of stepwise breakpoints — drops 30-50% of media queries.
- Always set `<meta name="viewport" content="width=device-width, initial-scale=1">` and never `maximum-scale=1` (a11y).
- Ship `srcset` + `sizes` for hero images; verify the right candidate fires at each viewport via DevTools "Resources" panel.
- Test on a real low-end Android (Moto G class) at least once per release — emulators hide jank.

## AI-agent gotchas
- Agents lift breakpoint values from Bootstrap (576/768/992/1200) without checking project tokens; the file becomes inconsistent.
- LLMs convert `vh` to `dvh` mechanically and break older browsers — keep the `vh` fallback line.
- Generated container-query code omits `container-type: inline-size` on the parent → no styles apply, agent declares "done".
- When asked to "make it responsive", agents add `flex-wrap: wrap` everywhere; the result is correct on phones and looks broken on desktop.
- Touch-target rule is forgotten on icon buttons (`<Button size="sm">` with `padding: 4px`); agents mark a11y "fixed" without re-running pa11y.
- `srcset` `sizes` attribute is regularly written as `100vw` for everything — wastes bandwidth on multi-column layouts.

## References
- MDN Responsive Design — https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design
- WCAG 2.5.8 Target Size — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Container queries (CSS Containment Module) — https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- Josh Comeau, "The Surprising Truth About Pixels and Accessibility" — https://www.joshwcomeau.com/css/surprising-truth-about-pixels-and-accessibility/
- Playwright device emulation list — https://playwright.dev/docs/emulation
