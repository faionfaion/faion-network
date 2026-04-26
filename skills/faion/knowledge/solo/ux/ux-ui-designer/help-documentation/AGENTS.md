# Help and Documentation

## Summary

Nielsen's Usability Heuristic #10: even though it is better if a system needs no documentation, help must be provided when needed. Effective help is contextual (placed where users need it), task-focused (organized by user goals not feature names), searchable, concise, and kept current. The help hierarchy: fix the interface first, then inline hints, then tooltips, then FAQs, then documentation, then human support.

## Why

Users who cannot find help give up. Increased support ticket volume is the measurable signal of help failure. Good contextual help reduces support costs, improves feature adoption, and shortens the time to proficiency for new users.

## When To Use

- Auditing an existing product for help gaps during a UX review sprint
- Generating first-draft contextual tooltips, inline hints, or FAQ entries for a new feature
- Analyzing support ticket logs to identify recurring help needs not covered by existing docs
- Producing a help article from a list of step-by-step procedures
- Creating onboarding tour scripts tied to specific UI actions

## When NOT To Use

- When the interface itself needs a redesign to eliminate confusion — fix the root, not the docs
- Replacing qualitative usability testing — help audits do not substitute for observing real users
- Generating legally binding product documentation without human legal review
- When the feature set is still unstable and help content will be outdated before it ships

## Content

| File | What's inside |
|------|---------------|
| `content/01-hierarchy.xml` | Help hierarchy, contextual patterns (inline hints, tooltips, tours), content types |
| `content/02-rules.xml` | Authoring rules, common mistakes, measuring effectiveness, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/help-article.md` | Help article structure: overview, numbered steps, result, troubleshooting, related |
| `templates/help-audit.md` | Help audit: feature × coverage/type/quality + gap table + priority improvements |
| `templates/help_gap_finder.py` | Python script to find features missing help coverage |
