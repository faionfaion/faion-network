# Agent Integration — Brainstorming Techniques

## When to use
- Generating a large idea set for a specific, well-defined problem (product name, feature list, risk audit)
- Running asynchronous remote ideation where participants write before discussing
- Breaking a creative block with structured diverge → converge cycles
- Exploring negatives via Reverse Brainstorming when stakeholders are too polite to surface risks directly

## When NOT to use
- Convergence and decision-making phase — brainstorming is divergent only; run a separate evaluation step
- Solo ideation with a single narrow constraint; SCAMPER or direct prompting works better
- When the "problem" is actually a predefined requirement masquerading as an open question
- Time-critical triage where idea quantity is irrelevant

## Where it fails / limitations
- AI-generated idea lists tend to cluster around obvious solutions; second-pass prompting is required to force weird/wild ideas
- Deferred judgment principle breaks down when the LLM ranks or filters in the same pass that generates
- Classic Brainstorming (6-3-5) assumes a fixed group; agent must simulate multiple personas, which can produce homogeneous output
- No real group dynamics: the "energy dip" recovery techniques (change method, take break) don't apply to single-agent runs
- Quantity ≠ quality; agent can hit 108 ideas in seconds, but clustering and scoring become the bottleneck

## Agentic workflow
A subagent receives a problem statement and a technique selector (classic / brainwriting / round-robin / reverse). It generates ideas in a structured bulk pass, then clusters via semantic grouping in a second pass. A third pass scores clusters against an impact/effort rubric and returns a shortlist. The facilitator-script logic (Osborn's 4 rules, silence cues) is embedded in the system prompt, not in conversation turns.

### Recommended subagents
- `faion-brainstorm` — structured diverge/converge cycles; use for multi-round ideation with review gate
- General Claude Opus call — for generating wild-idea batches where novelty matters more than structure

### Prompt pattern
```
Generate exactly 30 ideas for: <PROBLEM>.
Rules: no criticism, quantity over quality, wild ideas encouraged.
Format: numbered list only. No explanations.
```

Second-pass clustering:
```
Cluster these 30 ideas into 5-7 themes.
For each theme: name, 3-5 member ideas, one-line rationale.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `miro-cli` (unofficial) | Programmatic Miro board creation for remote brainstorm boards | npm: `miro-api` SDK |
| `obsidian-mcp` | Write clustered ideas as notes with backlinks | MCP server for Obsidian |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Miro | SaaS | Partial — REST API for boards/cards | Agent can create sticky notes, but real-time cursor presence is human-only |
| MURAL | SaaS | Partial — REST API | Similar to Miro; session management limited |
| Stormboard | SaaS | No API | Human-only |
| Excalidraw | OSS | Via JSON import | Agent can generate JSON scene files; no live session support |

## Templates & scripts
See `templates.md` for the Brainstorm Session Plan and Remote Setup templates.

Inline utility — bulk idea deduplication:
```python
# Remove near-duplicate ideas from a brainstorm list (simple Jaccard)
def dedup_ideas(ideas: list[str], threshold: float = 0.5) -> list[str]:
    from itertools import combinations
    def jaccard(a: str, b: str) -> float:
        sa, sb = set(a.lower().split()), set(b.lower().split())
        return len(sa & sb) / len(sa | sb) if sa | sb else 0.0
    keep = list(ideas)
    to_remove = set()
    for i, j in combinations(range(len(keep)), 2):
        if i not in to_remove and jaccard(keep[i], keep[j]) >= threshold:
            to_remove.add(j)
    return [idea for idx, idea in enumerate(keep) if idx not in to_remove]
```

## Best practices
- Split the prompt into two calls: pure generation (no evaluation language), then pure clustering. Mixing them causes premature convergence.
- Use Reverse Brainstorming first when stakeholders resist criticism — "How would we destroy this product?" gets honest answers.
- For impact/effort scoring: weight impact 3x, feasibility 2x; keep cost/time at 1x to avoid over-optimizing for cheapness.
- Seed the brainwriting pass with one "wild" idea per round to prevent the LLM settling on safe output.
- When simulating multiple personas in Round Robin, assign specific roles (skeptic, optimist, user, engineer) rather than anonymous "person N".

## AI-agent gotchas
- LLMs default to evaluation language ("this is a good idea because...") even when prompted not to — enforce format strictly (numbered list, no justification).
- The "108 ideas from 6-3-5" calculation is theoretical; agent-generated ideas plateau in novelty around 30-40 without persona switching or domain constraint injection.
- Dot voting in an automated context requires a separate agent or human in the loop — never let the generating agent also vote, as it will favor its own first-pass ideas.
- Human checkpoint required before moving from cluster to scoring: the agent's semantic clustering can merge genuinely distinct ideas with similar wording.
- Large idea lists (100+) hit context limits during the scoring pass; chunk into 25-idea batches with accumulated scoring state.

## References
- Osborn, A. (1953). Applied Imagination
- Stanford d.school Brainstorming Rules: https://dschool.stanford.edu/resources/brainstorm-rules
- IDEO Brainstorming Guide: https://www.ideou.com/blogs/inspiration/how-to-brainstorm
- Miro REST API: https://developers.miro.com/reference/api-reference
