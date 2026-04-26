# Agent Integration — WCAG 2.2 Compliance

## When to use
- Auditing or upgrading from WCAG 2.0 / 2.1 to 2.2 — focused work on the 9 new SC plus the 4.1.1 Parsing removal.
- Implementing the 2.2-introduced AA criteria most teams miss: 2.4.11 Focus Not Obscured (Min), 2.5.7 Dragging Movements, 2.5.8 Target Size (Min), 3.3.7 Redundant Entry, 3.3.8 Accessible Authentication.
- Drafting or reviewing acceptance criteria for new components against 2.2 AA.
- Future-proofing for ADA Title II April 2026 (currently 2.1 AA, 2.2 expected next).

## When NOT to use
- General-purpose a11y triage on a new codebase — start with `a11y-basics`.
- AT runtime testing — use `testing-with-assistive-technology`.
- Compliance paperwork / VPAT-ACR / region matrix — use `regulatory-compliance-2026`.
- XR / spatial — use `vr-design-patterns`, `ar-design-patterns`, `spatial-accessibility`.

## Where it fails / limitations
- Automated tools cover 2.2 partially: axe-core has rules for 2.5.8 (target size) and 2.4.11 partial; 2.5.7 (drag) and 3.3.x (auth) are mostly manual.
- 2.5.8 Target Size minimum is **24 × 24 CSS pixels** in WCAG 2.2 AA — not 44 × 44 (that's iOS HIG / 2.5.5 AAA). Agents conflate these.
- 4.1.1 Parsing is **removed** in 2.2 — automation that still reports it is stale.
- 3.3.8 / 3.3.9 Accessible Authentication are easy to misread: copy/paste enabled, password manager support, and passkeys are conformant; CAPTCHA puzzles fail.
- "Consistent Help" (3.2.6) requires *relative* order, not absolute pixels — agents over-specify.

## Agentic workflow
Treat 2.2 as a delta layer on top of 2.1. Agents run a 2.2-specific axe ruleset for what is automatable, then drive a structured manual checklist (drag alternatives, focus-obscuration scroll path, target sizes for each interactive element, redundant-entry across multi-step flows, auth without cognitive tests). Output is a per-criterion pass/warn/fail with selectors and remediation snippets. Pair with `wcag-22-compliance/checklist.md` for the human-driven items and `testing-with-assistive-technology` for keyboard/AT validation.

### Recommended subagents
- `faion-accessibility-specialist-agent` — audit per SC and produce remediation list with WCAG references.
- `faion-frontend-developer-agent` — apply fixes (autocomplete, paste, target sizing, drag alternatives).
- `faion-ux-ui-designer-agent` — design-token review for target sizes, focus indicators, sticky-header z-index conflicts.
- `faion-testing-developer-agent` — wire axe + custom rules into CI; gate on 2.2 AA.

### Prompt pattern
```
Role: WCAG 2.2 AA delta auditor.
Input: page or component + interaction list.
For each new SC (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) return
{status: pass/warn/fail, evidence (selector + scenario), fix snippet, WCAG link}.
Note 4.1.1 Parsing as DEPRECATED; do not report.
Validate target sizes against 24 CSS px AA threshold (not 44 px AAA).
```

```
Role: drag-alternative generator.
Given component <kanban card list>, output an accessible non-drag alternative
that meets 2.5.7: button-driven move (up/down/column-x), keyboard shortcuts,
visible affordance, ARIA live confirmation. Keep drag too. JSX + ARIA.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` ≥ 4.8 | WCAG 2.2 rules: target-size, focus-not-obscured (partial) | `npm i -D axe-core` |
| `axe-core/playwright` | Wire axe into Playwright tests | `npm i -D @axe-core/playwright` |
| `pa11y-ci` with `--standard WCAG2AA` | Headless scan; standard flag set to AA | `npm i -D pa11y-ci` |
| `Sa11y` | In-page editor a11y assistant for content | https://sa11y.netlify.app |
| `eslint-plugin-jsx-a11y` | React lints (target-size and focus visibility hints) | `npm i -D eslint-plugin-jsx-a11y` |
| `lighthouse-ci` ≥ 12 | Updated for some 2.2 rules | `npm i -D @lhci/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools / Auditor | SaaS + browser ext | Yes — REST | Best 2.2 coverage as it lands |
| TPGi ARC Toolkit | SaaS + browser ext | Partial — REST | Strong 2.2 manual guidance |
| WAVE | SaaS + browser ext | Limited | Adding 2.2 rules; UI-driven |
| Lighthouse | OSS | Yes — CLI | 2.2 partial; supplement with axe |
| SiteImprove | SaaS | Yes — REST | Tracks 2.2 conformance trend |
| Tota11y / Sa11y | OSS | Manual | Quick 2.2 spot checks |
| 1Password / Bitwarden / Apple Passwords | App | N/A | Test 3.3.8 — paste + autofill must work |

## Templates & scripts
See `templates.md` for the migration checklist (2.1 → 2.2). Inline target-size assertion that agents can drop into Playwright + axe:

```js
// tests/a11y/target-size.spec.js
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('WCAG 2.2 target-size minimum (24x24 CSS px AA)', async ({ page }) => {
  await page.goto('/');
  const r = await new AxeBuilder({ page })
    .withTags(['wcag22aa'])
    .withRules(['target-size'])
    .analyze();
  expect(r.violations, JSON.stringify(r.violations, null, 2)).toEqual([]);
});

test('No drag-only interactions (2.5.7)', async ({ page }) => {
  // Heuristic: every element with draggable=true must have a sibling button alternative.
  await page.goto('/board');
  const draggables = await page.$$eval('[draggable="true"]', els =>
    els.map(e => ({ tag: e.tagName, hasButtonAlt: !!e.parentElement.querySelector('button[data-move]') }))
  );
  const failing = draggables.filter(d => !d.hasButtonAlt);
  expect(failing).toEqual([]);
});
```

## Best practices
- Set `autocomplete="username"` and `autocomplete="current-password"` on auth fields; never block paste — it's a conformance failure under 3.3.8.
- Implement 2.5.7 as keyboard-button alternatives, not just keyboard drag — drag-and-drop with keys still excludes screen-reader users.
- For 2.5.8, prefer 24 × 24 CSS px minimum for tight UI but use 44 × 44 for primary mobile actions (good practice, not 2.2 AA requirement).
- Add `scroll-margin-top` to focusable elements when sticky headers are present — fixes 2.4.11 in one CSS line per layout.
- Replace image CAPTCHA with invisible (behavioral) or hCaptcha accessibility mode — meets 3.3.9 AAA cleanly.
- "Same as billing" pre-fill is the canonical 3.3.7 pattern — apply it to all multi-step forms.
- Audit consistent-help placement once, store in design-system docs — recurrence prevents 3.2.6 regressions.

## AI-agent gotchas
- Agents cite 44 × 44 px from older WCAG / iOS HIG; pin "WCAG 2.2 AA = 24 × 24 minimum" in prompts.
- LLMs add CAPTCHA "for security" without warning — flag any new auth flow with object/image recognition as 3.3.9 fail.
- Agents leave `autocomplete="off"` on password fields by reflex — explicit instruction needed.
- Drag alternatives generated as keyboard-drag (Space + arrows) only; require button-driven alt as well.
- "Help in the same place" misread as pixel-perfect; correct read is *relative* position in repeating page sections.
- 4.1.1 Parsing flagged as a current rule — agents trained on older data still report it. Strip from outputs.
- Human-in-loop checkpoints: auth flow review, drag-and-drop component, modal focus management with sticky headers, every multi-step form for 3.3.7.

## References
- W3C WCAG 2.2 Recommendation — https://www.w3.org/TR/WCAG22/
- W3C "What's New in WCAG 2.2" — https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
- Deque "WCAG 2.2 is here" — https://www.deque.com/blog/wcag-2-2-is-here/
- WebAIM WCAG 2.2 overview — https://webaim.org/articles/wcag22/
- TPGi WCAG 2.2 map — https://www.tpgi.com/wcag-2-2-all-new-success-criteria/
- WAI ARIA Authoring Practices Guide — https://www.w3.org/WAI/ARIA/apg/
