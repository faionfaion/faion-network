// purpose: Bash-invoked worker script with hard timeout + artifact capture
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-agent-workflow
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

#!/usr/bin/env node
// Usage: timeout 60 node worker.mjs <url> > /tmp/agent-run/result.json
import puppeteer from 'puppeteer';
import fs from 'node:fs';

const URL = process.argv[2];
if (!URL) { console.error('URL required'); process.exit(2); }

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
});
try {
  const page = await browser.newPage();
  page.setDefaultTimeout(20000);
  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  await page.waitForSelector('[data-testid="root"]');

  const data = await page.evaluate(() => {
    const root = document.querySelector('[data-testid="root"]');
    return { text: root?.textContent?.trim() ?? null };
  });

  const artifactPath = process.env.ARTIFACT_PATH ?? '/tmp/agent-run/result.json';
  fs.mkdirSync('/tmp/agent-run', { recursive: true });
  fs.writeFileSync(artifactPath, JSON.stringify(scrub(data), null, 2));
  console.log(artifactPath);
} finally {
  await browser.close();
}

function scrub(obj) {
  const s = JSON.stringify(obj);
  return JSON.parse(s
    .replace(/Bearer [A-Za-z0-9._\-]+/g, 'Bearer [REDACTED]')
    .replace(/eyJ[A-Za-z0-9._\-]+/g, '[JWT_REDACTED]')
    .replace(/\b\d{16}\b/g, '[CARD_REDACTED]'));
}
