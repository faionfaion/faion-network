# AI-Assisted Persona Building

## Summary

A three-stage pipeline for building data-driven personas from behavioral analytics data: Haiku ingests and normalizes event exports; Opus identifies cluster boundaries with silhouette validation; Sonnet generates persona narratives, JTBD maps, and pain-point summaries. A mandatory human gate sits between clustering and narrative generation — the researcher names and validates clusters before the agent writes about them.

## Why

Assumption-based personas mislead roadmap decisions. AI clustering surfaces behavioral segments that human intuition misses; JTBD integration replaces vague demographic labels with actionable motivation statements. Cluster stability validation (silhouette score, multi-seed runs) prevents the most common failure: confident personas built on statistically weak segments.

## When To Use

- Building initial personas from existing behavioral data (analytics, CRM, interview transcripts).
- Updating stale personas when new behavioral data or cohort segments emerge.
- Generating JTBD statements from clustered behavioral patterns.
- Automating persona refresh as part of a recurring monthly or quarterly pipeline.

## When NOT To Use

- When no actual user data exists — without data the result is a synthetic persona, not a data-driven one.
- As a final deliverable without team validation — AI clusters need human labeling and context.
- When the user base is too homogeneous — clustering adds overhead without insight gain.
- High-stakes segmentation (pricing tiers, feature gating) without statistical validation of cluster stability.

## Content

| File | What's inside |
|------|---------------|
| `content/01-method.xml` | Persona process, JTBD integration, modern components, limitations. |
| `content/02-agent-workflow.xml` | Three-stage pipeline, silhouette validation rules, prompt patterns, gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/persona-cluster.py` | K-means clustering on behavioral CSV with cluster summary output. |
| `templates/validate-clusters.py` | Silhouette scoring to find optimal k; flags weak clusters. |
| `templates/persona-prompt.txt` | Prompt for generating structured persona JSON from validated clusters. |
