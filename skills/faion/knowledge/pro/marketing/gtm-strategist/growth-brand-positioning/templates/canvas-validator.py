"""
Dunford-style positioning canvas validator.

Input:  canvas dict with keys: target_customer, alternatives (list),
        unique_capabilities (list), category (str), proof_points (list)
Output: dict with ok (bool) and issues (list of str)

Usage:
    canvas = {
        "target_customer": "marketing manager at Series A SaaS startup trying to increase trial-to-paid conversion with limited engineering resources",
        "alternatives": ["HubSpot", "manual drip sequences", "doing nothing"],
        "unique_capabilities": ["code-free funnel builder for non-technical marketers"],
        "category": "sub-category: conversion-rate optimization for SaaS onboarding",
        "proof_points": ["customers reduce TTV from 14 to 3 days on average", "150+ Series A SaaS customers"],
    }
    result = validate_canvas(canvas)
    print(result)
"""


def validate_canvas(canvas: dict) -> dict:
    issues = []

    # Rule 1: target customer must be specific
    target = canvas.get("target_customer", "")
    broad_terms = ["businesses", "developers", "users", "companies", "people", "anyone"]
    if len(target.split()) < 8:
        issues.append("Target customer too short — must include role + company type + situation + obstacle.")
    if any(t in target.lower() for t in broad_terms) and len(target.split()) < 12:
        issues.append(f"Target customer may be too broad — avoid generic terms without qualifiers.")

    # Rule 2: alternatives must include at least 2 plus status quo
    alternatives = canvas.get("alternatives", [])
    if len(alternatives) < 2:
        issues.append("List at least 2 competitive alternatives. Include the status-quo option.")
    if not any("nothing" in a.lower() or "manual" in a.lower() or "status quo" in a.lower() for a in alternatives):
        issues.append("Consider adding the status-quo option ('doing nothing' or 'manual process') to alternatives.")

    # Rule 3: pick 1-2 differentiators maximum
    unique = canvas.get("unique_capabilities", [])
    if len(unique) > 2:
        issues.append(f"Too many unique capabilities ({len(unique)}). Pick 1-2 to own; more dilutes the claim.")
    if len(unique) == 0:
        issues.append("At least 1 unique capability required.")

    # Rule 4: category must be defined
    if not canvas.get("category"):
        issues.append("Choose category strategy: existing | sub-category | new | versus. Add one-sentence rationale.")

    # Rule 5: proof points
    proof = canvas.get("proof_points", [])
    if len(proof) < 2:
        issues.append("Need at least 2 proof points (metric, named customer, award, or benchmark).")

    return {"ok": len(issues) == 0, "issues": issues}
