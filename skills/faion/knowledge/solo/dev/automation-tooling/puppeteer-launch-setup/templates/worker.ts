// purpose: Worker showing try/finally browser.close discipline
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-launch-setup
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import { launch } from './launch';
import { safeGoto } from './goto';

const url = process.argv[2];
if (!url) { console.error('URL required'); process.exit(2); }

const browser = await launch({ env: process.env.RUN_ENV as any ?? 'ci', defaultTimeoutMs: 20000 });
try {
  const page = await browser.newPage();
  await safeGoto(page, url, '[data-testid="root"]');
  // ... do work ...
} finally {
  await browser.close();
}
