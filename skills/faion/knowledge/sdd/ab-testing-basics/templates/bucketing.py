# __faion_header_v1__
# purpose: Deterministic hash-based bucketing for stable variant assignment
# consumes: see content/02-output-contract.xml
# produces: spec
# depends-on: content/04-procedure.xml + content/01-core-rules.xml#deterministic-hash-bucketing
# token-budget-impact: ~230 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"Deterministic hash-based bucketing for stable variant assignment","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/04-procedure.xml + content/01-core-rules.xml#deterministic-hash-bucketing","token_budget_impact":"~230 tokens when loaded as context"}}
import hashlib


def assign(experiment_id: str, user_id: str, variants: list[tuple[str, float]]) -> str:
    raw = f"{experiment_id}:{user_id}".encode()
    bucket = int(hashlib.sha256(raw).hexdigest(), 16) % 10000
    cum = 0
    for variant_id, weight in variants:
        cum += int(weight * 10000)
        if bucket < cum:
            return variant_id
    return variants[-1][0]
