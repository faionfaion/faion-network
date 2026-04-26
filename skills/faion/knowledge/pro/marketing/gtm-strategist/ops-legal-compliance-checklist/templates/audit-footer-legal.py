"""
Legal-page presence audit with EU cookie-banner check.

Inputs:
  base_url  -- full URL including scheme (e.g. "https://example.com")
  locales   -- list of locale strings to test for cookie banner (e.g. ["en-US", "de-DE", "fr-FR"])

Output:
  dict with pages (presence by path) and cookie_banner (by locale)

NOTE: this checks PRESENCE only, not legal sufficiency of content.
Run against both logged-out and logged-in state for full coverage.
"""

import asyncio
from playwright.async_api import async_playwright

REQUIRED_PAGES = ["/privacy", "/terms", "/cookies", "/dpa"]
EU_LOCALES = {"de-DE", "fr-FR", "en-GB", "pl-PL", "nl-NL"}


async def audit_legal_presence(base_url: str, locales: list[str]) -> dict:
    issues = []
    page_results = {}
    cookie_banner_results = {}

    async with async_playwright() as p:
        # Check required page existence
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for path in REQUIRED_PAGES:
            try:
                resp = await page.goto(f"{base_url}{path}", timeout=10000)
                status = resp.status if resp else None
                page_results[path] = status
                if not resp or resp.status >= 400:
                    issues.append({"path": path, "status": status, "issue": "page missing or error"})
            except Exception as e:
                page_results[path] = None
                issues.append({"path": path, "status": None, "issue": str(e)})
        await browser.close()

        # Check cookie banner per locale
        for loc in locales:
            ctx = await p.chromium.launch_persistent_context(
                user_data_dir=f"/tmp/audit-{loc}",
                locale=loc,
                args=[f"--accept-lang={loc}"],
            )
            pg = await ctx.new_page()
            await pg.goto(base_url, timeout=15000)
            banner_count = await pg.locator("[data-testid='cookie-banner'], [id*='cookie'], [class*='consent']").count()
            banner_present = banner_count > 0
            cookie_banner_results[loc] = banner_present
            if loc in EU_LOCALES and not banner_present:
                issues.append({"locale": loc, "issue": "no cookie consent banner detected for EU locale"})
            await ctx.close()

    return {
        "base_url": base_url,
        "pages": page_results,
        "cookie_banner_by_locale": cookie_banner_results,
        "issues": issues,
        "note": "Presence only — content accuracy requires attorney review.",
    }


# asyncio.run(audit_legal_presence("https://example.com", ["en-US", "de-DE", "fr-FR"]))
