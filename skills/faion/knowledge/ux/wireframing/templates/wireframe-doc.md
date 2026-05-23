<!--
purpose: wireframe document skeleton (layout + annotations + states + open questions)
consumes: feature spec + content inventory + technical constraints
produces: a wireframing artefact validating against scripts/validate-wireframing.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
-->
# Wireframe: [Page/Screen Name]

**Version:** [X.X]
**Date:** [Date]
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
| [Element] | Click / Hover / Submit | [What happens] | [Outcome / state change] |

## Responsive Notes

- **Desktop (1280px+):** [How layout changes]
- **Tablet (768-1279px):** [How layout changes]
- **Mobile (375-767px):** [How layout changes]

## Open Questions

- [Question 1 — decision needed before engineering begins]
- [Question 2]
