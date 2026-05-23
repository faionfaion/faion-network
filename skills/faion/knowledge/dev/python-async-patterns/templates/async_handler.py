"""purpose: Async handler skeleton with TaskGroup, timeout, Semaphore, sync-offload pattern.
consumes: see content/02-output-contract.xml inputs for python-async-patterns
produces: artefact conforming to content/02-output-contract.xml
depends-on: content/01-core-rules.xml + content/04-procedure.xml
token-budget-impact: ~200-700 tokens when loaded as context"""

import asyncio
import httpx

FANOUT_CAP = asyncio.Semaphore(50)

async def fetch_one(client: httpx.AsyncClient, url: str) -> dict:
    async with FANOUT_CAP:
        async with asyncio.timeout(3.0):
            r = await client.get(url)
            r.raise_for_status()
            return r.json()

async def handle(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_one(client, u)) for u in urls]
    return [t.result() for t in tasks]

async def heavy_sync_wrapper(blob: bytes) -> bytes:
    return await asyncio.to_thread(compress_legacy_sync, blob)

def compress_legacy_sync(blob: bytes) -> bytes:
    return blob[::-1]
