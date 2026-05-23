<!--
purpose: human-readable decision record for fine-tune vs prompt/RAG/route choice.
consumes: numbers populated into the inline frontmatter JSON block.
produces: a one-page artefact stored in the team's RFC log.
depends-on: decision-record.schema.json validator.
token-budget-impact: ~600 tokens per filled record.
-->

# Fine-tune Cost vs Prompt Decision — <workload>

**Owner:** <name + email>
**Created:** <YYYY-MM-DD>   **Recheck:** <YYYY-MM-DD ≤ 6mo>
**Lift bar (pre-committed):** <e.g. +0.03 F1>
**Recommendation:** `<fine-tune|prompt-improve|rag|route|hybrid>`

## Baseline

| Metric | Value |
|---|---|
| eval score | <0.78> |
| $/k tokens | <3.0> |
| daily volume | <50000> |

## Candidate (fine-tune)

| Metric | Value |
|---|---|
| training cost | <800> |
| hosting $/k | <0.5> |
| training examples | <6500> |
| pilot lift | <+0.02> |

## Break-even math

`break_even_months = (training_cost + ops_overhead) / (Δ_cost_per_k * volume_per_k * 30)`

→ <X.X months>

## Strong signals (need ≥2 for fine-tune)

- [ ] format-adherence problem prompt can't solve
- [ ] latency-critical workload
- [ ] data-volume-5k+ (≥ 5,000 high-quality examples)
- [ ] safety/policy domain
- [ ] cost amortises within 12 months

## Narrative

<2-3 paragraphs: what we tried, what the numbers say, what could change at recheck.>

## Sign-off

- Product owner: <name>  (sets lift_bar)
- Eng manager: <name>    (signs `owner`)
