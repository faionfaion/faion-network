# AI Content Strategy

## Summary

**One-sentence:** Spec for an AI+human content pipeline where AI handles research, outlines, and drafts while humans add experience, proprietary data, and opinions — gated by E-E-A-T checks and a hard human approval before publish.

**One-paragraph:** AI-only content aggregates the top 10 search results without new insight; Google's Helpful Content Updates actively deprioritise it. This methodology specifies the six-stage workflow (AI research → human enrichment → AI draft → human voice/opinion → AI SEO → human approval), the mandatory human-approval gate before publish, and the E-E-A-T signal floor every piece must clear. Output is a published spec the content team and the agentic pipeline both read from.

**Ефективно для:** B2B content teams shipping >10 pieces/week with AI drafts; solo founders running an editorial cadence; agencies needing a repeatable AI+human gate.

## Applies If (ALL must hold)

- Building or running a multi-channel content pipeline with AI drafts
- Editorial cadence ≥10 pieces/week and human review capacity is the bottleneck
- Brand voice guide exists with concrete examples
- Conversion / ranking is a goal, not just volume

## Skip If (ANY kills it)

- Breaking news / time-sensitive commentary — AI draft + review cycle is too slow
- Highly regulated content (medical / legal / financial) — compliance risk overrides
- Personal brand content needing genuine first-person voice — AI cannot generate it
- Brand voice still undefined — AI amplifies generic 'marketing voice'

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Brand voice guide with examples | Markdown | marketing repo |
| Topic brief with target ICP | Markdown | editorial planner |
| Asset library: expert quotes, proprietary data, case studies | YAML / wiki | content ops |
| Approval-gate workflow (n8n / approval queue) | Workflow file | automation stack |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/marketing/content-marketer` | parent role skill |
| [[anti-slop-rubric]] | rubric for every published piece |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `research_outline_draft` | sonnet | Bounded synthesis from research notes |
| `seo_optimisation_pass` | haiku | Mechanical: apply Surfer/MarketMuse suggestions |
| `brand_voice_review` | opus | Cross-section synthesis; high-stakes voice check |

## Templates

| File | Purpose |
|------|---------|
| `templates/content-brief.md` | AI content prompt template with role/constraints/context/task/output |
| `templates/differentiation-checklist.md` | Pre-publish checklist: generic signals out, differentiation signals in |
| `templates/eeat-enhancement.md` | Template for adding Experience / Expertise / Authoritativeness / Trust signals |
| `templates/_smoke-test.md` | Minimum-viable filled brief |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-content-strategy.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/marketing/`
- [[ai-marketing-tools-stack-2026]]
- [[anti-slop-rubric]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-content-strategy applies: root question — "Is the editorial cadence ≥10 pieces/week with AI drafting AND brand voice codified?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-role-division, r2-no-prompt-and-publish, r3-differentiation-signal-floor, r4-brand-voice-pinned, r5-channel-native-repurposing, r6-claim-verification.
