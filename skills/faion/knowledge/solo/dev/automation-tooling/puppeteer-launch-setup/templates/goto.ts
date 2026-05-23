// purpose: SPA-safe page.goto helper
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-launch-setup
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { Page } from 'puppeteer';

export async function safeGoto(page: Page, url: string, anchorSelector: string, timeoutMs = 20000) {
  page.setDefaultTimeout(timeoutMs);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector(anchorSelector, { timeout: timeoutMs });
}
