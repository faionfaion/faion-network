# __faion_header_v1__
# purpose: Two-proportion z-test with Wilson 95% CI
# consumes: see content/02-output-contract.xml
# produces: code; depends-on: content/01-core-rules.xml#typed-event-schema
# faion_header_json: {"__faion_header__":{"purpose":"Two-proportion z-test with Wilson 95% CI","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-event-schema","token_budget_impact":"~150 tokens when loaded"}}
import math


def two_proportion_z(c1: int, n1: int, c2: int, n2: int) -> dict:
    if n1 == 0 or n2 == 0:
        return {"p_value": None, "reason": "empty arm"}
    p1, p2 = c1 / n1, c2 / n2
    p_pool = (c1 + c2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        return {"p_value": 1.0, "lift": 0.0}
    z = (p2 - p1) / se
    # two-sided p via normal CDF approximation
    p_value = math.erfc(abs(z) / math.sqrt(2))
    return {"p1": p1, "p2": p2, "z": z, "p_value": p_value, "lift": p2 - p1}


def wilson_ci(c: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    phat = c / n
    denom = 1 + z * z / n
    centre = (phat + z * z / (2 * n)) / denom
    half = (z * math.sqrt(phat * (1 - phat) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))
