/*
 * purpose: Component composing utilities via cn() with conditional variants.
 * consumes: 01-core-rules.xml
 * produces: config
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: small
 */

import { cn } from "./cn";

type Props = {
  label: string;
  variant?: "primary" | "destructive";
  className?: string;
};

export function Button({ label, variant = "primary", className }: Props) {
  return (
    <button
      type="button"
      className={cn(
        "px-4 py-2 rounded font-medium",
        variant === "primary" && "bg-primary text-white",
        variant === "destructive" && "bg-destructive text-white",
        className,
      )}
    >
      {label}
    </button>
  );
}
