// lib/utils.ts — canonical cn() helper
// Combines clsx (conditional class logic) with tailwind-merge (deduplication)
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
