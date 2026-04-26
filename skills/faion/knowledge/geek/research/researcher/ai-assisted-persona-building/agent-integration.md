# Agent Integration — AI-Assisted Persona Building

## When to use
- Building initial personas from an existing body of user data (analytics, CRM, interview transcripts)
- Updating stale personas when new behavioral data or cohort segments emerge
- Generating JTBD statements from clustered behavioral patterns
- Creating persona drafts as a starting point for a team workshop (human refinement required)
- When product team is operating from pure assumption-based personas and needs a data-grounded alternative

## When NOT to use
- When no actual user data exists — without data, the result is a synthetic persona (see `synthetic-users`), not a data-driven persona
- As a final deliverable without team validation — AI clusters need human labeling and context
- When the user base is too homogeneous (single segment, clear dominant use case) — clustering adds overhead without insight gain
- For high-stakes segmentation decisions (pricing tiers, feature gating) without statistical validation of cluster stability

## Where it fails / limitations
- K-means and similar clustering algorithms require a predefined number of clusters; agents choosing k arbitrarily produce misleading persona counts
- Behavioral data from analytics tools (Mixpanel, Amplitude) captures what users do, not why — JTBD inference from behavioral data alone is unreliable
- Personas built primarily from digital behavior underrepresent users who are active offline or on channels the product does not track
- AI-generated persona narratives tend toward archetypes, not individuals — the "busy startup founder" persona tells engineers what they already assume
- Persona drift: if data is not refreshed, personas become outdated and mislead roadmap decisions within 6-12 months

## Agentic workflow
A three-stage pipeline: Haiku ingests and structures raw behavioral data from analytics exports or CRM dumps; Opus applies clustering logic and identifies behavioral segment boundaries; Sonnet generates narrative persona documents, JTBD maps, and pain-point summaries per cluster. Human review between Opus (clusters) and Sonnet (narratives) is mandatory — a researcher must name and validate each cluster before it becomes a persona.

### Recommended subagents
- `faion-sdd-executor-agent` — orchestrates multi-stage data pipelines with quality gates between clustering and narrative generation
- General Claude subagent (Haiku) — data ingestion, normalization, frequency counts
- General Claude subagent (Opus) — behavioral pattern recognition, cluster boundary identification
- General Claude subagent (Sonnet) — persona narrative, JTBD statement generation, pain-point synthesis

### Prompt pattern
```
You are a UX researcher building data-driven personas.
I have behavioral data for [N] users across these dimensions: [list dimensions].
The data is: [paste CSV or JSON sample, or summary statistics]

Step 1: Identify 3-5 distinct behavioral clusters. For each cluster:
- Label it with a descriptive name (not a demographic label)
- List the 3 most distinctive behavioral signals
- Estimate what % of users fall into this cluster

Step 2: For each cluster, generate a persona with:
- Name and archetype label
- Primary JTBD: "When [situation], I want to [motivation], so I can [outcome]"
- Top 3 pain points (with quantified impact if data supports it)
- Trigger analysis: what event causes them to seek this product?

Flag any cluster where the behavioral signals could plausibly represent 2 different user types.
```

```
Given this persona draft: [paste persona]
Identify which attributes are data-derived vs. assumed.
For each assumed attribute, either:
(a) suggest a data source that could validate it, or
(b) flag it as an untested hypothesis.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Python + scikit-learn | K-means / DBSCAN clustering on behavioral data | `pip install scikit-learn pandas` |
| Python + umap-learn | Dimensionality reduction for high-dim behavioral vectors | `pip install umap-learn` |
| Amplitude CLI / API | Export behavioral cohort data for clustering | developers.amplitude.com |
| Mixpanel Data Export API | Export user-level event data | developer.mixpanel.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amplitude | SaaS | Yes (API) | Behavioral cohort export; Amplitude AI has built-in persona suggestions |
| Mixpanel | SaaS | Yes (API) | User-level event export; strong for behavioral clustering inputs |
| Heap | SaaS | Yes (API) | Auto-capture behavioral data; persona export via API |
| Dovetail | SaaS | Yes (API) | Qualitative data repository; links research insights to persona attributes |
| Maze | SaaS | No | Usability test behavioral data; no API for persona output |
| Hotjar | SaaS | Partial | Session recordings + heatmaps; limited API for behavioral data export |
| Xtensio | SaaS | No | Persona documentation; no API; human-facing templates only |
| UXPressia | SaaS | No | Persona + journey mapping tool; no agent-accessible API |

## Templates & scripts
Clustering pipeline for persona building (Python, inline):
```python
# persona_cluster.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def cluster_users(csv_path: str, n_clusters: int = 4) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    features = df.select_dtypes(include="number")
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled)

    # Cluster summary
    summary = df.groupby("cluster")[features.columns].mean()
    summary["user_count"] = df.groupby("cluster").size()
    return summary

summary = cluster_users("user_events.csv", n_clusters=4)
print(summary.to_markdown())
```

## Best practices
- Always combine behavioral data (what users do) with qualitative data (why they do it); behavioral-only personas miss motivation and are not actionable for copy or feature design
- Validate cluster stability by running clustering 3 times with different random seeds — if cluster membership changes significantly, the segments are not robust
- Use descriptive behavioral labels for clusters ("Power users who export weekly") not demographic labels ("35-45 year old managers") — demographic labels introduce bias
- Present personas in a team workshop before use; the act of naming and discussing personas surfaces assumptions that the data cannot validate
- Include a "persona retirement date" in the document — personas without expiry become organizational mythology

## AI-agent gotchas
- Agents generating JTBD statements from behavioral data alone will fabricate motivations; always require the agent to cite a data point or flag the statement as inferred
- Cluster count (k) is a human decision, not an agent decision — agents given free choice will pick the number that makes the narrative cleanest, not the number statistically justified by the data
- LLMs produce persona narratives that sound authoritative regardless of data quality; weak input data produces confident-sounding but unreliable personas
- Human checkpoint mandatory between cluster identification and narrative generation — the researcher labels clusters before the agent writes about them
- Persona documents generated by agents should be version-controlled and tagged with the data snapshot date; undated personas cannot be audited for staleness

## References
- https://www.nngroup.com/articles/persona-types/ (archetypes vs. data-driven)
- https://www.producttalk.org/2021/09/personas/ (Teresa Torres on assumption-based vs. data-driven)
- Pruitt, J. & Adlin, T. — The Persona Lifecycle (2006)
- https://amplitude.com/blog/user-personas
- https://heap.io/topics/user-personas
