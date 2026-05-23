# AI-Assisted Lessons-Learned Synthesis

## Summary

**One-sentence:** AI-assisted synthesis of multi-project retro corpora into a 2-3 page lessons-learned report with verbatim citations, themed clusters, and named-owner action items.

**One-paragraph:** AI-Assisted Lessons-Learned Synthesis produces a report artefact for the sdlc-ai domain. It pins observable preconditions, scores candidate decisions against ≥5 testable rules, fails fast on disqualifiers, and emits a schema-validated output. The methodology routes between apply and skip-this-methodology via an explicit decision tree so downstream agents never run it on an unsuitable input.

**Ефективно для:**

- Annual / semi-annual lessons-learned review across ≥ 5 written retros.
- Multi-project programme where retros are heterogeneous and manual synthesis takes days.
- Delivery-process maturity audits that need traceable evidence per claim.
- Knowledge-transfer for new leadership inheriting a retro corpus.

## Applies If (ALL must hold)

- ≥ 5 project retros from the past 18 months in searchable text format.
- Retros are written (not verbal-only) and have minimal structure (what went well / didn't / actions).
- Project manager or delivery lead owns the synthesis and signs the final.
- LLM API access (Claude or equivalent) and a sample budget exists.

## Skip If (ANY kills it)

- < 5 retros — sample too small for honest clustering.
- Retros only verbal / on whiteboards — start with the retro-writing methodology first.
- Single team, single project — manual synthesis is faster than tooling setup.
- HR-adjacent or IP-dispute retro content — keep manual; never feed to LLM.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Retro corpus | Markdown / PDF / HTML / Notion exports | team archive |
| Synthesis audience profile | 1-paragraph note | PM / leadership |
| LLM access + budget | API key + cost ceiling | ops |
| Past synthesis baseline | previous year's lessons-learned doc | archive |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[kb-codebase-rag-symbol-chunked]] | RAG pattern adapted for retro corpora |
| [[kb-versioned-agent-memory-files]] | Memory of previous synthesis informs next cycle |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-rule + rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom/root-cause/fix) | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with decision gates | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion ref=rule-id | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `retro_ingestion_and_dedup` | sonnet | Per-doc parsing + near-duplicate detection. |
| `theme_clustering` | opus | Cross-doc synthesis, semantic grouping. |
| `severity_recurrence_scoring` | sonnet | Per-theme deterministic scoring. |
| `action_item_proposal_with_owner` | opus | Cross-theme reasoning + org knowledge. |
| `executive_summary_draft` | sonnet | Templated narrative compression. |

## Templates

| File | Purpose |
|------|---------|
| `templates/synthesis-doc.md` | Final 2-3 page synthesis structure |
| `templates/themed-appendix.md` | Long-form appendix with theme deep-dives |
| `templates/action-item-table.md` | Action items with owners + deadlines |
| `templates/source-citation-format.md` | Verbatim quote → retro source schema |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-lessons-learned-synthesis.py` | Verify every theme has ≥ 2 verbatim quotes + traceable sources | pre-publication |

## Related

- [[kb-ai-assisted-quarter-retro-synthesis]]
- [[kb-versioned-agent-memory-files]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (precondition flag, repo metric, capability flag) and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on a rule that triggers the procedure or on `skip-this-methodology`.
