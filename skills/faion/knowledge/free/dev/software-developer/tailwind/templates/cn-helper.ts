// lib/utils.ts — cn() helper combining clsx + tailwind-merge
// Install: npm install clsx tailwind-merge
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Merge Tailwind classes with conflict resolution.
 * Use for all conditional class joining — never template literals.
 *
 * @example
 * cn("p-4 text-sm", isActive && "bg-blue-500", className)
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
