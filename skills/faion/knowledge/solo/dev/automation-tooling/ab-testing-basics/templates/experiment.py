"""Experiment schema and deterministic assignment for A/B tests."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import hashlib


class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Variant:
    name: str
    allocation: float  # 0.0 to 1.0, all variants must sum to 1.0
    description: str = ""


@dataclass
class Metric:
    name: str
    type: str  # "conversion" | "continuous" | "count"
    primary: bool = False
    direction: str = "increase"  # "increase" | "decrease"


@dataclass
class Experiment:
    id: str
    name: str
    hypothesis: str
    variants: list[Variant]
    metrics: list[Metric]
    status: ExperimentStatus = ExperimentStatus.DRAFT
    target_sample_size: int = 0  # set via sample_size_per_variant(), never a round number
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> list[str]:
        errors = []
        total = sum(v.allocation for v in self.variants)
        if abs(total - 1.0) > 0.001:
            errors.append(f"Allocations must sum to 1.0, got {total}")
        if len(self.variants) < 2:
            errors.append("Need at least 2 variants")
        if not self.metrics:
            errors.append("Need at least one metric")
        primary_count = sum(1 for m in self.metrics if m.primary)
        if primary_count != 1:
            errors.append(f"Must have exactly 1 primary metric, got {primary_count}")
        return errors


class ExperimentAssigner:
    """Assigns users to variants deterministically using md5 hash bucketing."""

    def __init__(self, experiments: dict[str, Experiment]):
        self.experiments = experiments

    def get_variant(
        self,
        experiment_id: str,
        user_id: str,
        override: Optional[str] = None,
        is_staff: bool = False,
    ) -> Optional[str]:
        experiment = self.experiments.get(experiment_id)
        if not experiment or experiment.status != ExperimentStatus.RUNNING:
            return None

        # Override only allowed for staff — never expose as unauthenticated param
        if override and is_staff and any(v.name == override for v in experiment.variants):
            return override

        # Deterministic bucketing — do NOT change the hash function after launch
        hash_key = f"{experiment_id}:{user_id}"
        hash_value = int(hashlib.md5(hash_key.encode()).hexdigest(), 16)  # noqa: S324
        bucket = (hash_value % 10000) / 10000.0

        cumulative = 0.0
        for variant in experiment.variants:
            cumulative += variant.allocation
            if bucket < cumulative:
                return variant.name

        return experiment.variants[-1].name
