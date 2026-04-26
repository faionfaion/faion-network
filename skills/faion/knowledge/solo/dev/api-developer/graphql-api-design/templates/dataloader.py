"""
Strawberry GraphQL DataLoader template.
Instantiate per-request in context factory, never at module scope.

Usage in context factory (FastAPI + Strawberry):

    @app.post("/graphql")
    async def graphql_endpoint(request: Request):
        context = {
            "request": request,
            "loaders": {
                "organization": OrganizationLoader(repository=org_repo),
            },
        }
        return await schema.execute_async(
            ..., context_value=context
        )

Usage in resolver:

    @strawberry.type
    class User:
        organization_id: UUID

        @strawberry.field
        async def organization(self, info: Info) -> "Organization":
            return await info.context["loaders"]["organization"].load(self.organization_id)
"""
from strawberry.dataloader import DataLoader
from typing import List
from uuid import UUID


class OrganizationLoader(DataLoader):
    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, keys: List[UUID]) -> List:
        # Fetch all in a single query
        organizations = await self.repository.find_by_ids(keys)

        # Return in the SAME ORDER as keys — DataLoader requirement
        org_map = {org.id: org for org in organizations}
        return [org_map.get(key) for key in keys]
