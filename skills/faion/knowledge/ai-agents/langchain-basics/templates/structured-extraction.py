# purpose: inline chain using with_structured_output() for reliable extraction
# consumes: a text string to analyse
# produces: validated Extraction Pydantic model
# depends-on: langchain, langchain-anthropic, pydantic v2
# token-budget-impact: ~250 tokens per call (input dependent)
"""LCEL chain that runs structured extraction with Pydantic validation."""
from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Extraction(BaseModel):
    entities: list[str] = Field(description="Named entities found.")
    sentiment: str = Field(description="positive | neutral | negative")
    summary: str = Field(description="One-sentence summary.")


model = ChatAnthropic(model="claude-sonnet-4-7")
structured_model = model.with_structured_output(Extraction)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract entities, sentiment, and a one-sentence summary from the text."),
    ("human", "{text}"),
])

chain = (prompt | structured_model).with_retry(stop_after_attempt=3, wait_exponential_jitter=True)


def extract(text: str) -> Extraction:
    return chain.invoke({"text": text})
