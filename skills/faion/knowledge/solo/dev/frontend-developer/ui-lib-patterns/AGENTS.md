# UI Library Advanced Patterns

## Summary

Advanced React component patterns for scalable UI libraries: compound components (shared context via `createContext`), modal portals (focus trap, ESC, overlay-click, scroll lock), and Storybook CSF 3 stories with interaction testing. Every primitive ships as a 4-file unit: component + stories + a11y test + CSS.

## Why

Compound components expose a self-documenting sub-component API (`<Card.Header>`, `<Card.Content>`) while sharing state through context without prop drilling. Modal portals must implement the WAI-ARIA dialog pattern precisely — agents routinely miss `aria-modal`, `aria-labelledby`, and focus return on close.

## When To Use

- Building compound components (Tabs, Accordion, Card) for an in-house UI library.
- Implementing accessible Modal/Dialog/Popover with portal, focus trap, ESC handling.
- Producing a `Component.stories.tsx` for every primitive in a Storybook-backed library.
- Migrating a one-off component into a reusable, typed library entry.

## When NOT To Use

- One-off page UI that will never be reused — compound pattern adds context overhead with no payoff.
- Apps already using Radix UI or React Aria — wrap those instead of re-implementing dialog semantics.
- Server Components-only trees: compound components rely on React context, requiring `'use client'`.

## Content

| File | What's inside |
|------|---------------|
| `content/01-compound-component.xml` | Compound pattern: createContext, Object.assign export, named sub-component exports for tree-shaking. |
| `content/02-modal-portal.xml` | Modal via createPortal: WAI-ARIA dialog, focus trap, scroll lock, SSR mount guard, ESC handler. |
| `content/03-storybook-stories.xml` | CSF 3 story conventions, args matrix, play functions, autodocs tag, interaction testing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gen-compound.sh` | Scaffolds compound component skeleton from name + sub-component list. |

## Scripts

none
