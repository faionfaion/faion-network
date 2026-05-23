// purpose: Authenticate once and persist storageState to auth.json
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for playwright-automation
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { chromium, FullConfig } from '@playwright/test';

export default async function globalSetup(_config: FullConfig) {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto(`${process.env.BASE_URL}/login`);
  await page.getByLabel('Email').fill(process.env.PW_USER!);
  await page.getByLabel('Password').fill(process.env.PW_PASS!);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL('**/dashboard');
  await ctx.storageState({ path: 'auth.json' });
  await browser.close();
}
