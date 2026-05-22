# purpose: working scaffold rendered from the llamaindex-ingestion-pipeline decision-record
# consumes: the JSON decision-record + the profile YAML
# produces: a Python module wired with the chosen options
# depends-on: framework deps per the decision (LangChain / LlamaIndex / asyncio)
# token-budget-impact: ~300 tokens when included in agent context
"""Reference artefact for llamaindex-ingestion-pipeline. Self-test only verifies the scaffold compiles."""
from __future__ import annotations


def build(decision: dict):
    """Build the runtime object from a validated decision-record."""
    if not isinstance(decision, dict):
        raise TypeError("decision must be dict from validated decision-record")
    return decision  # placeholder: real implementations wire here


def _self_test() -> int:
    out = build({"slug": "llamaindex-ingestion-pipeline", "version": "2.0.0"})
    return 0 if out["slug"] == "llamaindex-ingestion-pipeline" else 1


if __name__ == "__main__":
    import sys
    if "--self-test" in sys.argv:
        raise SystemExit(_self_test())
    if "--help" in sys.argv:
        print(__doc__)
