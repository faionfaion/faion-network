# shadcn/ui Architecture

## Summary

**One-sentence:** Architecture spec for shadcn/ui: components/ui/* as vendored primitives only, semantic CSS tokens, cva variants with compoundVariants, forwardRef + displayName, CODEOWNERS gate on primitive edits.

**One-paragraph:** shadcn/ui rots when business logic sneaks into `components/ui/*`, when concrete Tailwind shades replace semantic tokens in dark mode, when variant lists balloon to 12+ via flat cva, and when primitives are edited silently inside feature PRs. This methodology produces a spec: primitive vendoring rule, semantic-token vocabulary (`--background`, `--foreground`, etc.), cva + compoundVariants rules, mandatory forwardRef + displayName, and a CODEOWNERS gate on the primitive directory.

**Ефективно для:**

- Перший shadcn/ui rollout - зафіксувати primitive vs feature boundary.
- Variant explosion в Button (>6 variants) - перейти на compoundVariants.
- Dark mode виглядає неузгоджено - перейти на semantic tokens.
- Primitive edits всередині feature PR - впровадити CODEOWNERS.
- ref-passing не працює (Radix asChild) - винести forwardRef правило.

## Applies If (ALL must hold)

- Codebase uses React + Tailwind + shadcn/ui (vendored primitives).
- Design system is in active growth (new primitives + features regularly).
- Build pipeline supports CODEOWNERS + lint rules.
- Team can refuse PRs that violate primitive purity.

## Skip If (ANY kills it)

- Codebase uses a different design-system approach (MUI, Chakra, Mantine).
- Project is a tiny prototype with <10 components.
- Team chose Web Components or CSS-in-JS - shadcn vocabulary does not apply.
- Primitives are externally maintained (e.g. design-system as a separate package).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| shadcn primitive set | list of vendored primitives | design system |
| Token catalogue | CSS variable list under :root and .dark | design |
| Variant policy | max variants per prop (e.g. 6) | design |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tailwind-architecture]] | shared token + cn() discipline. |
| [[react-component-architecture]] | primitive layer composed inside feature folder shape. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: primitives no business, CODEOWNERS gate, semantic tokens only, cva + compound, forwardRef+displayName, export variants fn, asChild slot | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: dir layout, tokens, variants, CODEOWNERS, lint | ~900 |
| `content/05-examples.xml` | essential | Worked example for a Next.js shadcn rollout | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-primitive-leakage` | sonnet | Per-import judgement. |
| `refactor-variants` | sonnet | Per-component cva re-design. |
| `wire-lint` | haiku | Boilerplate ESLint config. |
| `review-asChild-coverage` | opus | Stakes high; missing asChild breaks Radix slots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/button.tsx` | shadcn-style Button primitive with cva + compoundVariants + forwardRef + asChild. |
| `templates/globals.css` | Semantic token sheet for shadcn primitives. |
| `templates/scaffold.sh` | Bash scaffold: bootstrap shadcn primitive directory + cn util. |
| `templates/_smoke-test.json` | Minimum viable shadcn architecture artefact for validator smoke-test. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-shadcn-ui-architecture.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[tailwind-architecture]]
- [[react-component-architecture]]
- [[ui-component-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - primitive import shape, token kind, variant count, ownership gate - onto a rule from `content/01-core-rules.xml`. Use it before merging primitive edits: it catches business-in-primitive and variant-explosion upstream.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/button.tsx`

```tsx
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

export const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: { sm: 'h-9 px-3', default: 'h-10 px-4 py-2', lg: 'h-11 px-8' },
    },
    compoundVariants: [
      { variant: 'outline', size: 'sm', class: 'border-2' },
    ],
    defaultVariants: { variant: 'default', size: 'default' },
  },
);

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return <Comp ref={ref} className={cn(buttonVariants({ variant, size }), className)} {...props} />;
  },
);
Button.displayName = 'Button';
```

### `templates/globals.css`

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --primary: 222 47% 11%;
  --primary-foreground: 210 40% 98%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 210 40% 98%;
  --accent: 210 40% 96%;
  --accent-foreground: 222 47% 11%;
  --ring: 215 20% 65%;
  --radius: 0.5rem;
}
.dark {
  --background: 222 47% 11%;
  --foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222 47% 11%;
  --destructive: 0 63% 31%;
  --destructive-foreground: 210 40% 98%;
  --accent: 217 33% 17%;
  --accent-foreground: 210 40% 98%;
  --ring: 217 33% 17%;
}
```

### `templates/scaffold.sh`

```bash
#!/usr/bin/env bash
# Usage: ./scaffold.sh button card dialog form input label
# Adds shadcn primitives from the registry, then generates a barrel export.
# Requires: npx shadcn@latest (Node + configured project)
set -euo pipefail

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 <component> [component...]" >&2
  exit 1
fi

for c in "$@"; do
  echo "Adding $c..."
  npx shadcn@latest add "$c" --yes
done

BARREL="components/ui/index.ts"
{
  echo "// auto-generated barrel — do not edit manually"
  for c in "$@"; do
    echo "export * from './$c';"
  done
} > "$BARREL"

echo "Barrel written to $BARREL"
npx tsc --noEmit
echo "Scaffolded: $*"
```

### `templates/_smoke-test.json`

```json
{
  "primitive_dir": "src/components/ui/",
  "token_source": "src/styles/globals.css",
  "variant_policy": {
    "max_variants_per_prop": 6,
    "compound_variants_required": true
  },
  "lint_rules": [
    "no-arbitrary-tailwind",
    "require-forwardRef"
  ],
  "codeowners_path": "/components/ui/ @design-system"
}
```
