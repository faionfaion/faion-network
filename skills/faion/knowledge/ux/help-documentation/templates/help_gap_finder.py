#!/usr/bin/env python3
"""help_gap_finder.py — find product features missing help article coverage.

Usage:
    python3 help_gap_finder.py

Edit the `features` and `articles` lists below, or extend to read from files.
"""


def slugify(s: str) -> str:
    """Normalize a string to a URL-slug-like form for fuzzy matching."""
    return s.lower().replace(" ", "-").replace("_", "-")


def find_gaps(features: list[str], articles: list[str]) -> list[str]:
    """Return features with no matching article slug."""
    article_slugs = [slugify(a) for a in articles]
    return [f for f in features if not any(slugify(f) in slug for slug in article_slugs)]


if __name__ == "__main__":
    # Edit these lists for your product
    features = [
        "password reset",
        "team invite",
        "export CSV",
        "billing settings",
        "two-factor authentication",
    ]

    articles = [
        "how-to-export-csv",
        "billing-faq",
        "password-reset-guide",
    ]

    gaps = find_gaps(features, articles)

    if gaps:
        print(f"MISSING help coverage ({len(gaps)} features):")
        for gap in gaps:
            print(f"  - {gap}")
    else:
        print("All features have help coverage.")
