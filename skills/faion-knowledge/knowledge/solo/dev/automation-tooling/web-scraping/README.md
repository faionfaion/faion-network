# Web Scraping Techniques

**Layer:** Technical reference
**Used by:** faion-browser-agent

## Element Extraction

### Basic Extraction

```javascript
// Single value
const title = await page.$eval('h1', el => el.textContent);
const href = await page.$eval('a.link', el => el.href);

// Multiple values (Puppeteer)
const items = await page.$$eval('.product', products =>
  products.map(p => ({
    name: p.querySelector('.name')?.textContent,
    price: p.querySelector('.price')?.textContent,
    image: p.querySelector('img')?.src
  }))
);

// Playwright locator approach
const texts = await page.locator('.item').allTextContents();
const count = await page.locator('.item').count();
```

### Table Extraction

```javascript
const tableData = await page.$$eval('table tbody tr', rows =>
  rows.map(row => {
    const cells = row.querySelectorAll('td');
    return {
      col1: cells[0]?.textContent?.trim(),
      col2: cells[1]?.textContent?.trim(),
      col3: cells[2]?.textContent?.trim()
    };
  })
);
```

### Attribute Extraction

```javascript
// Single attribute
const src = await page.$eval('img', el => el.getAttribute('src'));

// All attributes
const attrs = await page.$eval('#element', el =>
  Object.fromEntries(
    [...el.attributes].map(attr => [attr.name, attr.value])
  )
);
```

## Pagination Handling

### Next Button Pattern

```javascript
async function scrapeAllPages(page) {
  const allData = [];

  while (true) {
    // Scrape current page
    const data = await page.$$eval('.item', items =>
      items.map(item => item.textContent)
    );
    allData.push(...data);

    // Check for next button
    const nextButton = await page.$('a.next:not(.disabled)');
    if (!nextButton) break;

    // Click and wait
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle0' }),
      nextButton.click()
    ]);
  }

  return allData;
}
```

### Infinite Scroll Pattern

```javascript
async function scrapeInfiniteScroll(page) {
  let previousHeight = 0;
  const allData = [];

  while (true) {
    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

    // Wait for new content
    await page.waitForTimeout(2000);

    // Check if more content loaded
    const newHeight = await page.evaluate(() => document.body.scrollHeight);
    if (newHeight === previousHeight) break;
    previousHeight = newHeight;

    // Extract new items
    const items = await page.$$eval('.item', els => els.map(e => e.textContent));
    allData.push(...items.slice(allData.length));
  }

  return allData;
}
```

### Load More Button Pattern

```javascript
async function scrapeLoadMore(page) {
  while (true) {
    const loadMoreBtn = await page.$('button.load-more');
    if (!loadMoreBtn) break;

    const isVisible = await loadMoreBtn.isIntersectingViewport();
    if (!isVisible) break;

    await loadMoreBtn.click();
    await page.waitForSelector('.item:nth-child(n+10)'); // wait for new items
  }

  return await page.$$eval('.item', items => items.map(i => i.textContent));
}
```

## Rate Limiting and Throttling

### Request Delay

```javascript
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function scrapeWithDelay(urls, page) {
  const results = [];

  for (const url of urls) {
    await page.goto(url);
    const data = await extractData(page);
    results.push(data);

    // Random delay between 1-3 seconds
    await delay(1000 + Math.random() * 2000);
  }

  return results;
}
```

### Concurrent Requests with Limit

```javascript
const pLimit = require('p-limit');

async function scrapeWithConcurrency(urls, browser, concurrency = 3) {
  const limit = pLimit(concurrency);

  const tasks = urls.map(url =>
    limit(async () => {
      const page = await browser.newPage();
      try {
        await page.goto(url);
        return await extractData(page);
      } finally {
        await page.close();
      }
    })
  );

  return Promise.all(tasks);
}
```

## Retry Patterns

### Basic Retry

```javascript
async function retry(fn, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      console.log(`Attempt ${i + 1} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Usage
const data = await retry(async () => {
  await page.goto('https://flaky-site.com');
  return await page.$eval('#data', el => el.textContent);
});
```

### Exponential Backoff

```javascript
async function retryWithBackoff(fn, maxRetries = 5, baseDelay = 1000) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = baseDelay * Math.pow(2, i) + Math.random() * 1000;
      console.log(`Retry ${i + 1}/${maxRetries} in ${delay}ms`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

## Memory Management

### Close Pages When Done

```javascript
// Close pages when done
await page.close();

// Limit concurrent pages
const MAX_PAGES = 5;
const semaphore = new Semaphore(MAX_PAGES);

async function processUrl(browser, url) {
  await semaphore.acquire();
  const page = await browser.newPage();
  try {
    await page.goto(url);
    return await extractData(page);
  } finally {
    await page.close();
    semaphore.release();
  }
}
```

### Connection Pooling

```javascript
class BrowserPool {
  constructor(size = 5) {
    this.size = size;
    this.browsers = [];
    this.available = [];
  }

  async initialize() {
    for (let i = 0; i < this.size; i++) {
      const browser = await puppeteer.launch({ headless: true });
      this.browsers.push(browser);
      this.available.push(browser);
    }
  }

  async acquire() {
    while (this.available.length === 0) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
    return this.available.pop();
  }

  release(browser) {
    this.available.push(browser);
  }

  async close() {
    await Promise.all(this.browsers.map(b => b.close()));
  }
}
```

## Data Cleaning

### Text Normalization

```javascript
function normalizeText(text) {
  return text
    ?.trim()
    ?.replace(/\s+/g, ' ')           // collapse whitespace
    ?.replace(/[\r\n\t]/g, '')       // remove line breaks
    ?.replace(/[^\x20-\x7E]/g, '');  // remove non-printable chars
}

const title = normalizeText(await page.$eval('h1', el => el.textContent));
```

### Price Extraction

```javascript
function parsePrice(text) {
  const match = text?.match(/[\d,]+\.?\d*/);
  return match ? parseFloat(match[0].replace(/,/g, '')) : null;
}

const price = parsePrice(await page.$eval('.price', el => el.textContent));
// "$1,234.56" → 1234.56
```

### Date Parsing

```javascript
function parseDate(text) {
  const date = new Date(text);
  return isNaN(date) ? null : date.toISOString();
}

const publishedDate = parseDate(await page.$eval('.date', el => el.textContent));
```

## Anti-Detection Techniques

### Randomized User Agents

```javascript
const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36...'
];

const randomUA = userAgents[Math.floor(Math.random() * userAgents.length)];
await page.setUserAgent(randomUA);
```

### Request Headers

```javascript
await page.setExtraHTTPHeaders({
  'Accept-Language': 'en-US,en;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Referer': 'https://www.google.com/'
});
```

### Browser Fingerprinting Protection

```javascript
// Override webdriver detection
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
});

// Randomize canvas fingerprint
await page.evaluateOnNewDocument(() => {
  const getParameter = WebGLRenderingContext.prototype.getParameter;
  WebGLRenderingContext.prototype.getParameter = function(parameter) {
    if (parameter === 37445) return 'Intel Inc.';
    if (parameter === 37446) return 'Intel Iris OpenGL Engine';
    return getParameter.call(this, parameter);
  };
});
```

## Error Handling

### Safe Extraction

```javascript
async function safeExtract(page, selector, defaultValue = null) {
  try {
    await page.waitForSelector(selector, { timeout: 5000 });
    return await page.$eval(selector, el => el.textContent?.trim());
  } catch {
    return defaultValue;
  }
}

// Usage
const title = await safeExtract(page, 'h1', 'No title');
const price = await safeExtract(page, '.price', '0');
```

### Browser Crash Recovery

```javascript
async function withBrowserRecovery(fn, options = {}) {
  const { maxRecoveries = 3, launchOptions = {} } = options;
  let browser = null;
  let recoveries = 0;

  while (recoveries < maxRecoveries) {
    try {
      if (!browser || !browser.isConnected()) {
        browser = await puppeteer.launch(launchOptions);
      }
      return await fn(browser);
    } catch (error) {
      if (error.message.includes('Target closed') ||
          error.message.includes('Session closed')) {
        recoveries++;
        console.log(`Browser crashed, recovery attempt ${recoveries}`);
        browser = null;
      } else {
        throw error;
      }
    }
  }

  throw new Error('Max browser recovery attempts exceeded');
}
```

## Data Storage

### JSON Output

```javascript
const fs = require('fs');

async function scrapeAndSave(page, url, outputPath) {
  await page.goto(url);
  const data = await page.$$eval('.item', items =>
    items.map(item => ({
      title: item.querySelector('.title')?.textContent,
      price: item.querySelector('.price')?.textContent,
      url: item.querySelector('a')?.href
    }))
  );

  fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
  return data;
}
```

### CSV Output

```javascript
const { createObjectCsvWriter } = require('csv-writer');

async function scrapeToCSV(page, url, outputPath) {
  await page.goto(url);
  const data = await page.$$eval('.item', items =>
    items.map(item => ({
      title: item.querySelector('.title')?.textContent,
      price: item.querySelector('.price')?.textContent,
      url: item.querySelector('a')?.href
    }))
  );

  const csvWriter = createObjectCsvWriter({
    path: outputPath,
    header: [
      { id: 'title', title: 'Title' },
      { id: 'price', title: 'Price' },
      { id: 'url', title: 'URL' }
    ]
  });

  await csvWriter.writeRecords(data);
  return data;
}
```

## Quick Reference

| Task | Puppeteer | Playwright |
|------|-----------|------------|
| Extract text | `page.$eval(sel, el => el.textContent)` | `page.textContent(sel)` |
| Extract all | `page.$$eval(sel, fn)` | `page.locator(sel).allTextContents()` |
| Count elements | `(await page.$$(sel)).length` | `await page.locator(sel).count()` |
| Check existence | `await page.$(sel) !== null` | `await page.locator(sel).count() > 0` |
| Wait for element | `page.waitForSelector(sel)` | `page.waitForSelector(sel)` |
## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Generate OpenAPI spec from code | haiku | Pattern extraction |
| Review API design for consistency | sonnet | Requires API expertise |
| Design API security model | opus | Security trade-offs |

