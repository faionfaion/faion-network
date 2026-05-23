"""
purpose: Thin FastAPI router: Depends() for session, Pydantic schema in/out, calls service.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ItemIn, ItemOut
from .service import create_item
from .deps import get_session

router = APIRouter()


@router.post("/items", response_model=ItemOut, status_code=201)
async def create_item_endpoint(
    payload: ItemIn,
    session: AsyncSession = Depends(get_session),
) -> ItemOut:
    return await create_item(session, payload)
