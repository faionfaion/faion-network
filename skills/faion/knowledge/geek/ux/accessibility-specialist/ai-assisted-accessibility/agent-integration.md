# Agent Integration — AI-Assisted Accessibility

## When to use
- Running automated WCAG audits as part of a CI/CD pipeline before each deployment
- Generating alt text suggestions at scale for image-heavy content pipelines
- Producing draft VPAT/accessibility conformance reports from scan results
- Triaging a large backlog of accessibility issues by AI-assisted priority ranking
- Providing in-context fix suggestions to developers without switching tools
- Generating auto-captions for video content as a first pass before human review

## When NOT to use
- Replacing real user testing with people who use assistive technology — AI cannot substitute
- Accepting AI overlay widgets as an accessibility solution (they do not fix underlying code)
- Treating AI-generated alt text as final without editorial review for context, brand voice, and purpose
- Using AI scan results alone as proof of WCAG compliance for legal or procurement purposes
- Cognitive accessibility evaluation — AI tools have poor coverage here even in 2026

## Where it fails / limitations
- Automated scanning (even AI-enhanced) covers only 30–50% of WCAG 2.x success criteria
- False positive rate reduced but not eliminated (10–15% still noise) — human triage required
- Alt text generators describe image content but cannot determine why the image matters to the user
- Caption accuracy at AI-only level (80–90%) does not meet the 99% legal requirement — always add human review
- AI cannot evaluate keyboard navigation flow, logical reading order, or focus management reliably
- Cognitive inclusion (WCAG 2.2 SC 3.3.7/3.3.8) remains largely outside AI detection capability
- Overlay/widget AI "fixes" create new barriers for screen reader users — explicitly block from agent recommendations

## Agentic workflow
A Claude subagent (Haiku) triggers axe-playwright or pa11y in a headless browser, parses the JSON output, filters false positives by pattern, and ranks issues by user impact using a scoring prompt. A second Sonnet subagent generates code fix suggestions per issue, attaching them to the issue report. A third agent (Haiku) batches image alt text generation for new assets uploaded to a content pipeline. Human experts review ranked issues and validate fix suggestions before developer tickets are created.

### Recommended subagents
- General Claude subagent (Haiku) — automated scan execution and false-positive filtering
- General Claude subagent (Sonnet) — code fix suggestion generation and WCAG criterion explanation
- General Claude subagent (Haiku) — bulk alt text generation for image assets

### Prompt pattern
```
You are an accessibility engineer. Given the following axe-core JSON scan results,
filter out likely false positives (violations where the element role or context
makes the rule inapplicable), rank remaining issues by user impact (Critical/High/Med/Low),
and group related issues. Output a ranked issue list as JSON with fields:
id, wcag_criterion, impact, element_selector, description, suggested_fix.
```

```
Given this WCAG violation: [criterion] on element [selector] with code [snippet],
write a concrete code fix in [framework: React/HTML/Vue].
Explain why the fix satisfies the criterion in one sentence.
Provide one alternative fix if multiple approaches exist.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-playwright` | Headless WCAG scanning in CI | `npm install @axe-core/playwright` / github.com/dequelabs/axe-core-npm |
| `pa11y` | Lightweight CLI accessibility tester | `npm install -g pa11y` / pa11y.org |
| `pa11y-ci` | CI-integrated batch page scanning | `npm install -g pa11y-ci` / github.com/pa11y/pa11y-ci |
| `lighthouse-ci` | Performance + a11y scoring in CI | `npm install -g @lhci/cli` / github.com/GoogleChrome/lighthouse-ci |
| `jest-axe` | Unit-level accessibility assertions | `npm install jest-axe` / github.com/nickcolley/jest-axe |
| `eslint-plugin-jsx-a11y` | Static analysis for JSX accessibility | `npm install eslint-plugin-jsx-a11y` / github.com/jsx-eslint/eslint-plugin-jsx-a11y |
| `storybook-addon-a11y` | Component-level a11y testing in Storybook | `npm install @storybook/addon-a11y` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Deque axe DevTools Pro | SaaS | Partial — CLI + API | AI fix suggestions per issue; requires license |
| Evinced | SaaS | Yes — CI integration | AI-powered continuous scanning; REST API for issue data |
| Siteimprove | SaaS | Yes — REST API | Enterprise monitoring; AI trend analysis via API |
| Level Access | SaaS | Partial — chatbot | Ask Level AI for WCAG Q&A; no programmatic API |
| 3Play Media | SaaS | Yes — REST API | AI + human caption review pipeline; media upload API |
| Microsoft Azure Computer Vision | SaaS | Yes — REST API | Alt text generation from image bytes |
| Google Cloud Vision AI | SaaS | Yes — REST API | Object/scene detection for alt text generation |
| OpenAI GPT-4 Vision | SaaS | Yes — REST API | Contextual image description for alt text drafts |
| UserWay | SaaS | No (overlay) | Widget-based — not recommended for agent-driven fixes |

## Templates & scripts
See `templates.md` for the VPAT draft template and accessibility issue ticket template.

Inline script — CI accessibility gate using pa11y-ci:
```bash
#!/usr/bin/env bash
# Run pa11y-ci against a list of URLs, fail build on critical issues
set -euo pipefail

URLS_FILE="${1:-urls.txt}"
THRESHOLD="${2:-0}"  # 0 = fail on any critical error

pa11y-ci \
  --config .pa11yci.json \
  --threshold "$THRESHOLD" \
  $(cat "$URLS_FILE" | tr '\n' ' ')
```

`.pa11yci.json` config:
```json
{
  "standard": "WCAG2AA",
  "runners": ["axe", "htmlcs"],
  "ignore": ["WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail"],
  "chromeLaunchConfig": { "args": ["--no-sandbox"] }
}
```

## Best practices
- Integrate axe-playwright or pa11y-ci into the CI pipeline as a blocking gate for critical violations only — warnings go to the issue tracker
- Use AI fix suggestions as a starting point; require developer to understand and confirm the fix, not just apply it blindly
- For alt text generation: always include surrounding page context and image purpose in the prompt, not just the image file
- Caption review is non-negotiable for legal compliance — never publish AI-only captions for video content
- Scan new pages on every deployment, not just periodically — regressions appear silently
- Document which AI suggestions were accepted or rejected and why — creates a learning corpus for future fine-tuning
- Pair automated scanning with quarterly manual audits using real assistive technology (VoiceOver, NVDA, JAWS)

## AI-agent gotchas
- Agent must be explicitly instructed to skip overlay/widget fix suggestions — they are never an acceptable remediation
- axe JSON output can be large (>100 issues on poorly maintained pages) — chunk before sending to LLM to avoid context overflow
- Alt text agents hallucinate confident descriptions for images with ambiguous content — require explicit uncertainty markers in output
- Fix suggestions for dynamic/AJAX content are often incorrect — flag these for manual review rather than automated fix
- VPAT generation agents produce legally significant documents; always require human legal/compliance sign-off before publication
- Human-in-loop checkpoint: before developer tickets are created from AI-ranked issues, a human accessibility expert must validate the priority ranking

## References
- Deque axe-core: https://github.com/dequelabs/axe-core
- WebAIM evaluation tools: https://webaim.org/articles/tools/
- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- Overlay Fact Sheet: https://overlayfactsheet.com/
- pa11y: https://pa11y.org/
- Microsoft Accessibility Insights: https://accessibilityinsights.io/
