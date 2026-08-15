# __faion_header_v1__
# purpose: @feature(name) decorator gating a function on flag state
# consumes: see content/02-output-contract.xml
# produces: code
# depends-on: content/04-procedure.xml + content/01-core-rules.xml#single-call-site
# token-budget-impact: ~200 tokens when loaded as context
# faion_header_json: {"__faion_header__":{"purpose":"@feature(name) decorator gating a function on flag state","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/04-procedure.xml + content/01-core-rules.xml#single-call-site","token_budget_impact":"~200 tokens when loaded as context"}}
from functools import wraps
from typing import Callable


def feature(name: str, manager):
    def deco(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not manager.is_enabled(name):
                raise PermissionError(f"feature {name} disabled")
            return fn(*args, **kwargs)
        return wrapper
    return deco
