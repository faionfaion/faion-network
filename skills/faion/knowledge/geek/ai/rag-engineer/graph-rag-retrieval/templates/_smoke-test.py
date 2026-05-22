# purpose: minimum runnable smoke test for the router scaffold
# consumes: in-memory fixture (graph + fake vector_store + fake summaries)
# produces: prints a result dict and exits 0 on success
# depends-on: templates/router.py.tmpl
# token-budget-impact: zero at runtime

from dataclasses import dataclass
import networkx as nx
from router import route, QueryType  # rename router.py.tmpl -> router.py to run


@dataclass
class FakeStore:
    def search(self, q, k):
        return [{"id": f"chunk-{i}-{q[:6]}", "score": 0.5 - 0.05 * i} for i in range(k)]


G = nx.Graph()
G.add_edges_from([("Alice", "Acme"), ("Acme", "Globex"), ("Bob", "Acme")])
summaries = {"global": "The corpus describes founders, companies, and acquisitions."}

if __name__ == "__main__":
    res = route("How is Alice connected to Globex?", QueryType.RELATIONSHIP, G, summaries, FakeStore())
    assert res["query_type"] == "RELATIONSHIP"
    assert res["retrieval_path"] in ("shortest-path", "vector-search")
    print(res)
