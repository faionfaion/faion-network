# Agent Integration — WCAG 2.2 Compliance

## When to use
- Validating a web product against WCAG 2.2 AA — the global baseline by 2025/2026.
- Adding a CI gate that flags new violations of the nine WCAG 2.2 success criteria added on top of 2.1.
- Auditing focus visibility, target size, dragging, accessible authentication, redundant entry, consistent help.
- Preparing VPAT 2.5 / ACR conformance documentation.

## When NOT to use
- Native mobile-only apps without web surfaces — defer to platform a11y APIs (UIAccessibility, Android a11y).
- Internal tooling with a documented narrow user pool that does not include disabled users (rare; document the decision).
- WCAG 3.0 silver-bullet conversations — 3.0 is still working draft; do not retire 2.2 baselines.
- Pure visual design review — heuristics and cognitive walkthrough cover that better.

## Where it fails / limitations
- Automated scanners catch ~30-40% of WCAG issues; manual + assistive-tech testing still required.
- "Accessible Authentication (Min)" and "Consistent Help" need cross-page reasoning — single-page scanners miss them.
- "Focus Not Obscured" depends on z-index / sticky headers at runtime — needs viewport + keyboard simulation.
- Drag alternatives often added as hidden controls that fail "discoverability" — passes scanner, fails users.
- Target size 24x24 CSS px is computed including spacing exception — agents misread the SC.

## Agentic workflow
Use a subagent to run axe-core / Pa11y / Lighthouse on each route, parse violations, and triage them against WCAG 2.2 SC IDs. A second agent walks new SCs (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8, 3.3.9) by writing Playwright keyboard scripts that inspect focus rect, target size, drag alternatives. A human reviews authentication and help-consistency findings.

### Recommended subagents
- `faion-usability-agent` — manual SC evaluation, screen-reader walk-throughs.
- `faion-sdd-executor-agent` — patches code, adds CI a11y gates, runs axe in Playwright.
- `faion-ux-researcher-agent` — recruits AT users for validation.

### Prompt pattern
```
For SC <id>, write a Playwright script that: navigates to <url>,
focuses each interactive element, captures the focus bounding box,
checks against viewport-visible region. Report any element where
the focus indicator overlaps less than 100% with viewport.
```

```
Given axe-core JSON output, group violations by WCAG 2.2 SC.
List which are 2.2-new (2.4.11, 2.4.12, 2.4.13, 2.5.7, 2.5.8,
3.2.6, 3.3.7, 3.3.8, 3.3.9) vs 2.1-carryover. Suggest minimal CSS
or HTML fix for each.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` / `@axe-core/cli` | Rule engine, ~57% of WCAG covered | `npm i -g @axe-core/cli`; deque.com/axe |
| `pa11y` / `pa11y-ci` | Headless WCAG scan, CI-friendly | `npm i -g pa11y-ci`; pa11y.org |
| Lighthouse CI | Full audit incl. a11y subset | `npm i -g @lhci/cli` |
| `nu html-validator` | Catches HTML errors that break a11y trees | validator.github.io/validator |
| `wcag-em-report-tool` | W3C evaluation report builder | github.com/w3c/wcag-em-report-tool |
| `playwright` + `@axe-core/playwright` | Stateful, route-by-route a11y in CI | playwright.dev |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Deque axe DevTools | SaaS+OSS | Yes — REST API, axe-core CLI | Pro tier adds Intelligent Guided Tests for 2.2 SCs. |
| Siteimprove | SaaS | Yes — REST API for crawl results | Enterprise-grade tracking. |
| Tenon.io | SaaS | Yes — REST API | Strong color-contrast logic. |
| Stark | SaaS plugin | Partial — Figma plugin first, API for some plans | Good for design-time checks. |
| TPGi ARC | SaaS | Yes — REST API | Manual + automated hybrid. |
| Equally AI / accessiBe | SaaS overlay | No — overlays often regress UX | Avoid; not a substitute for fixes. |

## Templates & scripts
See `templates.md` for VPAT shells. Inline 2.2-aware Playwright check:

```js
import { test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("WCAG 2.2 AA — focus not obscured (2.4.11)", async ({ page }) => {
  await page.goto("/checkout");
  const all = page.locator("button, a, input, select, textarea, [tabindex]");
  for (let i = 0; i < (await all.count()); i++) {
    const el = all.nth(i);
    await el.focus();
    const box = await el.boundingBox();
    if (!box) continue;
    const visible = await page.evaluate(b => {
      const r = { top: 0, left: 0, bottom: innerHeight, right: innerWidth };
      return b.top >= r.top && b.bottom <= r.bottom;
    }, box);
    if (!visible) throw new Error(`Focus obscured on element ${i}`);
  }
  const results = await new AxeBuilder({ page }).withTags(["wcag22aa"]).analyze();
  if (results.violations.length) throw new Error(JSON.stringify(results.violations, null, 2));
});
```

## Best practices
- Run automated scans on every PR; fail on any new 2.2 SC violation, warn on existing.
- Pair each automated check with one human AT walkthrough per release on top user flows.
- Document focus styles in tokens (`--focus-ring-width`, `--focus-ring-color`) so 2.4.11/12/13 stay consistent.
- For drag interactions, ship the non-drag alternative first; add drag as enhancement.
- Keep "Help" link in identical position site-wide (3.2.6) — usually footer or persistent header.
- Test authentication with no copy/paste, no autofill — many "captcha" patterns now fail 3.3.8/9.

## AI-agent gotchas
- LLMs assume "accessible" means "alt text added"; 2.2 is mostly about interaction quality.
- Agents miss focus-indicator regressions caused by `outline: none` in design tokens — lint for this.
- `aria-hidden` and `inert` get over-applied; agents must verify keyboard reachability after applying.
- Color-contrast checks fail on gradients and images-of-text — agents need pixel sampling, not CSS reads.
- Target-size SC: agents must include the spacing exception; otherwise they over-report icon buttons.
- Never let an agent ship an "overlay/widget" as a fix — flag and refuse.

## References
- WCAG 2.2 Recommendation — w3.org/TR/WCAG22/
- "What's new in WCAG 2.2" — w3.org/WAI/standards-guidelines/wcag/new-in-22/
- Deque, "Achieving WCAG 2.2 conformance" — deque.com/blog/whats-new-in-wcag-2-2/
- TPGi, "Understanding the new SCs" — tpgi.com/wcag-2-2-and-what-it-means-for-you/
- VPAT 2.5 templates — itic.org/policy/accessibility/vpat
- Axe-core 2.2 ruleset — github.com/dequelabs/axe-core
