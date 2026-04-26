"""FeatureFlagManager — env overrides, group/user lists, percentage bucketing."""
import hashlib
import json
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class FlagType(Enum):
    RELEASE = "release"
    EXPERIMENT = "experiment"
    OPS = "ops"
    PERMISSION = "permission"
    KILL_SWITCH = "kill_switch"


@dataclass
class FeatureFlag:
    name: str
    flag_type: FlagType
    default: bool = False
    description: str = ""
    owner: str = ""


@dataclass
class RolloutConfig:
    percentage: int = 0          # 0-100
    user_ids: set[str] = field(default_factory=set)
    groups: set[str] = field(default_factory=set)


class FeatureFlagManager:
    def __init__(self):
        self._flags: dict[str, FeatureFlag] = {}
        self._rollouts: dict[str, RolloutConfig] = {}
        self._overrides: dict[str, bool] = {}
        self._load_overrides()

    def _load_overrides(self):
        for key, value in os.environ.items():
            if key.startswith("FF_"):
                self._overrides[key[3:].lower()] = value.lower() in ("true", "1", "yes")
        config_path = os.getenv("FEATURE_FLAGS_CONFIG")
        if config_path and os.path.exists(config_path):
            with open(config_path) as f:
                self._overrides.update(json.load(f))

    def register(self, flag: FeatureFlag) -> None:
        self._flags[flag.name] = flag

    def set_rollout(self, flag_name: str, config: RolloutConfig) -> None:
        self._rollouts[flag_name] = config

    def is_enabled(
        self,
        flag_name: str,
        user_id: Optional[str] = None,
        groups: Optional[set[str]] = None,
    ) -> bool:
        if flag_name in self._overrides:
            return self._overrides[flag_name]
        flag = self._flags.get(flag_name)
        if not flag:
            return False
        rollout = self._rollouts.get(flag_name)
        if not rollout:
            return flag.default
        if user_id and user_id in rollout.user_ids:
            return True
        if groups and rollout.groups & groups:
            return True
        if rollout.percentage > 0 and user_id:
            key = f"{flag_name}:{user_id}"
            bucket = int(hashlib.md5(key.encode()).hexdigest(), 16) % 100
            return bucket < rollout.percentage
        return flag.default


feature_flags = FeatureFlagManager()
