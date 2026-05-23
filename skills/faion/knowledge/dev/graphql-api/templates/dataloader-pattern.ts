// purpose: DataLoader factory pattern per request
// consumes: See content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1000 tokens when loaded as context
// dataloader-pattern.ts — Per-request DataLoader context factory
// Wire into your GraphQL server context function.
// Each request gets fresh DataLoader instances — never share across requests.

import DataLoader from 'dataloader';
import { db } from './db';

// Batch function: receives array of IDs, returns array of items in same order
async function batchUsers(ids: readonly string[]) {
  const users = await db.user.findMany({ where: { id: { in: [...ids] } } });
  const userMap = new Map(users.map((u) => [u.id, u]));
  // Must return items in the same order as input IDs, null for missing
  return ids.map((id) => userMap.get(id) ?? null);
}

async function batchProductsByOrderId(orderIds: readonly string[]) {
  const items = await db.orderItem.findMany({
    where: { orderId: { in: [...orderIds] } },
    include: { product: true },
  });
  const grouped = new Map<string, typeof items>();
  for (const item of items) {
    const list = grouped.get(item.orderId) ?? [];
    list.push(item);
    grouped.set(item.orderId, list);
  }
  return orderIds.map((id) => grouped.get(id) ?? []);
}

export interface GraphQLContext {
  userId: string | null;
  loaders: {
    user: DataLoader<string, Awaited<ReturnType<typeof batchUsers>>[number]>;
    productsByOrder: DataLoader<string, Awaited<ReturnType<typeof batchProductsByOrderId>>[number]>;
  };
}

// Called once per request by the GraphQL server
export function createContext(req: { user?: { id: string } }): GraphQLContext {
  return {
    userId: req.user?.id ?? null,
    loaders: {
      user: new DataLoader(batchUsers),
      productsByOrder: new DataLoader(batchProductsByOrderId),
    },
  };
}
