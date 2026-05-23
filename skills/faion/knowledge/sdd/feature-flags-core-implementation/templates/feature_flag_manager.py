# __faion_header_v1__
# purpose: FeatureFlagManager: typed flag registry + env/file loader + is_enabled API
# consumes: see content/02-output-contract.xml
# produces: code; depends-on: content/01-core-rules.xml#typed-flag-registration
# faion_header_json: {"__faion_header__":{"purpose":"FeatureFlagManager: typed flag registry + env/file loader + is_enabled API","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#typed-flag-registration","token_budget_impact":"~150 tokens when loaded"}}
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class FeatureFlag:
    name: str
    description: str
    default: bool = False
    rollout_percent: int = 0
    targeting: dict = field(default_factory=dict)


class FeatureFlagManager:
    def __init__(self) -> None:
        self._flags: dict[str, FeatureFlag] = {}
        self._overrides: dict[str, bool] = {}

    def register(self, flag: FeatureFlag) -> None:
        self._flags[flag.name] = flag

    def load_env(self, prefix: str = "FF_") -> None:
        for k, v in os.environ.items():
            if not k.startswith(prefix):
                continue
            name = k.removeprefix(prefix).lower().replace("_", "-")
            self._overrides[name] = v.lower() in ("1", "true", "yes")

    def load_file(self, path: Path) -> None:
        if not path.is_file():
            return
        data = json.loads(path.read_text())
        for name, value in data.items():
            self._overrides[name] = bool(value)

    def is_enabled(self, name: str, user_id: str | None = None) -> bool:
        if name in self._overrides:
            return self._overrides[name]
        flag = self._flags.get(name)
        if flag is None:
            return False
        return flag.default
