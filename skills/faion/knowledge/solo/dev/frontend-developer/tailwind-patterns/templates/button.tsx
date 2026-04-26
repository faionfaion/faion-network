/**
 * Button component — canonical cva() + cn() pattern.
 *
 * Rules applied:
 * - One cva() block, colocated with the component
 * - Variants describe intent (tone=) not style (color=)
 * - No dynamic class interpolation
 * - cn() wraps all className construction
 * - data-* selectors for state (e.g. data-loading)
 */
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  [
    "inline-flex items-center justify-center gap-2 font-medium rounded-md",
    "transition-colors focus-visible:outline-none focus-visible:ring-2",
    "focus-visible:ring-ring focus-visible:ring-offset-2",
    "disabled:pointer-events-none disabled:opacity-50",
    // data-loading state: show spinner cursor
    "data-[loading=true]:cursor-wait",
  ],
  {
    variants: {
      tone: {
        default:
          "bg-primary text-primary-foreground hover:bg-primary/90",
        danger:
          "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline:
          "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost:
          "hover:bg-accent hover:text-accent-foreground",
        link:
          "text-primary underline-offset-4 hover:underline",
      },
      size: {
        sm: "h-9 px-3 text-sm",
        md: "h-10 px-4",
        lg: "h-11 px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      tone: "default",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, tone, size, loading = false, disabled, children, ...props }, ref) => (
    <button
      ref={ref}
      data-loading={loading}
      disabled={disabled || loading}
      className={cn(buttonVariants({ tone, size }), className)}
      {...props}
    >
      {loading && (
        <span
          className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
          aria-hidden="true"
        />
      )}
      {children}
    </button>
  )
);
Button.displayName = "Button";

export { Button, buttonVariants };
