/**
 * DataLoader pattern for GraphQL resolvers.
 * Always instantiate per-request in GraphQL context factory — never module-global.
 *
 * Usage in context factory:
 *   context: ({ req }) => ({
 *     loaders: {
 *       user: createUserLoader(),
 *       order: createOrderLoader(),
 *     }
 *   })
 *
 * Usage in resolver:
 *   async user(order: Order, _: unknown, ctx: Context) {
 *     return ctx.loaders.user.load(order.userId);
 *   }
 */
import DataLoader from 'dataloader';

// Type your DB record
interface UserRecord {
  id: string;
  name: string;
  email: string;
}

export function createUserLoader(
  db: { users: { findMany: (q: { where: { id: { in: string[] } } }) => Promise<UserRecord[]> } }
): DataLoader<string, UserRecord | null> {
  return new DataLoader<string, UserRecord | null>(
    async (userIds: readonly string[]) => {
      const users = await db.users.findMany({
        where: { id: { in: [...userIds] } },
      });
      // Return in the same order as keys — DataLoader requirement
      const byId = new Map(users.map(u => [u.id, u]));
      return userIds.map(id => byId.get(id) ?? null);
    },
    { maxBatchSize: 500 }
  );
}
