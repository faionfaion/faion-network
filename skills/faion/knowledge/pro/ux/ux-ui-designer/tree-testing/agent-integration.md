# Agent Integration — Tree Testing

## When to use
- Validating a draft information architecture after card sorting and before visual design.
- Comparing two IA candidates (A/B trees) on real user findability data.
- Diagnosing why search analytics show high "no-result" or zero-click rates on category pages.
- Re-baselining IA after a major content reorg or merger of two product taxonomies.

## When NOT to use
- Before any IA exists — start with card sorting.
- For visual/UX issues unrelated to navigation — usability testing fits better.
- For workflows with strong cross-linking and search dominance (no hierarchical paths to test).
- One-page apps and dashboards — too few branches for meaningful tree-test signal.

## Where it fails / limitations
- Text-only trees strip context cues users actually rely on (icons, search, recency, recommendations).
- Self-selection bias: panel users are not your users; high success in tests, low in production.
- Doesn't catch label fatigue — users may pick a "good enough" wrong answer because they're tired.
- N=30-50 only stabilizes top-line success; per-task confidence intervals stay wide for low-frequency tasks.
- Mobile context (narrow viewport, swipe nav) is not represented in standard tree tests.

## Agentic workflow
Drive Claude to convert an IA spec into the test tool's tree format, write tasks (without revealing labels), and define correct/acceptable answer paths. Once results come back as CSV, a synthesizer agent computes per-task success/directness/first-click and clusters wrong paths into "label confusion vs. structure mismatch". A copy-iteration agent proposes label rewrites and the cycle re-runs until success >80%.

### Recommended subagents
- `faion-ux-researcher-agent` — task writing, correct-path definition, test plan.
- `faion-usability-agent` — synthesize results, recommend label/structure fixes.
- A custom `tree-csv-analyzer` — load Treejack/UXtweak CSV, output success/directness/first-click tables.

### Prompt pattern
```
Given <IA YAML>, generate 12 tree-test tasks:
- Cover 3 navigation depths and 4 content types.
- Phrase as "Where would you go to <user goal>?" using user vocabulary.
- Do NOT include any tree label verbatim.
- Output JSON with task, correct path(s), acceptable alternates, priority.
```

```
Given <CSV from Treejack>, output:
- Task table: success%, directness%, median time, top-3 paths.
- Wrong-path clusters with hypothesized cause (label vs. structure vs. depth).
- Specific renames or moves to test next round.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `optimal-workshop` API | Programmatically launch Treejack tests, pull results | optimalworkshop.com/api |
| `uxtweak` API | Same for UXtweak Tree Testing | uxtweak.com/api |
| `pandas` | Analyze exported CSVs | `pip install pandas` |
| `jq` | Quick JSON path analysis on test outputs | stedolan.github.io/jq |
| `csvkit` | CSV slicing for first-click and path analysis | `pip install csvkit` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop Treejack | SaaS | Yes (REST) | Industry standard, large recruited panel |
| UXtweak Tree Testing | SaaS | Yes | Cheaper alternative; free tier |
| Maze | SaaS | Yes (REST) | Modern UX; tree-test feature |
| PlaybookUX | SaaS | Partial | Affordable, smaller feature set |
| UserZoom (UserTesting) | SaaS | Partial | Enterprise; gated API |
| Lyssna (formerly UsabilityHub) | SaaS | Yes | Quick first-click and tree tests |

## Templates & scripts
See `templates.md`. Inline analyzer stub (≤50 lines, pandas):

```python
import sys, pandas as pd
df = pd.read_csv(sys.argv[1])
def task_summary(g):
    n = len(g)
    success = (g["correct"] == True).mean()
    direct = (g["backtracks"] == 0).mean()
    first = g["first_click"].value_counts(normalize=True).head(3).to_dict()
    paths = g["path"].value_counts(normalize=True).head(3).to_dict()
    return pd.Series({"n": n, "success": round(success, 3),
                      "directness": round(direct, 3),
                      "median_sec": int(g["seconds"].median()),
                      "top_first_clicks": first, "top_paths": paths})
report = df.groupby("task").apply(task_summary)
print(report.to_markdown())
weak = report[report["success"] < 0.6]
if not weak.empty: print("\nFOCUS:", weak.index.tolist())
```

## Best practices
- Run baseline test on the EXISTING tree before launching the redesign — gives you a delta target.
- Aim for 50 participants per tree variant; under 30 the per-task CI is too wide to act on.
- Don't paraphrase tasks across rounds — comparability breaks.
- Pair tree testing with a 5-user moderated think-aloud: numbers say where, qualitative says why.
- Test at most 12-15 tasks; longer tests degrade attention, especially after task 10.
- Use first-click data to triage: if first click is wrong on >40% of users, fix the top-level labels first.

## AI-agent gotchas
- LLMs writing tasks frequently leak tree labels into the prompt ("Find the Returns section"); enforce a labels-blacklist check.
- Auto-generated "correct paths" miss legitimate cross-link routes — designer review required.
- LLM cluster summaries flatten signal — always retain raw wrong-path top 5 for human inspection.
- Human-in-loop checkpoint: a human IA owner must approve label/structure changes before the next test round; agent recommendations skew toward removing depth which sometimes worsens scent.
- For multilingual sites, never let one agent translate tasks AND grade results — translation drift inflates apparent success.

## References
- Rosenfeld, Morville, Arango — *Information Architecture* (4th ed.)
- Optimal Workshop — *The Tree Testing Guide*
- Nielsen Norman Group — *Tree Testing* — nngroup.com/articles/tree-testing
- Boxes and Arrows — *Tree Testing for IA*
- Usability.gov — *Tree Testing*
