// Discriminated union Result type
export type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Assertion helper — narrows T | null | undefined to T
export function assertDefined<T>(
  value: T | null | undefined,
  message = 'Value is null or undefined',
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}
