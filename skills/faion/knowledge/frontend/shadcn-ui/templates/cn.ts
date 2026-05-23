/**
 * cn() — class name merger for shadcn/ui and Tailwind projects.
 *
 * Combines clsx (conditional class strings) with tailwind-merge
 * (conflict resolution, e.g. p-2 p-4 → p-4).
 *
 * Usage:
 *   cn("p-2", isLarge && "p-4")  → "p-4"
 *   cn(buttonVariants({ variant }), className)
 */
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
