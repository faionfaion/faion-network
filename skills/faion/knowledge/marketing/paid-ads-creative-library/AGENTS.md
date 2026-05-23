# Paid Ads Creative Library

## Summary

**One-sentence:** Specifies a versioned + tagged creative library (asset, tag-taxonomy, performance, lineage) that survives campaign rotations and powers AI-assisted creative iteration.

**One-paragraph:** PPC manuals cover platform basics but not the meta-asset — the versioned tagged creative library — which is the 2026 paid-ads moat. This methodology specs library structure (asset_id, version, lineage_parent, tags, performance_metrics), tagging taxonomy (hook-type / offer / format / persona / funnel-stage), and the performance feedback loop (auto-tag winners; deprecate fatigued assets). Output: library spec + tag taxonomy + feedback-loop runbook.

**Ефективно для:**

- PPC manager з >= $2k/mo spend і > 3 campaigns шукає creative moat.
- AI-assisted creative iteration: треба versioned lineage для prompt-feed.
- Cross-platform reuse: Meta winner → LinkedIn variant без перебудови.
- Onboarding нового creative-vendor зі стандартизованим tagging.

## Applies If (ALL must hold)

- Paid-ads spend >= $2k/month.
- >= 3 active campaigns OR >= 6 creative variants in rotation.
- Marketing owner with authority to standardize creative pipeline.
- Storage substrate available (Notion / Airtable / Frame.io / Drive)

## Skip If (ANY kills it)

- Spend < $2k/month — overhead exceeds value.
- Single creative variant — no lineage, no library needed yet.
- Owner unwilling to enforce tagging on upload — library decays without it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~900 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-paid-ads-creative-library` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton |
| `templates/output.json` | JSON spec sidecar with __faion_header__ |
| `templates/_smoke-test.md` | Minimum viable filled spec |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-paid-ads-creative-library.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
