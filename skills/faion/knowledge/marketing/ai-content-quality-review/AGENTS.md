# AI Content Quality Review

## Summary

**One-sentence:** Generates a 7-section rubric pass — entity density, citation depth, original POV, intro tax, stat verification, ICP fit, snippet-readiness — so AI-drafted long-form ships only when it can rank.

**One-paragraph:** Generates a 7-section rubric pass — entity density, citation depth, original POV, intro tax, stat verification, ICP fit, snippet-readiness — so AI-drafted long-form ships only when it can rank.

**Ефективно для:**

- Solo founder shipping AI-drafted blog posts weekly.
- Newsletter operator publishing AI-assisted long-form.
- Pre-publish gate where Google AI Overviews + Perplexity will judge.

## Applies If (ALL must hold)

- Draft is substantially AI-generated (≥30% LLM tokens).
- Destination is indexable (blog, Substack, LinkedIn article, KB).
- Piece is ≥600 words.
- Primary ICP and target query are declared before review.

## Skip If (ANY kills it)

- Transactional micro-copy (CTA, error message).
- Verbatim founder transcript with light AI cleanup.
- Internal-only KB entry never indexed.
- Content already reviewed by a domain expert with sign-off.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Draft markdown | md | final-form file |
| ICP + target query | yaml | frontmatter or paired brief |
| Research notes | md | entities + citations + original observations |
| Image presence | bool | no-publish-without-image guard |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice doc gates tone. |
| content-atomization-engine | Atomized pieces also pass this rubric. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-entity-density-floor, r2-citation-depth-floor, r3-original-pov-required, r4-intro-tax-cap, r5-stat-verification | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the AI Content Quality Review artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: entity-thin, hallucinated-stats, intro-tax | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-ai-content-quality-review` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-ai-content-quality-review` | sonnet | Bounded structural check against the output contract. |
| `review-ai-content-quality-review` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-content-quality-review.json` | JSON skeleton matching the output contract. |
| `templates/ai-content-quality-review.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-content-quality-review.py` | Validate AI Content Quality Review output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[brand-voice-consistency-system]]
- [[content-atomization-engine]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
