# __faion_header_v1__
# purpose: Strawberry DataLoaders: per-request batch loading, key-order preservation, 1:N grouping
# consumes: see content/02-output-contract.xml
# produces: spec
# depends-on: content/01-core-rules.xml#dataloader-mandatory
# token-budget-impact: ~420 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"Strawberry DataLoaders: per-request batch loading, key-order preservation, 1:N grouping","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#dataloader-mandatory","token_budget_impact":"~420 tokens when loaded as context"}}
from typing import List
from uuid import UUID

from strawberry.dataloader import DataLoader


class OrganizationLoader(DataLoader):
    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, keys: List[UUID]):
        orgs = await self.repository.find_by_ids(keys)
        org_map = {org.id: org for org in orgs}
        # CRITICAL: return in the same order as keys; None for missing.
        return [org_map.get(key) for key in keys]


class UserLoader(DataLoader):
    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, keys: List[UUID]):
        users = await self.repository.find_by_ids(keys)
        user_map = {u.id: u for u in users}
        return [user_map.get(key) for key in keys]


class OrdersByUserLoader(DataLoader):
    """1:N grouping — one list of orders per user_id, empty list when none."""

    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, user_ids: List[UUID]):
        orders = await self.repository.find_by_user_ids(user_ids)
        grouped: dict[UUID, list] = {uid: [] for uid in user_ids}
        for order in orders:
            grouped[order.user_id].append(order)
        return [grouped[uid] for uid in user_ids]


def create_loaders(repository_factory) -> dict:
    """Call once per request from get_context(). Never at module scope —
    a module-level loader caches across requests and leaks user data."""
    return {
        "organization": OrganizationLoader(repository_factory.organization),
        "user": UserLoader(repository_factory.user),
        "orders_by_user": OrdersByUserLoader(repository_factory.order),
    }
