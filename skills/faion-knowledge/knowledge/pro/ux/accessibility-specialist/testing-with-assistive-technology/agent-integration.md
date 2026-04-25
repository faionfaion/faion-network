# Agent Integration — Testing with Assistive Technology

## When to use
- Verifying screen-reader and keyboard parity before release on web, iOS, Android, or Electron desktop apps.
- Catching the 30–50 % of issues automated tools miss (focus management, dynamic announcements, custom widget semantics).
- Reproducing user-reported a11y bugs with the exact AT and browser combination they use.
- Authoring step-by-step test cases agents can execute (where the AT is automatable) or a human can follow exactly.

## When NOT to use
- Pure first-pass scanning — start with `a11y-basics` and `axe-core` to remove easy issues before AT work.
- Compliance documentation / VPAT generation — that needs `regulatory-compliance-2026` plus AT findings as input.
- Native mobile UI design language reviews — separate from AT execution; AT here means VoiceOver/TalkBack runtime test.
- Fully automated AT-driven E2E without human verification — current screen-reader automation lies about announcements.

## Where it fails / limitations
- Screen-reader output is not directly capturable from headless browsers; most automation cheats by reading the accessibility tree, not the speech buffer.
- JAWS, NVDA, VoiceOver, TalkBack, Orca behave differently for the same DOM — testing one is not testing all.
- AT + browser pairings matter (NVDA + Firefox vs. NVDA + Chrome); a green run on one combo does not generalize.
- Mobile AT (VoiceOver iOS, TalkBack) gestures are model- and OS-version-specific; flaky in CI.
- Live-region timing is non-deterministic — agents fail to assert announcements reliably without polling.

### Tooling note: real speech vs. accessibility tree
Most "AT automation" tools (axe-core, Guidepup's tree introspection mode, Cypress a11y plugins) inspect the **accessibility tree** the OS/browser exposes, not the actual speech that NVDA/VoiceOver would produce. They miss bugs where the tree is correct but the screen reader announces nothing or announces something redundant. Real-speech automation requires `Guidepup` driving NVDA via screenshots or `voiceover-test` driving VO via AppleScript — both are slow and platform-locked.

## Agentic workflow
Drive AT testing as a tiered chain: a Playwright agent runs `axe-core` for tree-level coverage; a `Guidepup` agent (where supported) drives NVDA/VoiceOver and captures real speech output for a curated set of critical flows; a human accessibility tester runs the comprehensive 2–4 hour pass on full release candidates. The agent's job is to keep regressions cheap to detect, not replace expert testing. Always pair the test plan with a person who actually uses an AT daily for final sign-off.

### Recommended subagents
- `faion-testing-developer-agent` — author Playwright + axe and Guidepup scripts; integrate into CI.
- `faion-accessibility-specialist-agent` — write AT test cases per WCAG SC; review output for false positives.
- `faion-frontend-developer-agent` — fix focus management, ARIA states, live regions surfaced by AT runs.
- A human AT user (consultant or in-house) — required for sign-off on custom widgets and complex flows.

### Prompt pattern
```
Role: AT test-case author.
Input: feature spec + WCAG SC list.
For each AT (NVDA+Firefox, JAWS+Chrome, VoiceOver+Safari, TalkBack+Chrome
Android, VoiceOver iOS Safari) emit Gherkin test cases:
  Given <state>, When <user keystroke/gesture>, Then <expected announcement>.
Mark each "automatable" or "human-only".
```

```
Role: Guidepup test author.
Generate JS test that opens <url>, navigates by headings (H), then to a form,
fills it incorrectly, submits, and asserts the inline error is announced
within 1 s via aria-live="assertive". Use Guidepup NVDA driver. Fail-fast on
missing announcement.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `@guidepup/guidepup` | Drive NVDA + VoiceOver, capture real speech | `npm i -D @guidepup/guidepup` (https://www.guidepup.dev) |
| `@guidepup/playwright` | Guidepup wired into Playwright | `npm i -D @guidepup/playwright` |
| `axe-playwright` / `axe-puppeteer` | Tree-level checks alongside AT runs | `npm i -D @axe-core/playwright` |
| `pa11y` | Headless CLI scanner with Aria-Snapshot output | `npm i -D pa11y` |
| `voiceover-test` | macOS AppleScript wrapper for VO | https://github.com/AccessKit/voiceover-test |
| `aria-snapshot` | Capture accessibility tree to text for diffing | `npm i -D @testing-library/dom` (`logRoles`) |
| `accerciser` | Linux GTK/Orca a11y inspector | `apt install accerciser` |
| Xcode Accessibility Inspector | macOS / iOS native AT inspection | Bundled with Xcode |
| Android Accessibility Scanner | Android device-side scanner | Play Store |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| BrowserStack Accessibility | SaaS | Yes — REST + Playwright | Cross-browser AT runs in cloud, axe + automated Guidepup-style |
| Sauce Labs Accessibility | SaaS | Yes — REST | Similar; integrates with Sauce Insights |
| Deque axe Auditor | SaaS | Yes — REST | Combines automated + guided manual |
| Microsoft Accessibility Insights | OSS desktop | Partial | Guided assessment + automated checks |
| Fable Tech Labs | SaaS | Yes — managed program | Real disabled-user testing; agent prepares scripts only |
| Applause / UserTesting Accessibility | SaaS | Partial | Crowdsourced AT users; agent preps tasks |
| TestRail / Xray | SaaS | Yes — REST | Track AT test cases per WCAG SC |

## Templates & scripts
See `templates.md` for keyboard-navigation, screen-reader, and dynamic-content checklists. Inline Guidepup + Playwright test asserting an inline form error is announced via NVDA on Windows:

```js
// tests/at/nvda-form-error.spec.js (Windows runner)
const { nvdaTest } = require('@guidepup/playwright');
nvdaTest('NVDA announces required-email error', async ({ page, nvda }) => {
  await page.goto('https://example.test/signup');
  await nvda.perform(nvda.keyboardCommands.moveToNextHeading);  // H key
  await nvda.perform(nvda.keyboardCommands.moveToNextFormField); // F key
  await nvda.type('not-an-email');
  await page.keyboard.press('Enter');
  // wait for aria-live region to fire
  await page.waitForTimeout(1500);
  const phrases = await nvda.spokenPhraseLog();
  const heard = phrases.join(' | ').toLowerCase();
  if (!heard.includes('email') || !(heard.includes('invalid') || heard.includes('required'))) {
    throw new Error('Expected NVDA to announce email error. Got: ' + heard);
  }
});
```

## Best practices
- Anchor every AT test to a specific WCAG 2.2 Success Criterion — easier to triage and to defend in audit.
- Test pairs that real users actually use: NVDA+Firefox, JAWS+Chrome, VoiceOver+Safari, TalkBack+Chrome.
- Run keyboard-only and screen-reader passes separately — different bugs surface in each.
- Maintain a "known false positive" list; axe and pa11y misfire and noise destroys trust.
- Keep one small, fast AT smoke suite in PR CI; full run nightly or pre-release.
- Recruit at least one paid AT user for quarterly review — automation will not catch what a habitual user catches.
- Treat focus restoration after modal close as its own checklist line item; it's the most common regression.

## AI-agent gotchas
- Agents conflate accessibility-tree probes with real speech output — call out which mode each test uses.
- LLM-generated AT test cases assume single-page app behavior; multi-page navigation breaks focus expectations.
- Generated assertions like "screen reader will say 'invalid'" overspecify — assert on intent, not exact phrasing.
- Mobile AT gesture sequences hallucinate; copy from official Apple/Google docs.
- Agents miss the difference between `aria-live="polite"` vs `assertive` for error timing — require explicit choice and justification.
- `tabindex="0"` on non-interactive divs is suggested too easily — escalate to human.
- Human-in-loop checkpoints: every custom-widget pattern (combobox, tree, grid), live-region semantics, modal/dialog focus trap, mobile gesture coverage, final pre-release suite.

## References
- WebAIM screen-reader testing — https://webaim.org/articles/screenreader_testing/
- NVDA user guide — https://www.nvaccess.org/files/nvda/documentation/userGuide.html
- Apple VoiceOver guide — https://support.apple.com/guide/voiceover/welcome/mac
- Google TalkBack — https://support.google.com/accessibility/android/answer/6283677
- Guidepup docs — https://www.guidepup.dev
- ARIA Authoring Practices Guide — https://www.w3.org/WAI/ARIA/apg/
- Deque keyboard testing — https://www.deque.com/blog/keyboard-testing/
