# Component: Button

## Variants

| Variant | Use Case | Appearance |
|---------|----------|------------|
| Primary | Main action per view (one max) | Blue filled |
| Secondary | Alternative action | Blue outlined |
| Destructive | Delete or remove operations | Red filled |
| Ghost | Tertiary or inline actions | Text only |

## Sizes

| Size | Padding | Font Size | Use Case |
|------|---------|-----------|----------|
| Small | 8px 12px | 14px | Dense UIs, table actions |
| Medium | 12px 16px | 16px | Default for most contexts |
| Large | 16px 24px | 18px | Primary CTAs, hero sections |

## States

| State | Visual Change |
|-------|---------------|
| Default | Standard appearance |
| Hover | Slightly darker background |
| Active/Pressed | Even darker, slight inset |
| Disabled | 50% opacity, pointer-events: none |
| Loading | Spinner replaces label text |
| Focus | 2px focus ring, offset 2px |

## Usage Rules

- Maximum one primary button per view
- Primary button is always on the right in form/dialog button groups
- Destructive actions always require confirmation before execution
- Loading state is required for any async action over 300ms
- Do not use icon-only buttons without tooltip and aria-label
