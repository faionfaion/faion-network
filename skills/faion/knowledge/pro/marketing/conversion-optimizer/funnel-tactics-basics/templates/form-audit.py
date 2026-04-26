"""
form_audit.py — Playwright-based signup form checklist auditor.

Checks the Signup Form section of the stage-specific checklist:
- Field count (pass: <= 3)
- Social login presence
- Single CTA (pass: exactly 1)
- Progress indicator presence
- Page load time (pass: <= 3000ms)

Usage: python form_audit.py <url>

Requires: pip install playwright && playwright install chromium
"""
import sys

from playwright.sync_api import sync_playwright


def audit_signup(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        fields = page.locator(
            "input:not([type=hidden]):not([type=submit]), textarea, select"
        ).count()
        social_login = (
            page.locator(
                "[data-provider], button:has-text(/google|github|apple/i)"
            ).count()
            > 0
        )
        ctas = page.locator(
            "button[type=submit], a.cta, button.cta"
        ).count()
        progress = (
            page.locator("[role=progressbar], .progress, [class*=step]").count() > 0
        )
        load_ms = page.evaluate(
            "performance.timing.loadEventEnd - performance.timing.navigationStart"
        )

        browser.close()

    return {
        "fields_count": fields,
        "fields_pass": fields <= 3,
        "social_login": social_login,
        "single_cta": ctas == 1,
        "progress_indicator": progress,
        "load_ms": load_ms,
        "load_pass": load_ms <= 3000,
    }


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/signup"
    result = audit_signup(url)
    for k, v in result.items():
        status = "PASS" if v is True else ("FAIL" if v is False else v)
        print(f"  {k:<25} {status}")
