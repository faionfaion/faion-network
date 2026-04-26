# Browser Automation Overview

## Summary

A routing layer for headless browser tasks: compare Puppeteer vs Playwright using the feature matrix, pick one, then load the appropriate sibling methodology (`puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`). This file does not contain implementation patterns — it is the decision layer only.

## Why

Picking the wrong tool (Puppeteer for cross-browser E2E, Playwright for simple Chrome scraping) introduces unnecessary complexity or missing features. The comparison matrix gives concrete criteria: cross-browser need → Playwright; scraping Chrome-only → Puppeteer. Loading a single focused sibling avoids the token cost of the full 2100-line decomposed set.

## When To Use

- Choosing between Puppeteer and Playwright for a new automation, scraping, or E2E project.
- Onboarding a project that needs headless browser tasks (PDF, screenshots, form fill, scraping, E2E).
- Triaging an existing browser-automation codebase: which tool is in use and where are the gaps.
- Routing an agent to the correct sibling skill before producing any code.

## When NOT To Use

- Deep implementation: jump directly to `puppeteer-automation/`, `playwright-automation/`, or `web-scraping/`.
- Mobile app automation (Appium, Detox, Maestro) — browser-only scope.
- API-only testing — use `api-testing` patterns; a browser is wasteful.
- Browser fingerprinting / strong anti-bot evasion at scale — out of scope here.

## Content

| File | What's inside |
|------|---------------|
| `content/01-tool-selection.xml` | Puppeteer vs Playwright feature matrix, when-to-use rules, minimal code comparison, routing decision logic. |
| `content/02-ci-gotchas.xml` | CI launch flags, timeout discipline, memory/cleanup rules, managed browser service routing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decide-browser.js` | Scoring script: pick Puppeteer vs Playwright based on boolean requirements flags. |
