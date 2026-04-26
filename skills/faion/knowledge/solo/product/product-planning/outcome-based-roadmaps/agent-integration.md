# Agent Integration — Outcome-Based Roadmaps

## When to use
- Founder needs a quarterly plan but solutions for the underlying problems are still uncertain.
- Stakeholders keep mistaking feature lists for commitments — pivoting away from "ship X by date" toward "move metric Y" buys planning slack.
- A discovery loop is active and you want a roadmap that survives the next experiment instead of being rewritten every sprint.
- Multiple teams or contractors need alignment on goals without locking solutions.

## When NOT to use
- Contractually committed deliverables (RFPs, enterprise SLAs, regulator deadlines) that demand date-bound feature delivery — use a timeline roadmap instead.
- Pure execution phases of a single feature where scope and design are fully validated — fall back to a sprint plan or release plan.
- Teams without a metrics pipeline. Outcome roadmaps require trustworthy baselines; without analytics, the outcome column is theatre.
- Pre-PMF zero-to-one stages where the priority is finding *any* user, not moving a metric.

## Where it fails / limitations
- Vanity outcomes ("increase engagement") that nobody can operationalise — agents will happily generate verbose roadmaps around immeasurable goals.
- Outcome inflation: every quarter declares 5+ outcomes, none get the focus needed; LLMs default to plural lists and worsen this.
- Disconnect from delivery — engineering still runs a feature backlog and the roadmap becomes a parallel doc nobody trusts.
- Confusing inputs (activities) with outcomes (metric movements). Common LLM error: emitting "run 5 user interviews" as the outcome.
- Outcome roadmaps are weak for stakeholders who pay per feature; they push back unless you also produce a feature-derivative view.

## Agentic workflow
Drive this with a small Claude pipeline: a discovery agent surfaces candidate outcomes from analytics + interview notes, a strategist agent picks 2–4 quarterly outcomes against business goals, and a roadmap-writer agent emits the doc using the structure from `README.md`. Keep humans in the loop on outcome selection and target-number setting — those decisions are loaded with judgement an LLM cannot supply alone. Re-run the pipeline at quarter boundaries; mid-quarter only refresh the "potential solutions" column.

### Recommended subagents
- `faion-mlp-impl-planner-agent` — present in `pro/product/product-manager` and referenced from related methodologies; reuse for outcome → solution-option translation.
- `faion-idea-generator-agent` — fan out solution candidates per outcome without committing.
- `faion-spec-reviewer-agent` — sanity-check outcome wording (verb + metric + delta + timeframe) before publication.
- `faion-mvp-scope-analyzer-agent` — turn the chosen outcome bucket into a scoped slice once an experiment converges.

### Prompt pattern
```
System: You are a roadmap strategist. Output ONLY YAML matching the schema.
Input: {analytics_summary, interview_themes, business_goals, constraints}
Task: Propose 3 outcomes for next quarter. Each must have:
  outcome (verb + metric + delta + timeframe),
  rationale (<=2 sentences, cite evidence),
  leading_indicators (2–4),
  candidate_solutions (3–6, marked "to-validate"),
  not_doing (2–3 explicit exclusions).
Forbidden: dates per solution, feature commitments.
```

```
System: You are a roadmap reviewer. For each outcome, score 0–2 on
  measurability, evidence, focus, falsifiability. Return JSON. Reject any
  outcome scoring <6/8 with a one-line reason.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| GitHub Projects CLI (`gh project`) | Track outcomes as projects, link issues as candidate solutions | `gh extension install github/gh-projects` · https://cli.github.com/manual/gh_project |
| Linear CLI (`linear-cli`) | Create initiatives = outcomes, projects = experiments | `npm i -g @linear/cli` (community) · https://developers.linear.app |
| `productboard-mcp` (community MCP) | Read/write objectives + features for agent loops | https://github.com/productboard (search MCP) |
| `posthog` CLI / API | Pull leading indicators to validate outcome targets | https://posthog.com/docs/api |
| `metabase-api` (npm) | Query KPI dashboards programmatically for outcome scorecards | https://www.npmjs.com/package/metabase-api |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| ProductBoard | SaaS | Yes (REST + OAuth) | Native objectives → features mapping; supports outcome roadmaps natively. |
| Productplan | SaaS | Limited (REST) | Visual outcome lanes, weak write API for agents. |
| Aha! | SaaS | Yes (REST) | Strong "Goals → Initiatives → Releases" hierarchy fits outcome model. |
| Linear | SaaS | Yes (GraphQL) | Initiatives + projects map cleanly to outcomes + experiments. |
| Roadmunk | SaaS | Yes (REST) | Quarter swimlane export easy to script. |
| Notion + Database template | SaaS | Yes (REST) | Cheapest path; agent can CRUD outcome rows; brittle for big orgs. |
| OpenProject | OSS | Yes (REST) | Self-host; relies on custom fields for outcome metrics. |
| Plane (makeplane.so) | OSS | Yes (REST) | Modern OSS Linear-clone; cycles + modules ≈ outcomes + bets. |

## Templates & scripts
See `README.md` for the outcome roadmap structure (Q1/Q2 outcome blocks). Inline helper to validate that each outcome row has a measurable target before committing to a tracker:

```python
import re, sys, yaml
SCHEMA = {"outcome", "metric", "baseline", "target", "timeframe", "evidence"}
PATTERN = re.compile(r"(reduce|increase|decrease|raise|cut)\b", re.I)

def lint(path: str) -> int:
    data = yaml.safe_load(open(path))
    bad = 0
    for row in data.get("outcomes", []):
        miss = SCHEMA - row.keys()
        if miss:
            print(f"[FAIL] {row.get('outcome','?')}: missing {miss}"); bad += 1
        if not PATTERN.search(str(row.get("outcome", ""))):
            print(f"[WARN] {row['outcome']}: no movement verb"); bad += 1
        try:
            if float(row["target"]) == float(row["baseline"]):
                print(f"[FAIL] {row['outcome']}: target == baseline"); bad += 1
        except (KeyError, ValueError):
            pass
    return bad

sys.exit(1 if lint(sys.argv[1]) else 0)
```

## Best practices
- Cap quarterly outcomes at 3 (solo) or 5 (small team). More outcomes ⇒ no focus, agents will pad.
- Pair every outcome with a falsifying signal: "If activation drops below X, kill the bet by week 6."
- Maintain a single "Not doing" list per quarter — explicit exclusions stop scope creep more than priorities do.
- Keep the outcome immutable mid-quarter; only the solution list mutates as experiments resolve.
- Two-tier publishing: internal roadmap shows outcomes + bets; external roadmap shows themes only, no targets.
- Tie outcomes to existing dashboards before publishing — if you cannot link a chart URL, the outcome is not real.
- Run a retrospective at quarter-end on outcome accuracy, not feature delivery: "Did we move the metric? Why/why not?"

## AI-agent gotchas
- LLMs frequently restate features as outcomes ("ship onboarding redesign" → "improve onboarding"). Add a validator that requires a metric + delta + verb.
- Without a numeric baseline pulled from analytics, agents will hallucinate plausible but fake percentages. Inject real baselines as context or refuse to generate the target.
- Solution lists balloon to 10+ "candidate experiments" — clamp to 6 in prompts and reject extra rows.
- Agents tend to drop the "not doing" column because it produces no content. Treat it as a required field; reject documents missing it.
- Quarterly cadence is a human-coordination artefact. Daily-running discovery agents will keep churning the doc; add a freeze window (e.g. only re-write outcomes in week 12 of each quarter).
- Human checkpoint mandatory before publishing externally — outcome targets are commitments and an LLM should not set business goals unilaterally.
- When outcomes are vague ("delight users"), follow-up agents (RICE scorers, sprint planners) cannot ground their reasoning and produce confident garbage.

## References
- Marty Cagan — *Inspired* (2nd ed.), chapters on outcome vs output.
- Teresa Torres — *Continuous Discovery Habits* (Opportunity Solution Tree underpins outcome roadmaps).
- Jeff Gothelf — *Outcomes Over Output* (book + jeffgothelf.com posts).
- ProductBoard — "Outcome-based roadmaps" guide: https://www.productboard.com/glossary/outcome-based-roadmap/
- Roman Pichler — "GO Product Roadmap" template: https://www.romanpichler.com/tools/go-product-roadmap/
- Atlassian — "From Output to Outcomes": https://www.atlassian.com/agile/project-management/outcomes
