# Agent Integration — Cognitive Walkthrough

## When to use
- Evaluating learnability for first-time users, especially walk-up-and-use products (kiosk, sign-up, onboarding).
- Pre-launch sanity check before usability testing — cheaper, faster than recruiting users.
- Reviewing a defined task path (account setup, checkout, onboarding step) where "correct sequence" is known.
- Auditing govt / public-service flows where novice users dominate.

## When NOT to use
- Open-ended exploratory tasks (browsing) where there is no single "correct sequence".
- Replacing real user research — walkthrough finds learnability issues, not preference, satisfaction, or value.
- Highly subjective brand/aesthetic review — heuristic eval is better.
- Late-stage performance / efficiency tuning for expert users — different method (keystroke-level, GOMS).

## Where it fails / limitations
- Evaluators bring tacit knowledge — "obvious" buttons aren't obvious to the persona.
- Group-think when 2-4 evaluators converge fast on the first answer; structure each question independently.
- Misses motivational issues ("user knows what to do, just doesn't want to").
- Ignores accessibility unless persona explicitly includes AT use.
- Agents reflexively answer "Yes" — needs structured contradiction prompts.

## Agentic workflow
Use a subagent as the "naive persona" — feed it a screen capture or DOM snapshot plus the persona file, and have it answer the four CW questions per step. A second agent role-plays an "advocate" arguing the opposite, then a synthesizer extracts genuine ambiguities. Humans confirm prioritized issues and own the fix list.

### Recommended subagents
- `faion-usability-agent` — drives the four-question protocol per step.
- `faion-ux-researcher-agent` — converts findings into research-grade report and recruits real users for confirmation.
- `faion-sdd-executor-agent` — applies UI fixes (label, position, feedback) once approved.

### Prompt pattern
```
You are the persona <persona> on screen <screenshot/DOM>. The
correct next action is <action>. Answer Yes/No/Partial with
2-sentence rationale for: Q1 right effect; Q2 action visible;
Q3 label associates with effect; Q4 progress feedback. Be skeptical.
```

```
Take all No/Partial answers and produce: severity (H/M/L),
WCAG/heuristic tag, smallest fix in 1 sentence, owner team.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `playwright` (`page.screenshot()` / `page.accessibility.snapshot()`) | Capture per-step DOM/AX trees | playwright.dev |
| `axe-core` CLI | Tag a11y issues alongside CW | deque.com/axe |
| `pa11y-ci` | Repeatable a11y baseline per route | pa11y.org |
| Storybook + interaction tests | Walk through each step in isolation | storybook.js.org |
| Lighthouse CLI | Snap perf/accessibility per step | github.com/GoogleChrome/lighthouse |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Maze | SaaS | Partial — REST for results | Auto-tracks first-click, time-to-complete. |
| UserTesting | SaaS | Partial — REST API | Real-user complement after CW. |
| Lookback | SaaS | No — manual | Use only for live observation. |
| Useberry | SaaS | Yes — REST | First-click + path data feeds CW question 2. |
| Loom + transcript LLM | Mixed | Yes — Loom API | Capture evaluator narrative, summarize. |

## Templates & scripts
See `templates.md` for Walkthrough Plan, Evaluation Form, Summary Report. Inline orchestration script (Python pseudo):

```python
STEPS = ["sign-up-click", "email-entry", "password-entry",
         "create-account", "profile-name", "complete-setup"]
QUESTIONS = [
    "Will the user try to achieve the right effect?",
    "Will the user notice the correct action is available?",
    "Will the user associate the correct action with the desired effect?",
    "Will the user see that progress is being made?",
]
results = []
for step in STEPS:
    snap = capture(step)  # screenshot + AX tree
    for q in QUESTIONS:
        ans = ask_persona_agent(persona, snap, step, q)
        results.append({"step": step, "q": q, **ans})
write_report(results)
```

## Best practices
- Write the correct action sequence before evaluation; if you can't, the task is too vague to walkthrough.
- Use a *novice* persona — for expert flows, run a separate session with a power-user persona.
- Score each question independently per step; do not let evaluators see prior answers until the end.
- For each issue, force a one-sentence fix proposal — "report the bug, propose the fix" rule.
- Re-walk after fixes; CW iterations are cheap and catch regressions.
- Pair with one round of moderated usability testing on the top 5 issues.

## AI-agent gotchas
- LLM evaluators are too charitable — explicitly require Yes only with positive evidence in the screenshot.
- Hallucinated UI elements: ground via DOM + AX tree, not pixel guessing.
- Agents conflate Q1 (motivation) with Q3 (labelling) — separate the prompts.
- "Progress feedback" question is often answered for the page transition, not the user's goal — anchor on the user's narrative.
- Persona drift: agent forgets the persona midway; reseed it every step.
- Severity inflation: agents mark everything H; calibrate with a rubric (H = blocks task, M = >10% slow, L = polish).

## References
- Wharton, Rieman, Lewis, Polson — *The Cognitive Walkthrough: A Practitioner's Guide* (1994).
- NN/g, "Cognitive Walkthrough" — nngroup.com/articles/cognitive-walkthrough-workshop/
- IDF, "How to Conduct a Cognitive Walkthrough" — interaction-design.org/literature/article/how-to-conduct-a-cognitive-walkthrough
- Usability.gov, "Cognitive Walkthroughs" — usability.gov/how-to-and-tools/methods/cognitive-walkthroughs.html
- Spencer, "Streamlined Cognitive Walkthrough" — uxbooth.com
