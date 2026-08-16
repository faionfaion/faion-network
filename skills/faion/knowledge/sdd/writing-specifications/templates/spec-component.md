<!--
purpose: UI component specification — props/interface, states, behavior (FR-X), accessibility, non-goals.
consumes: a problem statement and persona list for the component's consumer (see Prerequisites)
produces: component specification artefact
depends-on: content/02-output-contract.xml
token-budget-impact: ~280 tokens when filled
-->

# {ComponentName}: Component Specification

<!-- SUMMARY: {One sentence describing what this component does} -->

## Purpose

{What problem this component solves. Who uses it. Where it appears.}

## Props / Interface

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `propName` | `string` | yes | — | {what it controls} |
| `onAction` | `(id: string) => void` | no | `undefined` | <callback_description> |
| `variant` | `'primary' \| 'secondary'` | no | `'primary'` | <visual_variant> |

## States

| State | Trigger | Visual |
|-------|---------|--------|
| default | initial | <description> |
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

- Keyboard: <keyboard>
- Screen reader: {ARIA roles, labels}
- Focus: {focus management on open/close/action}

## Non-Goals

- {Explicit exclusion — prevents feature creep}

## Open Questions

- <unresolved_design_question>
