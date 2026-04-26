# Cross-Tool Migration Basics

## Summary

A structured approach to migrating project management data between tools, covering pre-migration audit, field mapping, ETL execution, and post-cutover validation. The critical rule: run the migration three times — dev test, full dry-run with rollback, real cutover — and preserve source IDs in a `legacy_id` custom field on the target so every external link and commit message that hardcoded `PROJ-1234` still resolves.

## Why

Tool migrations routinely underestimate hidden costs: field semantics rarely map 1:1, attachment size limits silently drop files mid-migration, and comment threads lose ordering when user IDs don't resolve in the target. Migration cost (data, automations, integrations, training, parallel-run period) is frequently 30-50% of year-1 TCO — quantifying this before committing is the methodology's primary value.

## When To Use

- Switching PM tools (Jira to Linear, Trello to ClickUp, Asana to Notion).
- Consolidating two or more tools after acquisition or department merge.
- Outgrowing a starter tool onto an enterprise tool requiring audit trails.
- Compliance push forces migration to a tool with stronger security posture.
- Current vendor's pricing model becomes hostile (per-seat hike, mandatory tier upgrade).

## When NOT To Use

- One person and fewer than 100 issues — re-create them by hand in an afternoon.
- Vendor offers a guided managed migration that already handles data ETL — use it; this brief adds overhead.
- Tool change is driven by hype rather than measurable pain — wait three months and re-evaluate.
- Active product launch or freeze period — defer until after.
- Source data is too dirty to be worth migrating; archive and start fresh.

## Content

| File | What's inside |
|------|---------------|
| `content/01-migration-assessment.xml` | Pre-migration audit checklist, field mapping rules, status/priority mapping tables. |
| `content/02-execution.xml` | Freeze strategy, cutover steps, validation (count, comments, attachments by byte), parallel-run period, rollback. |
| `content/03-agent-usage.xml` | Agentic workflows: migration-auditor, field-mapper, dry-run-extractor, mapping-validator. Gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/field-mapping.md` | Source-to-target field mapping table with transformation rules and ambiguity flags. |
| `templates/count-check.py` | Compare source vs target issue counts post-migration; exit 1 if drift exceeds 1%. |
