/**
 * cn() — canonical class name helper for Tailwind + cva() projects.
 *
 * Combines clsx (conditional, array, and object class inputs)
 * with tailwind-merge (resolves conflicting utilities deterministically).
 *
 * Install: npm i clsx tailwind-merge
 *
 * Usage:
 *   cn("p-2", isActive && "bg-primary", className)
 *   cn(buttonVariants({ tone, size }), className)
 */
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
