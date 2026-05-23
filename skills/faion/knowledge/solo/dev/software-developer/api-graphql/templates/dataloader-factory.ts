/*
 * purpose: TypeScript DataLoader factory for 1-to-N relations
 * consumes: Relation list
 * produces: Per-relation DataLoader instance
 * depends-on: content/01-core-rules.xml
 * token-budget-impact: ~300 tokens when loaded
 */
import DataLoader from 'dataloader';
import { db } from '../db';

// Call once per request in context setup — never at module level
export const createLoaders = () => ({
  userById: new DataLoader<string, User | null>(async (ids) => {
    const rows = await db.users.findMany({ where: { id: { in: [...ids] } } });
    const map = new Map(rows.map(u => [u.id, u]));
    // Return in the exact same order as input ids
    return ids.map(id => map.get(id) ?? null);
  }),

  ordersByUserId: new DataLoader<string, Order[]>(async (userIds) => {
    const rows = await db.orders.findMany({
      where: { userId: { in: [...userIds] } },
    });
    const grouped = new Map<string, Order[]>();
    for (const r of rows) {
      const arr = grouped.get(r.userId) ?? [];
      arr.push(r);
      grouped.set(r.userId, arr);
    }
    return userIds.map(id => grouped.get(id) ?? []);
  }),
});

// Usage: in GraphQL context factory
// export async function getContext(request: Request) {
//   return { loaders: createLoaders(), currentUserId: ... };
// }
