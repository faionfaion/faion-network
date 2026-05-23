// purpose: cn() helper: clsx + tailwind-merge composition for variants.
// consumes: see content/02-output-contract.xml inputs for tailwind-architecture
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// lib/cn.ts — Project-tuned class merging utility
// Combines clsx (conditional joining) + tailwind-merge (conflict resolution).
// Export ONLY this cn(); ban raw clsx() calls in eslint.

import { clsx, type ClassValue } from 'clsx';
import { extendTailwindMerge, twMerge } from 'tailwind-merge';

// Extend tailwind-merge if you have custom token utilities in tailwind.config.ts
// Example: theme.extend.spacing adds custom spacing utilities
const customTwMerge = extendTailwindMerge({
  // Uncomment and adapt when using custom token utilities:
  // extend: {
  //   classGroups: {
  //     'font-size': [{ text: ['display', 'hero'] }],  // custom font-size tokens
  //   },
  // },
});

export function cn(...inputs: ClassValue[]): string {
  return customTwMerge(clsx(inputs));
}

// Usage:
// <div className={cn('base-class', isActive && 'active-class', className)} />
// <Button className={cn(button({ intent: 'primary' }), props.className)} />
