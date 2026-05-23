# __faion_header_v1__
# purpose: Typed ExperimentEvent (exposure + conversion) with stable schema
# consumes: see content/02-output-contract.xml
# produces: code; depends-on: content/01-core-rules.xml#typed-event-schema
# faion_header_json: {"__faion_header__":{"purpose":"Typed ExperimentEvent (exposure + conversion) with stable schema","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-event-schema","token_budget_impact":"~150 tokens when loaded"}}
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal


@dataclass
class ExperimentEvent:
    experiment_id: str
    user_id: str
    variant_id: str
    kind: Literal["exposure", "conversion"]
    ts: datetime
    properties: dict = field(default_factory=dict)
