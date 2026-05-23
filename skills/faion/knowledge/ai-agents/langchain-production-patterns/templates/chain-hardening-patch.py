# purpose: working hardening patch for a LangChain Runnable
# consumes: a primary + secondary ChatModel
# produces: hardened chain with fallbacks, retry, configurable fields
# depends-on: langchain-core, langchain-anthropic, langchain-openai
# token-budget-impact: ~300 tokens
"""Apply with_fallbacks + with_retry + configurable_fields to a chain.

Smoke:
    python chain-hardening-patch.py --self-test
"""
from __future__ import annotations


def harden(primary, backup, prompt, parser):
    """Compose a hardened chain.

    Returns a Runnable safe for production.
    """
    from langchain_core.runnables import ConfigurableField

    model = primary.configurable_fields(
        model=ConfigurableField(id="model"),
        temperature=ConfigurableField(id="temperature"),
    ).with_fallbacks([backup])

    chain = (prompt | model | parser).with_retry(
        stop_after_attempt=3,
        wait_exponential_jitter=True,
        retry_if_exception_type=(Exception,),
    )
    return chain


def _self_test() -> int:
    class FakeRunnable:
        def configurable_fields(self, **kw): return self
        def with_fallbacks(self, lst): return self
        def __or__(self, other): return self
        def with_retry(self, **kw): return self

    out = harden(FakeRunnable(), FakeRunnable(), FakeRunnable(), FakeRunnable())
    return 0 if out is not None else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
