# purpose: redacting CallbackHandler scaffold for LangChain
# consumes: chain runs
# produces: structured JSON log lines + safe LangSmith payloads
# depends-on: langchain-core
# token-budget-impact: ~300 tokens when included
"""Wrap LangSmith with redaction + structured logging.

Use as:
    chain.invoke(payload, config={"callbacks": [RedactingHandler()]})
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler

LOG = logging.getLogger("langchain.obs")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")


def _redact(s: str) -> str:
    s = SSN_RE.sub("[REDACTED-SSN]", s)
    s = EMAIL_RE.sub("[REDACTED-EMAIL]", s)
    return s


class RedactingHandler(BaseCallbackHandler):
    raise_error = True  # do NOT swallow callback errors

    def on_chain_start(self, serialized: dict[str, Any], inputs: dict[str, Any], **kw: Any) -> None:
        LOG.info(json.dumps({"event": "chain_start", "name": serialized.get("name"), "input_keys": list(inputs)}))

    def on_chain_end(self, outputs: dict[str, Any], **kw: Any) -> None:
        red = {k: _redact(str(v)) for k, v in outputs.items()}
        LOG.info(json.dumps({"event": "chain_end", "outputs": red}))

    def on_chain_error(self, error: BaseException, **kw: Any) -> None:
        LOG.error(json.dumps({"event": "chain_error", "error": str(error)}))


def _self_test() -> int:
    assert _redact("contact me at a@b.com") == "contact me at [REDACTED-EMAIL]"
    assert _redact("ssn 123-45-6789") == "ssn [REDACTED-SSN]"
    return 0


if __name__ == "__main__":
    import sys

    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
