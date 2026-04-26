"""AIFeature build-vs-buy decision model.

Input: feature attributes (differentiator, data advantage, speed priority).
Output: build/buy recommendation with 12-month review date.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class AIFeature:
    name: str
    is_differentiator: bool
    has_data_advantage: bool
    speed_priority: bool
    review_date: date = field(default=None)

    def __post_init__(self):
        if self.review_date is None:
            self.review_date = date.today() + timedelta(days=365)

    def decision(self) -> str:
        if self.is_differentiator and self.has_data_advantage:
            return "BUILD"
        if self.is_differentiator and not self.has_data_advantage:
            return "BUY (now) -> BUILD (when data matures)"
        if self.speed_priority and not self.is_differentiator:
            return "BUY"
        return "BUY"
