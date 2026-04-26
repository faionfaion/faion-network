"""LlamaIndex RAG Workflow with typed events and parallel retrieval."""
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context,
)
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.response_synthesizers import get_response_synthesizer
from pydantic import BaseModel
from typing import Optional


class QueryEvent(Event):
    query: str


class RetrievedEvent(Event):
    query: str
    nodes: list


class RAGWorkflow(Workflow):
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 5, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.similarity_top_k = similarity_top_k

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> RetrievedEvent:
        """Retrieve relevant nodes from the index."""
        query = ev.get("query")
        retriever = self.index.as_retriever(similarity_top_k=self.similarity_top_k)
        nodes = await retriever.aretrieve(query)
        return RetrievedEvent(query=query, nodes=nodes)

    @step
    async def synthesize(self, ctx: Context, ev: RetrievedEvent) -> StopEvent:
        """Synthesize answer from retrieved nodes."""
        synthesizer = get_response_synthesizer(response_mode="compact")
        response = await synthesizer.asynthesize(ev.query, nodes=ev.nodes)
        return StopEvent(result=str(response))


async def run_rag(index: VectorStoreIndex, query: str) -> str:
    """Execute RAG workflow and return answer."""
    workflow = RAGWorkflow(index=index, timeout=60)
    result = await workflow.run(query=query)
    return result
