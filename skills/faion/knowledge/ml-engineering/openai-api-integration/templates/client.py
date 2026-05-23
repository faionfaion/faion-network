# purpose: Singleton OpenAI client + AsyncOpenAI factory
# consumes: Inputs declared in `AGENTS.md` Prerequisites.
# produces: Filled artefact for `openai-api-integration` matching `content/02-output-contract.xml`.
# depends-on: `content/01-core-rules.xml`, `scripts/validate-openai-api-integration.py`.
# token-budget-impact: small.
"""Skeleton for the `openai-api-integration` template `client.py` — fill the placeholders."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skeleton:
    slug: str = "openai-api-integration"
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
    import sys
    sys.stdout.write(json.dumps(Skeleton().render(), indent=2) + "\n")
