# Agent Integration — Accessibility (Web)

## When to use
- Default for all web work — treat WCAG 2.1 AA as the minimum, 2.2 AA where mandated.
- Public sector / EU services (EAA from June 2025), US federal (Section 508), education, banking, healthcare.
- E-commerce checkouts and any flow tied to revenue — a11y bugs convert into lost sales.
- Components in a design system / library — fix once, benefit everywhere.
- Any product where keyboard-only or screen-reader use is expected (admin tools, content creation).

## When NOT to use
- Internal one-off scripts/tools used by 1-2 people who don't need assistive tech (still nice, but not budget-worthy).
- Throwaway experimental prototypes — defer until validated.
- Highly visual experiences where alternatives are mandated separately (interactive 3D demos with a documented text/audio alternate).
- "Skip a11y" is rarely the right answer; almost always the question is *which level of effort*, not *whether*.

## Where it fails / limitations
- Automated tools (axe, Lighthouse, pa11y) catch 30-40% of issues at best — keyboard nav, focus order, screen-reader semantics need manual review.
- "ARIA-first" thinking leads to over-ARIA: redundant `role="button"` on `<button>`, `aria-label` duplicating visible text. First rule of ARIA: don't use it.
- Custom components (combobox, listbox, tree) are harder than they look; the WAI-ARIA Authoring Practices patterns are exhaustive but easy to implement subtly wrong.
- Color contrast tools accept gradients and overlays poorly; APCA (newer) gives different results than WCAG 2's relative-luminance.
- Internationalization interacts: lang attributes, RTL, dynamic content language switches; agents almost always miss these.
- Mobile screen readers (VoiceOver iOS, TalkBack Android) behave differently from desktop; testing on desktop alone misses bugs.
- "Reduced motion" + animation libraries (framer-motion, GSAP) don't always respect `prefers-reduced-motion` by default.
- Live regions can over-announce or under-announce; finding the right `aria-live` polite/assertive level is empirical.

## Agentic workflow
A planner subagent classifies the work: new component (build accessible from scratch), new page (audit semantics), or remediation (run axe + manual checklist). A scaffolder subagent uses Radix UI / React Aria as the accessible primitive layer when possible (don't roll your own combobox). A test subagent generates `jest-axe` unit tests, Playwright keyboard-nav tests, and a Lighthouse-CI threshold. A reviewer subagent runs through the WCAG 2.2 AA checklist for changed templates.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → impl → axe/lighthouse tests → manual checklist.
- A user-defined `axe-runner` (model: haiku) — runs `axe-core` over a route list, returns violations as JSON.
- A user-defined `aria-reviewer` (model: sonnet) — flags wrong/redundant ARIA, missing labels, focus-trap omissions.
- A user-defined `kbd-nav-tester` (model: haiku) — generates Playwright tests that Tab through the page and assert focus order.
- `password-scrubber-agent` — sweep test fixtures.

### Prompt pattern
- "Read `accessibility/README.md`. Audit `<file>` against WCAG 2.2 AA. Output a markdown table: severity (blocker/major/minor), WCAG criterion, evidence (line + snippet), fix. Do not edit code. Limit to real violations — no `aria-label` advice for already-labeled `<button>`s."
- "Implement an accessible Combobox in React. Do **not** roll your own — use `@radix-ui/react-popover` + `cmdk` or React Aria. Include keyboard support: ArrowUp/Down, Home/End, Enter to select, Escape to close. Add `jest-axe` and Playwright keyboard tests."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `@axe-core/cli` | Headless axe over URLs | `npm i -g @axe-core/cli` |
| `pa11y` / `pa11y-ci` | Multi-URL CI runner | `npm i -D pa11y-ci` |
| `lighthouse` / `@lhci/cli` | Includes a11y category | `npm i -D @lhci/cli` |
| `jest-axe` / `vitest-axe` | Component-level axe in unit tests | `npm i -D jest-axe` |
| `@axe-core/playwright` | Per-page axe inside Playwright | `npm i -D @axe-core/playwright` |
| `accessibility-insights` (CLI) | Microsoft's pattern + needs-review report | https://accessibilityinsights.io |
| `IBM Equal Access Toolkit` | Custom rule engine | https://github.com/IBMa/equal-access |
| `wave` API | WebAIM WAVE checks via API | https://wave.webaim.org/api/ |
| `color-contrast-checker` (npm) | Programmatic ratio checks for tokens | `npm i color-contrast-checker` |
| `cypress-axe` | Cypress integration if you use Cypress | `npm i -D cypress-axe` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools / axe Monitor | SaaS / browser ext | Yes (CLI + REST) | Industry standard. |
| Tenon.io | SaaS | Yes (REST) | Per-URL audits. |
| Siteimprove | SaaS | Partial | Enterprise; less scriptable. |
| Stark | SaaS / Figma plugin | Limited | Design-time contrast + colorblind sims. |
| Accessibility Insights for Web | OSS | Limited | Excellent manual workflow; CLI exists. |
| Radix UI | OSS | Yes | Headless accessible primitives — use these in React. |
| React Aria / React Aria Components | OSS | Yes | Adobe's a11y primitives; keyboard + screen reader handled. |
| Reach UI (legacy) | OSS | Limited | Predecessor to Radix; only for older codebases. |
| WAVE (WebAIM) | SaaS | Yes (API) | Long-time community standard. |
| Assistiv Labs | SaaS | Limited | Real screen-reader testing in cloud. |

## Templates & scripts
See `templates.md`. Drop-in Playwright + axe smoke test for the top 10 routes:

```ts
// e2e/a11y.spec.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const ROUTES = ['/', '/login', '/dashboard', '/settings', '/pricing'];

for (const route of ROUTES) {
  test(`a11y: ${route}`, async ({ page }) => {
    await page.goto(route, { waitUntil: 'networkidle' });
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice'])
      .disableRules(['color-contrast-enhanced']) // AAA, optional
      .analyze();
    expect.soft(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([]);
  });
}
```

## Best practices
- Use **semantic HTML first**; reach for ARIA only to fill gaps the platform can't.
- Every `<input>` has a programmatic label (`<label htmlFor>` or `aria-labelledby`); placeholders are not labels.
- Visible focus on every interactive element; never `outline: none` without a `:focus-visible` replacement.
- Tab order matches visual order; if you reorder visually with CSS, fix the DOM, not `tabindex`.
- Skip-links to `<main>` on every page; they're cheap and they help.
- Maintain a single `<h1>` per page; don't skip heading levels.
- Live regions: use `aria-live="polite"` for status updates, `assertive` only for errors. Never both on the same node.
- Modals: trap focus, restore on close, `aria-modal="true"`, label the dialog, Escape closes.
- Forms: announce errors via `role="alert"` summary + `aria-describedby` on the input; focus the summary.
- Color contrast: 4.5:1 normal text, 3:1 large/UI; check on dark mode separately.
- Honour `prefers-reduced-motion` everywhere (framer-motion `useReducedMotion`, CSS media query).
- Test with keyboard only **and** with at least one screen reader (NVDA on Win, VoiceOver on macOS/iOS, TalkBack on Android).
- Treat axe failures as build failures via `lighthouse-ci` thresholds (`categories:accessibility >= 0.95`).
- Document a11y decisions in component READMEs (which keys do what, which patterns are followed).

## AI-agent gotchas
- LLMs over-ARIA: `role="button"` on `<button>`, `aria-label` duplicating visible text, `aria-required` on already-required inputs. Trim aggressively.
- Agents emit `<div onClick>` patterns easily; force `<button>` unless there's a real reason. Add a CSS rule + ESLint check.
- "alt text" generated by agents is generic ("image of a person"); reject if not contextual.
- Focus management is the #1 silent regression — agents add a route change but forget to move focus to the new heading.
- Agents skip keyboard handlers on custom widgets (combobox arrow keys, radio group arrow keys, tab list with `tabIndex={focusIndex===i ? 0 : -1}`). Force the WAI-ARIA Authoring Practices pattern.
- Live regions appended dynamically don't always announce — the region must be in the DOM **before** content is inserted.
- Agents add `aria-hidden="true"` on focusable elements, hiding them from screen readers but not from keyboards — guaranteed bug.
- Color contrast generators give one ratio, but agents forget to check **all** state combinations (hover, focus, disabled, error).
- Modal focus traps: agents trap forward Tab but not Shift+Tab; or they trap focus but never restore it on close.
- `prefers-reduced-motion`: agents add transitions everywhere then forget the media query.
- Server-rendered pages with later hydration: focus management bugs only appear on real navigation, not in unit tests. Always add E2E.
- Human-in-loop checkpoint: WCAG conformance claims (e.g. in marketing copy or VPATs) must be reviewed; agents will overstate compliance.
- Internationalization + a11y: when agents add a language switcher, they forget `<html lang>` updates and `dir="rtl"`/`ltr` toggling.

## References
- WCAG 2.2 quickref — https://www.w3.org/WAI/WCAG22/quickref/
- WAI-ARIA Authoring Practices (APG) — https://www.w3.org/WAI/ARIA/apg/
- A11y Project checklist — https://www.a11yproject.com/checklist/
- Inclusive Components (Heydon Pickering) — https://inclusive-components.design/
- Deque University — https://dequeuniversity.com/
- WebAIM — https://webaim.org
- Radix UI — https://www.radix-ui.com
- React Aria — https://react-spectrum.adobe.com/react-aria/
- APCA contrast — https://www.myndex.com/APCA/
- European Accessibility Act 2025 summary — https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/disability/union-equality-strategy-rights-persons-disabilities-2021-2030/european-accessibility-act_en
