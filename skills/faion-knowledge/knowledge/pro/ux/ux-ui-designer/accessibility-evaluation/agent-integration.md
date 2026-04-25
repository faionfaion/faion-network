# Agent Integration — Accessibility Testing Process

## When to use
- Pre-release WCAG 2.1/2.2 AA audit of a web app or marketing site before launch.
- Regression check after a design system upgrade, framework migration (e.g., Vue 2 → 3, Angular 14 → 17), or major refactor.
- Procurement / RFP response that requires VPAT or ACR documentation.
- Post-incident remediation when a user complaint or lawsuit names specific WCAG criteria.
- CI gating on PRs that touch components in a shared library (axe-core + Pa11y).

## When NOT to use
- Early sketch / lo-fi wireframe stage — defer to accessibility-first-design heuristics, not a full audit.
- For pure ATAG (authoring-tool) or UAAG (user-agent) compliance — different rule sets, this methodology assumes WCAG content/UI scope.
- For native iOS/Android — axe/WAVE rules do not apply; use Accessibility Inspector (Xcode) and Accessibility Scanner (Android) instead.
- For PDF or document accessibility — use PAC 2024, Adobe Acrobat Pro checker, or Grackle.

## Where it fails / limitations
- Automated tools catch only ~30-40% of issues (Deque, WebAIM 2024 figures); claiming "axe-clean = compliant" is the most common audit failure.
- ARIA misuse is invisible to most scanners until tested with a real screen reader; an LLM rendering DOM cannot judge announcement quality.
- Color-contrast tools fail on text over images / video / gradients — needs human spot check.
- Cognitive accessibility (1.3.5, 3.3.5, plain-language) is largely subjective; agents can flag candidates but cannot certify.
- Headless-browser scans miss focus order in modals, focus traps, and live-region behaviour without scripted interaction.

## Agentic workflow
Drive the audit as a five-stage pipeline: scan → triage → manual scripts → AT verification → report. Stage 1 (scan) and Stage 5 (report) are fully agent-owned; Stage 3 (keyboard) is scripted via Playwright; Stage 4 (screen reader) is human-in-the-loop because no LLM can replicate NVDA/JAWS/VoiceOver speech buffers reliably. Use one orchestrator subagent that fans out to a scanner subagent (axe + Pa11y JSON output), a triage subagent (de-dupe + WCAG mapping), and a writer subagent (markdown report against the template in `templates.md`). Treat each WCAG criterion as a separate test case with a stable ID so re-runs produce diffs, not full rewrites.

### Recommended subagents
- `faion-usability-agent` — orchestrator; owns the audit lifecycle and the `Accessibility Audit Report` template.
- `faion-sdd-executor-agent` — executes Playwright/axe-core scripts in CI; emits structured JSON.
- `password-scrubber-agent` — sanitises captured DOM snapshots before logging (forms with PII).
- A purpose-built `a11y-triage` subagent prompt: takes raw axe JSON + Pa11y JSON, deduplicates by selector + rule-id, maps to WCAG 2.2 SCs, and produces the `Findings by Principle` tables verbatim from `README.md`.

### Prompt pattern
"Given the attached axe-core JSON (`violations[]`), produce the `## Detailed Findings` section. For each violation: WCAG SC, priority (Critical/High/Medium/Low using the table in step 5), location (selector + page URL), recommendation (cite the matching technique from W3C/WAI), and a minimal HTML before/after. Group by Perceivable/Operable/Understandable/Robust."

"You have a Playwright trace of a keyboard-only walk-through. Emit a row in the keyboard-testing table for: Tab navigation, Focus visible, Logical order, Skip links, Traps, Shortcuts. Pass = boolean + evidence (frame index)."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| axe-core CLI | Headless WCAG scan, JSON output | `npm i -g @axe-core/cli` — https://github.com/dequelabs/axe-core-npm |
| Pa11y / Pa11y-CI | Batch URL audits, sitemap-driven | `npm i -g pa11y pa11y-ci` — https://github.com/pa11y/pa11y |
| Lighthouse CI | Accessibility category in CI | `npm i -g @lhci/cli` — https://github.com/GoogleChrome/lighthouse-ci |
| WAVE API | Page-level scan with screenshots | https://wave.webaim.org/api/ (paid) |
| IBM Equal Access Checker | Cross-platform CLI + browser | https://github.com/IBMa/equal-access |
| Playwright + `@axe-core/playwright` | Scripted scans tied to user flows | `npm i -D @axe-core/playwright` |
| color-contrast-checker | Token / palette validation in CI | `npm i color-contrast-checker` |
| html-validate | Catches role/aria errors statically | https://html-validate.org |
| accessibility-checker (npm) | Wrapper for IBM ruleset | `npm i accessibility-checker` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Deque axe DevTools Pro | SaaS | Yes (REST API + axe-core OSS) | Best false-positive rate; "Intelligent Guided Tests" require human |
| Siteimprove | SaaS | Partial (REST API) | Strong for large sites; expensive |
| Tenon.io | SaaS | Yes (REST API) | Lightweight scans, JSON only |
| Stark | SaaS / Figma plug-in | Limited (no REST) | Design-time contrast and vision sim |
| TPGi ARC Toolkit | SaaS | Yes (Selenium hooks) | Manual + automated, VPAT-friendly |
| BrowserStack Accessibility Testing | SaaS | Yes (CI integration) | Cross-browser real-device scans |
| AssistivLabs | SaaS | Partial | Remote NVDA/JAWS/VoiceOver — still human-driven |
| AccessiBe / UserWay | SaaS overlay | No — anti-pattern | Avoid; widely litigated, does not produce conformance |
| Evinced | SaaS | Yes (CLI + CI) | Component-level dynamic analysis |
| Microsoft Accessibility Insights | OSS desktop + Web | Yes (FastPass automatable) | Free, AI-assistant-readable HTML reports |

## Templates & scripts
See `templates.md` for the full `Accessibility Audit Report` and per-issue templates referenced from `README.md` step 5.

Inline runner (Playwright + axe; emits per-page JSON the triage agent consumes):

```javascript
// scan.mjs — node scan.mjs urls.txt out/
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const [, , urlsPath, outDir = 'out'] = process.argv;
mkdirSync(outDir, { recursive: true });
const urls = readFileSync(urlsPath, 'utf8').split('\n').filter(Boolean);
const browser = await chromium.launch();
for (const url of urls) {
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();
  const slug = url.replace(/[^a-z0-9]+/gi, '_');
  writeFileSync(join(outDir, `${slug}.json`), JSON.stringify(results, null, 2));
  await ctx.close();
}
await browser.close();
```

## Best practices
- Run scans on the **rendered DOM** of representative states (modal open, error, empty, loaded), not just the initial route — single-snapshot scans miss the majority of dynamic-content issues.
- Pin axe-core version per repo; rule additions between minor versions cause "phantom regressions" that derail review cycles.
- Map every finding to a WCAG SC and a remediation technique (G/H/F numbers from W3C); reviewers reject reports that just cite axe rule ids.
- Maintain a shared "known-issues" allowlist with expiry dates, not infinite suppressions; review quarterly.
- Combine NVDA + Firefox, JAWS + Chrome, VoiceOver + Safari in AT testing — pairings change announcement behaviour materially.
- Re-test the **fix** in the same flow that exposed it, not in isolation; refactors often re-break neighbouring components.
- For SPA frameworks, audit after route transitions and after async state changes — focus management is the #1 SPA failure.
- VPAT/ACR drafts: preserve evidence (screenshots, DOM snapshots, AT transcripts) so claims can be defended in procurement.

## AI-agent gotchas
- LLMs hallucinate "alt='Description'" placeholders that pass automated checks but fail 1.1.1 (decorative vs informative); always require the agent to cite the source content the alt is derived from.
- Agents that "fix" colour contrast by editing CSS variables can break dark-mode tokens; require diffs at the token layer with both modes regenerated.
- Headless scans of authenticated pages need session cookies — agents that scan logged-out fallback pages produce false negatives that look like clean reports.
- Agents tend to mass-add `aria-label` to elements that already have visible text → 2.5.3 (Label in Name) violations; lint for label/accessible-name mismatch.
- Screen-reader transcripts cannot be invented; if a subagent claims VoiceOver said X without an audio/text artifact attached, reject the finding.
- Do not let an agent close findings as "won't fix"; that decision belongs to a human accessibility lead with documented rationale.
- Pa11y and axe disagree on rule severity; the agent must pick one severity authority per audit and stick to it for the whole report.

## References
- WCAG 2.2 Recommendation — https://www.w3.org/TR/WCAG22/
- WAI-ARIA Authoring Practices 1.2 — https://www.w3.org/WAI/ARIA/apg/
- Deque "Automated Testing Best Practices" — https://www.deque.com/blog/automated-testing-best-practices/
- WebAIM Million 2024 Report — https://webaim.org/projects/million/
- W3C "Easy Checks" — https://www.w3.org/WAI/test-evaluate/preliminary/
- VPAT 2.5 (Rev 508) template — https://www.itic.org/policy/accessibility/vpat
