"""
Customer health score calculator.

Computes a 0-100 health score from five weighted components:
  usage_freq      (30%) — product usage frequency
  features_adopted (25%) — number of core features adopted
  support_sentiment (20%) — last support interaction sentiment
  engagement       (15%) — email/activity engagement level
  payment          (10%) — payment health status

Usage:
    score = health("weekly", 3, "neutral", "medium", "current")
    print(score)        # e.g., 67
    print(bucket(score)) # "stable"
"""

from typing import Literal

UsageFreq = Literal["daily", "weekly", "monthly", "inactive"]
SupportSentiment = Literal["positive", "neutral", "negative", "escalated"]
Engagement = Literal["high", "medium", "low", "none"]
Payment = Literal["current", "minor", "overdue", "failed"]


USAGE_SCORES: dict[str, int] = {
    "daily": 30, "weekly": 20, "monthly": 10, "inactive": 0
}

SUPPORT_SCORES: dict[str, int] = {
    "positive": 20, "neutral": 15, "negative": 5, "escalated": 0
}

ENGAGEMENT_SCORES: dict[str, int] = {
    "high": 15, "medium": 10, "low": 5, "none": 0
}

PAYMENT_SCORES: dict[str, int] = {
    "current": 10, "minor": 7, "overdue": 3, "failed": 0
}


def health(
    usage_freq: UsageFreq,
    features_adopted: int,
    support_sentiment: SupportSentiment,
    engagement: Engagement,
    payment: Payment,
    total_core_features: int = 5,
) -> int:
    u = USAGE_SCORES.get(usage_freq, 0)
    f = round(min(features_adopted / total_core_features, 1.0) * 25)
    s = SUPPORT_SCORES.get(support_sentiment, 0)
    e = ENGAGEMENT_SCORES.get(engagement, 0)
    p = PAYMENT_SCORES.get(payment, 0)
    return u + f + s + e + p


def bucket(score: int) -> str:
    if score >= 80:
        return "healthy"
    if score >= 60:
        return "stable"
    if score >= 40:
        return "at_risk"
    return "critical"


if __name__ == "__main__":
    examples = [
        ("daily", 5, "positive", "high", "current"),
        ("weekly", 3, "neutral", "medium", "current"),
        ("monthly", 1, "negative", "low", "overdue"),
        ("inactive", 0, "escalated", "none", "failed"),
    ]
    print(f"{'Usage':<10} {'Features':<10} {'Support':<12} {'Engage':<8} {'Payment':<10} {'Score':>6} {'Bucket'}")
    for args in examples:
        s = health(*args)
        print(f"{args[0]:<10} {args[1]:<10} {args[2]:<12} {args[3]:<8} {args[4]:<10} {s:>6} {bucket(s)}")
