"""
purpose: LCEL pipe-syntax chain skeleton.
consumes: see AGENTS.md ## Prerequisites
produces: code
depends-on: content/02-output-contract.xml schema for langchain
token-budget-impact: ≤500 tokens to fill
"""

# LCEL chain: prompt | model | parser, composed with the pipe operator.
# r1: LCEL only while the flow is linear and stateless. The first loop, retry-with-feedback,
#     or human-approval step means rewriting on LangGraph (templates/langgraph-router-node.py).
# Requires: pip install langchain-core langchain-anthropic   (LCEL `|` composition, stable since 2024)
#           ANTHROPIC_API_KEY in the environment.

from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from pydantic import BaseModel, Field

MAX_DOC_CHARS = 40_000

model = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0, max_tokens=1024)


class Extraction(BaseModel):
    title: str = Field(description="Document title, or a 5-word synthesis if absent.")
    key_points: list[str] = Field(description="3-5 bullet-length findings.")
    sentiment: str = Field(description="positive | neutral | negative")


def _clip(inputs: dict) -> dict:
    """Plain-Python step: any callable in a pipe becomes a Runnable."""
    doc = inputs["document"]
    if len(doc) > MAX_DOC_CHARS:
        raise ValueError(f"document is {len(doc)} chars; chunk upstream, LCEL does not loop (r1)")
    return {**inputs, "document": doc.strip()}


summarise_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarise the document in at most 120 words. Plain prose, no lists."),
    ("human", "{document}"),
])

extract_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the requested fields from the summary. Do not invent facts."),
    ("human", "Summary:\n{summary}\n\nDocument title hint: {title_hint}"),
])

# Stage 1: text in, text out.
summarise = summarise_prompt | model | StrOutputParser()

# Stage 2: keep the original inputs, add `summary`, then produce a typed object.
# .with_retry is a bounded retry on transport errors only; it never feeds output back in.
chain = (
    RunnableLambda(_clip)
    | RunnablePassthrough.assign(summary=summarise)
    | extract_prompt
    | model.with_structured_output(Extraction)
).with_retry(stop_after_attempt=3).with_config(run_name="doc-extract")  # run_name shows in LangSmith traces


if __name__ == "__main__":
    payload = {"document": "<document text>", "title_hint": "<title or empty>"}
    result: Extraction = chain.invoke(payload)
    print(result.model_dump_json(indent=2))

    # Same chain, other call shapes; nothing else changes:
    # chain.batch([payload, payload2], config={"max_concurrency": 4})
    # for chunk in summarise.stream(payload): print(chunk, end="", flush=True)
