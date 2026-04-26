# User Story Mapping

## Summary

User story mapping arranges stories into a two-dimensional model: user activities as the horizontal backbone (left to right = user's journey) and tasks stacked vertically by priority within each activity. The walking skeleton — exactly one task per activity, forming an end-to-end working flow — becomes the earliest shippable version. Release slices are horizontal cuts that span the full backbone.

## Why

Flat backlogs lose the context of user workflows: stories get prioritized in isolation without seeing whether the full journey is covered. A story map makes missing steps visible, prevents releases that cover only one column of the journey, and creates a shared picture for cross-functional teams before sprint planning.

## When To Use

- Designing an end-to-end user journey across multiple activities.
- Slicing a backlog into shippable releases when a flat list lost journey context.
- Cross-functional alignment before sprint planning (engineering, design, PM need a shared picture).
- Identifying the walking skeleton for an MVP — pairs with mvp-scoping.

## When NOT To Use

- Pure technical work (infrastructure, refactors, platform changes) — no user-facing backbone exists.
- Tiny single-flow features — direct user stories with acceptance criteria suffice.
- Teams without shared journey understanding yet — do user-journey-mapping or JTBD interviews first.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Backbone, tasks, walking skeleton, and release slices — definitions and rules for each layer |
| `content/02-process.xml` | 5-step mapping process: frame journey, build backbone, add tasks, identify skeleton, slice releases |
| `content/03-examples.xml` | E-commerce and project management story map examples |
| `content/04-antipatterns.xml` | Noun backbones, solo mapping, static maps, releases that don't span full backbone |

## Templates

| File | Purpose |
|------|---------|
| `templates/story-map.md` | Tabular story map with backbone, skeleton, release rows, and parking lot |
| `templates/story-card.md` | Per-task story card with placement, user story, acceptance criteria, and estimate |
| `templates/storymap-check.py` | Validates skeleton coverage and that each release spans the full backbone |
