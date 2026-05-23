// purpose: Reusable launch wrapper with environment-aware flags
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-launch-setup
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import puppeteer, { Browser, LaunchOptions } from 'puppeteer';

export interface LaunchEnv {
  env: 'local' | 'docker' | 'ci' | 'serverless';
  defaultTimeoutMs?: number;
}

export async function launch(env: LaunchEnv): Promise<Browser> {
  const args = ['--disable-dev-shm-usage'];
  if (env.env !== 'local') {
    args.push('--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu');
  }
  const opts: LaunchOptions = {
    headless: 'new',
    args,
  };
  return puppeteer.launch(opts);
}
