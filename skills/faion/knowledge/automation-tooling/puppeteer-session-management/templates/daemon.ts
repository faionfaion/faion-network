// purpose: Daemon runner serving session work via HTTP
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-session-management
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

import http from 'node:http';
import { launchFor, isolatedContext } from './session';

const browsers: Record<string, any> = {};

async function getBrowser(identity: string) {
  browsers[identity] ||= await launchFor(identity);
  return browsers[identity];
}

const server = http.createServer(async (req, res) => {
  if (req.method !== 'POST' || req.url !== '/run') {
    res.writeHead(404); res.end(); return;
  }
  let body = '';
  req.on('data', (c) => { body += c; });
  req.on('end', async () => {
    const job = JSON.parse(body);
    const browser = await getBrowser(job.identity);
    const ctx = await isolatedContext(browser);
    try {
      const page = await ctx.newPage();
      await page.goto(job.url, { waitUntil: 'domcontentloaded' });
      const data = await page.evaluate(() => ({ title: document.title }));
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify(data));
    } finally {
      await ctx.close();
    }
  });
});

server.listen(7878, () => console.log('agent-daemon up'));
