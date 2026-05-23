# {ComponentName}: Component Specification

<!-- SUMMARY: {One sentence describing what this component does} -->

## Purpose

{What problem this component solves. Who uses it. Where it appears.}

## Props / Interface

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `propName` | `string` | yes | — | {what it controls} |
| `onAction` | `(id: string) => void` | no | `undefined` | {callback description} |
| `variant` | `'primary' \| 'secondary'` | no | `'primary'` | {visual variant} |

## States

| State | Trigger | Visual |
|-------|---------|--------|
| default | initial | {description} |
| loading | async op in progress | spinner, disabled |
| error | async op failed | error message, retry |
| disabled | `disabled` prop | muted, no interaction |

## Behavior

### FR-1: {Behavior title}

{What the component does}

- Given: {precondition}
- When: {user action}
- Then: {expected result}

### FR-2: {Behavior title}

- Given: {precondition}
- When: {user action}
- Then: {expected result}

## Accessibility

- Keyboard: {Tab / Enter / Escape behavior}
- Screen reader: {ARIA roles, labels}
- Focus: {focus management on open/close/action}

## Non-Goals

- {Explicit exclusion — prevents feature creep}

## Open Questions

- {Unresolved design question}
