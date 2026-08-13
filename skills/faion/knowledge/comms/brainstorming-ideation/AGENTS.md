# Brainstorming Ideation (Agentic Pipeline)

## Summary

**One-sentence:** Generates a scored idea shortlist via an agentic pipeline (diverge → semantic dedup → cluster → impact-effort score) seeded with persona injection for diversity.

**One-paragraph:** Brainstorming-ideation is the agent-pipeline twin of brainstorming-techniques. Where the latter facilitates a human session, this methodology runs a programmatic pipeline: prompt-driven divergence (Classic / Reverse), semantic deduplication via embeddings, theme clustering, impact-effort scoring, and persona injection (3-5 personas) to diversify exploration. Output is a scored shortlist JSON consumable by PMs or downstream automation.

**Ефективно для:**

- Solo founder wanting a structured idea sweep without booking a workshop.
- Pre-workshop divergence to seed a human session with non-obvious candidates.
- Generating 50-200 candidate angles for a marketing or product brief.
- Auditing a roadmap for under-explored corners via persona injection.

## Applies If (ALL must hold)

- Problem statement is open-ended enough for ≥30 candidate ideas.
- Operator can run an LLM with embeddings (cluster step requires it).
- Downstream consumer of the shortlist is named (PM, founder, marketer).
- Persona inputs are available or generatable.

## Skip If (ANY kills it)

- Decision is between 2-3 known options — use evaluation methodology instead.
- Confidentiality forbids sending the problem to an LLM.
- Group facilitation is actually needed for buy-in — use brainstorming-techniques.
- Embedding/cluster tooling unavailable — fall back to manual brainstorming-techniques.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement | 1-3 sentences, open-ended | founder / PM |
| Personas | 3-5 personas (role + need) JSON | research / persona file |
| Embedding endpoint | URL + key for cluster step | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[brainstorming-techniques]] | sister methodology — pick this when human facilitation is unavailable |
| [[ideation-methods]] | downstream — SCAMPER on top of the shortlist if needed |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routes by observable signal to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `divergence-prompt` | sonnet | Persona-conditioned creative generation. |
| `semantic-dedup` | haiku | Embedding + threshold merge — mechanical. |
| `cluster-naming` | sonnet | Theme labeling needs judgment. |
| `impact-effort-score` | sonnet | Calibration judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-diverge.txt` | Persona-conditioned divergence prompt (Classic branch) |
| `templates/prompt-reverse.txt` | Persona-conditioned Reverse-brainstorm prompt |
| `templates/semantic-dedup.py` | Embedding-based dedup utility with cosine threshold |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-brainstorming-ideation.py` | Validate brainstorming-ideation artefact against the schema | CI on each artefact change; pre-commit |

## Related

- [[brainstorming-techniques]]
- [[ideation-methods]]
- [[stakeholder-communication]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on persona-count, raw_count, and cluster band; each gate failure routes to a specific repair rule before continuing to scoring.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prompt-diverge.txt`

```text
Generate <N> distinct ideas for: <PROBLEM_STATEMENT>.
Constraints: <CONSTRAINTS — e.g., "must be implementable by a 2-person team in one sprint">
Perspectives to include: skeptic, optimist, first-time user, engineer (inject at least one idea from each).
Format: numbered list only. One idea per line. No explanations. No duplicates.
Do NOT evaluate, rank, or justify any idea in this pass.
```

### `templates/prompt-reverse.txt`

```text
PASS 1 — Inversion:
List <N> specific ways to make <PROBLEM_AREA> as bad as possible.
Be specific. Format: numbered list only. No explanations.

PASS 2 — Reversal:
For each item in the inversion list, write the corresponding positive mitigation.
Format: two-column numbered list: [negative idea] → [reversed solution].
Run as two separate calls. Do not combine passes.
```

### `templates/semantic-dedup.py`

```python
"""
Semantic deduplication for brainstorming idea lists.
Removes near-duplicate ideas using sentence-transformers cosine similarity.

Install: pip install sentence-transformers
Usage:
  ideas = ["Automate onboarding email", "Send automated onboarding emails", "Build a kanban board"]
  unique = semantic_dedup(ideas, threshold=0.82)
"""

from sentence_transformers import SentenceTransformer, util


def semantic_dedup(ideas: list[str], threshold: float = 0.82) -> list[str]:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(ideas, convert_to_tensor=True)
    keep: list[str] = []
    dropped: set[int] = set()

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
