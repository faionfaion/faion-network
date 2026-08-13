# UI Component Library

## Summary

**One-sentence:** UI component library spec: layered architecture (tokens / primitives / patterns / templates), Storybook story per component, semver release process, a11y baseline, visual regression gate.

**One-paragraph:** UI libraries fail when there is no clear layering, when stories miss states (loading / empty / error), when a11y is checked only manually, when releases are tagged ad-hoc, and when visual regression is skipped. This methodology produces a library spec: 4-layer architecture (tokens / primitives / patterns / templates), Storybook story per component with all variants, axe-core a11y baseline in CI, Chromatic / Percy visual gate, semver + changelog, deprecation policy.

**Ефективно для:**

- Перший проект design system - зафіксувати layering + Storybook + release.
- Adoption blocked відсутністю stories - запровадити мандат.
- A11y regressions - axe-core в CI.
- Visual regressions - Chromatic snapshot gate.
- Деpreations губляться - зафіксувати policy.

## Applies If (ALL must hold)

- Project ships a reusable component library (internal or public).
- Multiple consuming apps OR one app with sustained component growth.
- Team can ship Storybook + visual regression infrastructure.
- Owner can sign off semver bumps and deprecation timelines.

## Skip If (ANY kills it)

- Project is a single app with <20 components - library overhead is not justified.
- Library is externally maintained (e.g. shadcn vendored primitives) - use that methodology.
- Team is in pre-MVP discovery - components churn too fast for stable library.
- Compliance forbids external visual-regression services and no internal alternative exists.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Component inventory | list of components + consumers | engineering |
| Design tokens | tailwind.config or design-tokens JSON | design |
| Visual regression budget | Chromatic / Percy / internal | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[shadcn-ui-architecture]] | primitive layer convention this spec inherits. |
| [[tailwind-architecture]] | styling layer this spec assumes is in place. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: 4-layer arch, story per component+states, a11y axe in CI, visual regression gate, semver+changelog, deprecation timeline, no business in library | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: layers, storybook, a11y, visual regression, release | ~900 |
| `content/05-examples.xml` | essential | Worked example for an internal SaaS UI library | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-layers` | sonnet | Per-component judgement. |
| `author-stories` | haiku | Boilerplate per state. |
| `wire-a11y` | haiku | Config snippet. |
| `review-visual-diff` | opus | Stakes high; visual regressions ship to all consumers. |

## Templates

| File | Purpose |
|------|---------|
| `templates/Button.stories.tsx` | Storybook story covering all required states for a Button primitive. |
| `templates/changeset.md` | Changeset entry template for a UI library release. |
| `templates/new-component.sh` | Bash scaffolder: new library component (story + spec + changeset stub). |
| `templates/_smoke-test.json` | Minimum viable UI-library spec for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ui-component-library.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[shadcn-ui-architecture]]
- [[tailwind-architecture]]
- [[react-component-architecture]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - consumer count, storybook coverage, a11y gate, release process - onto a rule from `content/01-core-rules.xml`. Use it before adopting a library: it catches missing-states and ad-hoc tagging upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/Button.stories.tsx`

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '../Button';

const meta: Meta<typeof Button> = {
  title: 'primitives/Button',
  component: Button,
  parameters: { a11y: { config: { rules: [{ id: 'color-contrast', enabled: true }] } } },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Default: Story = { args: { children: 'Save' } };
export const Hover: Story = { ...Default, parameters: { pseudo: { hover: true } } };
export const Focus: Story = { ...Default, parameters: { pseudo: { focusVisible: true } } };
export const Disabled: Story = { args: { children: 'Save', disabled: true } };
export const Loading: Story = { args: { children: 'Saving…', loading: true } };
export const Empty: Story = { args: { children: '' } };
export const Error: Story = { args: { children: 'Retry', variant: 'destructive' } };
```

### `templates/new-component.sh`

```bash
#!/usr/bin/env bash
# Usage: ./new-component.sh <layer> <ComponentName>
# Example: ./new-component.sh primitives Toast
# Creates component folder with tsx, module.css, stories, and updates barrel.
set -euo pipefail

LAYER=${1:?First arg: layer (primitives|composite|patterns|layout)}
NAME=${2:?Second arg: ComponentName (PascalCase)}
DIR="src/components/$LAYER/$NAME"

mkdir -p "$DIR"

cat > "$DIR/$NAME.tsx" <<EOF
import { forwardRef } from 'react';
import { clsx } from 'clsx';
import styles from './$NAME.module.css';

export interface ${NAME}Props extends React.HTMLAttributes<HTMLDivElement> {}

export const $NAME = forwardRef<HTMLDivElement, ${NAME}Props>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={clsx(styles.root, className)} {...props} />
  )
);
$NAME.displayName = '$NAME';
EOF

cat > "$DIR/$NAME.module.css" <<EOF
.root {
  display: block;
}
EOF

cat > "$DIR/$NAME.stories.tsx" <<EOF
import type { Meta, StoryObj } from '@storybook/react';
import { $NAME } from './$NAME';

const meta: Meta<typeof $NAME> = {
  component: $NAME,
  title: '$LAYER/$NAME',
};
export default meta;

export const Default: StoryObj<typeof $NAME> = { args: {} };
EOF

cat > "$DIR/$NAME.test.tsx" <<EOF
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { $NAME } from './$NAME';

expect.extend(toHaveNoViolations);

describe('$NAME', () => {
  it('has no axe violations', async () => {
    const { container } = render(<$NAME />);
    expect(await axe(container)).toHaveNoViolations();
  });
});
EOF

cat > "$DIR/index.ts" <<EOF
export { $NAME } from './$NAME';
export type { ${NAME}Props } from './$NAME';
EOF

# Update layer barrel
BARREL="src/components/$LAYER/index.ts"
echo "export * from './$NAME';" >> "$BARREL"

echo "Created $DIR"
echo "Updated $BARREL"
```

### `templates/_smoke-test.json`

```json
{
  "layers": [
    "tokens",
    "primitives",
    "patterns",
    "templates"
  ],
  "storybook": {
    "enabled": true,
    "states_required": [
      "default",
      "hover",
      "focus",
      "disabled",
      "loading",
      "empty",
      "error"
    ]
  },
  "a11y": {
    "tool": "axe-core",
    "gate": "block_merge"
  },
  "visual_regression": {
    "tool": "chromatic",
    "gate": "block_merge"
  },
  "release_process": {
    "semver": true,
    "changelog": "CHANGELOG.md"
  }
}
```
