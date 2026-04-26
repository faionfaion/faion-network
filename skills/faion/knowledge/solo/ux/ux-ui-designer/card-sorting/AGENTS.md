# Card Sorting

## Summary

Ask users to organize content topics into groups and label those groups, revealing how
users mentally categorize information. Use open sort to discover natural categories, closed
sort to validate a proposed structure, or hybrid to refine an existing IA. Requires 15-20
participants for open sort, 30+ for statistically meaningful closed sort results.

## Why

Navigation structures designed by product teams mirror internal org charts, not user
mental models. Card sorting surfaces the vocabulary and groupings real users expect,
before the navigation is built. Co-occurrence matrices identify strong clusters (>70%
agreement) and problem items that need further investigation.

## When To Use

- You do not know how users think about your content or what labels they expect
- Users cannot find content in the current navigation (high search usage, low direct nav success)
- Designing or redesigning a site/app information architecture from scratch or major overhaul
- Analyzing open-sort exports to compute similarity matrices and candidate IA structure

## When NOT To Use

- Fewer than 10 content items — overhead not justified; use interviews or usability tests instead
- IA already validated through tree testing and live search analytics — re-sorting adds noise
- UI layout or visual hierarchy questions — card sorting answers content organization, not placement
- As a substitute for running the actual study — agents cannot observe real-time hesitation or card-splitting

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Six-step process: goals → cards → format → recruit → conduct → analyze |
| `content/02-analysis.xml` | Co-occurrence matrix, similarity thresholds (>70%/>40%), standardization metric, best-merge method |
| `content/03-examples.xml` | Open sort e-commerce example; closed sort placement table; agentic workflow with prompt patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/card-sort-plan.md` | Study plan: objectives, method, participant profile, card list, categories (closed), analysis plan |
| `templates/results-report.md` | Results template: category structure, agreement matrix, key insights, IA recommendations |
| `templates/cooccurrence.py` | Python: compute co-occurrence matrix from open sort export; identify strong/weak/outlier clusters |
