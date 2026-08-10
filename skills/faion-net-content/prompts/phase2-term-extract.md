# Term-extraction agent prompt — Phase 2.5 (NEW in v8)

You extract glossary candidates from a clean, ready-to-translate EN article. For each technical / domain term used in the article that has NO existing glossary entry, you produce a rich glossary `.mdx` file with definition, sources, and metadata.

This stage runs ONCE per article, AFTER editor pass on EN, BEFORE translators. Output is read by the build-time `remark-glossary-wrap` plugin to auto-wrap all your additions on the next build.

## Inputs

- **Article** (canonical EN): `{{article_path}}` — `content/ultimate-guide/<slug>/en.mdx`, `status: ready-to-translate`.
- **Existing glossary corpus**: `content/glossary/*.mdx` — 161+ entries. List slugs:
  ```bash
  cd /home/nero/workspace/projects/faion-net/faion-net-fe
  ls content/glossary/*.mdx | sed 's|.*/||; s|\.mdx$||' > /tmp/existing-slugs.txt
  ```
- **Glossary entry template**: `content/glossary/mrr.mdx`, `runway.mdx`, `claude-code.mdx` — model new entries on these.

## What counts as a term-candidate

Extract a glossary candidate if ALL of:
1. **Technical, domain-specific, or named-concept** (SaaS metric, finance term, tool, framework concept, cognitive bias, named cultural phenomenon).
2. **Reader would benefit from inline tooltip on first mention** (term is non-obvious to mid-career reader outside the niche).
3. **NOT already in `content/glossary/`** — check existing-slugs list.
4. **Used 2+ times in article** OR central to article's argument (single use of a foundational term is enough).

What does NOT count:
- Common English words.
- Brand names (Stripe, Vercel, GitHub) — UNLESS they have a glossary entry already (`claude-code`, `cursor-ide`).
- Single-use jargon you won't see again.
- Proper nouns of people (handled by translit doctrine).
- Methodology slugs (those are CLI-only content).

## What to produce

For each candidate, write a new file `content/glossary/<slug>.mdx`:

```mdx
---
term: "<canonical display label, e.g. 'survivor bias'>"
fullName: "<long form for EN, e.g. 'survivor bias'>"
fullNameUk: "<UA equivalent, e.g. 'ефект виживших'>"
slug: "<kebab-case-slug>"
category: "<one of: product, finance, founder-economics, tooling, community, cognitive, marketing, engineering, security, ops>"
shortDefinition: "<60-120 word definition in EN that explains the term clearly for a mid-career reader; this is the tooltip text>"
keywords:
  - <keyword 1>
  - <keyword 2>
  - ...
relatedTerms:
  - <other glossary slug>
  - ...
sources:
  - title: "<title of source 1>"
    url: "<real URL>"
    type: "article"
  - title: "<source 2>"
    url: "<real URL>"
    type: "<article | book | paper | docs>"
createdAt: "<YYYY-MM-DD>"
updatedAt: "<YYYY-MM-DD>"
---

# <term> (full form if applicable)

<150-300 word body explaining the term in the context of solo-SaaS / indie-founder audience. Use existing entries as the tone reference. Patio11-relentless register if it lands naturally. Include the formula or numerical example where applicable. Conclude with how it appears in faion's ecosystem (CLI / methodology / playbook references where relevant).>

## Section subhead (optional, only if body > 200 words)

<additional content>
```

## Hard rules

- **Real sources only.** Two minimum, prefer 3-4. Verifiable URLs (no fabrication). If you can't find a real source, do NOT create the entry — flag in your report instead.
- **shortDefinition fits in 60-120 words.** This is the tooltip — concise.
- **Body 150-300 words.** Not a Wikipedia article; just enough that clicking through gives the reader real value.
- **fullNameUk = canonical UA form.** This is what UA translators will see. Get it right. If unsure, check how other entries handle it.
- **category enum** strict to existing categories used by current entries.
- **Do NOT modify the article itself.** Term-extraction reads, glossary writes.
- **Do NOT add `<GlossaryTerm>` wraps to the article.** Build-time plugin handles wrapping; your new entries get picked up on next build.

## After writing

Run:

```bash
node scripts/build-glossary-map.mjs
```

This regenerates `src/__generated__/glossary-map.json`. Verify your new slugs appear:

```bash
node -e "const m = require('./src/__generated__/glossary-map.json'); console.log(Object.keys(m).filter(s => ['<your-new-slug>', '<your-other-slug>'].includes(s)))"
```

## Final report

Three sections:

1. **New entries created** — list of `<slug>` + brief justification (why this term, how many times in article, where used).
2. **Existing terms confirmed used** — slugs from article that already had entries (so the next build auto-wraps them).
3. **Skipped candidates with reasoning** — terms you considered but rejected (single use, common English, no good source, etc.).

Token budget: aim ~5-10 new entries per ultimate-guide article. If you find >15, you're being too aggressive — narrow to truly foundational terms.
