// purpose: Per-identity session launch + cleanup
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-session-management
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import puppeteer, { Browser, BrowserContext } from 'puppeteer';
import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.env.PROFILES_ROOT ?? '/var/lib/agent/profiles';

export function dirFor(identity: string): string {
  const d = path.join(ROOT, identity);
  fs.mkdirSync(d, { recursive: true, mode: 0o700 });
  return d;
}

export async function launchFor(identity: string): Promise<Browser> {
  return puppeteer.launch({
    headless: 'new',
    userDataDir: dirFor(identity),
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
}

export async function isolatedContext(browser: Browser): Promise<BrowserContext> {
  return browser.createIncognitoBrowserContext();
}
