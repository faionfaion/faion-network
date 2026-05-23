// purpose: Request interception blocking analytics + ads
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-page-interaction
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { Page } from 'puppeteer';

const BLOCK = [
  'google-analytics.com',
  'doubleclick.net',
  'googletagmanager.com',
  'fullstory.com',
  'hotjar.com',
  'segment.com',
];

export async function blockNoise(page: Page) {
  await page.setRequestInterception(true);
  page.on('request', (req) => {
    const url = req.url();
    if (BLOCK.some((d) => url.includes(d))) return req.abort();
    return req.continue();
  });
}
