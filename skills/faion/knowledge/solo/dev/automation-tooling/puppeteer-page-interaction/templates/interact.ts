// purpose: Interaction helpers using data-testid + wait + native APIs
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-page-interaction
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { Page } from 'puppeteer';

const sel = (testId: string) => `[data-testid="${testId}"]`;

export async function clickByTestId(page: Page, testId: string) {
  const handle = await page.waitForSelector(sel(testId), { visible: true });
  if (!handle) throw new Error(`element not found: ${testId}`);
  const disabled = await handle.evaluate((el: any) => !!el.disabled);
  if (disabled) throw new Error(`element disabled: ${testId}`);
  await handle.click();
}

export async function typeByTestId(page: Page, testId: string, value: string) {
  await page.waitForSelector(sel(testId), { visible: true });
  await page.type(sel(testId), value);
}

export async function selectByTestId(page: Page, testId: string, value: string) {
  await page.waitForSelector(sel(testId), { visible: true });
  await page.select(sel(testId), value);
}
