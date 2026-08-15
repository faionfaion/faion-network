<!--
purpose: Template fixture for growth-seo-fundamentals: seo-content-brief.md
consumes: content/01-core-rules.xml
produces: Markdown artefact
depends-on: content/02-output-contract.xml
token-budget-impact: small
variables:
  - name: target_keyword
    type: string
    required: true
    description: The exact query you are writing for, as a searcher types it. One per brief - a page targeting three keywords ranks for none of them and reads like it was written for a machine.
  - name: search_volume
    type: string
    required: true
    description: Monthly search volume with the tool and country it came from. Tools disagree by multiples, so the source is half the number - without it nobody can sanity-check the effort estimate.
  - name: keyword_difficulty
    type: integer
    required: true
    description: Difficulty score 1-100 from the same tool as the volume. If it is above your site's realistic ceiling, say so here rather than discovering it four months after publishing.
  - name: search_intent
    type: enum
    required: true
    options: [informational, commercial, transactional, navigational]
    description: What the searcher actually wants, read off the current SERP rather than guessed. Writing a guide against a transactional SERP is the single most common reason good content never ranks.
  - name: current_position
    type: string
    required: true
    description: Where you rank today, or "not ranking". It decides whether this is a rewrite or a new page - and a page at position 12 is usually worth more attention than a new one.
  - name: target_word_count
    type: string
    required: true
    description: Target length as a range, derived from the top three results and not from a house style. If the SERP winners are 800 words, a 3,000-word piece is padding that dilutes the thing being ranked.
  - name: url_slug
    type: string
    required: true
    description: The URL slug, lowercase and hyphenated. Decide it now - changing it after publication costs a redirect and some of the authority the page earned.
-->
# SEO Content Brief: {{target_keyword}}

## Keyword Data
- Volume: {{search_volume}}
- Difficulty: {{keyword_difficulty}}
- Intent: {{search_intent}}
- Current ranking: {{current_position}}

## SERP Analysis

### Top 3 Results
1. [URL] - [word count] words - Key sections: [list]
2. [URL] - [word count] words - Key sections: [list]
3. [URL] - [word count] words - Key sections: [list]

### Common Elements (all top 3 include)
- [element 1]
- [element 2]

### Missing From All (opportunity)
- [opportunity 1]

## Content Requirements
- Target word count: {{target_word_count}}
- H2s to include: [list based on SERP analysis]
- People Also Ask questions to answer: [list]
- Related entities to mention: [list]

## On-Page SEO
- Title tag: [suggestion, max 60 chars]
- Meta description: [suggestion, 120-160 chars]
- URL slug: /{{url_slug}}
- H1: [suggestion]

## Internal Links
- Link TO these pages from this article: [existing pages]
- Update THESE existing pages to link here: [pages to update]
