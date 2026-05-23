# Agent Integration — Card Sorting

## When to use
- When designing or redesigning site navigation and the category structure is uncertain
- When analytics show high search usage suggesting users cannot find content through browse paths
- Before a content migration where existing IA is being reconsidered
- When user research has revealed that internal org structure is leaking into navigation labels
- As a complement to tree testing: run card sort first to generate the candidate IA, then tree test to validate it

## When NOT to use
- For navigation structures with fewer than 10 items — direct user interviews are faster and more insightful
- When the IA is constrained by regulatory or legal requirements that cannot change regardless of user preference
- To validate content quality or discoverability within an already-defined structure (use tree testing or first-click testing instead)
- When the product audience is too narrow to recruit 15+ participants who match the target profile

## Where it fails / limitations
- Open card sorting produces category names that reflect individual vocabulary, not consensus — aggregating labels requires interpretation, not just frequency counting
- Items that belong to multiple categories produce ambiguous placement data; the methodology does not capture this multi-membership well
- Card sort results reflect how users think about content labels, not whether they can find content in a real navigation — follow-up tree testing is mandatory before shipping
- Online participants sort faster and with less deliberation than in-person participants, producing shallower groupings
- 30+ cards create cognitive fatigue; participants rush the last third, producing noisy data for those items specifically

## Agentic workflow
A Claude subagent is effective at two stages: (1) preparing the card list by extracting content labels from a sitemap or content inventory and removing jargon, and (2) analyzing open sort results — given a similarity matrix or raw sort data exported from a tool, the agent can identify high-agreement clusters, flag ambiguous items, suggest canonical category labels based on participant-generated names, and produce a draft IA recommendation. The actual sorting sessions must be conducted with participants via a dedicated tool.

### Recommended subagents
- Any general-purpose Claude subagent (Sonnet) — card list preparation, jargon removal, open sort analysis, IA recommendations
- `faion-sdd-executor-agent` — structure follow-up tree testing tasks based on the proposed IA

### Prompt pattern
```
You are an information architect analyzing open card sort results. The data below shows which cards participants grouped together (similarity matrix: value = % of participants who placed both cards in the same group).

Tasks:
1. Identify clusters of cards with >60% similarity — these are strong groupings
2. Identify cards with no clear cluster (<40% similarity with any other card) — these are orphans
3. Suggest 5–8 category names based on participant-generated labels (provided separately)
4. Flag items placed inconsistently (high variance in placement) — these need further research

Similarity matrix: [CSV or JSON]
Participant category names (frequency): [list]
```

```
You are preparing a card list for a card sorting study. Given the sitemap below:
1. Extract all navigation item labels
2. Remove internal jargon (replace with plain user-facing descriptions)
3. Remove duplicates
4. Flag items that are ambiguous and may need rewording
5. Return: final card list (max 50 items) + list of flagged items with suggested rewording

Target audience: [description]
Sitemap: [list]
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `optimal-workshop-cli` (via API) | Create studies and export results from Optimal Workshop | REST API / [help.optimalworkshop.com/en/articles/api](https://help.optimalworkshop.com/en/articles/api) |
| `python pandas` | Compute similarity matrices from raw sort data exported as CSV | `pip install pandas` |
| `scipy` | Hierarchical clustering on similarity matrix to identify groups programmatically | `pip install scipy` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Optimal Workshop | SaaS | Yes — REST API | Full-featured card sort; exports similarity matrix and dendrograms; API for result retrieval |
| UXtweak | SaaS | Yes — API | Card sorting + tree testing; budget-friendly; API for study creation and results |
| Maze | SaaS | Yes — REST API | Modern interface; card sort feature; results exportable via API |
| Lyssna | SaaS | Yes — API | Quick unmoderated card sorts; result export via API |
| Miro | SaaS | Partial | In-person or facilitated remote card sorts with sticky notes; no structured sort data export |

## Templates & scripts
See `README.md` for Card Sort Plan and Card Sort Results templates.

Script — compute pairwise similarity matrix from Optimal Workshop CSV export:
```python
#!/usr/bin/env python3
"""
Usage: python similarity.py sorts_export.csv
Input: CSV where each row is a participant, columns are card labels, values are category assigned.
Output: Similarity matrix as CSV (% of participants who placed each pair in the same category).
"""
import csv, sys
from itertools import combinations
from collections import defaultdict

def compute_similarity(path):
    with open(path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    cards = [k for k in rows[0] if k != "participant"]
    pair_same = defaultdict(int)
    pair_total = defaultdict(int)
    for row in rows:
        for a, b in combinations(cards, 2):
            if row[a] and row[b]:
                pair_total[(a, b)] += 1
                if row[a] == row[b]:
                    pair_same[(a, b)] += 1
    print("card_a,card_b,similarity_pct")
    for (a, b), total in pair_total.items():
        sim = round(pair_same[(a, b)] / total * 100)
        print(f"{a},{b},{sim}")

if __name__ == "__main__":
    compute_similarity(sys.argv[1])
```

## Best practices
- Write card labels in user language, not product language — run the label list past a non-technical user before the study
- Cap at 40 cards for remote unmoderated sorts; 30 is safer — fatigue degrades data quality for the final 20–30%
- For open sorts, ask participants to label their groups immediately after sorting while the rationale is fresh; delayed labeling produces generic names
- Run a pilot sort with one internal person who did not design the IA to catch confusing card wording before the real study
- Do not present cards in alphabetical order — it artificially biases groupings toward alphabetic proximity
- Always follow card sorting with tree testing on the proposed IA before implementing; sort results are an input, not a final decision

## AI-agent gotchas
- Agents cannot run the sorting session — they can only process exported data; the study must be configured and distributed through a dedicated tool
- Similarity matrix interpretation requires domain knowledge: an agent may cluster "Privacy Policy" with "Terms of Service" (logical) but miss that users actually expect them under "Footer" not "Legal"
- Frequency-based category naming from participant labels is mechanical but interpretation of ambiguous labels requires a human decision
- When passing raw sort data (not a pre-computed similarity matrix), the agent must be given clear column semantics — "participant" vs. "card" vs. "category" columns must be labeled explicitly
- Open sort analysis by an agent should be treated as a hypothesis, not a conclusion; the final IA recommendation must be validated by a human researcher before tree testing

## References
- [Card Sorting — NNG](https://www.nngroup.com/articles/card-sorting-definition/)
- [Optimal Workshop Card Sorting Guide](https://www.optimalworkshop.com/learn/101s/card-sorting/)
- [Information Architecture: For the Web and Beyond — Rosenfeld, Morville, Arango](https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/)
- [Optimal Workshop API Reference](https://help.optimalworkshop.com/en/articles/api)
- [Card Sorting: A Definitive Guide — Boxes and Arrows](https://boxesandarrows.com/card-sorting-a-definitive-guide/)
