# Agent Integration — Cognitive Walkthrough: Basics

## When to use
- Pre-launch usability inspection of an onboarding flow, signup, or first-run experience where no users are available yet.
- Evaluating clickable prototypes (Figma, Framer, deployed staging) for learnability before investing in moderated usability testing.
- Reviewing AI-generated UI from a design-to-code tool against the four-question framework before merging to main.
- Onboarding-flow regressions in CI: a vision-capable agent walks the latest preview build and flags new Q2/Q3/Q4 failures.

## When NOT to use
- Expert-user efficiency tasks (power-user shortcuts, dashboards). Use heuristic evaluation or quantitative testing.
- Highly subjective aesthetic decisions; the four questions don't catch visual hierarchy issues well.
- When you have real users available — actual usability testing always beats inspection.
- Static brand/marketing pages with no task flow — there are no "steps" to walk through.

## Where it fails / limitations
- Agent's "first-time user" simulation is a fiction. LLMs have implicit prior knowledge of every common UI pattern, so they almost never fail Q2 ("notice action") on familiar buttons.
- Q3 ("associate action with effect") depends on cultural/domain mental models the LLM may not represent for the actual target persona (e.g., elderly users, B2B-finance users).
- Q4 ("see progress") requires observing the live UI response, not just the static screen — purely-screenshot agents miss missing loaders and silent failures.
- Inspection methods systematically miss issues that only emerge from real human distraction, fatigue, or low motivation.

## Agentic workflow
Treat each task-step as a self-contained unit: feed the agent (a) the persona description, (b) a screenshot of the current screen, (c) the intended next action. The agent answers Q1-Q4 with Yes/No/Partial plus evidence and a one-line fix. Run one screen at a time to keep context focused. A second `meta-reviewer` agent then ranks issues by severity and produces the summary report. Keep a human checkpoint before fixes are filed as tickets — agents over-flag minor wording.

### Recommended subagents
- `cog-walk-evaluator` — stateless per-step evaluator; takes persona + screenshot + intended action, returns Q1-Q4 JSON with citations. Sonnet-class with vision.
- `severity-ranker` — converts raw Q1-Q4 outputs into prioritized issue list (High/Med/Low) using the action's criticality and frequency.
- `persona-keeper` — single-paragraph persona file injected into every evaluation prompt to prevent drift toward expert mental models.

### Prompt pattern
```
You are evaluating ONE step of a user task using the Cognitive Walkthrough method.

Persona: <<<one-paragraph first-time user persona>>>
Goal: <<<task goal>>>
Step <N> action: <<<exact intended action>>>
Screen: <attached image>

Answer ONLY in JSON: {q1:{ans:"yes|no|partial", evidence:""},
q2:{...}, q3:{...}, q4:{...}, suggested_fix:""}.
For each "no" or "partial", evidence MUST quote a visible UI element or explicitly state what is missing.
Do not assume capabilities the persona lacks.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` | Drive a browser, capture per-step screenshots into the agent | `npm i -D @playwright/test` |
| `puppeteer` | Lighter alternative for static walks | `npm i puppeteer` |
| `gh issue create` | File each "No" finding as a tracked ticket | `gh` CLI |
| `axe-core` (`@axe-core/cli`) | Run alongside cog walk for a11y issues Q2 misses | `npm i -g @axe-core/cli` |
| `oxipng` / `pngquant` | Compress screenshots before sending to vision API | system pkg |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Figma | SaaS | Yes — REST API exports frames + prototype flows | Pull frames per step via `/v1/files/:key/images`. |
| Maze | SaaS | Partial | Good for follow-up moderated tests after the walkthrough. |
| Lookback | SaaS | No — recordings only | Use for human follow-up, not agent input. |
| Storybook | OSS | Yes — static HTML per state | Trivial to feed component states into evaluator. |
| BrowserStack / Sauce Labs | SaaS | Yes — Playwright bridges | Multi-device walks (mobile vs desktop) at scale. |

## Templates & scripts
See `examples.md` and the matched `cog-walk-process` methodology for full templates. Minimal evaluator harness:

```python
# walk.py — drive a Playwright session and emit one JSON per step for the agent
import json, asyncio
from playwright.async_api import async_playwright

STEPS = [
  ("https://app.example.com/", "Click 'Get Started'", "button:has-text('Get Started')"),
  ("",                          "Enter email",         "input[type=email]"),
]

async def main():
  async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page()
    for i, (url, action, selector) in enumerate(STEPS, 1):
      if url: await page.goto(url)
      shot = f"step_{i}.png"
      await page.screenshot(path=shot, full_page=True)
      print(json.dumps({"step": i, "action": action, "shot": shot}))
      await page.locator(selector).click()
    await browser.close()

asyncio.run(main())
```

## Best practices
- Persona must be concrete: name, age, prior tools used, first-time flag. Vague personas cause vague Q3 answers.
- Always capture the screen *before* the action, not after. Q1-Q3 are about decision-making, Q4 alone is about post-action feedback.
- Evaluate every step including "obvious" ones. The most useful findings are usually on a step the team thought was trivial.
- Keep the codebook tight: Yes / No / Partial — no free-text answers for the four questions. Free text goes in evidence.
- Pair the walk with a heuristic evaluation pass; they catch different issue classes (learnability vs efficiency).
- Re-run after each fix; cog walk is cheap, regression coverage matters.

## AI-agent gotchas
- Vision-LLMs over-recognize standard patterns ("That hamburger menu is obvious"). Inject the persona's tech-savviness explicitly and forbid assumptions.
- Agents will conflate Q1 (motivation) with Q2 (visibility) — separate prompts per question reduce contamination.
- Q4 needs the *next* screen too; static screenshots can't show absence of feedback. Capture before+after pairs or animated GIFs.
- Locale: a Ukrainian-speaking persona walking an English-only UI fails Q3 by default. Don't let the agent pretend it doesn't.
- Severity inflation: agents tend to rank everything Medium. Force a forced ranking: top 3 issues only at High; rest must be Medium or Low.
- Privacy: prototype screenshots may contain real names/emails in placeholder data. Scrub before any vision call to a third-party API.

## References
- Nielsen Norman Group — How to Conduct a Heuristic Evaluation
- Wharton, Rieman, Lewis, Polson — The Cognitive Walkthrough Method: A Practitioner's Guide (1994)
- Interaction Design Foundation — How to Conduct a Cognitive Walkthrough
- usability.gov — Cognitive Walkthroughs
- Spencer & Blackmon — Streamlined Cognitive Walkthrough (CHI 2000)
