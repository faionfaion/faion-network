"""
ExperimentAnalyzer: z-test for proportions, Wilson CI, power calculation.
Input: control/treatment counts from experiment data
Output: ExperimentResults dataclass with significance, lift, CI, power
"""
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Optional


@dataclass
class VariantStats:
    name: str
    sample_size: int
    conversions: int = 0
    conversion_rate: float = 0.0
    confidence_interval: tuple[float, float] = (0.0, 0.0)


@dataclass
class ExperimentResults:
    experiment_id: str
    metric_name: str
    control: VariantStats
    treatment: VariantStats
    relative_lift: float
    p_value: float
    is_significant: bool
    confidence_level: float
    power: float
    sample_size_needed: int


class ExperimentAnalyzer:
    def __init__(self, confidence_level: float = 0.95):
        self.confidence_level = confidence_level
        self.alpha = 1 - confidence_level

    def analyze_conversion(
        self, experiment_id: str, metric_name: str,
        control_conversions: int, control_total: int,
        treatment_conversions: int, treatment_total: int,
    ) -> ExperimentResults:
        """Two-proportion z-test for binary conversion metric."""
        cr = control_conversions / control_total if control_total > 0 else 0
        tr = treatment_conversions / treatment_total if treatment_total > 0 else 0
        lift = (tr - cr) / cr if cr > 0 else 0

        pooled = (control_conversions + treatment_conversions) / (control_total + treatment_total)
        se = np.sqrt(pooled * (1 - pooled) * (1 / control_total + 1 / treatment_total))
        z = (tr - cr) / se if se > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

        return ExperimentResults(
            experiment_id=experiment_id,
            metric_name=metric_name,
            control=VariantStats("control", control_total, control_conversions,
                                 cr, self._wilson_ci(control_conversions, control_total)),
            treatment=VariantStats("treatment", treatment_total, treatment_conversions,
                                   tr, self._wilson_ci(treatment_conversions, treatment_total)),
            relative_lift=lift,
            p_value=p_value,
            is_significant=p_value < self.alpha,
            confidence_level=self.confidence_level,
            power=self._power(cr, tr, control_total, treatment_total),
            sample_size_needed=self._sample_size(cr, lift),
        )

    def _wilson_ci(self, successes: int, total: int) -> tuple[float, float]:
        if total == 0:
            return (0.0, 0.0)
        z = stats.norm.ppf(1 - self.alpha / 2)
        p, n = successes / total, total
        denom = 1 + z**2 / n
        center = (p + z**2 / (2 * n)) / denom
        margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / denom
        return (max(0.0, center - margin), min(1.0, center + margin))

    def _power(self, p1: float, p2: float, n1: int, n2: int) -> float:
        if n1 == 0 or n2 == 0:
            return 0.0
        effect = abs(p2 - p1) / np.sqrt(p1 * (1 - p1)) if p1 > 0 else 0
        pooled_n = 2 / (1 / n1 + 1 / n2)
        z_alpha = stats.norm.ppf(1 - self.alpha / 2)
        return float(stats.norm.cdf(effect * np.sqrt(pooled_n / 2) - z_alpha))

    def _sample_size(self, baseline: float, mde: float, power: float = 0.80) -> int:
        if baseline == 0 or mde == 0:
            return 0
        effect_rate = baseline * (1 + mde)
        z_a = stats.norm.ppf(1 - self.alpha / 2)
        z_b = stats.norm.ppf(power)
        p_avg = (baseline + effect_rate) / 2
        n = 2 * ((z_a + z_b) ** 2) * p_avg * (1 - p_avg) / (effect_rate - baseline) ** 2
        return int(np.ceil(n))
