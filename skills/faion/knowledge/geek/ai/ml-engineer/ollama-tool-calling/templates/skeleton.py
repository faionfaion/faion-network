# purpose: skeleton implementation of ollama-tool-calling
# consumes: task brief + constraints
# produces: python module implementing the contract
# depends-on: content/02-output-contract.xml
# token-budget-impact: medium

"""ollama-tool-calling skeleton — fill the TODO blocks and wire to your pipeline.

Implements the output contract in content/02-output-contract.xml.
Run scripts/validate-ollama-tool-calling.py against the emitted payload before handing off.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Payload:
    language: str
    entry_point: str
    files: list[dict[str, str]]


def build_payload(brief: dict[str, Any]) -> Payload:
    """Convert an upstream task brief into the methodology payload."""
    # TODO: replace with the real business logic for ollama-tool-calling.
    return Payload(
        language=brief.get("language", "python"),
        entry_point=brief.get("entry_point", "skeleton.py"),
        files=[{"path": "skeleton.py", "purpose": "main module"}],
    )


if __name__ == "__main__":
    p = build_payload({})
    print(p)
