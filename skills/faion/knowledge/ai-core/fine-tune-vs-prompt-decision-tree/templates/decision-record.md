<!--
purpose: human-readable 4-axis decision record (FT vs prompt+RAG+routing+distillation).
consumes: axis scores, alternative experiments, owner sign-off.
produces: a one-page artefact for the RFC log.
depends-on: decision-record.schema.json validator.
token-budget-impact: ~500 tokens per filled record.
-->

# Fine-tune vs Prompt+RAG Decision — <workload>

**Owner:** <name>      **Created:** <YYYY-MM-DD>
**Recommendation:** `<no-change|prompt-improve|rag|routing|distillation|fine-tune|hybrid>`

## Axes (1=below target, 5=well above)

| Axis | Score | Note |
|---|---|---|
| quality     | <1-5> | <one-line> |
| cost        | <1-5> | <one-line> |
| latency     | <1-5> | <one-line> |
| maintenance | <1-5> | <one-line> |

## Alternatives tried

| Alt | Lift | Status |
|---|---|---|
| prompt-improve | <±X> | <tried/untried/skipped> |
| rag            | <±X> | <tried/untried/skipped> |
| routing        | <±X> | <tried/untried/skipped> |
| distillation   | <±X> | <tried/untried/skipped> |

## Counter-case (required if FT)

<1 paragraph: what would make me wrong about this?>

## Revisit triggers (≥2)

- <trigger 1, observable>
- <trigger 2, observable>
