/**
 * Input component — cva() state variants, full a11y wiring.
 *
 * Rules applied:
 * - State variants via cva() (state: default | error | success)
 * - aria-invalid and aria-describedby wired to error/hint
 * - No hardcoded hex or raw Tailwind in className props
 */
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const inputVariants = cva(
  [
    "w-full rounded-md border bg-background px-3 py-2 text-sm",
    "placeholder:text-muted-foreground",
    "focus:outline-none focus:ring-2 focus:ring-offset-0",
    "disabled:cursor-not-allowed disabled:opacity-50",
    "transition-colors",
  ],
  {
    variants: {
      state: {
        default: "border-input focus:ring-ring focus:border-ring",
        error:   "border-destructive focus:ring-destructive focus:border-destructive",
        success: "border-green-500 focus:ring-green-500 focus:border-green-500",
      },
    },
    defaultVariants: { state: "default" },
  }
);

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "id">,
    VariantProps<typeof inputVariants> {
  id?: string;
  label?: string;
  error?: string;
  hint?: string;
}

export function Input({
  id,
  label,
  error,
  hint,
  state,
  className,
  required,
  ...props
}: InputProps) {
  const inputId = id ?? (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);
  const resolvedState = error ? "error" : state;

  return (
    <div className="space-y-1">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-foreground"
        >
          {label}
          {required && <span className="ml-1 text-destructive">*</span>}
        </label>
      )}

      <input
        id={inputId}
        required={required}
        className={cn(inputVariants({ state: resolvedState }), className)}
        aria-invalid={!!error}
        aria-describedby={
          error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined
        }
        {...props}
      />

      {error && (
        <p id={`${inputId}-error`} className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-sm text-muted-foreground">
          {hint}
        </p>
      )}
    </div>
  );
}
