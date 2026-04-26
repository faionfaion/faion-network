"""
Bounded concurrent HTTP fan-out: TaskGroup + Semaphore + per-call timeout + ordered results.
Pattern: create all tasks up front (cheap), limit concurrent execution via Semaphore.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class FetchResult:
    url: str
    status: int | None = None
    data: Any = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


async def fetch_one(
    client: httpx.AsyncClient,
    url: str,
    sem: asyncio.Semaphore,
    timeout: float = 10.0,
) -> FetchResult:
    """Fetch a single URL with semaphore-bounded concurrency and per-call timeout."""
    async with sem:  # Semaphore acquired inside the task (not outside)
        try:
            async with asyncio.timeout(timeout):
                response = await client.get(url)
                response.raise_for_status()
                return FetchResult(url=url, status=response.status_code, data=response.json())
        except TimeoutError:
            return FetchResult(url=url, error=f"Timed out after {timeout}s")
        except httpx.HTTPStatusError as e:
            return FetchResult(url=url, status=e.response.status_code, error=str(e))
        except httpx.RequestError as e:
            return FetchResult(url=url, error=str(e))


async def fetch_all(
    urls: list[str],
    *,
    concurrency: int = 10,
    timeout: float = 10.0,
    base_url: str = "",
) -> list[FetchResult]:
    """
    Fetch all URLs concurrently, bounded to `concurrency` simultaneous requests.
    Returns results in the same order as the input URLs.
    """
    sem = asyncio.Semaphore(concurrency)
    limits = httpx.Limits(
        max_connections=concurrency + 5,
        max_keepalive_connections=concurrency,
    )

    async with httpx.AsyncClient(base_url=base_url, limits=limits) as client:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(fetch_one(client, url, sem, timeout))
                for url in urls
            ]
    # TaskGroup guarantees all tasks completed (or all cancelled on first unhandled error)
    return [task.result() for task in tasks]


# ─── Example usage ───────────────────────────────────────────────────────────

async def main() -> None:
    urls = [f"https://httpbin.org/get?n={i}" for i in range(50)]
    results = await fetch_all(urls, concurrency=10, timeout=5.0)

    succeeded = [r for r in results if r.ok]
    failed = [r for r in results if not r.ok]

    print(f"Succeeded: {len(succeeded)}/{len(results)}")
    for r in failed:
        print(f"  FAIL {r.url}: {r.error}")


if __name__ == "__main__":
    asyncio.run(main())
