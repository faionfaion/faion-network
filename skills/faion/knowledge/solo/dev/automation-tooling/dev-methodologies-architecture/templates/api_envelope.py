# __faion_header_v1__
# purpose: Standard API response envelope: data + meta + errors
# consumes: see content/02-output-contract.xml
# produces: rubric; depends-on: content/01-core-rules.xml#indexed-foreign-keys
# faion_header_json: {"__faion_header__":{"purpose":"Standard API response envelope: data + meta + errors","consumes":"see content/02-output-contract.xml","produces":"rubric","depends_on":"content/01-core-rules.xml#indexed-foreign-keys","token_budget_impact":"~150 tokens when loaded"}}
from typing import Any
from dataclasses import dataclass, field


@dataclass
class ApiResponse:
    data: Any = None
    meta: dict = field(default_factory=dict)
    errors: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"data": self.data, "meta": self.meta, "errors": self.errors}
