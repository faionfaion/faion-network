// purpose: Form submission waiting for API response
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-page-interaction
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { Page } from 'puppeteer';
import { clickByTestId, typeByTestId } from './interact';

export async function submitCheckout(page: Page, email: string, card: string) {
  await typeByTestId(page, 'email', email);
  await typeByTestId(page, 'card-number', card);
  const [response] = await Promise.all([
    page.waitForResponse((r) => r.url().includes('/api/checkout')),
    clickByTestId(page, 'submit'),
  ]);
  if (!response.ok()) throw new Error(`checkout failed: ${response.status()}`);
  return response.json();
}
