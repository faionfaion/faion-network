# Golden Set Curation and Maintenance

## Summary

**One-sentence:** Curates 50-200 hand-labelled I/O pairs (stratified buckets + anti-output + incident-derived growth + quarterly drift audit + versioned promotion) as the anchor dataset for AI-feature regression eval.

**One-paragraph:** Curates 50-200 hand-labelled I/O pairs (stratified buckets + anti-output + incident-derived growth + quarterly drift audit + versioned promotion) as the anchor dataset for AI-feature regression eval. The methodology pins the artefact shape, ties every conclusion to a rule, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- AI-feature shipped до production з measurable correctness criteria.
- Регулярні regressions: model swap, prompt change, schema migration — потрібен anchor.
- Incident-driven growth: кожен production-bug → golden-set candidate.
- Quarterly drift audit: 10-20% items застаріває за квартал — потрібен retire-loop.
- Eval-pipeline gate: CI blocks merge коли golden-set score regresses >X%.

## Applies If (ALL must hold)

- AI feature is shipped or near-shipping into a non-AI product.
- Feature has measurable correctness criteria (not just vibes).
- Team owns the model boundary (input + output schema).
- Production logging captures inputs + outputs with PII-safe redaction.
- Team is willing to spend ~1 engineer-week to seed the initial set.

## Skip If (ANY kills it)

- Pre-prototype unstable schema — golden items rot daily.
- Pure exploratory research with no production-deploy plan.
- Creative-content output without consensus correctness (poetry, brand copy).
- Existing RAG-eval framework already covers golden-set discipline.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature input/output schema | JSON Schema / Protobuf | Eng team |
| Production log sample | JSONL / parquet (PII-safe) | Logging pipeline |
| Incident channel | PagerDuty / Slack / ticketing export | Ops team |
| `golden/` directory in repo | Git directory | Eng team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source + skip rule | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/05-examples.xml` | essential | Worked example end-to-end (input → output) | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-golden-set-curation-and-maintenance` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | Markdown spec skeleton — sections + acceptance criteria slots |
| `templates/spec-instance.json` | Instance of a filled spec (machine-readable mirror) |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-golden-set-curation-and-maintenance.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/ai/ml-engineer/AGENTS.md`
- [[shadow-traffic-rollout-pattern]]
- [[llm-hallucination-test-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
