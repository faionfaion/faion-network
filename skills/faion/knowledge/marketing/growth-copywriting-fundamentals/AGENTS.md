# Growth Copywriting Fundamentals

## Summary

**One-sentence:** Generates a copywriting spec — VoC research → formula (AIDA/PAS/BAB/4Ps) → 10 headline variants → benefit translation → CTA — so landing-page copy converts on persuasion fundamentals.

**One-paragraph:** Generates a copywriting spec — VoC research → formula (AIDA/PAS/BAB/4Ps) → 10 headline variants → benefit translation → CTA — so landing-page copy converts on persuasion fundamentals.

**Ефективно для:**

- Solo founder writing or rewriting landing-page copy.
- Ad / email campaign requiring headline variants at scale.
- Feature-to-benefit translation pass before launch.

## Applies If (ALL must hold)

- Writing or rewriting landing-page copy (hero, benefits, CTA, objection handling).
- Drafting email subject lines, ad copy, or social posts at scale.
- Converting feature lists into benefit-oriented messaging.
- Applying a specific formula (AIDA, PAS, BAB) to a defined piece.

## Skip If (ANY kills it)

- Brand voice is undefined — copy frameworks produce generic output without tone.
- Highly regulated content (pharma, legal, financial advice) — legal review first.
- Target audience research incomplete — copy applied to wrong ICP.
- Long-form editorial — copywriting is for persuasion, not journalism.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VoC research | json | customer review excerpts |
| ICP description | md | ICP doc |
| Brand voice doc | path | brand-voice-consistency-system output |
| Feature list | yaml | features with benefits |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice doc gates tone. |
| growth-content-marketing | Distribution context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-ten-headline-variants, r2-voc-language, r3-feature-to-benefit, r4-one-cta-per-section, r5-named-owner | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Growth Copywriting Fundamentals artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: first-headline-ships, feature-soup, cta-fatigue | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-growth-copywriting-fundamentals` | opus | High-stakes synthesis — sets the artefact baseline. |
| `validate-growth-copywriting-fundamentals` | sonnet | Bounded structural check against the output contract. |
| `review-growth-copywriting-fundamentals` | sonnet | Per-section critique against rules + failure modes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/growth-copywriting-fundamentals.json` | JSON skeleton matching the output contract. |
| `templates/growth-copywriting-fundamentals.md` | Markdown skeleton with required fields. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-growth-copywriting-fundamentals.py` | Validate Growth Copywriting Fundamentals output JSON against the schema. | After subagent returns, before downstream consumer reads. |

## Related

- [[brand-voice-consistency-system]]
- [[growth-content-marketing]]
- [[ai-content-quality-review]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
