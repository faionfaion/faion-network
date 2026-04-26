# Agent Integration — AI-Assisted Persona Building (geek/researcher variant)

## Note on scope
This methodology overlaps significantly with `ai-assisted-persona-building` in the same directory. The distinction is emphasis: this file focuses on the AI-agent execution layer — how to automate the data ingestion, clustering, and narrative generation pipeline end-to-end. For the broader methodology, decision criteria, and team workshop context, see `../ai-assisted-persona-building/agent-integration.md`.

## When to use
- Automating persona generation as part of a recurring research pipeline (e.g., monthly cohort refresh)
- Building personas programmatically from large user datasets (> 1,000 users) where manual review is infeasible for the clustering step
- Running JTBD map generation at scale across multiple product areas or markets simultaneously
- Integrating persona data into a downstream agent system (copywriting agent, feature-priority agent) that needs structured persona inputs

## When NOT to use
- One-off persona creation for a single product decision — use `ai-assisted-persona-building` with direct team involvement
- When data quality is unknown — run data audit before feeding into the pipeline
- When personas will be presented to external stakeholders without human review of the narrative layer

## Where it fails / limitations
- Pipeline automation removes the human review step that catches cluster misinterpretations; outputs can be confidently wrong
- Recurring automated pipelines produce persona drift alerts that require human triage; without triage, stale personas accumulate
- JTBD generation from behavioral data alone produces statements that describe usage patterns, not underlying motivations — motivations require qualitative input
- Automated pipelines are brittle to schema changes in the upstream data source (Amplitude, Mixpanel export format changes break ingestion)

## Agentic workflow
A fully automated pipeline: Haiku ingests behavioral event exports via API (Amplitude, Mixpanel, Heap), normalizes them to a feature matrix, and computes cluster centroids. Opus validates cluster separability and generates a cluster report. Sonnet transforms validated clusters into persona documents, JTBD maps per persona, and a pain-point summary. Results are written to a JSON schema that downstream agents (copywriting, feature-priority) can consume directly. A human approval gate sits between Opus (cluster validation) and Sonnet (narrative generation).

### Recommended subagents
- `faion-sdd-executor-agent` — manages the multi-stage pipeline with quality gates and retry logic
- General Claude subagent (Haiku) — data ingestion, normalization, feature matrix construction
- General Claude subagent (Opus) — cluster separability analysis, coverage validation, governance checks
- General Claude subagent (Sonnet) — persona narrative, JTBD statements, pain-point summary generation

### Prompt pattern
```
You are a data analyst building user personas from behavioral data.
Input: feature matrix with [N] users and [M] behavioral dimensions.
[paste or reference data]

Task:
1. Identify [3-5] behavioral clusters using the provided feature matrix summary.
2. For each cluster, list:
   - Dominant behavioral signals (top 3 features by variance from mean)
   - Estimated user count and % of total
   - A descriptive cluster label (behavior-based, not demographic)
3. Flag any cluster with fewer than 50 users as "fragile" — insufficient for generalization.
4. Flag any two clusters with >70% feature overlap as "potentially redundant."
Output: JSON array of cluster objects.
```

```
Given validated clusters: [paste JSON]
Generate a persona document for cluster "[label]":
{
  "name": "...",
  "archetype_label": "...",
  "jtbd": "When [situation], I want to [motivation], so I can [outcome].",
  "pain_points": [{"pain": "...", "frequency": "high/medium/low", "impact": "high/medium/low"}],
  "trigger": "...",
  "data_confidence": "H/M/L",
  "assumptions": ["list any attributes not directly supported by behavioral data"]
}
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| Python + scikit-learn | K-means, DBSCAN, silhouette scoring for cluster validation | `pip install scikit-learn pandas numpy` |
| Python + umap-learn | UMAP dimensionality reduction for visualization | `pip install umap-learn matplotlib` |
| Amplitude Data Export API | Pull user-level event data for clustering | developers.amplitude.com/docs/export-api |
| Mixpanel Export API | Pull raw event streams per user | developer.mixpanel.com/reference/export |
| Heap Connect | Export behavioral data to S3/warehouse | heap.io/docs/heap-connect |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amplitude | SaaS | Yes (API) | Best-in-class behavioral export; cohort API; Amplitude AI persona suggestions |
| Mixpanel | SaaS | Yes (API) | Strong for event-level export; JQL for custom behavioral queries |
| Heap | SaaS | Yes (API) | Auto-capture reduces instrumentation gaps; Heap Connect exports to data warehouse |
| Dovetail | SaaS | Yes (API) | Qualitative layer; attach interview clips to persona attributes |
| Segment | SaaS | Yes (API) | CDP; aggregates behavioral data from all sources into one schema |
| dbt (OSS) | OSS | Yes (CLI) | Transform raw event data into clustering-ready feature tables |

## Templates & scripts
Cluster validation + silhouette scoring (Python, inline):
```python
# validate_clusters.py
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def find_optimal_k(X: np.ndarray, k_range: range = range(2, 8)) -> dict:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    results = {}
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(X_scaled)
        sil = silhouette_score(X_scaled, labels)
        results[k] = round(sil, 3)
    best_k = max(results, key=results.get)
    return {"scores": results, "recommended_k": best_k}

# Silhouette score > 0.5 = strong clusters
# 0.25-0.5 = moderate, proceed with caution
# < 0.25 = weak, reconsider feature selection
```

## Best practices
- Always run silhouette scoring or elbow method before fixing k — never accept an agent's arbitrary k choice
- Store the persona JSON schema in version control; downstream agents depend on a stable schema and schema changes break them silently
- Tag each persona attribute as `data_derived` or `assumed`; downstream agents must not treat assumed attributes as facts
- Set a persona refresh cadence (monthly or quarterly) and automate drift detection by comparing new cluster centroids against stored ones; flag > 15% centroid shift for human review
- Keep a persona changelog: date, data snapshot version, k, silhouette score, and a one-line summary of what changed

## AI-agent gotchas
- Fully automated pipeline without a human gate between clustering and narrative generation is high-risk: a bad cluster produces a confidently-written persona that gets adopted without scrutiny
- Agents generating JTBD statements from behavioral data without qualitative input will produce feature-descriptions dressed as motivations; they are not equivalent
- Schema changes in Amplitude/Mixpanel exports silently break the ingestion step; add schema validation at the pipeline entry point
- When silhouette scores are low (< 0.3), agents should abort and surface the issue rather than proceeding — pipeline auto-retry on weak clusters compounds the error
- Human checkpoint: cluster validation is non-negotiable before narrative generation

## References
- https://www.nngroup.com/articles/persona-types/
- https://scikit-learn.org/stable/modules/clustering.html#silhouette-analysis
- https://amplitude.com/blog/user-personas
- https://developers.amplitude.com/docs/export-api
- https://heap.io/docs
