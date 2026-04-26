"""
Expansion trigger detector — emits upsell opportunities from account data.

Two trigger types:
  1. usage_threshold: account at >= 80% of its plan limit AND on an upgradeable plan
  2. advanced_feature_use: account used an advanced feature >= 5 times in 30 days
     AND is not on pro tier or higher

Input:  list of account dicts with required keys (see below)
Output: generator of opportunity dicts

Required account keys:
  id                  — account identifier
  usage_pct           — float 0.0-1.0 (current usage / plan limit)
  limit               — int or float (plan limit value)
  unit                — str (e.g., "subscribers", "API calls", "seats")
  plan_rank           — int (current plan position, 0 = free, 1 = basic, 2 = pro, ...)
  max_plan_rank       — int (highest available plan rank)
  next_plan           — str (name of the next tier)
  next_plan_price     — float (monthly price of next tier)
  current_price       — float (current monthly price)
  advanced_feature_uses_30d — int (times advanced feature used in last 30 days)
  advanced_feature_name — str (name of the feature)
  on_pro_or_higher    — bool

Usage:
    accounts = load_accounts_from_csv("accounts.csv")
    for opp in opportunities(accounts):
        print(opp)
"""


def opportunities(accounts: list[dict]):
    for a in accounts:
        # Trigger 1: usage threshold
        if a.get("usage_pct", 0) >= 0.80 and a.get("plan_rank", 0) < a.get("max_plan_rank", 0):
            yield {
                "account_id": a["id"],
                "trigger": "usage_threshold",
                "evidence": f"{int(a['usage_pct'] * 100)}% of {a['limit']} {a['unit']}",
                "offer_plan": a["next_plan"],
                "delta_mrr": round(a["next_plan_price"] - a["current_price"], 2),
                "urgency": "high" if a["usage_pct"] >= 0.90 else "medium",
            }

        # Trigger 2: advanced feature use without pro plan
        if (
            a.get("advanced_feature_uses_30d", 0) >= 5
            and not a.get("on_pro_or_higher", False)
        ):
            yield {
                "account_id": a["id"],
                "trigger": "advanced_feature_use",
                "evidence": (
                    f"used {a['advanced_feature_name']} "
                    f"{a['advanced_feature_uses_30d']}x in last 30 days"
                ),
                "offer_plan": "pro",
                "delta_mrr": round(a.get("next_plan_price", 0) - a["current_price"], 2),
                "urgency": "medium",
            }
