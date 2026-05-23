"""
Score landing page sections against conversion checklist criteria.
Input: dict with section keys and text content values.
Output: scores per section with flagged issues.

Usage:
  sections = {"hero": "...", "social_proof": "...", "final_cta": "..."}
  from audit_score import audit_landing_page
  print(audit_landing_page(sections))
"""


def audit_landing_page(sections: dict) -> dict:
    """
    sections keys: 'hero', 'problem', 'solution', 'how_it_works',
                   'social_proof', 'faq', 'final_cta'
    Returns score per section and flagged issues.
    """
    checks = {
        "hero": [
            ("single_cta", "One primary CTA button"),
            ("headline_short", "Headline under 12 words"),
            ("social_proof", "Social proof visible near CTA"),
            ("product_visual", "Product screenshot or visual present"),
        ],
        "social_proof": [
            ("photos", "Testimonials include photos"),
            ("specific_results", "Results are specific with numbers"),
            ("company_logos", "Company logos present (B2B)"),
        ],
        "final_cta": [
            ("risk_reversal", "Guarantee, free trial, or no-credit-card statement"),
            ("benefit_reminder", "Benefit restated near final CTA"),
        ],
    }

    scores = {}
    for section, criteria in checks.items():
        section_text = sections.get(section, "").lower()
        passed = []
        failed = []
        for key, label in criteria:
            # Heuristic: check if keyword is present; human review required for accuracy
            if key.replace("_", " ") in section_text or len(section_text) > 100:
                passed.append(label)
            else:
                failed.append(f"MISSING: {label}")
        scores[section] = {
            "score": len(passed),
            "max": len(criteria),
            "passed": passed,
            "failed": failed,
        }
    return scores


if __name__ == "__main__":
    example = {
        "hero": "Build your SaaS in 2 weeks. Start Free Trial. Trusted by 5,000 developers.",
        "social_proof": "Jane Smith, CTO at Acme — doubled our deployment speed in 30 days.",
        "final_cta": "Start building today. 30-day money-back guarantee. No credit card required.",
    }
    result = audit_landing_page(example)
    for section, data in result.items():
        print(f"{section}: {data['score']}/{data['max']}")
        for issue in data["failed"]:
            print(f"  {issue}")
