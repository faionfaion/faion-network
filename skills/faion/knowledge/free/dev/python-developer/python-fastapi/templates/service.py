"""
purpose: Service function skeleton: AsyncSession dependency, returns Pydantic response model.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ItemIn, ItemOut


async def create_item(session: AsyncSession, payload: ItemIn) -> ItemOut:
    # ORM logic lives here; route stays thin.
    return ItemOut(id=1, name=payload.name)
