# __faion_header_v1__
# purpose: Strawberry DataLoader: per-request batch loading with key-order preservation
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#schema-first
# faion_header_json: {"__faion_header__":{"purpose":"Strawberry DataLoader: per-request batch loading with key-order preservation","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#schema-first","token_budget_impact":"~150 tokens when loaded"}}
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
        return [org_map.get(key) for key in keys]
