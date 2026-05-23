// purpose: Capture helpers: screenshot, pdf, har with safe defaults
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-output-capture
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { Page } from 'puppeteer';
import fs from 'node:fs';

export async function screenshot(page: Page, outPath: string, opts: { fullPage?: boolean } = {}) {
  await page.screenshot({
    path: outPath,
    type: 'jpeg',
    quality: 80,
    fullPage: opts.fullPage ?? false,
  });
}

export async function pdf(page: Page, anchorSelector: string, outPath: string) {
  await page.waitForSelector(anchorSelector);
  await page.evaluate(() => (document as any).fonts?.ready);
  await page.pdf({
    path: outPath,
    printBackground: true,
    preferCSSPageSize: true,
    format: 'A4',
  });
}
