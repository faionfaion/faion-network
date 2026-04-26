# Content Audit Basics

## Summary

A content audit is a systematic inventory and quality review of all content on a site or application. It catalogs what exists (URL, type, owner, date, analytics), evaluates each item against rubric criteria (accuracy, relevance, quality scored 1-5), and produces a keep/update/consolidate/remove action column. The basics methodology covers audit types, spreadsheet schema, evaluation criteria, and tooling.

## Why

Without an inventory you cannot make scope decisions for redesigns, migrations, or SEO resets. Subjective "we should clean up the blog" discussions block action; a scored spreadsheet with analytics-joined data unblocks it. LLM-assisted scoring makes audits tractable at scale, but requires a locked rubric, deterministic model settings, and human sign-off on high-traffic rows.

## When To Use

- Pre-redesign or migration: build a complete URL inventory with quality scores before scope decisions.
- SEO/content strategy reset: combine crawl data + analytics + LLM quality scoring.
- Quarterly content governance: rolling audits of high-traffic clusters with freshness checks.
- Site consolidation (M&A, multi-brand merge): de-duplicate near-identical pages across domains.

## When NOT To Use

- Site under ~50 pages — a manual spreadsheet review is faster than tooling setup.
- Greenfield (content does not yet exist) — use content modeling, not auditing.
- Analytics performance only — GA4/GSC views suffice; no inventory needed.
- Pre-launch QA of a single page batch — use editorial review instead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-audit-types.xml` | Audit types (quantitative, qualitative, comparative, ROI), when to run each, frequency by content type. |
| `content/02-scoring-rubric.xml` | Accuracy/relevance/quality scoring guide (1-5), action decision matrix, pipeline architecture. |
| `content/03-antipatterns.xml` | Common mistakes, LLM-scoring failure modes, privacy and cost gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-spreadsheet-schema.md` | Column definitions for the content audit spreadsheet (ID, URL, metrics, scores, action). |
| `templates/rubric.yaml` | Scoring rubric in YAML for LLM prompt injection; version-controlled for reproducibility. |
| `templates/audit-pipeline.py` | Async Python sketch: crawl → extract → score via Claude API → write scored.jsonl. |
