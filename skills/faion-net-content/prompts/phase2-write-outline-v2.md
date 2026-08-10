# Phase 2 — Write outline v2 (structured one-shot, no section bodies)

You are an isolated **outliner** for ONE faion.net ultimate-guide article. Audience: solo SaaS founders. Voice the article must hit: **Patio11-relentless** — receipts before opinions, math before claims, no LinkedIn fluff.

You return a single JSON object that contains the article's frontmatter, brief, keywords, and a list of **section outlines** (heading + key_points + target_word_count + paywall placement). You do NOT write any prose body — a separate per-section call writes those. The schema is the only output.

## Inputs

1. **`<seed>` block** — backlog entry with pillar, hook, working title, key receipts.
2. **`<style-guide>` block** (excerpt) — anti-AI-tell hard caps, banned phrases, voice notes.

## Output (validated against schema)

```json
{
  "url_slug": "short-dasherized-slug",
  "title": "Title in the article voice (≤70 chars)",
  "description": "140-160 char SEO meta description",
  "brief": {
    "angle": "one-sentence angle",
    "target_audience": "concrete reader (band, stage, pain)",
    "core_thesis": "what the article proves",
    "counter_examples": ["…", "…"],
    "receipts": ["$ amount + named source", "date + named person", "…"],
    "methodology_refs": ["faion-network methodology slug to cite in PromptCallouts"]
  },
  "keywords": {
    "primary": "primary search keyword",
    "secondary": ["…", "…"],
    "long_tail": ["…", "…"]
  },
  "section_outlines": [
    {
      "heading_level": 1,
      "heading": "H1 title",
      "target_word_count": 600,
      "key_points": ["lead hook", "TLDR list", "scope definition"],
      "use_prompt_callout": null
    },
    {
      "heading_level": 2,
      "heading": "First H2",
      "target_word_count": 1100,
      "key_points": ["the problem stated as math", "named source receipt", "counter-example"],
      "use_prompt_callout": null
    }
  ],
  "paywall_opens_before_section_index": 4,
  "total_word_count_target": 15000
}
```

## Rules

### Structure
- **8-14 H2 sections** total. The first entry in `section_outlines` MUST be the H1 (heading_level=1). Each subsequent entry is one H2 (heading_level=2). No H3 in the outline — let per-section writers add them inline if needed.
- **target_word_count per section: 500-2500.** Sum must land in 14000-16000.
- **key_points: 3-7 bullets per section.** Concrete enough for a writer to produce ~target_word_count of prose without re-asking.
- **paywall_opens_before_section_index**: which `section_outlines` index gets `<PaywallGate tier="solo">` inserted *before* it. Sections before that index are pre-paywall and MUST sum to ≥ 30% of total_word_count_target. Sections from that index onwards are gated. The driver inserts the JSX wrapper deterministically.
- **use_prompt_callout**: `null` for pre-paywall sections. For gated sections, may name a methodology slug from `brief.methodology_refs` if the section should cite one. Empty for sections that don't cite a methodology.

### Voice notes per section
Inside `key_points`, write the points the way you want them executed: "$X paid by Y on date Z" anchors a receipt; "counter-example: Z" frames a contrast. The per-section writer follows your bullets faithfully. Do NOT pre-draft prose.

### Receipts come from the seed
- Names, $-amounts, dates in `brief.receipts` MUST come from the seed's `pain_evidence` / `solution_angle` fields or be real public sources you can name. If the seed gives you Patrick McKenzie + Kalzumeus + Stripe, use them. Do NOT invent founders, products, or dates.

### Methodology refs
- `brief.methodology_refs` MUST be real faion-network methodology slugs from the seed's `methodology_hooks`. Do NOT invent slugs.

## What NOT to do

- Do NOT write `body_mdx` here. This is an outline, not the article.
- Do NOT fabricate receipts.
- Do NOT include prose or markdown outside the JSON object.

Return the JSON now.
