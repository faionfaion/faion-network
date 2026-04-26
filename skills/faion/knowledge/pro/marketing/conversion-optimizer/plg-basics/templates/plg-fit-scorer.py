"""
plg_fit_scorer.py — score a product against the PLG fit matrix.

Six binary factors from the README "Is PLG Right for You?" table.
Returns fit score 0-6 and recommendation string.

Use before recommending any PLG model; never skip the matrix.
"""
from dataclasses import dataclass


@dataclass
class ProductFit:
    complexity_simple: bool         # intuitive (1) vs requires-training (0)
    end_user_decides: bool          # end user (1) vs C-level/procurement (0)
    price_under_50k: bool           # < $50K/year (1) vs above (0)
    ttv_minutes_to_hours: bool      # minutes-hours (1) vs days-weeks (0)
    trial_feasible: bool            # easy to try (1) vs requires implementation (0)
    market_large: bool              # large TAM (1) vs niche (0)

    @property
    def score(self) -> int:
        return sum([
            self.complexity_simple,
            self.end_user_decides,
            self.price_under_50k,
            self.ttv_minutes_to_hours,
            self.trial_feasible,
            self.market_large,
        ])

    @property
    def recommendation(self) -> str:
        if self.score >= 5:
            return "pure_plg"
        if self.score >= 3:
            return "hybrid_plg_sales"
        return "sales_led_with_plg_signals"

    def gaps(self) -> list[str]:
        """Return factor names where score is 0 (PLG risk areas)."""
        result = []
        if not self.complexity_simple:
            result.append("product_requires_training")
        if not self.end_user_decides:
            result.append("c_level_or_procurement_decides")
        if not self.price_under_50k:
            result.append("acv_above_50k")
        if not self.ttv_minutes_to_hours:
            result.append("ttv_days_or_weeks")
        if not self.trial_feasible:
            result.append("trial_requires_implementation")
        if not self.market_large:
            result.append("niche_market")
        return result
