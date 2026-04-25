# Agent Integration — Accessibility Basics (a11y)

## When to use
- Onboarding a team or codebase to accessibility for the first time — POUR principles, WCAG levels, basic checks.
- Pre-launch sanity sweep on a small site or feature where full WCAG 2.2 conformance audit is overkill.
- Wiring CI to catch the obvious 30 % automated tools find: missing alt, label, contrast, heading order.
- Educating a new agent or developer before they edit UI — set expectations on POUR + manual + AT testing layers.

## When NOT to use
- Final compliance sign-off — use `wcag-22-compliance` and `regulatory-compliance-2026`.
- Real assistive-technology testing — use `testing-with-assistive-technology` (NVDA/VoiceOver/TalkBack flow).
- Procurement / VPAT-ACR generation — that lives in `regulatory-compliance-2026`.
- XR / spatial — see `vr-design-patterns`, `ar-design-patterns`, `spatial-accessibility`.

## Where it fails / limitations
- Automated scanners catch ~30 % of issues — the methodology says so explicitly. Agents will overweight scanner output.
- POUR is a teaching frame, not a checklist; treating it as a checklist produces shallow audits.
- Heuristics here are HTML-centric — native iOS/Android, desktop apps, kiosks need platform-specific guidelines.
- ARIA recommendations are easy to misapply ("first rule of ARIA: don't use ARIA"). Agents add ARIA aggressively and break semantics.

## Agentic workflow
Use as the on-ramp / triage layer: a fast agent runs `axe-core` + `pa11y` over routes, plus heuristic checks against the README's quick checklist (Tab path, 200 % zoom, alt text sanity, label binding, heading order). It produces a categorized issue list (perceivable / operable / understandable / robust), routes critical issues to fix-PR agents, and escalates anything ambiguous (ARIA, complex components, dynamic regions) to human accessibility review or to `testing-with-assistive-technology`.

### Recommended subagents
- `faion-accessibility-specialist-agent` — POUR-categorized triage and remediation suggestions.
- `faion-frontend-developer-agent` — apply fixes (alt, label, contrast, heading hierarchy, focus styles).
- `faion-testing-developer-agent` — wire `axe-core` / `pa11y-ci` / `lighthouse-ci` into CI; gate PRs on regressions.
- `faion-ux-ui-designer-agent` — design-token review for contrast, focus indicator, target size before code lands.

### Prompt pattern
```
Role: a11y triage.
Input: URL list or HTML snapshot.
Run conceptual checks against POUR: missing alt, unlabelled inputs, contrast <4.5:1
(text) / 3:1 (UI), heading skips, keyboard-only path broken, focus invisible,
duplicate IDs, language not set. Return JSON {issue_id, principle, severity:
critical/major/minor, selector, fix, wcag_ref}.
```

```
Role: 5-minute test runner.
Walk these routes: <list>. For each:
1) Tab from top → list focus path + first unreachable element.
2) Zoom 200 % → list reflow breakages.
3) Pick one img → critique alt text.
4) Pick one form → list label/aria-describedby gaps.
5) axe scan → report critical violations only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` | Programmatic a11y checks (in-browser, Node, Playwright, Puppeteer) | `npm i -D axe-core @axe-core/playwright` |
| `pa11y` / `pa11y-ci` | CLI runner over URLs, JSON output, CI integration | `npm i -D pa11y-ci` |
| `lighthouse-ci` | Aggregate perf + a11y + SEO with budgets in CI | `npm i -D @lhci/cli` |
| `axe-cli` | CLI-only axe runner | `npm i -g @axe-core/cli` |
| `wcag-zoo` | Heading-order + skip-link checks, simple Python | `pip install wcag-zoo` |
| `eslint-plugin-jsx-a11y` | Lint React/JSX for known a11y mistakes | `npm i -D eslint-plugin-jsx-a11y` |
| `eslint-plugin-vuejs-accessibility` | Same for Vue | `npm i -D eslint-plugin-vuejs-accessibility` |
| `headingsmap` (browser ext) | Manual heading-tree review | Chrome/Firefox stores |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools / Auditor | SaaS + browser ext | Yes — REST + CLI | Most accurate scanner; paid tiers expand coverage |
| WAVE (WebAIM) | SaaS + browser ext | Limited — UI-centric | Strong educational visualization |
| SiteImprove | SaaS | Yes — REST | Enterprise crawl + remediation tracking |
| Tenon | SaaS | Yes — REST | API-first scanner |
| Accessibility Insights for Web (Microsoft) | OSS | Partial — assessment-driven | Guided manual + automated |
| Pa11y Dashboard | OSS, self-host | Yes | Tracks scans over time |
| Tota11y | OSS bookmarklet | Manual | Visual overlay for first-pass review |

## Templates & scripts
See `templates.md` for the 5-minute and pre-commit checklists. Inline CI gate using axe + Playwright:

```js
// tests/a11y.spec.js — `npm exec playwright test tests/a11y.spec.js`
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const ROUTES = ['/', '/pricing', '/login', '/dashboard'];
for (const route of ROUTES) {
  test(`a11y: ${route}`, async ({ page }) => {
    await page.goto(route, { waitUntil: 'networkidle' });
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag22aa'])
      .analyze();
    const critical = results.violations.filter(v => v.impact === 'critical' || v.impact === 'serious');
    expect(critical, JSON.stringify(critical, null, 2)).toEqual([]);
  });
}
```

## Best practices
- Wire `axe-core` into PR CI early; failing PR is cheaper than a lawsuit.
- Lint with `eslint-plugin-jsx-a11y` (or framework equivalent) in editor — catch issues at type time.
- Build the team habit: every PR that touches UI runs the 5-minute manual test before review.
- Use semantic HTML first; reach for ARIA only when no semantic equivalent exists.
- Keep an a11y backlog separate from feature backlog — visible debt, owned, not buried.
- Train designers on contrast (4.5:1 text, 3:1 UI) and focus visibility — most bugs originate in design tokens.

## AI-agent gotchas
- Agents add `aria-label` to native elements that already have accessible names — duplicates and confuses screen readers.
- Agents recommend `role="button"` on `<div>` instead of using `<button>` — keyboard handlers go missing.
- Agents conflate WCAG levels (A vs. AA vs. AAA); pin "WCAG 2.2 AA" in every prompt.
- Color-contrast checks fail on text over images / gradients; agents miss this — escalate to manual review.
- Generated alt text from filenames is bad; require model to read surrounding context before authoring alt.
- Agents skip cognitive accessibility; explicitly include "plain language, predictable, error-prevention" in audit scope.
- Human-in-loop checkpoints: ARIA additions, custom-component patterns (combobox, tabs, modal), focus-management refactors, anything dynamic with live regions.

## References
- W3C WCAG 2.2 Quick Reference — https://www.w3.org/WAI/WCAG22/quickref/
- WebAIM intro to web accessibility — https://webaim.org/intro/
- The A11y Project checklist — https://www.a11yproject.com/checklist/
- Deque University (paid) — https://dequeuniversity.com/
- MDN Accessibility — https://developer.mozilla.org/en-US/docs/Web/Accessibility
- ARIA Authoring Practices Guide — https://www.w3.org/WAI/ARIA/apg/
