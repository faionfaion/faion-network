# Content Audit Process

## Summary

A structured 6-step process for systematically inventorying and evaluating all content assets,
assigning each item an action (Keep/Update/Consolidate/Rewrite/Remove/Review), and producing a
prioritized report. Triggers a crawler-based or manual inventory, applies multi-criteria scoring,
and outputs concrete migration or cleanup recommendations.

## Why

Without a systematic audit, content decisions are guesswork. The process surfaces stale content
before migration, identifies duplicate coverage that dilutes SEO, and generates an evidence-based
action list that stakeholders can prioritize. Running it before any redesign or platform migration
prevents carrying over problems to the new system.

## When To Use

- Before a site migration or CMS switch — avoid importing bad content to the new platform.
- When SEO is underperforming and the cause is unclear — old or duplicate content may be to blame.
- When users report finding outdated information — audit scope starts at the affected content type.
- After significant product or pricing changes — detect pages that reference stale information.
- Annually as content governance to prevent slow decay.

## When NOT To Use

- For a single-page or micro-site with fewer than 20 content items — a full audit adds overhead
  without payoff; a manual review suffices.
- When there is no plan to act on findings — audit data decays quickly; run only when there is
  owner commitment to execute the action list.
- Mid-sprint as a reactive measure — plan as a dedicated project with tooling and stakeholder buy-in.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | 6-step procedure: scope, inventory, spreadsheet, evaluation, action assignment, reporting |
| `content/02-examples.xml` | Real audit findings for blog and help center; good vs bad action decisions |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-spreadsheet.md` | Column schema for the content inventory spreadsheet |
| `templates/audit-report.md` | Executive summary + findings report skeleton |
