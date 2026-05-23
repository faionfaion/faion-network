// purpose: Stealth-plugin-only worker (stance documented at top)
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-stealth-proxy
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

// STEALTH STANCE: plugin-only.
// Reason: puppeteer-extra-plugin-stealth is the maintained baseline. We do not
// stack manual navigator overrides on top; assertions never depend on overridden props.
import puppeteer from 'puppeteer-extra';
import Stealth from 'puppeteer-extra-plugin-stealth';
puppeteer.use(Stealth());

export async function launch(opts: { proxyHost?: string } = {}) {
  const args = ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'];
  if (opts.proxyHost) args.push(`--proxy-server=${opts.proxyHost}`);
  return puppeteer.launch({ headless: 'new', args });
}
