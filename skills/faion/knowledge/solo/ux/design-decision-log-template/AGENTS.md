---
slug: design-decision-log-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Canonical decision-log format for design decisions made in Figma comments, Slack threads, and standups — prevents re-litigation, accelerates onboarding, and gives later AI handoffs a citable source.
content_id: 760dd09b25ff0056
---

# Design Decision Log Template

## Summary

Design decisions get split across Figma comments, Slack threads, and standup memory. Two weeks later nobody remembers why the empty-state copy is "Nothing here yet" instead of "Add your first item", and the decision gets re-litigated — or worse, silently reversed by the next designer. This methodology defines a one-entry-per-decision log format that captures context, options considered, decision, owner, and a stable link to the design artefact. Entries live in a single repo-or-Notion table that designers, PMs, and AI agents can grep before opening a thread.

## Updated 2026-05-20

## Applies If

- The team has more than one designer, OR designers hand off to engineering with non-trivial frequency.
- At least two recurring artefacts (Figma file, Storybook story, design system component) are in active iteration.
- Standups, comment threads, or chat already produce "we agreed X" moments that no one writes down.
- An onboarding designer or AI assistant will need to reconstruct decision history within the next 6 months.

## Skip If

- Single-designer team where the same person remembers every decision and there is no handoff target.
- One-off throwaway design exploration with no commitment to ship.

## Content
See `content/01-core-rules.xml`.

## Related
- [[handoff-spec-template]]
- [[anti-pattern-rationale-template]]
- [[design-system-changelog-template]]
