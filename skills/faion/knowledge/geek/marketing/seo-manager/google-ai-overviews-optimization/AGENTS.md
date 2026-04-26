# Google AI Overviews Optimization

## Summary

A methodology for structuring content so Google's AI Overviews extract and cite it. The core rule: place a direct answer (1-2 sentences) immediately after each section heading, add Article + FAQ schema, and update content within 30 days. These three actions account for the largest measurable citation gains.

## Why

Google AI Overviews reach 2B monthly users; 30% of searches trigger them. Citation frequency is highest in Science (26%), Computers & Electronics (18%), and Health niches. Content updated within 30 days gets 3.2x more citations. Article + FAQ schema adds ~28% citation lift on average. Without structural optimization, well-written content is invisible to the AI extraction pipeline.

## When To Use

- Target queries show AI Overview panels but site content is not cited.
- Launching content for Science, Technology, Health, or Computers & Electronics niches.
- Running a content freshness audit — pages not updated in 30+ days losing citations.
- Setting up tracking infrastructure for AI Overview impressions in Google Search Console.
- Preparing FAQ or Q&A content that maps directly to user query patterns.

## When NOT To Use

- YMYL queries requiring months of domain authority building — quick optimizations won't move citations.
- Domain authority is too low for Google's citation algorithm — address off-page authority first.
- Navigational queries (brand names, direct URLs) — AI Overviews rarely appear for these.
- Site is penalized or under manual review.
- Content is purely promotional with no informational substance.

## Content

| File | What's inside |
|------|---------------|
| `content/01-extraction-rules.xml` | Core rules for content structure: answer placement, heading hierarchy, semantic clarity, entity definition. |
| `content/02-schema-and-freshness.xml` | Schema markup requirements (Article, FAQ, Author), freshness signal rules, and trust signals. |
| `content/03-tracking-and-antipatterns.xml` | Tracking setup (GSC, Semrush, Otterly), competitive analysis checklist, and antipatterns to avoid. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gsc-fetch.sh` | Bash script to fetch AI Overview impression data from Google Search Console API. |
| `templates/content-audit-prompt.txt` | Prompt for auditing a page for AI Overview optimization readiness. |

## Scripts

None.
