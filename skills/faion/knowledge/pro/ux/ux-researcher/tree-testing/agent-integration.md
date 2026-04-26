# Agent Integration — Tree Testing

## When to use
- Validating a proposed information architecture (IA) before any visual design or build work begins.
- Comparing two or more candidate IAs head-to-head with the same task set ("which structure has higher findability?").
- Post-card-sort validation: turn the structure your card-sort produced into a tree, then test that real users can navigate it.
- Pre-redesign baselining: measure findability on the current site, then on the proposed site, to quantify the lift.

## When NOT to use
- The IA does not yet exist — run a card sort first.
- You're testing visual labels, calls-to-action, or filtering UI — that's first-click testing or full usability testing, not tree testing.
- Sites with strong search reliance (>50% of traffic enters via search) — findability through navigation is a smaller signal than search relevance.
- Single-page apps or tool surfaces without hierarchical navigation — there's no tree to test.

## Where it fails / limitations
- Decontextualized: removes design, content snippets, and search — real findability is higher than tree-test scores when these are present.
- Task wording leaks the answer: even careful researchers accidentally use the destination label in the task. LLM-generated tasks do this routinely.
- Synthetic LLM "participants" can roleplay the test, but their click paths reflect the model's prior on label semantics, not real user mental models. Useful as a smoke test, not as data.
- Trees with >100 nodes overwhelm participants and inflate failure rates artificially.
- Statistical confidence requires N≥30 per condition; agents that promise insights from N=5 are misusing the method.

## Agentic workflow
Treat the agent as a co-author of the test, not the participant. A research agent (1) ingests the proposed IA from a sitemap/JSON, (2) generates candidate tasks scoped to user goals, (3) flags tasks whose wording leaks an answer, (4) defines correct/acceptable destinations per task, (5) configures the test in Optimal Workshop / UXtweak / Maze via API, (6) post-test, parses CSV results, computes success/directness/first-click metrics, and identifies problem areas. Real human participants run the test; the agent never substitutes for them.

### Recommended subagents
- `faion-ux-researcher-agent` — task design, leak-check, results synthesis.
- `faion-content-marketer` — label rewriting suggestions when "label confusion" is the root cause.
- `faion-seo-manager` — cross-checks IA against search-demand keywords (so labels match user vocabulary).
- `faion-product-manager` — prioritizes problem areas by traffic/revenue impact.

### Prompt pattern
Task generation:
```
Tree:
{tree_yaml}
User goals (from research): {goals}
Generate 12-15 tree-test tasks. For each: scenario_text, target_path, acceptable_alternate_paths. Do NOT use the destination label in scenario_text. Reject tasks that make answer obvious by phrasing.
```
Leak check (run as second pass):
```
For each task, list overlapping word-stems between scenario_text and target_path nodes. Flag tasks with stem overlap on the target node — those leak the answer.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Optimal Workshop API | Programmatic test setup, results export | https://api.optimalworkshop.com |
| Maze API | Test creation + results | https://help.maze.co/hc/en-us/articles/360050842554 |
| `pandas` / `csvkit` | Compute success, directness, first-click breakdowns from exported CSVs | `pip install pandas csvkit` |
| `pyvis` / `graphviz` | Visualize wrong-path flows for stakeholder reports | `pip install pyvis` |
| `xmlstarlet` / `yq` | Convert sitemap.xml or YAML IA to tree-test format | distro / `pip install yq` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop Treejack | SaaS | Yes — REST API | Industry standard; best analytics |
| UserZoom (UserTesting) | SaaS | Partial — Enterprise API | Enterprise; bundled with usability suite |
| UXtweak Tree Testing | SaaS | Yes — API | Generous free tier, EU data residency |
| Maze Tree Test | SaaS | Yes — API | Modern UI, integrates with Figma |
| PlaybookUX | SaaS | Partial | Affordable; smaller participant panel |
| Lyssna (formerly UsabilityHub) | SaaS | Partial | Includes first-click testing too |
| Recruitment: User Interviews / Respondent / Prolific | SaaS | Yes — APIs | Pair with any of the above for participant supply |

## Templates & scripts
See `templates.md` for the test plan and results-report templates. Minimal results parser:

```python
# tree_test_metrics.py — compute success + directness from Treejack CSV export
import pandas as pd, sys
df = pd.read_csv(sys.argv[1])  # Treejack "tasks" export
out = []
for task_id, g in df.groupby("task_id"):
    n = len(g)
    success = (g["success"] == "Direct success").sum() + (g["success"] == "Indirect success").sum()
    direct = (g["success"] == "Direct success").sum()
    first_click_correct = (g["first_click_correct"] == True).sum()
    out.append({
        "task": task_id,
        "n": n,
        "success_rate": success / n,
        "directness": direct / n,
        "first_click_correct": first_click_correct / n,
        "median_time_s": g["time_taken_s"].median(),
    })
pd.DataFrame(out).to_csv("metrics.csv", index=False)
```

## Best practices
- Cap the tree at ~3-4 levels and ~100 nodes; deeper trees fatigue participants without producing extra signal.
- Write 10-15 tasks covering both shallow ("Returns" — 2 clicks) and deep ("Warranty for product X bought 2 years ago" — 4 clicks) destinations.
- Always include 2-3 "decoy" task types: tasks where the right answer doesn't exist in the tree, or where multiple paths are equally correct. Reveals false-confidence behavior.
- Recruit N=50 minimum for a single-tree test, N=30 per arm for an A/B comparison. Below this, success-rate confidence intervals are too wide.
- Run a leak-check pass on every task before launch; even researchers fail this regularly.
- Pair tree-test data with first-click analysis. A task with 80% success but 50% first-click-correct means users found it eventually but the IA still feels wrong; a task with 80% success and 80% first-click-correct is genuinely good.
- Re-test after iteration. Never ship IA changes off a single test cycle.

## AI-agent gotchas
- Tasks generated by an LLM tend to copy node labels verbatim — the leak check is mandatory, not optional.
- Synthetic LLM "participants" are tempting for cost/speed but produce paths biased toward the model's semantic priors, not naive-user mental models. Use only for sanity-checking task quality, never as data.
- Result CSV column names differ across tools (Treejack vs Maze vs UXtweak). Build adapter functions per provider rather than assuming a schema.
- Aggregating across tasks ("overall site success = 73%") hides the bottom 20% tasks that drag the average. Always report per-task metrics with the worst tasks called out.
- LLMs analyzing wrong-path data drift toward "users were confused"; force them to output specific label-renaming or restructuring proposals tied to evidence.
- Recruiting from low-quality panels (cheap general consumer) inflates success rates because professional respondents click confidently and randomly. Screen for category familiarity matching real users.

## References
- Spencer, Donna — *Card Sorting: Designing Usable Categories* (companion method)
- Rosenfeld, Morville, Arango — *Information Architecture* (4th ed.)
- Nielsen Norman Group — Tree Testing: https://www.nngroup.com/articles/tree-testing/
- Optimal Workshop — Tree Testing 101: https://www.optimalworkshop.com/learn/101s/tree-testing/
- Boxes and Arrows — Tree Testing: https://boxesandarrows.com/tree-testing/
