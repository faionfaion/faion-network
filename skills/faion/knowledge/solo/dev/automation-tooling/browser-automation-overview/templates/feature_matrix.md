<!-- __faion_header_v1__ -->
<!-- purpose: Puppeteer vs Playwright vs web-scraping feature matrix -->
<!-- consumes: see content/02-output-contract.xml -->
<!-- produces: decision-record; depends-on: content/01-core-rules.xml#tool-by-language -->
<!-- faion_header_json: {"__faion_header__":{"purpose":"Puppeteer vs Playwright vs web-scraping feature matrix","consumes":"see content/02-output-contract.xml","produces":"decision-record","depends_on":"content/01-core-rules.xml#tool-by-language","token_budget_impact":"~150 tokens when loaded"}} -->
| Feature | Puppeteer | Playwright |
|---|---|---|
| Multi-browser (Chromium/WebKit/Firefox) | Chromium-only | All three |
| Auto-wait | Manual | Built-in |
| Trace viewer | None | Built-in |
| Codegen | Limited | Mature |
| Languages | JS/TS | JS/TS/Python/.NET/Java |
| Mobile emulation | Chromium only | All three |
| Network interception | Yes | Yes (+route mocking) |
