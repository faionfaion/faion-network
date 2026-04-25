# Agent Integration — Testing with Assistive Technology

## When to use
- Pre-release accessibility QA for any public web/app — automated scans miss 50–70% of real issues.
- Validating WCAG 2.2 AA / EN 301 549 / ADA Title II conformance claims.
- Regression testing custom components (combobox, modal, tree, datagrid) where ARIA mistakes are easy.
- Investigating user complaints from screen-reader, switch-control, or keyboard-only users.
- Audit work for legal-risk reduction on B2C and government products.

## When NOT to use
- Pure backend / API services with no UI surface.
- Internal tools where the user population is known to not use AT (still test keyboard, but skip full SR sweep).
- Early-stage paper prototypes — methodology assumes interactive build.
- As a substitute for design-time accessibility (shift left; testing alone won't fix architectural a11y debt).

## Where it fails / limitations
- Screen reader behavior differs across SR + browser pairs (NVDA+Firefox vs. JAWS+Chrome vs. VoiceOver+Safari) — what works in one fails in another.
- Mobile SR (TalkBack, iOS VoiceOver) gestures need real devices; simulator parity is poor.
- Cognitive accessibility issues are invisible to SR/keyboard tests; you need separate user-with-disability sessions.
- Switch control, eye-gaze, and voice-control testing each need dedicated hardware setups.
- Automated tools score what they can reach; SPAs with delayed render or focus-trap bugs slip past.

## Agentic workflow
Agents can run automated scans in CI, cross-check ARIA against accessibility-tree snapshots, generate keyboard-traversal scripts, and triage findings into severity buckets. Real screen-reader audio cannot be evaluated by current LLMs reliably — capture it via human reviewer or video recording. Reserve human time for SR audio QA, switch-control, and lived-experience testing.

### Recommended subagents
- `faion-usability-agent` — runs automated suites (axe, pa11y, Lighthouse), cross-references findings, drafts remediation tickets.
- `faion-ux-researcher-agent` — recruits and runs sessions with screen-reader and keyboard-primary users.
- `faion-sdd-executor-agent` — fixes flagged issues with ARIA/semantic-HTML patches, then re-runs gates.

### Prompt pattern
```
Triage this axe-core JSON result.
Group by: {severity, wcag_criterion, component}.
For each violation:
  - Generate minimal repro (HTML snippet)
  - Suggest fix referencing WCAG 2.2 SC and ARIA APG pattern
  - Estimate scope: {single component | layout-wide | system}
Output JSONL.
```

```
You are scripting a keyboard-only walkthrough.
Component: <name>
List exact key sequence. For each step, expected:
  - visible focus state
  - SR announcement (NVDA + Firefox)
  - aria-live region behavior
Flag deviations as fail/warn/info.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` / `@axe-core/cli` | Industry-standard a11y rules, WCAG mapping | https://github.com/dequelabs/axe-core |
| `pa11y` / `pa11y-ci` | URL/site sweep, batch-friendly | https://pa11y.org |
| `lighthouse` (CI) | Includes Accessibility category | https://github.com/GoogleChrome/lighthouse |
| `playwright` + `@axe-core/playwright` | Component / user-flow a11y assertions | https://playwright.dev/docs/accessibility-testing |
| `cypress-axe` | a11y inside Cypress tests | https://github.com/component-driven/cypress-axe |
| `IBM Equal Access (achecker)` | Alternative ruleset, complements axe | https://www.ibm.com/able/toolkit/tools |
| `chrome-accessibility-tree` (DevTools Protocol) | Snapshot + diff a11y trees | Chrome DevTools |
| `nvda` (Windows) | Free SR for testing | https://www.nvaccess.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools / axe Auditor | SaaS | Yes (REST) | Best-in-class rule coverage; commercial tier needed for some rules. |
| WebAIM WAVE | SaaS + extension | Limited | Good visual report; weak API. |
| Tenon.io | SaaS | Yes (REST) | Solid CI integration. |
| AssistivLabs | SaaS | Limited | Real SR-on-cloud; manual sessions, not automation. |
| BrowserStack Accessibility | SaaS | Yes | Multi-AT cloud testing. |
| Sa11y | OSS | Yes | Lightweight in-page checker. |
| Pope Tech | SaaS | Yes | WAVE-based scanning at scale. |

## Templates & scripts
See `templates.md` for keyboard walkthrough sheet and SR test plan. Inline CI gate:

```bash
#!/usr/bin/env bash
# a11y-gate.sh — fail PR if axe finds any serious/critical issue
set -euo pipefail
URL="${1:?url}"
RESULT=$(npx @axe-core/cli "$URL" --tags wcag2aa,wcag22aa --exit 0 --stdout || true)
SERIOUS=$(echo "$RESULT" | jq '[.[].violations[]? | select(.impact == "serious" or .impact == "critical")] | length')
[ "$SERIOUS" -eq 0 ] || { echo "FAIL: $SERIOUS serious/critical a11y issues"; echo "$RESULT" | jq '.[].violations[]?' ; exit 1; }
echo "OK: no serious/critical issues"
```

## Best practices
- Three-tier test strategy: automated in CI (every PR), manual SR/keyboard sweeps (every release), user-with-disability sessions (quarterly).
- Maintain an SR + browser support matrix; pick 3 pairs and own them, don't try to cover all.
- Capture SR audio (OBS, screen recorder) for the bug reports — text descriptions get dismissed by devs.
- Test focus order with the browser dev-tools accessibility tree; visual order ≠ DOM order ≠ accessibility order.
- File a11y bugs with WCAG SC + repro + suggested ARIA pattern; vague tickets get postponed.
- Build a "regression catalog" — components with known a11y bugs get re-tested on every release.

## AI-agent gotchas
- LLMs invent ARIA patterns. Pin to ARIA Authoring Practices Guide URL per pattern; refuse output without citation.
- Automated tool output ≠ a passing site. Don't let an agent claim "WCAG AA conformant" from axe results alone.
- SR announcement strings vary across NVDA / JAWS / VoiceOver versions; agents quote outdated phrasings.
- Dynamic content (aria-live, route changes) is the #1 false-pass area. Force the agent to test post-state, not just initial render.
- Color-contrast checks fail on overlapping translucent layers; LLM static analysis misses this — must run in browser.
- "axe says no issues" → agent declares "fully accessible." Always reject that conclusion in prompt rules.

## References
- W3C, *WCAG 2.2 Recommendation*. https://www.w3.org/TR/WCAG22/
- W3C, *ARIA Authoring Practices Guide*. https://www.w3.org/WAI/ARIA/apg/
- Deque, *axe-core Rules*. https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- WebAIM, *Screen Reader User Survey* (current edition). https://webaim.org/projects/screenreadersurvey/
- ADA Title II final rule (2024) and EN 301 549 v3.2.1.
- Heydon Pickering, *Inclusive Components* (2018) — per-pattern accessibility guidance.
