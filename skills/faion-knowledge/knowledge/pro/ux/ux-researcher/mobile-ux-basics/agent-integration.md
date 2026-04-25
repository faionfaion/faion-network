# Agent Integration — Mobile UX (Basics)

## When to use
- Auditing an existing mobile experience: thumb-zone, touch-target, performance, and platform-convention compliance in one sweep.
- Pre-launch checklist enforcement before each mobile release: gates on Lighthouse mobile score, accessibility, touch-target sizes.
- Code review for mobile-affecting PRs: agent flags violations (small touch targets, hidden navigation, blocking JS, missing input types).
- Cross-platform parity reviews: same flow on iOS vs Android — list of platform-convention divergences.

## When NOT to use
- Greenfield strategic mobile design — start with research methods (interviews, diary studies) not basics; this knowledge is downstream.
- Native-only platform-specific work where Apple HIG / Material 3 are the primary references — load those directly.
- Single-component visual polish — that's UI/visual design feedback, not mobile-UX methodology.

## Where it fails / limitations
- Static analysis cannot catch contextual issues (one-handed use during commute, glove use, sun glare, low-vision settings).
- LCP/FID/CLS measured in Lighthouse lab differ from CrUX field data; lab-passing builds can still fail real-user metrics.
- Touch-target measurement on responsive sites depends on render breakpoints — agents must run multiple viewport sizes, not just one default.
- The README mixes design principles and design-system specifics; agents drawing rules from it must distinguish "must-have" (touch target ≥44pt) from "consider" (bottom nav for 3-5 items).
- Recommendations stale fast: iOS 18 / Material 3 Expressive shifted several patterns (dynamic island, predictive back, bottom-bar collapsing).

## Agentic workflow
Run as a CI-integrated audit: a static-analysis agent parses HTML/Flutter/React Native/SwiftUI source for touch-target sizes, input types, navigation patterns, and gesture handlers; a dynamic-analysis agent runs Lighthouse + Playwright at multiple mobile viewports producing perf + accessibility reports; a synthesis agent reconciles findings into a prioritized issue list keyed to the mobile-UX checklist. Human reviewers triage P1 issues; agents auto-file P2/P3 as tickets.

### Recommended subagents
- `faion-ux-researcher-agent` — owns the checklist, performs heuristic-style review.
- `faion-frontend-developer` (from `solo/dev/frontend-developer`) — translates UX findings into specific code changes (CSS, component props, breakpoints).
- `faion-accessibility-specialist` (from `pro/ux/accessibility-specialist`) — runs WCAG + mobile-AT-specific checks (VoiceOver, TalkBack rotor).
- `faion-cicd-engineer` — wires Lighthouse + axe + Playwright budgets into PR gates.
- `faion-conversion-optimizer` — analyzes mobile funnel drop-off vs UX issues.

### Prompt pattern
Source review:
```
Component source: {tsx_or_swift_or_kotlin}
Viewport context: 360x640 mobile.
Check: touch targets ≥44x44pt, input types appropriate to data type, no hover-only affordances, primary actions in thumb zone (lower 1/3), no horizontal overflow.
Output JSON list of {issue, severity, line, fix_hint}.
```
Funnel + UX correlation:
```
GA4 funnel by device: {funnel_json}
UX audit findings: {audit_json}
Map drop-off steps to UX findings. Output: step, drop_rate, candidate UX cause, evidence_link.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `lighthouse` / `lhci` | Mobile perf + a11y + best-practices scoring | `npm i -g @lhci/cli lighthouse` |
| `axe-core` (`@axe-core/cli`) | A11y violation detection at multiple viewports | `npm i -g @axe-core/cli` |
| Playwright | Multi-viewport, multi-device emulation | `npm i -D @playwright/test` |
| `webhint` | Best-practice scanner (pwa, perf, a11y) | `npm i -g hint` |
| Chrome DevTools Protocol (CDP) | Custom audits (touch-target measurement, thumb-zone heatmap) | https://chromedevtools.github.io/devtools-protocol/ |
| `react-native-debugger` / `flipper` | Native-app inspection | https://github.com/jondot/awesome-react-native#debugging |
| Xcode `xcrun simctl` | iOS simulator automation | bundled with Xcode |
| `adb` | Android device automation | Android SDK platform tools |
| `pa11y-ci` | Accessibility CI gate | `npm i -g pa11y-ci` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Lighthouse CI Server | OSS | Yes | Self-hosted perf budgets per branch |
| BrowserStack / Sauce Labs | SaaS | Yes — APIs | Real-device cloud testing |
| Firebase Test Lab | SaaS | Yes — gcloud CLI | Android device farm; pricing-friendly |
| WebPageTest | SaaS + OSS | Yes — REST API | Real-network mobile testing (3G Slow, Edge) |
| CrUX (Chrome UX Report) | SaaS | Yes — BigQuery + REST | Field metrics from real users |
| SpeedCurve | SaaS | Yes — API | Continuous mobile perf monitoring |
| Maze + Lookback | SaaS | Yes | Mobile usability sessions on real devices |
| App Store Connect / Play Console | SaaS | Yes — APIs | Crash + ANR data correlated with UX |

## Templates & scripts
See `templates.md` for the mobile audit checklist. Touch-target violation scanner via Playwright:

```javascript
// touch-target-audit.js — flag tap targets <44x44 in a rendered page at mobile viewport
const { chromium, devices } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ ...devices['iPhone 13'] });
  const page = await ctx.newPage();
  await page.goto(process.argv[2]);
  const small = await page.$$eval(
    'a, button, [role="button"], input[type="submit"], [onclick]',
    els => els.map(el => {
      const r = el.getBoundingClientRect();
      return { tag: el.tagName, text: (el.innerText||'').slice(0,40),
               w: r.width, h: r.height,
               tooSmall: r.width < 44 || r.height < 44 };
    }).filter(e => e.tooSmall)
  );
  console.log(JSON.stringify(small, null, 2));
  await browser.close();
})();
```

## Best practices
- Run audits at three viewports minimum: 360x640 (small Android), 390x844 (iPhone), 768x1024 (tablet). Single-viewport audits miss responsive breakpoint bugs.
- Treat Core Web Vitals targets (LCP <2.5s, INP <200ms, CLS <0.1) as PR-blocking budgets, not aspirations.
- Test on a Slow-3G throttle profile in Lighthouse; the median real-world mobile connection is closer to slow-3G than to fast-4G.
- Verify `inputmode` and `autocomplete` attributes on form fields — these are the highest-leverage 5-minute mobile fixes available.
- Check thumb-zone reachability dynamically: primary CTA position relative to viewport bottom matters more than absolute pixel coordinates.
- Reduced-motion respect: agents should grep for `prefers-reduced-motion` queries and flag missing handling on animation-heavy components.
- Always cross-reference Apple HIG and Material 3 specs directly when platform conventions are at stake — README is generic.

## AI-agent gotchas
- Headless browsers don't render `:hover`, `:active`, or `prefers-color-scheme: dark` realistically. Run audits with explicit emulation flags, not defaults.
- Lighthouse scoring is non-deterministic on flaky networks; use median-of-3 runs in CI before failing a PR.
- Touch-target measurement misses elements with hit-area expanded via `::before` pseudo-elements or padding tricks. Pair geometric measurement with manual spot-check.
- Native (iOS/Android/RN/Flutter) source analysis requires platform-specific subagents; a generic web-trained agent will misread `Pressable` props or `UIButton` configuration.
- LLM-generated mobile recommendations frequently cite outdated patterns (e.g., "use a hamburger menu") that current research shows underperform. Cross-check against NNg's recent mobile-nav research.
- Performance and UX findings get conflated in reports; keep them in separate sections — fixes have different owners (frontend vs platform vs design).
- Field data (CrUX, RUM) and lab data (Lighthouse) should both appear in reports; agents that only ship lab numbers create false confidence.

## References
- Apple — Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Google — Material Design 3: https://m3.material.io/
- Nielsen Norman Group — Mobile UX: https://www.nngroup.com/articles/mobile-ux/
- Wroblewski, Luke — *Mobile First* (A Book Apart)
- Hoober, Steven — *Touch Design for Mobile Interfaces*
- web.dev — Core Web Vitals: https://web.dev/vitals/
- Chrome DevRel — INP guidance: https://web.dev/articles/inp
