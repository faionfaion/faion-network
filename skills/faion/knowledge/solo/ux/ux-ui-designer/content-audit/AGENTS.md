# Content Audit

## Summary

A content audit is a systematic review of all content on a website or application — cataloging what exists, evaluating quality (accuracy, relevance, quality on a 1-5 scale), and deciding Keep / Update / Rewrite / Remove per item. Avg score &gt;= 4.0 → Keep; 3.0-3.9 → Update; 2.0-2.9 → Rewrite; &lt; 2.0 → Remove.

## Why

Without a content inventory, redesigns and migrations operate blind. Duplicate and outdated content degrades credibility and SEO. Structured audits with defined scoring criteria replace subjective "this feels old" judgments with actionable, defensible decisions that content owners can act on.

## When To Use

- Before a website redesign — establish full inventory before structural changes
- Before a CMS migration — map old URLs to keep/redirect/remove decisions
- SEO improvement sprints — combine crawl data with analytics to prune low-value pages
- Rolling content governance — quarterly review of core pages, bi-annual for blog
- Scoring content quality at scale when 50+ pages need evaluation

## When NOT To Use

- New sites with under 50 pages — a spreadsheet and manual review is faster
- When the primary goal is IA redesign — audit catalogs content, not structure (use card sorting)
- Highly regulated content (medical, legal) where agent quality judgments must not replace subject-matter expert review
- When analytics access is unavailable — remove/keep decisions without traffic data produce low-value output

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Audit types, scoring criteria, frequency by content type, governance workflow |
| `content/02-rules.xml` | Rules for agent usage, redirect risk, batching large sites, common mistakes |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-spreadsheet.md` | Column definitions for the full content audit spreadsheet |
| `templates/evaluation-criteria.md` | Scoring guide (1-5) for accuracy, relevance, quality + action thresholds |
| `templates/merge-audit.sh` | Shell script to join Screaming Frog crawl CSV with GA pageview data |
