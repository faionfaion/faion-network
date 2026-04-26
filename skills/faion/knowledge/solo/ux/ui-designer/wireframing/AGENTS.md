# Wireframing

## Summary

Wireframes are low-fidelity structural representations of a UI — boxes, labels, and annotations without colors, images, or final copy — used to validate layout, hierarchy, and interaction behavior before any visual design begins.

## Why

Jumping directly to high-fidelity design conflates structure decisions with aesthetic decisions, making both harder to evaluate. Wireframes keep feedback focused on "does this layout serve the user goal?" and allow cheap iteration before stakeholder attention locks in on visual details.

## When To Use

- Translating a product spec or user story into a structural layout before visual design begins
- Rapid exploration of multiple layout alternatives for a new page or feature
- Generating annotated wireframe documentation from existing designs for developer handoff
- Producing content hierarchy maps to align stakeholders on structure before aesthetics
- Auditing existing screens for missing states (empty, error, loading) and documenting them

## When NOT To Use

- After visual design has already been approved — retroactive wireframing is documentation theater
- For micro-interactions and animations — wireframes convey structure, not motion
- As a replacement for user research — wireframing answers "how to lay it out," not "what to build"
- When the deliverable requires interactive prototype testing — proceed directly to interactive prototypes
- One-screen fixes or copy changes where layout is already established

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Five-step wireframing process: understand requirements, sketch ideas, create wireframe, review/iterate, annotate; fidelity levels and what to include/exclude |
| `content/02-examples.xml` | Low and medium fidelity wireframe examples, common element patterns (nav, hero, card, form, footer), antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/wireframe-doc.md` | Full wireframe documentation: purpose, user goal, layout, annotations, states, interactions, responsive notes, open questions |
| `templates/component-wireframe.md` | Component-level wireframe: purpose, variants, states, content guidelines, usage notes |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/figma-pages.sh` | Bash script to list all pages and top-level frames in a Figma file via the Figma REST API |
