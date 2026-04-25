# Agent Integration — Brainstorming Ideation

## Note on methodology scope

This directory (`brainstorming-ideation`) contains the same README content as `brainstorming-techniques` (identical frontmatter ID `brainstorming-techniques`, same body). It appears to be a duplicate or an alias directory. The content covers Classic Brainstorming, Brainwriting 6-3-5, Round Robin, and Reverse Brainstorming — the same four techniques documented in `brainstorming-techniques/`.

Rather than duplicate the `brainstorming-techniques/agent-integration.md` content verbatim, this file documents the **ideation-specific integration angle**: how to use brainstorming as a generative input feeding downstream product or creative pipelines, rather than as a facilitation event.

---

## When to use
- Feeding an ideation pipeline where the output is a scored shortlist, not a facilitated group session
- Product feature generation: given a persona + pain point, produce candidate features to evaluate
- Content ideation: bulk-generating article topics, campaign angles, or ad copy variants
- Risk surfacing: Reverse Brainstorming to enumerate failure modes before a launch

## When NOT to use
- When a human group dynamic is the point (team alignment, buy-in, psychological safety) — agent bulk generation skips the relational work
- When the problem is too narrow for divergent thinking; use direct prompting or SCAMPER instead
- When ideas need domain-expert validation that an LLM cannot reliably provide (medical, legal, engineering safety)

## Where it fails / limitations
- Agent-generated idea lists are biased toward patterns already common in training data; genuinely novel ideas require cross-domain prompting or persona injection
- Brainwriting round-by-round simulation loses the "build on others" benefit because the agent reads its own prior ideas, creating an echo chamber
- Convergence (clustering, dot voting, scoring) is where agent errors compound — misclassified clusters lead to wrong shortlists
- Quantity is trivially achieved (100 ideas in seconds) but quality filtering requires human judgment at the evaluation gate

## Agentic workflow
Agent receives a problem statement, a target idea count, and an optional technique flag (classic / reverse / brainwriting-simulated). It runs a generation pass with enforced formatting (one idea per line, no justification), then a dedup pass (semantic similarity), then a cluster-and-score pass. Output is a scored shortlist (top 5-10) with cluster labels, ready for human review. The human selects finalists and the agent generates one-line implementation notes per finalist.

### Recommended subagents
- `faion-brainstorm` — purpose-built for structured diverge/converge; use when full multi-round review is needed
- General Claude Opus call — for raw generative passes where creativity > structure

### Prompt pattern
Diverge pass:
```
Generate <N> distinct ideas for: <PROBLEM_STATEMENT>.
Constraints: <CONSTRAINTS if any>.
Format: numbered list only. No explanations. No duplicates.
```

Reverse brainstorm pass:
```
List <N> ways to make <PROBLEM_AREA> as bad as possible.
Be specific. Format: numbered list only.
Then reverse each item into a solution in a second numbered list.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jq` | Parse and deduplicate JSON idea lists from agent output | Built-in most Unix systems |
| `sentence-transformers` (Python) | Semantic deduplication of idea lists | `pip install sentence-transformers` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Miro | SaaS | Partial — REST API | Sticky-note creation via API; cluster grouping is manual |
| Notion | SaaS | Yes — REST API | Ideal for logging scored idea shortlists |
| Linear | SaaS | Yes — REST API | Convert top ideas directly into backlog issues |
| Airtable | SaaS | Yes — REST API | Tabular idea scoring with weighted formula columns |

## Templates & scripts
See `templates.md` for the Brainstorm Session Plan template.

Semantic dedup pipeline (Python, ~30 lines):
```python
from sentence_transformers import SentenceTransformer, util

def semantic_dedup(ideas: list[str], threshold: float = 0.82) -> list[str]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(ideas, convert_to_tensor=True)
    keep = []
    dropped = set()
    for i in range(len(ideas)):
        if i in dropped:
            continue
        keep.append(ideas[i])
        for j in range(i + 1, len(ideas)):
            if j not in dropped:
                sim = float(util.cos_sim(embeddings[i], embeddings[j]))
                if sim >= threshold:
                    dropped.add(j)
    return keep
```

## Best practices
- Always separate the generation prompt from the evaluation prompt — same-call mixing causes premature pruning.
- Inject domain constraints into the generation prompt rather than the evaluation prompt: "ideas must be implementable by a 2-person team" up front produces better raw lists than filtering later.
- Run a Reverse Brainstorm variant on the same problem as a sanity check — if the negatives are hard to reverse into positives, the problem framing may be wrong.
- Store raw idea lists (pre-dedup, pre-score) in a scratch doc for future re-use; today's rejected idea may be valuable in a different context.

## AI-agent gotchas
- "Brainwriting simulation" (agent pretends to be 6 different people passing ideas) consistently produces less diverse output than a single well-seeded prompt with persona injection.
- Dot voting by the same agent that generated the ideas is circular — the agent will favor ideas it generated with higher confidence.
- Human checkpoint required before finalizing shortlist: the agent's semantic clustering can silently merge two distinct viable ideas into one cluster, eliminating a viable option.
- Long idea lists (50+) that get passed to a scoring prompt often see the first 10-15 ideas scored more generously due to positional bias.

## References
- Osborn, A. (1953). Applied Imagination.
- Stanford d.school Brainstorming Rules: https://dschool.stanford.edu/resources/brainstorm-rules
- IDEO Design Thinking: https://www.ideo.com/post/design-thinking-methods
- `sentence-transformers` docs: https://www.sbert.net
