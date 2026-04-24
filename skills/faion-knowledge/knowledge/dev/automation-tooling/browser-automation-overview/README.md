# Browser Automation Overview

**Layer:** Technical reference index
**Used by:** faion-browser-agent

## Purpose

Provides comprehensive patterns for browser automation using Puppeteer and Playwright. Covers web scraping, E2E testing, screenshot/PDF generation, form automation, and headless browser operations.

## 3-Layer Architecture

```
Layer 1: Domain Skills - orchestrators
    ↓ call
Layer 2: Agents (faion-browser-agent) - executors
    ↓ use
Layer 3: Technical Skills (this) - tools
```

## Files

| File | Purpose | Lines |
|------|---------|-------|
| [puppeteer-automation.md](puppeteer-automation.md) | Puppeteer patterns and best practices | ~800 |
| [playwright-automation.md](playwright-automation.md) | Playwright patterns and testing | ~700 |
| [web-scraping.md](web-scraping.md) | Scraping techniques, pagination, anti-detection | ~500 |
| [browser-automation-overview.md](browser-automation-overview.md) | This file, navigation and quick reference | ~100 |

Total: ~2100 lines (was 4712 in single file)

## Quick Navigation

### For Basic Automation
→ [puppeteer-automation.md](puppeteer-automation.md) - Simpler API, faster for basic tasks
→ [playwright-automation.md](playwright-automation.md) - Cross-browser, better for testing

### For Web Scraping
→ [web-scraping.md](web-scraping.md) - Extraction, pagination, rate limiting, anti-detection

### For E2E Testing
→ [playwright-automation.md](playwright-automation.md) - Test framework, fixtures, assertions

## Tool Comparison

| Feature | Puppeteer | Playwright |
|---------|-----------|------------|
| **Browsers** | Chrome/Chromium only | Chrome, Firefox, WebKit |
| **Auto-waiting** | Manual | Built-in |
| **Speed** | Fast | Slightly slower |
| **API complexity** | Simpler | More features |
| **Best for** | Web scraping, quick automation | Cross-browser testing, complex scenarios |
| **Stealth mode** | Via plugins (puppeteer-extra) | Built-in better detection evasion |
| **Selectors** | CSS, XPath | CSS, XPath, text, role (accessibility) |
| **Testing framework** | Separate (Jest, Mocha) | Built-in (@playwright/test) |
| **Video recording** | Via CDP | Built-in |
| **Tracing** | Manual | Built-in |

## When to Use What

### Use Puppeteer When
- Fast web scraping (Chrome-only is fine)
- Simple automation tasks
- PDF/screenshot generation
- Lightweight operations
- Chrome DevTools Protocol access needed

### Use Playwright When
- Cross-browser testing required
- Complex E2E test scenarios
- Need auto-waiting and retries
- Video/trace recording needed
- Accessibility testing (role selectors)
- Page Object Model patterns

## Common Patterns Quick Reference

### Puppeteer
```javascript
const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();
await page.goto('https://example.com');
const text = await page.$eval('h1', el => el.textContent);
await browser.close();
```

### Playwright
```javascript
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();
await page.goto('https://example.com');
const text = await page.textContent('h1');
await browser.close();
```

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| [faion-software-developer](CLAUDE.md) | Parent skill, uses browser automation |
| [testing.md](testing.md) | E2E testing integration |
| [api-testing.md](api-testing.md) | Combined API + browser testing |

## Agents Called

| Agent | Purpose |
|-------|---------|
| faion-browser-agent | Execute browser automation tasks using these patterns |

## References

- [Puppeteer Docs](https://pptr.dev/)
- [Playwright Docs](https://playwright.dev/)
- [puppeteer-extra](https://github.com/berstend/puppeteer-extra) - Stealth mode
- [playwright-extra](https://github.com/berstend/playwright-extra) - Stealth mode

---

*Browser Automation Skills v2.0 - 2026-01-23*
*Decomposed from single 4712-line file into 4 modular files*
*Each file <2000 tokens for efficient loading*
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Create CI/CD pipeline template | haiku | Pattern application |
| Optimize pipeline performance | sonnet | Requires optimization skills |
| Design CD rollback strategy | opus | Complex risk management |

