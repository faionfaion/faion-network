# purpose: minimum runnable smoke test for the RAG pipeline scaffold
# consumes: in-memory fake vector_store, reranker, llm, judge
# produces: prints a RAG answer dict and exits 0 on success
# depends-on: templates/rag-pipeline.py.tmpl
# token-budget-impact: zero at runtime

from rag_pipeline import run  # rename .tmpl -> .py


class FakeVS:
    def hybrid_search(self, q, k):
        return [{"chunk_id": f"c{i}", "source": "doc.md", "page": i, "text": f"chunk {i} about {q}", "score": 1 - 0.1 * i} for i in range(k)]


class FakeRerank:
    def rerank(self, q, c, top_k):
        return c[:top_k]


class FakeLLM:
    def complete(self, prompt):
        return {"text": "Answer [Source: doc.md, page 0].", "citations": [{"source": "doc.md", "page": 0, "chunk_id": "c0"}]}


class FakeJudge:
    def faithfulness(self, a, c):
        return 0.95


if __name__ == "__main__":
    out = run("test", FakeVS(), FakeRerank(), FakeLLM(), FakeJudge(), "Q: {query}\nC: {context}")
    assert out["faithfulness"] > 0.9
    assert out["citations"][0]["validated"] is True
    print(out)
