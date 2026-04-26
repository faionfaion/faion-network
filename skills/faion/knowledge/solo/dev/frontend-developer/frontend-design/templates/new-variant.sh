#!/usr/bin/env bash
# new-variant.sh <slug>
# Scaffold a designs/variant-N-<slug>/ directory with README template.
#
# Usage:
#   bash scripts/new-variant.sh minimalist-editorial
#   bash scripts/new-variant.sh bold-dashboard
set -euo pipefail

slug="${1:?Usage: new-variant.sh <slug>}"

# Auto-number based on existing variants
n=$(printf '%02d' "$(($(ls designs 2>/dev/null | grep -cE '^variant-' || echo 0) + 1))")
dir="designs/variant-${n}-${slug}"

if [[ -d "$dir" ]]; then
  echo "ERROR: $dir already exists."
  exit 1
fi

mkdir -p "$dir"

cat > "$dir/README.md" <<TEMPLATE
# Variant ${n} — ${slug}

## Rationale

### Audience fit
<!-- Who is this for? What problem does the visual direction solve? -->

### Aesthetic levers
<!-- Which diversity constraints are applied?
     - Typeface: ...
     - Palette family: ...
     - Density: tight | airy
     - Motion: none | subtle | expressive
     Levers must differ from sibling variants. -->

### Trade-offs
<!-- What does this direction sacrifice? Where does it excel? -->

## Files

| File | Purpose |
|------|---------|
| index.html | Runnable preview (static HTML) |
| tokens.css | Variant-local design tokens (do NOT promote to globals yet) |

## a11y Status

- [ ] axe-core: WCAG AA pass
- [ ] Color contrast checked (foreground/background pairs)
- [ ] Keyboard navigation verified

## Notes
<!-- Refinement history, feedback, decisions -->
TEMPLATE

cat > "$dir/tokens.css" <<TOKENS
/* tokens.css — variant-local tokens for variant-${n}-${slug}
 * Promote to src/styles/globals.css ONLY after user selects this variant.
 */
:root {
  /* Color */
  --color-primary: ;
  --color-primary-foreground: ;
  --color-background: ;
  --color-foreground: ;

  /* Typography */
  --font-sans: ;
  --font-heading: ;

  /* Spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-8: 2rem;

  /* Radius */
  --radius: 0.5rem;
}
TOKENS

cat > "$dir/index.html" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Variant ${n} — ${slug}</title>
  <link rel="stylesheet" href="tokens.css">
  <!-- Add your Tailwind CDN or compiled CSS here -->
</head>
<body>
  <!-- Variant preview goes here -->
  <p>Variant ${n} — ${slug}</p>
</body>
</html>
HTML

echo "Created $dir"
echo "Next: fill in tokens.css, implement index.html, run axe-core, update README."
