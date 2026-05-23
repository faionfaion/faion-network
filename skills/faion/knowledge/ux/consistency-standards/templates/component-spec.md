# Component: [Name]

## Purpose

[One sentence: what this component does and where it is used]

## Variants

| Variant | Use Case | Appearance |
|---------|----------|------------|
| Primary | Main action per view | [Color/style] |
| Secondary | Alternative action | [Color/style] |
| Destructive | Delete/remove | [Color/style] |
| Ghost | Tertiary action | [Color/style] |

## Sizes

| Size | Padding | Font Size | Use Case |
|------|---------|-----------|----------|
| Small | [X]px [Y]px | [N]px | Dense UIs |
| Medium | [X]px [Y]px | [N]px | Default |
| Large | [X]px [Y]px | [N]px | Primary CTAs |

## States

| State | Visual Change | Notes |
|-------|---------------|-------|
| Default | Standard appearance | |
| Hover | [Describe change] | |
| Active | [Describe change] | |
| Disabled | Grayed out, 50% opacity | Not interactive |
| Loading | Spinner, text hidden | For async actions |

## Usage Rules

- One primary variant per view
- [Additional rule]
- [Additional rule]

## Accessibility

- Minimum contrast ratio: 4.5:1 for text
- Focus indicator: visible on keyboard navigation
- Disabled state: `aria-disabled="true"`, not `disabled` attribute (for keyboard access)
