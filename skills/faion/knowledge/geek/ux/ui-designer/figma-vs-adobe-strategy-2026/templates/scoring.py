"""Weighted scoring for Figma vs Adobe CC toolchain selection.

Update FIGMA_SCORES and ADOBE_SCORES quarterly after each platform's major conference.
"""

CRITERIA = ["collaboration", "agent_api", "asset_creation", "dev_handoff", "cost_efficiency"]

# Baseline scores (update quarterly — Figma Config and Adobe MAX)
FIGMA_SCORES = {
    "collaboration": 5,
    "agent_api": 4,
    "asset_creation": 2,
    "dev_handoff": 5,
    "cost_efficiency": 4,
}
ADOBE_SCORES = {
    "collaboration": 3,
    "agent_api": 3,
    "asset_creation": 5,
    "dev_handoff": 3,
    "cost_efficiency": 3,
}


def score(platform_scores: dict, weights: dict) -> float:
    return sum(platform_scores[c] * weights.get(c, 1) for c in CRITERIA)


def recommend(weights: dict) -> str:
    fig = score(FIGMA_SCORES, weights)
    ado = score(ADOBE_SCORES, weights)
    winner = "Figma" if fig >= ado else "Adobe CC"
    return f"Figma: {fig:.1f} | Adobe: {ado:.1f} → Recommended: {winner}"


# Product team: collaboration + dev handoff + agent API matter most
product_weights = {
    "collaboration": 2,
    "agent_api": 1.5,
    "asset_creation": 0.5,
    "dev_handoff": 2,
    "cost_efficiency": 1,
}

# Creative agency: asset creation + cost matter most
agency_weights = {
    "collaboration": 1,
    "agent_api": 0.5,
    "asset_creation": 2.5,
    "dev_handoff": 1,
    "cost_efficiency": 2,
}

if __name__ == "__main__":
    print("Product team:", recommend(product_weights))
    print("Creative agency:", recommend(agency_weights))
