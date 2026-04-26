# Help and Documentation

## Summary

Nielsen Heuristic #10: provide help that is contextual, task-focused, searchable, and concise — following a layered hierarchy from inline hints through tooltips, guided tours, FAQs, and reference docs, with human support as a last resort.

## Why

Users who cannot find answers give up, generating support costs and reducing adoption. Help content reduces friction only when it is discoverable at the moment of confusion, written in user language (not product-team language), and maintained in sync with the actual UI.

## When To Use

- Writing or auditing in-app help content: tooltips, empty states, onboarding tours, inline hints
- Generating knowledge base articles or how-to guides from product specs or changelogs
- Auditing existing documentation for staleness, gaps, or coverage against support ticket patterns
- Building a help search index from existing markdown/docs content
- Creating contextual help copy for complex forms, settings pages, or error states

## When NOT To Use

- Replacing interface design improvements — if UI requires a tooltip to be understood, the UI is broken first
- Producing final user-facing copy without human editorial review (accuracy and tone)
- Generating API reference documentation without code-level context (hallucination risk on technical details)
- Substituting for user research on what users actually struggle with — support ticket analysis must precede content strategy

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Core help principles: contextual, task-focused, searchable, concise, current; help hierarchy; types of help by phase (onboarding, in-context, reference, support) |
| `content/02-examples.xml` | Good examples (Notion, Stripe, Slack) and antipatterns (hidden help, outdated docs, technical overload) |

## Templates

| File | Purpose |
|------|---------|
| `templates/help-content.md` | Step-by-step how-to article structure with overview, steps, result, troubleshooting, and related topics |
| `templates/help-audit.md` | Audit table for help availability, common user questions, content quality, gaps, and priorities |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/help-audit.sh` | Bash script to check docs directory for broken internal links and stale content markers |
