# Frontend Component Practices

## Summary

**One-sentence:** Produces a frontend component (React, Vue, Svelte, or Angular) following one-responsibility, typed props, accessibility-from-the-start, controlled-vs-uncontrolled separation, and CSS-isolation discipline.

**One-paragraph:** Component-level rules common to React, Vue, Svelte, and Angular: a component owns exactly one responsibility; props are typed (TS interface or PropTypes) and never spread blindly; ARIA roles/labels are present from day one; state is either controlled (parent owns the value) or uncontrolled (component owns it) but never both; styles are scoped (CSS modules / scoped CSS / styled-components) not global. The artefact is the component file + sibling .test + sibling .stories; the validator checks the canonical fields are present.

**Ефективно для:**

- New component in an existing frontend codebase.
- Refactor passes extracting a fat component into single-responsibility units.
- Accessibility audit fixes adding ARIA roles + keyboard handlers.
- Migrating uncontrolled <-> controlled in form components.

## Applies If (ALL must hold)

- Component-based framework (React / Vue / Svelte / Angular) with a build step.
- TypeScript or PropTypes for prop typing.
- Component-level CSS scoping mechanism available (CSS modules, scoped <style>, etc).
- Test runner (Vitest / Jest / Testing Library / Playwright Component) wired.

## Skip If (ANY kills it)

- Pure design-token work — see ui-designer methodology.
- Global layout / routing concerns — out of scope.
- Server-rendered HTML templates without a component model.
- Plain CSS site without a build step.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Framework + version | react@18|vue@3|svelte@4|angular@17 | package.json |
| Component spec | props list + states + intended a11y role | design hand-off |
| Styling system | css-modules|scoped|tailwind|styled-components | project convention |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[practices-js-ts-stack]] | shared TS config and lint rules |
| [[testing-js-ts-frontend]] | shared component test runner + Testing Library usage |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-component` | sonnet | create file + props interface + initial markup |
| `emit-a11y-attributes` | haiku | add role/aria-* based on spec |
| `write-sibling-test` | sonnet | Testing-Library test mirroring the public surface |

## Templates

| File | Purpose |
|------|---------|
| `templates/Component.tsx` | React functional component with typed props + a11y |
| `templates/Component.module.css` | Scoped CSS module — no global selectors |
| `templates/Component.test.tsx` | Testing Library sibling test |
| `templates/Component.stories.tsx` | Storybook sibling story with 3 variants |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-practices-frontend-components.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[practices-js-ts-stack]]
- [[testing-js-ts-frontend]]
- [[playwright-automation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Component.tsx`

```tsx
import * as React from 'react';
import styles from './Component.module.css';

export interface ComponentProps {
  id: string;
  label: string;
  selected?: boolean;
  onSelect: (id: string) => void;
}

export function Component({ id, label, selected = false, onSelect }: ComponentProps) {
  return (
    <button
      type="button"
      role="option"
      aria-selected={selected}
      className={selected ? styles.selected : styles.row}
      onClick={() => onSelect(id)}
    >
      {label}
    </button>
  );
}
```

### `templates/Component.module.css`

```css
.row {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border);
  background: transparent;
  cursor: pointer;
}

.selected {
  composes: row;
  border-color: var(--accent);
  background: var(--accent-bg);
}
```

### `templates/Component.test.tsx`

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Component } from './Component';

test('renders label and reports selection', async () => {
  const onSelect = jest.fn();
  render(<Component id="o1" label="Order #1" onSelect={onSelect} />);
  const btn = screen.getByRole('option', { name: /order #1/i });
  await userEvent.click(btn);
  expect(onSelect).toHaveBeenCalledWith('o1');
});
```

### `templates/Component.stories.tsx`

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Component } from './Component';

const meta: Meta<typeof Component> = { title: 'Orders/Component', component: Component };
export default meta;

type Story = StoryObj<typeof Component>;
export const Default: Story = { args: { id: 'o1', label: 'Order #1', onSelect: () => {} } };
export const Selected: Story = { args: { ...Default.args!, selected: true } };
export const LongLabel: Story = { args: { ...Default.args!, label: 'Order #1 — very long descriptive label' } };
```

### `templates/artefact.json`

```json
{
  "component_name": "OrderRow",
  "framework": "react",
  "typed_props": true,
  "a11y_attrs_present": true,
  "style_scope": "css-modules",
  "controlled_mode": "stateless",
  "lines": 64,
  "has_test": true,
  "has_story": true
}
```
