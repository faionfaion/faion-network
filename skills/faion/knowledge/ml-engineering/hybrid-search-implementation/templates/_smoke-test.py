# purpose: minimum runnable smoke test for HybridSearchService
# consumes: fake dense + sparse clients
# produces: prints a fused result and exits 0 on success
# depends-on: templates/hybrid_search_service.py.tmpl
# token-budget-impact: zero at runtime

import asyncio
from hybrid_search_service import HybridSearchService  # rename .tmpl -> .py to run


class Fake:
    def __init__(self, prefix):
        self.prefix = prefix

    async def search(self, q, k):
        return [{"id": f"{self.prefix}-{i}", "score": 1.0 - 0.1 * i} for i in range(k)]


async def main():
    svc = HybridSearchService(dense=Fake("d"), sparse=Fake("s"), k_final=5)
    out = await svc.search("test query")
    assert len(out["results"]) == 5
    assert out["fusion"] == "rrf"
    print(out)


if __name__ == "__main__":
    asyncio.run(main())
