import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * cn() — the only class merger in a shadcn/ui project.
 * Combines clsx (conditional logic) + tailwind-merge (conflict resolution).
 *
 * Usage:
 *   cn("p-4", condition && "bg-red-500", className)
 *   cn(buttonVariants({ variant, size }), className)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
