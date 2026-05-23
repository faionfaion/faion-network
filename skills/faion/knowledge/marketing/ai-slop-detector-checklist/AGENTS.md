# AI Slop Detector Checklist

## Summary

**One-sentence:** Generates a binary slop-or-ship score for an AI-drafted blog post — generic intro, hedging, factual grounding, original signal, formatting tics — gated by ≥80 / 100 to ship.

**One-paragraph:** AI drafts ship to production with generic intros, hedging ('it's important to note'), zero original signal, and Wikipedia-flavour formatting. Google E-E-A-T and humans both notice. This methodology scores a draft against 5 dimensions (originality, specificity, grounding, voice, formatting tics) with a binary scoring rubric. Output: a SlopScore with category scores + ship/rework verdict.

**Ефективно для:**

- Solo marketer running role-growth-marketing/Blog post brief → AI draft → human polish.
- Content team where 'looks fine' was the only review.
- SEO posture where E-E-A-T signal must be defensible.
- Pre-publish QA gate before blog or newsletter publish.

## Applies If (ALL must hold)

- Draft was AI-generated (LLM) — at least 30% of the prose.
- Draft will publish to a domain serving paying customers OR optimising for organic search.
- Operator has 5+ minutes to score before publishing.
- Brand voice matters (not internal-only docs).

## Skip If (ANY kills it)

- Internal-only docs / changelogs with no customer audience.
- Personal blog with no SEO or brand voice goals.
- Already passed an editor-driven review at this depth.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| AI-drafted markdown | .md file | operator workflow |
| Brand voice doc | ≤500 word style guide | brand-voice methodology |
| Topic-specific facts / sources | linked list | operator research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| brand-voice-consistency-system | Voice dimension scoring consumes the brand voice doc. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-original-signal-required, r2-no-hedging-tics, r3-factual-grounding, r4-named-owner, r5-binary-ship-gate | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the AI Slop Detector Checklist artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: wikipedia-intro, hedging-everywhere, no-grounding, listicle-padding | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `score-draft` | sonnet | Per-dimension scoring against rubric. |
| `suggest-rewrites` | opus | High-stakes — original signal injection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-slop-detector-checklist.json` | SlopScore JSON skeleton. |
| `templates/ai-slop-detector-checklist.md` | Scoring rubric + rewrite suggestions. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-slop-detector-checklist.py` | Validate SlopScore JSON against the schema. | After scoring before publish. |

## Related

- [[brand-voice-consistency-system]]
- [[audience-to-customer-funnel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
