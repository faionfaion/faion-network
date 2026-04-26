"""
Strawberry DataLoader batch functions.
Input: list of keys (UUIDs)
Output: list of entities in same order as keys (None for missing)
"""
from strawberry.dataloader import DataLoader
from typing import List
from uuid import UUID


class OrganizationLoader(DataLoader[UUID, "Organization"]):
    async def batch_load_fn(self, keys: List[UUID]) -> List["Organization"]:
        organizations = await self.repository.find_by_ids(keys)
        org_map = {org.id: org for org in organizations}
        # CRITICAL: return in same order as keys; None for missing
        return [org_map.get(key) for key in keys]


class UserLoader(DataLoader[UUID, "User"]):
    async def batch_load_fn(self, keys: List[UUID]) -> List["User"]:
        users = await self.repository.find_by_ids(keys)
        user_map = {u.id: u for u in users}
        return [user_map.get(key) for key in keys]


# 1:N grouping: orders keyed by user_id
class OrdersByUserLoader(DataLoader[UUID, List["Order"]]):
    async def batch_load_fn(self, user_ids: List[UUID]) -> List[List["Order"]]:
        orders = await self.repository.find_by_user_ids(user_ids)
        grouped: dict[UUID, list] = {uid: [] for uid in user_ids}
        for order in orders:
            grouped[order.user_id].append(order)
        return [grouped[uid] for uid in user_ids]


# Context factory — call once per request, never at module level
def create_loaders(repository_factory) -> dict:
    return {
        "organization": OrganizationLoader(repository_factory.organization),
        "user": UserLoader(repository_factory.user),
        "orders_by_user": OrdersByUserLoader(repository_factory.order),
    }
