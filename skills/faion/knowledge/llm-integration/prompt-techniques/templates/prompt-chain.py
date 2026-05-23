"""
purpose: PromptChain — compose PromptTemplate steps with idempotent transforms; side-effects sit outside.
consumes: list of (PromptTemplate, output_key) pairs + initial context dict.
produces: final context dict after every step has rendered + called the model.
depends-on: stdlib; the upstream PromptTemplate (`prompt-basics`).
token-budget-impact: linear in chain length; budget each step independently.
"""
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class ChainStep:
    name: str
    template_render: Callable[[dict], list[dict]]
    output_key: str


def run_chain(steps: list[ChainStep], llm_call: Callable[[list[dict]], str], context: dict) -> dict:
    """Run an idempotent chain of LLM steps.

    `llm_call(messages)` -> content string (use the retry-client wrapper).
    Each step writes its output to `context[step.output_key]`.
    """
    ctx = dict(context)
    for step in steps:
        messages = step.template_render(ctx)
        if not messages or messages[0].get("role") != "system":
            raise ValueError(f"step {step.name}: rendered messages must start with system role")
        result = llm_call(messages)
        if step.output_key in ctx:
            raise KeyError(f"step {step.name}: output_key '{step.output_key}' would overwrite existing context entry")
        ctx[step.output_key] = result
    return ctx


def commit_sink(ctx: dict, sink: Callable[[dict], Any]) -> Any:
    """Run any external side-effects ONCE after the chain completes.

    Chain steps are idempotent transforms; the sink is the only place state changes.
    """
    return sink(ctx)
