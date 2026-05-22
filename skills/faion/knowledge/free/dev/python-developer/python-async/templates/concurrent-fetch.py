"""
purpose: Bounded fan-out: TaskGroup + Semaphore + asyncio.timeout over httpx.AsyncClient.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import asyncio

import httpx


async def fetch_one(
    client: httpx.AsyncClient, url: str, sem: asyncio.Semaphore
) -> dict:
    async with sem:
        async with asyncio.timeout(10):
            response = await client.get(url)
            response.raise_for_status()
            return response.json()


async def fetch_all(urls: list[str], concurrency: int = 10) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(client, url, sem)) for url in urls]
    return [task.result() for task in tasks]
