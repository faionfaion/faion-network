# User Story Mapping

## Summary

Arrange user stories into a two-dimensional map: backbone activities run left-to-right (user journey), tasks are stacked vertically under each activity by priority. The map exposes a "walking skeleton" (one task per activity, end-to-end) and horizontal release slices, making scope decisions visual and defensible. Use verb phrases for backbone items; 5-10 activities is the target range.

## Why

Flat backlogs lose journey context — stories get prioritized without seeing the full picture, critical steps disappear, and release scope becomes guesswork. A story map forces the team to answer "How does our backlog connect to the user's journey?" before committing to a release. The walking skeleton also defines the earliest defensible MVP boundary, making it the foundation for all subsequent slicing decisions.

## When To Use

- Decomposing a new product or major feature where the user journey spans 3+ steps and the team needs a shared mental model.
- Slicing releases from a large feature backlog by identifying a walking skeleton then incremental slices.
- Discovery to delivery handoff: turning interview transcripts into structured backbone and tasks before sprint planning.
- Onboarding a new contributor who needs to understand the product end-to-end in one diagram.

## When NOT To Use

- Single isolated feature with no journey (e.g. "add audit log endpoint") — go directly to a story or spec.
- Maintenance / bug-fix work where the journey is already stable and mapped.
- Linear data-pipeline products with no user-facing journey; use technical sequence diagrams instead.
- When the team will not maintain the map — stale story maps actively mislead.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Backbone, walking skeleton, and release slices: definitions, rules, and worked examples. |
| `content/02-process.xml` | Five-step mapping process with rules and antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/story-map.md` | Story map template: context, backbone table, walking skeleton, release slices, parking lot. |
| `templates/story-card.md` | Individual user story card with placement, acceptance criteria, and dependencies. |
| `templates/validate-story-map.py` | Python script to validate a story-map JSON for backbone coverage and walking-skeleton completeness. |
