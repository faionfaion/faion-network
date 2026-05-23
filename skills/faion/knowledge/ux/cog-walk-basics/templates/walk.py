"""
walk.py — Drive a Playwright session and emit one JSON per step for the evaluator agent.
Input: STEPS list defined below (url, action description, CSS selector).
Output: JSON lines to stdout — one per step including screenshot path.

Install: pip install playwright && playwright install chromium
Run: python walk.py
"""
import json
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

# Define your task steps here:
# (url, action_description, css_selector_to_click)
# Leave url="" to stay on the current page.
STEPS = [
    ("https://app.example.com/", "Click 'Get Started'", "button:has-text('Get Started')"),
    ("", "Enter email address", "input[type=email]"),
    ("", "Enter password", "input[type=password]"),
    ("", "Click 'Create Account'", "button[type=submit]"),
]

OUTPUT_DIR = Path("walk-screenshots")


async def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 390, "height": 844})

        for i, (url, action, selector) in enumerate(STEPS, 1):
            if url:
                await page.goto(url, wait_until="networkidle")

            # Capture BEFORE screenshot (for Q1-Q3 evaluation)
            before_path = str(OUTPUT_DIR / f"step_{i:02d}_before.png")
            await page.screenshot(path=before_path, full_page=False)

            step_data = {
                "step": i,
                "action": action,
                "selector": selector,
                "before_screenshot": before_path,
            }

            # Perform the action
            try:
                await page.locator(selector).first.click()
                await page.wait_for_timeout(500)

                # Capture AFTER screenshot (for Q4 evaluation)
                after_path = str(OUTPUT_DIR / f"step_{i:02d}_after.png")
                await page.screenshot(path=after_path, full_page=False)
                step_data["after_screenshot"] = after_path
                step_data["action_success"] = True
            except Exception as e:
                step_data["action_success"] = False
                step_data["error"] = str(e)

            print(json.dumps(step_data))

        await browser.close()


asyncio.run(main())
