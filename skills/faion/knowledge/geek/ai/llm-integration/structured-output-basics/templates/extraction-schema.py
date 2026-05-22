# purpose: Pydantic schema template for extraction
# consumes: Inputs declared in `AGENTS.md` Prerequisites.
# produces: Filled artefact for `structured-output-basics` matching `content/02-output-contract.xml`.
# depends-on: `content/01-core-rules.xml`, `scripts/validate-structured-output-basics.py`.
# token-budget-impact: small.
"""Skeleton for the `structured-output-basics` template `extraction-schema.py` — fill the placeholders."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skeleton:
    slug: str = "structured-output-basics"
    version: str = "1.1.0"
    owner: str = "role:person"
    approver: str = "role:person"

    def render(self) -> dict:
        return {
            "slug": self.slug,
            "version": self.version,
            "owner": self.owner,
            "approver": self.approver,
        }


if __name__ == "__main__":
    import json
    print(json.dumps(Skeleton().render(), indent=2))
