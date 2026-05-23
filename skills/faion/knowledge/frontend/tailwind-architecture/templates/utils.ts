// cn() helper — resolves Tailwind class conflicts using clsx + tailwind-merge.
// Install: npm install clsx tailwind-merge
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
