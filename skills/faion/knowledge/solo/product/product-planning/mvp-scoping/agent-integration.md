# Agent Integration — MVP Scoping

## When to use
- Starting a new product or major feature where the goal is to validate a hypothesis, not ship the final UX.
- Founder / solo PM has 30+ "obvious" features and needs to cut to 3–5 buildable in one timebox.
- An agent is asked to convert an idea description into an implementation plan and you need an explicit scope before SDD/spec writing.
- You will follow up with mlp-planning, micro-mvps, or product-discovery — MVP scoping is the entry gate.

## When NOT to use
- Post-PMF feature work — use roadmap-design + RICE instead.
- Compliance-driven products where "minimum" is dictated by regulation (the floor is set, scoping happens around it).
- B2B enterprise sales where the "MVP" must include integrations and SLAs to be credible — that's an MMP, not an MVP.
- When you already know the answer and need to ship — don't ceremony-stall.

## Where it fails / limitations
- "Walking-skeleton MVP" is often confused with "ugly v1" and ships without a learning goal — useless either way.
- Founder over-scopes Must-Have to 80% of capacity; no buffer for unknowns.
- LLMs love the verb "minimum" and emit too-thin scopes that don't actually solve the user's job.
- MVP scope without a defined hypothesis is just a feature list with extra steps.
- Skipping the "what we'll learn" section means there's no kill criterion → product limps for a year.

## Agentic workflow
A scoping subagent receives the problem statement, target user, timebox, and constraints. It emits a strict JSON: `{problem, hypothesis, core_value, must_have[], should_have[], wont_have[], learning_goals[], success_metrics[], kill_criterion}`. A reviewer subagent applies the 5-question quick check (one problem, value today, minimum to prove, can-wait, fits timebox). A spec-writer subagent expands each Must-Have into spec.md acceptance criteria. The output flows directly into SDD `.aidocs/backlog/<feature>/spec.md`.

### Recommended subagents
- `faion-mvp-scope-analyzer-agent` — primary scoping agent named in this methodology's metadata.
- `faion-mlp-feature-proposer-agent` — generates the candidate Must/Should/Could before scoping.
- `faion-spec-reviewer-agent` — converts Must-Have list into acceptance criteria.
- `faion-feature-executor` (this repo's skill) — picks up the resulting SDD feature and runs implementation.

### Prompt pattern
```
Given problem=<x>, user=<y>, timebox=<weeks>, capacity=<dev-weeks>:
Produce JSON:
{
  "hypothesis": "If we ship X, we will observe Y in N users",
  "core_value": "<one sentence>",
  "must_have": [{id, name, why_must, est_days}],
  "should_have": [{id, name, why_wait}],
  "wont_have": [{id, reason}],
  "learning_goals": ["<question>", ...],
  "success_metrics": [{name, target}],
  "kill_criterion": "If <metric> < <target> by <date>, pivot or kill"
}
Constraint: sum(must_have.est_days) <= 0.6 * timebox * capacity.
Reject scope without a kill_criterion.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI + GitHub Projects | Track MVP scope as a project view | https://cli.github.com |
| Linear API | Spec + scope as a project, custom fields for Must/Should/Won't | https://developers.linear.app |
| Notion API | MVP one-pager templates, agent-writable | https://developers.notion.com |
| `mermaid-cli` (`@mermaid-js/mermaid-cli`) | Render scope diagrams (story map, journey) | https://github.com/mermaid-js/mermaid-cli |
| `pandoc` | Convert MVP doc to PDF for stakeholder share | https://pandoc.org |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear / Jira | SaaS | Yes | MVP as project; custom MoSCoW fields |
| Productboard | SaaS | Yes (REST) | Has dedicated MVP / release planning views |
| Aha! | SaaS | Yes (REST) | Strategy → release scope linkage |
| Notion | SaaS | Yes (REST) | Cheapest MVP one-pager backing store |
| Figma + FigJam | SaaS | Limited | Story-map / scope canvas (mostly human) |
| Maze | SaaS | Yes (REST) | Validate MVP prototype with usability tests |
| Typeform / Tally | SaaS | Yes (REST) | Pre-MVP problem-validation surveys |

## Templates & scripts
See `templates.md` for the MVP scope document and 5-question validator. Inline capacity guard (≤ 25 lines):

```python
# mvp_capacity.py — fail if MVP scope can't fit timebox
import json, sys

doc = json.load(sys.stdin)  # output of scoping agent
must_days = sum(item["est_days"] for item in doc["must_have"])
budget = doc["timebox_weeks"] * doc["capacity_dev_per_week"] * 0.6

problems = []
if must_days > budget:
    problems.append(f"Must-Have {must_days}d exceeds 60%-budget {budget}d")
if not doc.get("kill_criterion"):
    problems.append("Missing kill_criterion")
if not doc.get("learning_goals"):
    problems.append("Missing learning_goals")
if len(doc["must_have"]) > 5:
    problems.append(f"Too many Musts: {len(doc['must_have'])} (max 5)")

print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
sys.exit(1 if problems else 0)
```

## Best practices
- Cap Must-Have at 3–5 features; physical ceiling, not a guideline.
- Write the hypothesis and kill criterion before the feature list — they constrain what counts as Must.
- Define one numeric success metric and one numeric kill threshold per learning goal.
- Make Won't-Have explicit and ≥ 3 items — it's the scope-creep firewall.
- Time-budget: Must ≤ 60% of capacity; rest is Should/Could/buffer. Reserve 20% for unknowns.
- Distinguish MVP (validate) from MLP (love) from MMP (sell). Don't ship an MVP to enterprise buyers.
- When MVP scope feels right, stress-test by asking "what would have to be true for this to fail?" and add those as risks.

## AI-agent gotchas
- LLMs love to add "polish" features that don't validate the hypothesis. Reject any Must without a one-sentence link to the hypothesis.
- "Authentication" and "billing" are reflexive Musts; they're often Should for v0 (use magic links + Stripe checkout, no in-app billing UI).
- Agents underestimate effort 2–3x; require T-shirt sizes that map to known day-ranges, not freehand `est_days`.
- Without a kill criterion the MVP becomes a permanent v1; force the field, fail validation if missing.
- Human-in-loop checkpoints: (a) hypothesis + kill criterion approval, (b) Must-Have lock-in, (c) post-launch decision against kill criterion.
- Don't let the proposing agent also be the reviewer — bias inflates Must list.

## References
- Eric Ries, "The Lean Startup" — original MVP definition.
- Marty Cagan, "Inspired" — distinction between MVP, MLP, MMP.
- Henrik Kniberg — "Making sense of MVP" (skateboard / car analogy) https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp
- Steve Blank, "The Four Steps to the Epiphany" — customer-development frame for scope decisions.
