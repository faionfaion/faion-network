# __faion_header_v1__
# purpose: Deterministic per-user bucketing with rollout_percent + targeting attrs
# consumes: see content/02-output-contract.xml
# produces: spec; depends-on: content/01-core-rules.xml#deterministic-per-user
# faion_header_json: {"__faion_header__":{"purpose":"Deterministic per-user bucketing with rollout_percent + targeting attrs","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#deterministic-per-user","token_budget_impact":"~150 tokens when loaded"}}
import hashlib


def in_rollout(flag_name: str, user_id: str, rollout_percent: int) -> bool:
    raw = f"{flag_name}:{user_id}".encode()
    bucket = int(hashlib.sha256(raw).hexdigest(), 16) % 100
    return bucket < rollout_percent


def targeted(targeting: dict, attrs: dict) -> bool:
    for key, allowed in targeting.items():
        if attrs.get(key) not in allowed:
            return False
    return True
