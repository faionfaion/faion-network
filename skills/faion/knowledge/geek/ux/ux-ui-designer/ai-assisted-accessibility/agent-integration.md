# Agent Integration — AI-Assisted Accessibility

## When to use
- Sprint cycle includes new UI components that must meet WCAG 2.2 AA before merge
- Accessibility audit is needed for an existing product with no prior testing baseline
- Team is small and cannot afford dedicated accessibility specialist; AI augments coverage
- Preparing a VPAT (Voluntary Product Accessibility Template) for enterprise procurement
- Video/audio content is being published and captions/audio descriptions are required (ADA Title II 2026)

## When NOT to use
- Treating AI overlay widgets as a substitute for fixing underlying code — overlays are not compliant solutions
- As the only testing method — AI tools catch 60-70% of automatable issues; the remaining 30-40% require human + assistive technology testing
- When user testing with people with disabilities has already been scheduled — do automated pass first, fix issues, then test with real users
- For complex interactive patterns (drag-and-drop, data grids, custom widgets) — AI scoring is unreliable; manual AT testing is required

## Where it fails / limitations
- Automated tools (including AI-enhanced ones) cannot assess cognitive accessibility, plain language, or reading level
- Color contrast checkers fail on gradient backgrounds and complex imagery — requires human review
- AI alt-text generation for complex charts/infographics is often too generic to be useful to screen reader users
- ARIA role validation requires runtime context; static analysis tools miss dynamic state changes
- False-negative rates on custom JavaScript widgets are high — AI flags standard HTML well, custom components poorly
- No AI tool generates a legally defensible VPAT without human review and sign-off

## Agentic workflow
A Claude subagent can run a multi-step accessibility audit pipeline: invoke axe-core or Lighthouse programmatically, parse the JSON output, prioritize issues by WCAG criterion and user impact, and generate a developer-facing remediation brief with code snippets. The agent should never mark issues as resolved — only humans or automated regression tests can close findings. For VPAT generation, the agent drafts the document; a human accessibility expert must review each criterion.

### Recommended subagents
- Custom a11y-auditor agent — runs `axe-core` via Playwright, parses results, generates prioritized issue list with fix suggestions
- `faion-sdd-executor-agent` — executes accessibility remediation tasks defined in an SDD implementation plan

### Prompt pattern
```
You are an accessibility engineer. Analyze the following axe-core JSON output:
<axe_results>{{axe_json}}</axe_results>

For each violation:
1. Map to the specific WCAG 2.2 success criterion (e.g., 1.4.3 Contrast)
2. Rate impact: critical / serious / moderate / minor
3. Provide a concrete code fix (before/after)
4. Flag any that require human AT testing to verify

Return as Markdown table + code blocks.
```

```
Draft a WCAG 2.2 AA conformance statement for this product:
Product: {{product_name}}
Test date: {{date}}
Known issues: {{issues_list}}

Format as a standard VPAT 2.5 summary section.
Flag all items that require human legal review before publishing.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` (via Playwright/Puppeteer) | Automated WCAG scanning with JSON output | npmjs.com/package/axe-core |
| `lighthouse` CLI | Chrome-based a11y + perf audit | `npm install -g lighthouse` |
| `pa11y` | Command-line a11y testing with multiple runner support | `npm install -g pa11y` |
| `wave-cli` | WAVE accessibility checker (limited CLI mode) | wave.webaim.org |
| `colour-contrast-checker` | CLI contrast ratio verification | npmjs.com/package/color-contrast-checker |
| `htmlcs` | HTML_CodeSniffer for WCAG rule checking | squizlabs.github.io/HTML_CodeSniffer |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools | SaaS | Yes — REST API + CLI | Industry standard; AI-powered false-positive reduction; enterprise scanning |
| Level Access | SaaS | Partial — API available | "Ask Level AI" chatbot for issue Q&A; enterprise VPAT generation |
| Accessibility Insights | OSS (Microsoft) | No API | Browser extension; excellent for manual testing; not agent-drivable |
| UserWay | SaaS | Yes — widget API | AI remediation suggestions; not a replacement for code fixes |
| Stark (Figma plugin) | SaaS | No API | Contrast + vision simulation in design phase; Figma-only |
| 3Play Media | SaaS | Yes — REST API | AI-enabled captions and audio descriptions; agent can submit video, poll for output |
| Siteimprove | SaaS | Yes — REST API | Continuous monitoring; good for regression detection in CI/CD |
| Equal Web | SaaS | Yes — JS API | AI overlay + scanning; use for scanning only, not remediation |

## Templates & scripts
See templates.md for VPAT draft structure and issue report template.

Inline: axe-core via Playwright runner for agent use:
```python
import subprocess, json, sys

def run_axe(url: str) -> dict:
    script = f"""
const {{ chromium }} = require('playwright');
const {{ default: axe }} = require('axe-core');
(async () => {{
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('{url}');
  await page.addScriptTag({{ path: require.resolve('axe-core') }});
  const results = await page.evaluate(() => axe.run());
  console.log(JSON.stringify(results));
  await browser.close();
}})();
"""
    result = subprocess.run(["node", "-e", script], capture_output=True, text=True)
    return json.loads(result.stdout)

if __name__ == "__main__":
    data = run_axe(sys.argv[1])
    violations = data.get("violations", [])
    print(f"Found {len(violations)} violations")
    for v in violations[:10]:
        print(f"- [{v['impact']}] {v['id']}: {v['description']}")
```

## Best practices
- Run automated scan first to clear low-hanging fruit, then do manual AT testing — don't reverse the order
- Set axe-core as a CI/CD gate; fail builds on `critical` or `serious` violations only to avoid alert fatigue
- Generate developer-facing briefs (not raw JSON) from audit tools — raw axe output is not actionable for most developers
- Test with actual screen readers (NVDA + Chrome, VoiceOver + Safari) for interactive components — no automated tool substitutes
- Keep VPAT drafts versioned alongside product releases — outdated VPATs create legal exposure
- Caption quality from AI tools degrades significantly for technical jargon, proper nouns, and non-English content — always human-review captions

## AI-agent gotchas
- Axe-core runs in a browser context; agents invoking it via Playwright must handle auth flows, cookie consent banners, and dynamic content loading — all of which interfere with scan results
- LLMs confidently produce incorrect WCAG criterion references (e.g., citing 1.4.3 for a keyboard issue) — always validate criterion mappings
- AI-generated alt text is generic and keyword-stuffed for SEO by default; prompt explicitly for descriptive, functional alt text
- Page-level scanning misses component-level violations in SPA frameworks where DOM is rebuilt on navigation — agents must trigger navigation events between scans
- Assistive technology behavior (NVDA, JAWS, VoiceOver) diverges significantly from automated tool predictions; never mark an AT-dependent issue resolved without AT verification

## References
- WebAIM Million Report 2026 — webaim.org/projects/million
- WCAG 2.2 specification — w3.org/TR/WCAG22
- Deque axe-core GitHub — github.com/dequelabs/axe-core
- ADA Title II Final Rule (video accessibility, 2026) — ada.gov
- Level Access "AI for Accessibility" white paper — levelaccess.com
- "Accessibility for Everyone" — Laura Kalbag, A Book Apart 2017
