# Agent Integration — Aesthetic and Minimalist Design

## When to use
- Evaluating a finished or near-finished UI for visual noise and clutter before shipping
- Auditing a feature that has accumulated too many options after incremental additions
- Generating prioritized element-removal recommendations from a screenshot or design spec
- Pre-launch heuristic sweep as part of a broader usability review

## When NOT to use
- Data-dense tools (analytics dashboards, trading platforms, IDEs) where density is required
- Early exploration/wireframing phases — minimalism audits are premature without final content
- When the root problem is information architecture, not visual presentation
- As a substitute for actual user testing — agent opinions on "noise" are not user behavior data

## Where it fails / limitations
- Agents cannot reliably identify which elements users actually need without analytics or user research data
- "Remove" recommendations may conflict with legal, compliance, or accessibility requirements
- Minimalism judgments are context-dependent; what looks minimal for desktop feels sparse on mobile, and vice versa
- Agent has no access to session recordings, heatmaps, or scroll-depth data — can only analyze declared content

## Agentic workflow
A Claude subagent receives a list of UI elements (from a screenshot description, Figma JSON export, or HTML snapshot) plus the page's primary user task. It applies the content hierarchy (Primary / Secondary / Tertiary / Remove) framework from the README, outputs a scored element table, and returns remove/hide/keep recommendations with rationale. The agent should not auto-apply changes — it produces a recommendation report for designer review.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the audit task as a structured SDD step with documented output
- No specialized `faion-usability-agent` exists in the repo; use a general Claude subagent with the heuristic context loaded

### Prompt pattern
```
You are a UX auditor applying Nielsen's Heuristic #8 (Aesthetic and Minimalist Design).
Given the element list below, classify each as Primary / Secondary / Tertiary / Remove.
Return a markdown table: Element | Classification | Rationale | Recommended Action.
Do not suggest removing elements flagged as required by accessibility or legal requirements.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Lighthouse | Accessibility + performance audit (indirectly catches visual bloat via render cost) | `npm install -g lighthouse` / https://developer.chrome.com/docs/lighthouse |
| axe-core CLI | Flags redundant/hidden elements that still exist in DOM (clutter at markup level) | `npm install -g @axe-core/cli` / https://github.com/dequelabs/axe-core |
| Puppeteer | Headless screenshot for agent input | `npm install puppeteer` / https://pptr.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma API | SaaS | Yes (REST) | Export component tree for element enumeration; token scoped per project |
| Screaming Frog | SaaS/desktop | Partial | CLI mode exports element counts per page; feed to agent for density analysis |
| PageSpeed Insights API | SaaS (free) | Yes | Returns DOM element count; high count correlates with visual clutter |
| Heap / FullStory | SaaS | No direct agent API | Export interaction data manually; feed as CSV context to agent |

## Templates & scripts
See `templates.md` for the Content Audit table template (Element / Purpose / User Need / Priority / Action). Below is a minimal script that extracts visible text node count from a URL for a density proxy:

```bash
#!/usr/bin/env bash
# density-check.sh — count visible DOM elements on a page
# Usage: bash density-check.sh https://example.com/page
URL="${1:?Usage: $0 <url>}"
npx puppeteer-cli screenshot "$URL" /tmp/page-snap.png 2>/dev/null
node - <<'JS'
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto(process.argv[2] || process.env.URL);
  const count = await page.evaluate(() =>
    document.querySelectorAll('body *:not(script):not(style)').length
  );
  console.log('Visible DOM nodes:', count);
  await browser.close();
})();
JS
```

## Best practices
- Always define the page's single primary task before starting the audit — everything is classified relative to that task
- Use progressive disclosure for tertiary content rather than removal when regulatory or power-user access is required
- Validate removal recommendations against analytics (page views, click rates) before implementing
- Apply the audit on the mobile viewport first — mobile forces honest prioritization decisions
- Separate "visual clutter" (decoration, redundant labels) from "information density" (data tables, code) — they need different solutions
- Re-run the audit after each major feature addition as a lightweight regression check

## AI-agent gotchas
- Agent cannot see actual visual rendering — it works from element lists or HTML; provide enough context (element type, label text, position) to make useful judgments
- Without usage data, the agent will over-recommend removal of infrequently-named but critical edge-case actions (e.g., "export as PDF")
- Human-in-loop checkpoint required before any remove/hide action ships: designer must validate each recommendation against product requirements
- Agent may flag accessibility-required elements (skip links, ARIA landmarks) as "visual noise" — always cross-check against accessibility audit
- Stateful UI (tabs, accordions, modals) is invisible to static snapshots; ensure agent receives all states, not just the default view

## References
- https://www.nngroup.com/articles/aesthetic-minimalist-design/
- https://www.refactoringui.com/ (Refactoring UI by Tailwind CSS authors)
- https://m3.material.io/foundations/layout/understanding-layout/overview
- https://developer.apple.com/design/human-interface-guidelines/layout
- Don Norman, *The Design of Everyday Things* (revised ed.)
