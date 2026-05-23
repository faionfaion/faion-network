// purpose: cva variant authoring example: typed Variants + slot composition.
// consumes: see content/02-output-contract.xml inputs for tailwind-architecture
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml + content/04-procedure.xml
// token-budget-impact: ~200-700 tokens when loaded as context
// cva-variant-example.tsx — Button with cva variants + cn() passthrough
// Pattern: define base + variants in cva, accept className prop for overrides.

import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/cn';
import type { ButtonHTMLAttributes } from 'react';

const button = cva(
  // Base classes shared by all variants
  'inline-flex items-center justify-center rounded-button font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      intent: {
        primary:     'bg-primary text-primary-foreground hover:bg-primary/90',
        secondary:   'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        ghost:       'hover:bg-muted hover:text-foreground',
        outline:     'border border-input bg-background hover:bg-muted',
      },
      size: {
        sm: 'h-8 px-3 text-xs',
        md: 'h-10 px-4 text-sm',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      intent: 'primary',
      size: 'md',
    },
  }
);

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof button> {
  // className passthrough for per-use overrides via cn()
}

export function Button({ className, intent, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(button({ intent, size }), className)}
      {...props}
    />
  );
}
