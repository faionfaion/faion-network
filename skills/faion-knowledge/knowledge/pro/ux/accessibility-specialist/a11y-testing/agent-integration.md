# Agent Integration — Accessibility Testing Process

## When to use
- Pre-release WCAG 2.1/2.2 audit on a web product (manual + automated combined).
- CI gate for new pages/components — automated scan must pass before merge.
- Quarterly compliance review for ADA Title II / EAA-bound products.
- Procurement: generating VPAT/ACR evidence from real test runs.
- Triage: converting raw a11y issue dumps into prioritized remediation plan.

## When NOT to use
- Pure design-stage review — use `accessibility-first-design` instead (cheaper to fix in Figma).
- Native mobile-only flows — automated web tools (axe, Pa11y) don't cover XCUITest/Espresso a11y. Use platform-specific accessibility scanners.
- XR/spatial interfaces — WCAG doesn't fully cover them; use `spatial-accessibility` + W3C XAUR.
- One-off cosmetic contrast tweak — overkill, just run Colour Contrast Analyser locally.

## Where it fails / limitations
- Automated tools catch ~30-40% of WCAG issues (Deque benchmark). False sense of security if used alone.
- Screen reader testing cannot be reliably automated — LLM cannot "hear" NVDA/JAWS output without a recorded transcript.
- Headless axe-core misses focus order, reading order, meaningful alt text quality.
- Single-page apps with delayed render: scanners may snapshot before content paints. Need explicit `await` hooks.
- "Pass" on axe ≠ WCAG conformant — many criteria (1.3.1, 2.4.6, 3.3.3) need human judgment.

## Agentic workflow
Drive Steps 1, 2 (keyboard via Playwright), and 5 (issue triage/doc generation) with Claude subagents. Steps 3 (screen reader) and Step 4 (cognitive) require human-in-loop — agent prepares scripts and result templates but a tester executes. Pipeline: scanner agent → keyboard-bot → triage agent → report writer. Persist axe JSON between runs to track regressions.

### Recommended subagents
- `faion-sdd-executor-agent` — wrap remediation as SDD tasks once issues are categorized; quality-gate enforces WCAG criterion check before "done".
- General-purpose subagent driven by this methodology — runs axe-core + Pa11y, parses JSON, opens issues with WCAG criterion + code snippet.
- A "screen reader script writer" subagent — generates NVDA/VoiceOver test scripts (utterance expectations) for a human tester to execute.

### Prompt pattern
```
You are an a11y-testing agent. Run `axe --stdout --tags wcag2aa,wcag22aa $URL`,
parse JSON, group violations by WCAG criterion, attach the offending HTML
snippet (≤20 lines) and a fix recommendation. Output a markdown table sorted
by impact (critical → minor). Do NOT mark issues "passed" that axe couldn't
test (look at "incomplete" array).
```

```
Given this axe JSON + Pa11y JSON, deduplicate by selector+rule, map to
WCAG 2.2 AA criterion, assign priority {Critical, High, Medium, Low} per
README rubric, and write findings into the Audit Template.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `@axe-core/cli` | Headless axe scan, JSON output | `npm i -g @axe-core/cli`; https://github.com/dequelabs/axe-core-npm |
| `pa11y` / `pa11y-ci` | CI-friendly WCAG scanner, sitemap support | `npm i -g pa11y pa11y-ci`; https://pa11y.org |
| `lighthouse` | Audit incl. accessibility category | `npm i -g lighthouse` |
| `accessibility-insights` | MS scanner CLI + tab-stop validator | https://accessibilityinsights.io |
| `axe-playwright` / `jest-axe` | In-test a11y assertions | `npm i -D axe-playwright` |
| `cypress-axe` | Cypress integration | `npm i -D cypress-axe` |
| Colour Contrast Analyser | Pixel-sample contrast on any screen | https://www.tpgi.com/color-contrast-checker/ |
| `unified-doc-parse-pdf` + `pac-2024` | PDF a11y validation | https://pdfua.foundation/en/pdf-accessibility-checker-pac/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools Pro | SaaS | API + GitHub Action | IGT (Intelligent Guided Tests), bigger rule pack than OSS axe-core. |
| Siteimprove | SaaS | REST API | Site-wide crawl, monitors regressions, exports VPAT data. |
| Tenon.io | SaaS | REST API | Pure API a11y scanner — easy for agent loops. |
| Level Access (formerly eSSENTIAL) | SaaS | API | Enterprise audit + manual testing services. |
| Stark | Figma plugin / SaaS | Plugin only (no agent API) | Use during design phase. |
| Pa11y Dashboard | OSS | self-hosted, REST | Long-term tracking on multiple URLs. |
| Microsoft Accessibility Insights | OSS | CLI + extension | Free, includes guided manual checks. |
| Fable | SaaS (assistive tech user testing) | Human-in-loop | Connect to real disabled testers — agent cannot replace this. |

## Templates & scripts
See `templates.md` for the full Audit + Issue templates. Inline runnable scanner pipeline:

```bash
#!/usr/bin/env bash
# a11y-scan.sh URL [--ci]  → outputs reports/<host>/{axe.json,pa11y.json,lighthouse.json,summary.md}
set -euo pipefail
URL="${1:?url required}"
HOST=$(echo "$URL" | awk -F/ '{print $3}')
OUT="reports/$HOST"
mkdir -p "$OUT"
axe "$URL" --tags wcag2aa,wcag21aa,wcag22aa --stdout > "$OUT/axe.json" || true
pa11y --standard WCAG2AA --reporter json "$URL" > "$OUT/pa11y.json" || true
lighthouse "$URL" --only-categories=accessibility --output=json \
  --output-path="$OUT/lighthouse.json" --quiet --chrome-flags="--headless"
node -e '
  const fs=require("fs"),p=process.argv[1];
  const ax=JSON.parse(fs.readFileSync(p+"/axe.json")).violations||[];
  const pa=JSON.parse(fs.readFileSync(p+"/pa11y.json")).issues||[];
  const lh=JSON.parse(fs.readFileSync(p+"/lighthouse.json")).categories.accessibility.score;
  console.log(`# A11y summary\n- Lighthouse: ${(lh*100)|0}/100\n- axe violations: ${ax.length}\n- Pa11y issues: ${pa.length}`);
' "$OUT" > "$OUT/summary.md"
echo "Report → $OUT/summary.md"
```

## Best practices
- Always run BOTH axe AND Pa11y — their rule sets diverge on ~15% of issues; union catches more.
- Tag Playwright/Cypress tests with `@a11y-critical` and run on every PR; full crawl nightly only.
- Snapshot axe JSON per release in `reports/v<x.y>/axe.json` — diff against last release to catch regressions.
- For SPA: wait for `networkidle` AND a route-specific selector before scanning.
- Combine automated keyboard test (`page.keyboard.press('Tab')` loop, capture `:focus-visible`) with axe to cover focus order.
- Keep an "exempt" allowlist in repo (`a11y-exemptions.yml`) with WCAG criterion + reason + expiry — never silently ignore.
- Test with at least two screen readers per platform (e.g., NVDA+JAWS on Windows) — they diverge in ARIA interpretation.

## AI-agent gotchas
- **Don't trust "0 violations"** — always check axe `incomplete` and `inapplicable` arrays; "incomplete" means it gave up, not passed.
- LLM-rewritten alt text often invents content — clamp to what's literally visible/in surrounding text; require human approval for images of people, charts, diagrams.
- Headless Chrome reports different contrast than real device with OS-level color filters — sanity-check critical UI on hardware.
- Agent loop "fix until axe passes" can produce ARIA soup that breaks real screen readers. Limit to ≤3 auto-fix iterations and require AT regression test.
- Cookie banners/consent overlays distort scan results — dismiss them before measurement, log which cookie state you used.
- WCAG 2.2 added 9 new criteria (e.g., 2.5.7 Dragging Movements, 2.5.8 Target Size Min). Pin axe-core ≥ 4.8 to include them.
- Never let an agent close a a11y bug without linking to the WCAG criterion AND attaching pre/post screenshot — drift reviewers cannot audit otherwise.

## References
- WebAIM: Testing methodology — https://webaim.org/articles/testing/
- Deque: What axe doesn't catch — https://www.deque.com/blog/automated-testing-best-practices/
- W3C: Easy Checks (preliminary review) — https://www.w3.org/WAI/test-evaluate/preliminary/
- Microsoft Accessibility Insights — https://accessibilityinsights.io
- A11y Project Checklist — https://www.a11yproject.com/checklist/
- WCAG 2.2 quick reference — https://www.w3.org/WAI/WCAG22/quickref/
