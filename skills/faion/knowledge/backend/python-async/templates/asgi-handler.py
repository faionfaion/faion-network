"""
purpose: FastAPI-style handler showing TaskGroup composition inside a request.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import asyncio

from fastapi import FastAPI

app = FastAPI()


async def get_profile(user_id: int) -> dict:
    return {"id": user_id, "name": "demo"}


async def get_orders(user_id: int) -> list[dict]:
    return []


@app.get("/users/{user_id}/dashboard")
async def dashboard(user_id: int) -> dict:
    async with asyncio.TaskGroup() as tg:
        profile_task = tg.create_task(get_profile(user_id))
        orders_task = tg.create_task(get_orders(user_id))
    return {"profile": profile_task.result(), "orders": orders_task.result()}
