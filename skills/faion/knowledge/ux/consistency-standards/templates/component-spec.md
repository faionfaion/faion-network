<!-- purpose: Per-component spec pinning variants, sizes, states and a11y rules -->
<!-- consumes: design system reference, UI inventory -->
<!-- produces: component spec markdown -->
<!-- depends-on: none -->
<!-- token-budget-impact: ~250 tokens filled -->

# Component: <name>

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
| Small | [X]px [Y]px | <small>px | Dense UIs |
| Medium | [X]px [Y]px | <medium>px | Default |
| Large | [X]px [Y]px | <large>px | Primary CTAs |

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
- <additional_rule>
- <additional_rule>

## Accessibility

- Minimum contrast ratio: 4.5:1 for text
- Focus indicator: visible on keyboard navigation
- Disabled state: `aria-disabled="true"`, not `disabled` attribute (for keyboard access)
