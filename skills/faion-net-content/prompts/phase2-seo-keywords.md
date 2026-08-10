# Phase 2.0 — Semantic core + keyword research

You produce the `keywords.md` artifact that the writer, editor, and reviewers reference when authoring + auditing the article. This runs BEFORE the editorial brief is finalised (Phase 2.1) so the brief can declare the primary keyword and audience language.

## Inputs

- **Brief draft path**: `{{brief_path}}` (the working brief — read for thesis, audience, named framework).
- **Style guide**: `~/.claude/skills/faion-net-content/config/style-guide.md` — read § "SEO + LLM optimization".
- **Project positioning**: `/home/nero/workspace/projects/faion-net/AGENTS.md`.

## Investigation (mandatory ≥5 WebSearch)

You do real keyword research, not vibe-based guessing. Suggested queries (adapt to the brief's thesis):

1. The article's core problem stated as a question ("how to leave corporate engineering job", "indie hacker exit framework", "senior engineer to founder transition").
2. Long-tail variants ("safe way to quit tech job for startup", "should I leave my staff engineer job", "framework for going indie").
3. Audience-language forums:
   - Hacker News search for related threads (extract verbatim phrasings).
   - Indie Hackers post titles in the topic area.
   - Reddit subreddits (r/cscareerquestions, r/Entrepreneur, r/SaaS, r/Freelance).
   - X / Twitter threads from named founders in the space.
4. Competitor / authority articles — what are the top 5 articles currently ranking for the head term? What angle gaps exist?
5. Google's "People Also Ask" + autocomplete signals (search results pages — quote the suggestions).
6. Adjacent communities and what vocabulary they use (Designer News, Lobsters, Slow Indie, MicroConf).

Capture VERBATIM phrasings — the article should sound like the audience, not like a marketing team.

## Output schema

Write to `{{keywords_path}}` — `~/workspace/projects/faion-net/faion-net-fe/.aidocs/content/ultimate-guide/briefs/<slug>-keywords.md`:

```markdown
---
slug: <kebab-case>
generated_at: "<ISO-8601>"
primary_keyword: "<2-5 word head term>"
url_slug_suggestion: "<kebab-case URL match for primary keyword>"
---

# Keywords + semantic core: <slug>

## Primary keyword

`<2-5 word head term>` — the URL slug, the title's anchor, and the H1 should contain this phrase or a close paraphrase.

**Search intent**: <informational | navigational | commercial | transactional>
**Rough monthly search volume**: <estimate from research, OR mark UNKNOWN if no signal — DO NOT invent>
**Competition difficulty**: <low / medium / high based on top-5 SERP analysis>
**Why this term**: <2-3 sentences explaining why this is THE head term vs alternatives considered>

## Secondary keywords (5-8 long-tail variants)

| # | Phrase | Intent | Where to place |
|---|--------|--------|----------------|
| 1 | <phrase> | <intent> | H2 / intro / FAQ |
| ... | | | |

## LSI / semantically-related terms (15-30)

Terms the article should mention naturally to signal semantic completeness. Group by cluster:

### Cluster A — <name>
- term 1
- term 2
- ...

### Cluster B — <name>
- ...

(3-5 clusters total, 4-8 terms each.)

## Entity anchors (3-5 named people / brands / methodologies)

These double as anti-AI-tell receipts AND as schema.org entity references:

| Entity | Type | Disambiguation clause | First-mention paragraph |
|--------|------|----------------------|--------------------------|
| Patrick McKenzie | Person | Stripe Atlas founder; Kalzumeus essays author | Beat 1 |
| ... | | | |

## Named related queries (3-5 for FAQ block)

Real questions a reader would type into Google / ChatGPT / Perplexity. Each should be answerable in 40-100 words inline in the article (and surfaced explicitly in the FAQ block at end of free chunk or article).

| # | Question | Answer-anchor (Beat / section where this is implicitly answered) |
|---|----------|------------------------------------------------------------------|
| 1 | <verbatim question> | <Beat 4 — Search> |
| ... | | |

## Audience-language register

15-25 exact phrases the target audience uses. Source each one (HN thread URL, IH post, Twitter user, Reddit thread). These phrases SHOULD appear (or near-paraphrases of them) in the article so it sounds native.

| Phrase | Source | Notes |
|--------|--------|-------|
| "ramen profitable" | HN id=12345 | indie convention term |
| "the leap" | IH post X | shorthand for going indie |
| ... | | |

## Top-5 SERP analysis (competitive landscape)

What's currently ranking for the primary keyword? What's their angle? What gap do we fill?

| Rank | URL | Angle | Word count | Gap we can fill |
|------|-----|-------|------------|-----------------|
| 1 | <url> | <one-line angle> | <count> | <one-line gap> |
| ... | | | | |

## Differentiation thesis

Given the SERP landscape, the 2-3 sentence pitch for why THIS article is the one a reader should read, not the existing top-5. Becomes a 1-line input to the editorial brief.

## LLM / GEO optimization notes

Specific moves to maximise LLM-citation eligibility:

- **TLDR-at-top placement**: <paragraph A + paragraph B intro covers this — confirm>
- **Attributable claims density target**: <N claims per 1000 words, each with named entity + date + source>
- **FAQ block placement**: <end of free chunk or end of article — recommendation>
- **Schema.org additions** beyond Article: <FAQPage, HowTo, etc.>
- **Disambiguation discipline**: <list of entities that need extra disambiguation because they share names with other entities>

## Final report (1 paragraph)

Summary of: queries used, total terms in semantic core, entity anchors selected, FAQ questions identified, primary differentiation thesis.
```

## Hard rules

- ≥5 WebSearch calls before drafting any field.
- Capture VERBATIM phrases — never invent audience vocabulary.
- Search-volume numbers are estimates; mark UNKNOWN when no data — DO NOT invent precise figures.
- All entity disambiguation clauses must be factually verifiable (do NOT invent founder bios).
- The audience-language register table is the most important section — the article fails without it.
- No emojis.
- Output is markdown, not JSON.

## Failure modes

- Vibe-based keyword list (no SERP analysis, no verbatim audience quotes) → REJECT, redo.
- Primary keyword that doesn't match a real search query → REJECT.
- Invented founder bios in entity table → REJECT, look them up.
- Less than 15 LSI terms → REJECT (too thin to demonstrate semantic completeness).
