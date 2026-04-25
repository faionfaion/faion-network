# Agent Integration — Card Sorting

## When to use
- Preparing card content: extracting navigation items from a sitemap or content inventory and formatting them as a card list for a study
- Analyzing open-sort results: given participant groupings as structured data, compute similarity matrices and identify natural clusters
- Generating a card sort results report from raw exported data (Optimal Workshop JSON/CSV)
- Recommending an IA structure based on aggregated open-sort data and documented user mental models
- Drafting a card sort plan from a research brief or project spec

## When NOT to use
- As a substitute for running the actual study — agents cannot observe how participants hesitate, combine, or split cards in real time
- When content is fewer than 10 items — the overhead of a card sort is not justified; simple interviews or usability tests suffice
- When the IA is already well-validated through tree testing and live search analytics — re-sorting adds noise without new signal
- For UI layout questions — card sorting answers content organization, not visual hierarchy or component placement

## Where it fails / limitations
- Agent analysis of similarity matrices can surface clusters that look statistically strong but reflect how cards were worded, not genuine user mental models — ambiguous card labels corrupt results
- Open-sort labeling is highly variable; agents grouping participant-generated category names face a meta-classification problem (grouping the groupings)
- Closed sort placement percentages hide the reason for ambiguous items; agents cannot infer why a card was split without qualitative follow-up notes
- Automated cluster detection (hierarchical clustering, dendrograms) requires at least 15-20 participants to be stable; below that, results are noise
- Agents recommending IA from sort data alone will miss business constraints (legal requirements, content governance, technical limitations)

## Agentic workflow
A Claude agent receives a content inventory (list of page/item names) and generates a ready-to-use card list with any jargon replaced by user-friendly language. After a study runs, the agent receives exported participant groupings as JSON or CSV, computes a co-occurrence matrix (how often each pair of cards was grouped together), identifies strong clusters (>70% co-occurrence), weak clusters (40-70%), and outliers (<40%). It then proposes a candidate IA structure and flags items needing further tree testing validation.

### Recommended subagents
- `faion-sdd-executor-agent` — translates a card sort-derived IA structure into navigation spec acceptance criteria for the SDD design document

### Prompt pattern
```
You are a UX researcher preparing a card sort. Given the sitemap below, extract all leaf-level navigation items (pages and content categories). Rewrite any internal jargon into plain user-facing language. Output a numbered card list of 30-60 items, removing duplicates and merging near-synonyms.
```

```
You have open card sort data. Each row is a participant's grouping: participant_id, group_name_given, cards_in_group (comma-separated).
1. Build a co-occurrence matrix: for each pair of cards, what % of participants grouped them together?
2. Identify clusters: pairs >70% co-occurrence, borderline 40-70%, weak <40%
3. Propose 4-7 top-level IA categories based on strong clusters
4. List 3-5 cards that were split across multiple groups and need further research
Output as a structured report with a summary table, cluster list, and ambiguous items.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `python` + `scipy` | Hierarchical clustering on co-occurrence matrices from sort exports | `pip install scipy numpy` / scipy.org |
| Optimal Workshop CLI (none public) | Study managed via web UI; export data as CSV/JSON for agent processing | optimalworkshop.com |
| `pandas` | Parse and reshape Optimal Workshop or UXtweak CSV exports | `pip install pandas` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop (OptimalSort) | SaaS | Yes — CSV/JSON export | Industry standard; exports full participant data; no public write API |
| UXtweak | SaaS | Yes — CSV export | Budget-friendly; exports card sort results as CSV |
| Maze | SaaS | Partial — JSON export | Card sort module available; results exported via API |
| UserZoom | SaaS | Enterprise only | Full export via enterprise API; overkill for small teams |
| Dovetail | SaaS | Yes | Import card sort notes and cluster qualitative themes alongside quantitative data |

## Templates & scripts
See `templates.md` for the Card Sort Plan Template and Card Sort Results Template.

```python
# Co-occurrence matrix from open sort export
# Input: list of dicts [{participant_id, group_name, cards: [str]}]
from itertools import combinations
from collections import defaultdict

def cooccurrence(sessions: list) -> dict:
    pair_count = defaultdict(int)
    total = len(sessions)
    for s in sessions:
        for group in s["groups"]:
            cards = group["cards"]
            for a, b in combinations(sorted(cards), 2):
                pair_count[(a, b)] += 1
    return {pair: count / total for pair, count in pair_count.items()}

def strong_clusters(matrix: dict, threshold=0.7):
    return {pair: pct for pair, pct in matrix.items() if pct >= threshold}
```

## Best practices
- Write card labels from the user's vocabulary, not internal taxonomy — if your sitemap says "Resource Hub", the card should say "Guides and Templates"
- Run an open sort first (discover categories), then a closed sort (validate the proposed structure) — the two-phase approach gives both generative and confirmatory data
- Include 3-5 "anchor" cards whose categories are already well-established; use them to validate participant seriousness (if they mis-sort anchors, the session is suspect)
- After analysis, always run tree testing on the proposed structure before building — card sorting tells you how users group content, not whether they can find it in a hierarchy
- Report outlier cards explicitly; they often represent content that needs to be redesigned (renamed, split, or merged) rather than just re-categorized

## AI-agent gotchas
- Agents generating card lists from sitemaps will include admin/internal pages that should not be tested; always filter to user-facing content only
- Co-occurrence clustering is sensitive to card label wording — agents must not rephrase cards between the study design and analysis phases
- Human review required before publishing an IA recommendation from sort data alone — business, legal, and technical constraints are invisible to the agent
- Agents asked to "find clusters" in small datasets (< 15 participants) will produce confident-sounding but statistically meaningless recommendations; flag sample size in output
- Tree testing validation is a mandatory follow-up — agents should generate a tree test spec as part of the card sort results report, not treat sort results as final

## References
- https://www.nngroup.com/articles/card-sorting-definition/
- https://www.optimalworkshop.com/learn/101s/card-sorting/
- https://www.interaction-design.org/literature/article/how-to-conduct-a-card-sorting-session
- https://boxesandarrows.com/card-sorting-a-definitive-guide/
- https://www.nngroup.com/articles/tree-testing/
