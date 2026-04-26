# Browser Automation

## Summary

Headless browser automation using Playwright (preferred) or Puppeteer for E2E testing, web scraping, screenshot/PDF generation, and form automation. Use `role=` and `text=` locators before CSS selectors; always wait on conditions, never fixed timeouts; persist auth via `context.storageState`; block images/fonts/analytics on scraping runs. Prefer Playwright over Puppeteer for new projects — it auto-waits and supports multi-browser.

## Why

Browser automation handles dynamic SPAs, JavaScript-rendered content, and complex user flows that HTTP-only scrapers or API clients cannot reach. Playwright's auto-waiting and locator API reduce flakiness compared to manually timed waits. Page Object Model keeps selector changes isolated.

## When To Use

- E2E testing of web apps (Playwright test suite, preview verification).
- Scraping public sites that have no usable API.
- Programmatic screenshot/PDF generation for reports, OG cards, invoice rendering.
- Form fill and submit automation for portals lacking an API.
- Visual regression on component library builds.

## When Not To Use

- The site offers a REST/GraphQL/RSS API — always prefer the API; browser automation is brittle and slow.
- Sites with strong anti-bot protection (Cloudflare Turnstile, PerimeterX) — fight cost exceeds value.
- High-throughput scraping (>100 pages/sec) — use HTTP-only (`httpx`, `scrapy`) instead.
- Tasks requiring credentials you don't legitimately own.
- Behind-VPN or zero-trust portals where headless browser fingerprint trips MFA.

## Content

| File | What's inside |
|------|---------------|
| `content/01-playwright.xml` | Launch, auto-waiting, locators, form handling, network interception, storage state. |
| `content/02-puppeteer.xml` | Launch, selectors, screenshots/PDF, cookies, request interception, stealth. |
| `content/03-scraping.xml` | Element extraction, pagination patterns (next/infinite-scroll/load-more), concurrency limit. |
| `content/04-antipatterns.xml` | Fixed timeouts, inline selectors, per-page client creation, CSS-class selectors. |

## Templates

| File | Purpose |
|------|---------|
| `templates/page-object.js` | Page Object Model class scaffold for Playwright. |
| `templates/extract.js` | Minimal Playwright extractor with Zod schema validation. |
