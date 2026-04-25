# Agent Integration — MVP Scoping

## When to use
- Solo founder or small team turning a validated problem into a buildable first slice.
- Existing feature backlog has 30+ ideas and you need to compress to a 4–8 week slice.
- A larger product is going to enter a new vertical / persona and needs a smaller anchored release.
- Pivot moment: prior MVP failed and a leaner re-scope is required, with explicit "won't have" boundaries.

## When NOT to use
- The problem itself is unvalidated — run `product-discovery` and `problem-validation` first; an MVP scope around a wrong problem is worse than no scope.
- Compliance / regulated products (medical, fintech KYC) where "minimum" violates statutory requirements — use staged regulatory release plans instead.
- Replacing a production system with a feature parity migration — scope here is dictated by parity, not learning.
- Mature product with a polished user base; "minimum" disappoints loyal users. Use `mlp-planning` or incremental release planning.

## Where it fails / limitations
- "MVP" used as a euphemism for "less polished v1" — without explicit learning goals it produces unmeasurable releases.
- Must-have lists that grow past 5 items: scope ceases to be minimum and timelines slip into 6+ months.
- No definition of failure: if you cannot articulate which evidence kills the idea, the MVP cannot teach you.
- Team treats the MoSCoW classification as fixed; it should be revisited weekly during build as user data trickles in.
- LLM-generated MVP specs often miss non-functional minimums (auth, basic security, observability) which are still mandatory to ship anything real.

## Agentic workflow
A scope-analyzer agent ingests the raw idea/feature dump and outputs a MoSCoW-categorised list with a rationale per item. A second critic agent challenges every Must-Have ("would the product still teach us if we cut this?") and forces the writer to either justify or demote it. A third agent emits a structured MVP scope document plus a 5-question quick-check (templates already in `README.md`). Humans own two checkpoints: setting the learning goal and approving the final cut list — these are commitments, not classifications.

### Recommended subagents
- `faion-mvp-scope-analyzer-agent` — referenced in `README.md`; primary scoping role.
- `faion-idea-generator-agent` — divergent feature brainstorm before scoping.
- `faion-spec-reviewer-agent` — checks the resulting MVP spec for testability + clarity.
- `faion-task-creator-agent` — converts the Must-Have list into a backlog of acceptance-criteria-bearing items once scope is locked.

### Prompt pattern
```
System: You are an MVP scope analyzer. Output JSON only.
Input: {problem_statement, persona, hypothesis, constraints, raw_features[]}
For each feature emit:
  {name, moscow: must|should|could|wont, rationale, removal_cost, learning_value}
Hard limits: must <= 5, total must+should effort_days <= constraint_days,
  any "must" lacking removal_cost field is invalid.
```

```
System: You are an adversarial MVP critic. For each must-have, attempt to
  prove the experiment still works without it. If you succeed, recommend
  demotion to should/wont with a one-sentence justification.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh issue` / `gh project` | Stage MVP must-haves as a GitHub Project; cheap, scriptable | https://cli.github.com/manual |
| `linear-cli` | Create MVP cycle + issues directly from JSON output | `npm i -g @linear/cli` |
| `jira-cli` | Same for Jira-bound teams | https://github.com/ankitpokhrel/jira-cli |
| `claude` (Anthropic SDK) | Drive the analyzer/critic/writer pipeline locally | https://docs.anthropic.com |
| `ruff` / project linter | Run on emitted scope doc if stored as Python YAML/Pydantic models | https://docs.astral.sh/ruff |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes (GraphQL) | Cycles map onto MVP timebox; "Initiative" = MVP container. |
| GitHub Projects v2 | SaaS | Yes (GraphQL) | Free for solo; agents can mutate fields directly. |
| Notion | SaaS | Yes (REST) | Quick MVP scope tables, but weak validation. |
| Productboard | SaaS | Yes (REST) | Strong feature → release mapping with priority lanes. |
| Plane | OSS | Yes (REST) | Self-host alternative to Linear. |
| Aha! Develop | SaaS | Yes (REST) | Useful when MVP feeds into a wider roadmap. |
| Whimsical | SaaS | Limited | Good for visual MoSCoW / story map; manual integration. |
| Maze | SaaS | Yes (REST) | Run prototype tests on the MVP scope before code. |

## Templates & scripts
See `templates.md` and `README.md` for the MVP Scope Document and the 5-question quick check. Inline gate that fails CI/CD if the scope doc breaks the rules:

```python
import sys, yaml
doc = yaml.safe_load(open(sys.argv[1]))
errs = []
musts = [f for f in doc["features"] if f["priority"] == "must"]
if len(musts) > 5: errs.append(f"too many must-haves: {len(musts)} > 5")
if not doc.get("learning_goal"): errs.append("missing learning_goal")
if not doc.get("kill_signal"): errs.append("missing kill_signal (failure criterion)")
if not doc.get("wont_have"): errs.append("missing wont_have list")
budget = doc.get("budget_days", 0)
spent = sum(f.get("effort_days", 0) for f in doc["features"] if f["priority"] in {"must","should"})
if spent > budget: errs.append(f"effort {spent}d > budget {budget}d")
for e in errs: print("FAIL:", e)
sys.exit(1 if errs else 0)
```

## Best practices
- Force a kill-signal next to each learning goal: "If <X% of users complete the core flow in 2 weeks, we shut this down."
- Cap timebox at 4–8 weeks. Past 8 weeks "minimum" is a misnomer; switch to release planning with phases.
- Write the "Won't Have" list before the "Must Have" list — exclusions discipline scope better than inclusions.
- Validate end-to-end value, not isolated features. The walking skeleton from `user-story-mapping` is the integrity check.
- Pair every Must-Have with measurable acceptance criteria; otherwise it cannot be marked done.
- Decouple MVP from polish. Rough UI is fine; rough data integrity is not.
- Re-run scope review at week 2 and week 4 — build data invalidates assumptions, and demotions are cheaper than rewrites.

## AI-agent gotchas
- Agents inflate Must-Have counts because adding feels generative; explicitly enumerate maxima in the prompt.
- LLMs love hedging language ("important", "consider"). Replace with hard ranks (must/should/could/wont) and reject prose.
- Without explicit numeric constraints (budget_days, max_must_count) the model produces aspirational scopes that match no reality.
- Effort estimates from an LLM are noise; use them only for relative sizing and require a human to ratify days.
- Critic agents need temperature ≥ 0.5 to attack their own scope honestly; an over-aligned critic will rubber-stamp.
- When the analyzer and critic share a single context window they collude. Run them as separate prompts or separate sub-agents.
- Always emit a "kill_signal" field; otherwise the agent will write soft success metrics that justify shipping anyway.
- Token budget: a full MVP scoping pass on 30 features ≈ 6–10k input tokens; batch features in chunks if the brainstorm is larger.

## References
- Eric Ries — *The Lean Startup* (defines MVP as a learning vehicle).
- Frank Robinson / SyncDev — original MVP coinage: https://en.wikipedia.org/wiki/Minimum_viable_product
- Henrik Kniberg — "Making sense of MVP" (skateboard analogy): https://blog.crisp.se/2016/01/25/henrikkniberg/making-sense-of-mvp
- DSDM Consortium — MoSCoW prioritisation: https://www.agilebusiness.org/dsdm-project-framework/moscow-prioritisation.html
- Marty Cagan — *Inspired* (chapters on product viability vs feasibility risk).
