// purpose: TBD-template-header
// consumes: input from methodology
// produces: output artefact
// depends-on: 01-core-rules.xml
// token-budget-impact: small

import { z } from 'zod';
import type { Result } from './result';

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(2).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.date(),
});

export type User = z.infer<typeof UserSchema>;

// Partial schema for update endpoints — id cannot be changed
export const UpdateUserSchema = UserSchema.partial().omit({ id: true });
export type UpdateUserData = z.infer<typeof UpdateUserSchema>;

// Throws ZodError for invalid input
export function validateUser(data: unknown): User {
  return UserSchema.parse(data);
}

// Returns Result — safe to use at API boundaries
export function safeValidateUser(data: unknown): Result<User> {
  const result = UserSchema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data };
  }
  return { success: false, error: result.error };
}
