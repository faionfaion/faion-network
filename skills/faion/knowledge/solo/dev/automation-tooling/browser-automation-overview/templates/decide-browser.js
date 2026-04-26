/**
 * decide-browser.js — score Puppeteer vs Playwright based on project requirements.
 *
 * Edit the requirements object to match the project, then run:
 *   node scripts/decide-browser.js
 *
 * Output: "playwright" or "puppeteer" on stdout.
 */

const requirements = {
  crossBrowser: false,   // need Firefox or WebKit?
  e2eTesting: false,     // running as a structured test suite (@playwright/test)?
  videoTrace: false,     // need built-in video / trace capture?
  rolesA11y: false,      // need role/text/accessibility selectors?
  scraping: true,        // primary task is data extraction from Chrome?
  cdpAccess: false,      // need raw Chrome DevTools Protocol access?
};

const playwrightScore =
  (requirements.crossBrowser ? 3 : 0) +
  (requirements.e2eTesting   ? 2 : 0) +
  (requirements.videoTrace   ? 2 : 0) +
  (requirements.rolesA11y    ? 2 : 0);

// Puppeteer tie-break: simpler API + scraping + CDP
const puppeteerScore =
  (requirements.scraping  ? 2 : 0) +
  (requirements.cdpAccess ? 2 : 0) +
  1; // tie-break: simpler default

const choice = playwrightScore >= puppeteerScore ? 'playwright' : 'puppeteer';

console.log(choice);
console.log(`  playwright score: ${playwrightScore}`);
console.log(`  puppeteer score:  ${puppeteerScore}`);
console.log(`  rationale: cross-browser=${requirements.crossBrowser} e2e=${requirements.e2eTesting} scraping=${requirements.scraping}`);
