<!--
purpose: wireframe document skeleton (layout + annotations + states + open questions)
consumes: feature spec + content inventory + technical constraints
produces: a wireframing artefact validating against scripts/validate-wireframing.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
-->
# Wireframe: <page_screen_name>

**Version:** [X.X]
**Date:** <date>
**Designer:** [Name]
**Status:** Draft / Review / Approved

## Purpose

[What this page/screen is for and what user goal it serves]

## Layout

```
[ASCII layout diagram — boxes and labels only, no colors]

+------------------------------------------+
|  [Header / Navigation]                   |
+------------------------------------------+
|                                          |
|  [Main content area]                     |
|    [Element]     [Element]               |
|                                          |
+------------------------------------------+
|  [Footer]                                |
+------------------------------------------+
```

## Annotation Table

| # | Element | Description | Behavior / Notes |
|---|---------|-------------|------------------|
| 1 | [Name] | [What it is] | [Interaction or requirement] |
| 2 | [Name] | [What it is] | [Interaction or requirement] |

## States

- [ ] Default (populated, normal operation)
- [ ] Empty (first use or no data: "no results", "no items yet")
- [ ] Loading (while data fetches)
- [ ] Error (operation failed, network error, validation failure)
- [ ] Success (confirmation after completing action)
- [ ] Permission denied (user lacks access)

## Interactions

| Element | Trigger | Action | Result |
|---------|---------|--------|--------|
| <element> | Click / Hover / Submit | <what_happens> | <outcome_state_change> |

## Responsive Notes

- **Desktop (1280px+):** <how_layout_changes>
- **Tablet (768-1279px):** <how_layout_changes>
- **Mobile (375-767px):** <how_layout_changes>

## Open Questions

- [Question 1 — decision needed before engineering begins]
- <question_2>
