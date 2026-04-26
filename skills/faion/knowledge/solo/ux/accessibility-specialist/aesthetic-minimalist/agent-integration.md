# Agent Integration — Aesthetic and Minimalist Design

## When to use
- Auditing an existing UI for visual clutter before a redesign sprint
- Reviewing new feature additions to ensure they don't overload existing pages
- Conducting a content audit to identify remove/hide/keep candidates
- Evaluating dashboard and data-heavy screens where information overload is common
- Mobile-first simplification passes where screen real estate is constrained

## When NOT to use
- Data-dense tools (analytics dashboards, IDEs, spreadsheets) where density is a feature, not a bug
- First-pass feature discovery sessions — minimalism audits assume features already exist and need pruning
- When user research has not yet established which features are "rarely used" — guessing leads to removing the wrong things
- Branding or marketing contexts where visual richness drives emotion, not utility

## Where it fails / limitations
- "Remove everything" bias: agents applying this heuristic mechanically strip features that power users rely on
- Subjectivity of "noise": what looks decorative to an agent may convey brand trust to users
- Progressive disclosure can hide critical actions from new users, increasing support load
- Minimalism applied to forms often removes helpful hints and validation cues, increasing error rates
- Cannot substitute for actual task-completion data — a clean UI is not automatically a usable one

## Agentic workflow
A Claude subagent receives a page description or component list and runs a content prioritization pass: for each element it scores P1/P2/P3/Remove and outputs a structured audit table. A second agent reviews the audit against task-flow context to catch false positives (elements that look decorative but carry state or feedback roles). The output is a prioritized list of remove/hide/reorganize recommendations that a developer can execute without design tools.

### Recommended subagents
- `faion-sdd-executor-agent` — executes structured audit tasks from an implementation-plan task file
- General Claude subagent (sonnet) — runs content audit pass given element list + user task descriptions

### Prompt pattern
```
You are a UX auditor applying Nielsen's Heuristic #8 (Aesthetic and Minimalist Design).
Given the following list of UI elements on [page], classify each as P1 (essential), P2 (helpful),
P3 (rarely needed), or Remove. Output a markdown table with columns:
Element | Current role | User need | Priority | Action (Keep/Hide/Remove).
Do not remove elements without stating the task-flow impact.
```

```
Audit result summary prompt:
Given this content audit table, identify the top 3 candidates for removal and top 3 for
progressive disclosure. For each, state: (1) what user task is affected, (2) the risk of hiding it,
(3) the recommended interaction pattern (collapse, "More" menu, tooltip, separate settings page).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `axe-core` CLI | Automated accessibility + visual regression checks that catch contrast/layout regressions after simplification | `npm i -g axe-core` / https://github.com/dequelabs/axe-core |
| `lighthouse` | Audit for performance and best practices — confirms simplification didn't break UX metrics | `npx lighthouse <url>` / https://developer.chrome.com/docs/lighthouse |
| `unlighthouse` | Site-wide Lighthouse scan to find clutter outliers across pages | `npx unlighthouse` / https://unlighthouse.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Partial — Figma REST API reads file structure | Use API to count layers/components per frame as a clutter proxy metric |
| Maze | SaaS | No | Remote usability tests for first-click success after declutter; human required to interpret |
| FullStory / Hotjar | SaaS | No direct API | Heatmaps and click maps that reveal which elements users actually interact with — feeds audit data |
| Statsig / LaunchDarkly | SaaS | Yes (REST API) | Feature flags to progressively hide P3 elements and measure task-completion impact |

## Templates & scripts
See `templates.md` for the Content Audit template (element-by-element priority table).

Inline helper — count visible DOM elements on a page (Node.js / Puppeteer):
```javascript
// clutter-count.js — run with: node clutter-count.js <url>
const puppeteer = require('puppeteer');
const url = process.argv[2];
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });
  const counts = await page.evaluate(() => ({
    total: document.querySelectorAll('*').length,
    visible: [...document.querySelectorAll('*')].filter(el => {
      const s = getComputedStyle(el);
      return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0';
    }).length,
    images: document.querySelectorAll('img').length,
    buttons: document.querySelectorAll('button, [role="button"]').length,
    links: document.querySelectorAll('a').length,
  }));
  console.table(counts);
  await browser.close();
})();
```

## Best practices
- Always run a content audit before declaring a design "too cluttered" — gut feel is wrong more often than not
- Use feature-flag rollouts to hide P3 elements in A/B tests; measure task completion before permanent removal
- Progressive disclosure must guarantee the hidden action is findable via search or a predictable secondary location
- White space is earned by removing elements, not by increasing padding — padding on a cluttered layout is lipstick
- On mobile, apply a separate, stricter priority pass — not just a smaller version of the desktop audit
- Track "Help searches" and "support tickets" after a simplification push; a spike means you hid something essential

## AI-agent gotchas
- Agents tend to over-remove: without real usage data, they apply the heuristic too aggressively to anything that looks decorative
- "Decorative" classification is unreliable without design context — ask for the element's purpose before recommending removal
- Agents cannot run usability tests; any audit output must be treated as a hypothesis list, not a removal directive
- When generating audit tables, agents hallucinate usage frequency ("this is rarely used") — require agents to cite a source (analytics data, user research) or flag the claim as unverified
- Human checkpoint required before any removal is committed to production: agent produces the audit, human approves removals

## References
- https://www.nngroup.com/articles/aesthetic-minimalist-design/
- https://www.refactoringui.com/
- https://m3.material.io/foundations/layout/understanding-layout/overview
- https://developer.apple.com/design/human-interface-guidelines/layout
- Don Norman: The Design of Everyday Things (revised ed.)
