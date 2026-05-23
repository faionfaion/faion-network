# purpose: router chain using RunnableBranch with explicit fallback default
# consumes: user input with `topic` field for routing
# produces: routed chain output
# depends-on: langchain-core, langchain-anthropic
# token-budget-impact: ~250 tokens per call (input dependent)
"""Router chain template — sequential conditions + default fallback."""
from __future__ import annotations

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch

model = ChatAnthropic(model="claude-sonnet-4-7")
parser = StrOutputParser()

math_chain = ChatPromptTemplate.from_template("Solve this math problem: {input}") | model | parser
code_chain = ChatPromptTemplate.from_template("Write code for: {input}") | model | parser
general_chain = ChatPromptTemplate.from_template("Answer: {input}") | model | parser


def route(info: dict) -> str:
    topic = (info.get("topic") or "").lower()
    if "math" in topic:
        return "math"
    if "code" in topic:
        return "code"
    return "general"


branch = RunnableBranch(
    (lambda x: route(x) == "math", math_chain),
    (lambda x: route(x) == "code", code_chain),
    general_chain,  # default — required so unmatched inputs don't crash
).with_retry(stop_after_attempt=3, wait_exponential_jitter=True)
