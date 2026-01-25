# Puppeteer Browser Automation

**Layer:** Technical reference
**Used by:** faion-browser-agent

## Overview

Puppeteer is Google's Node.js library for controlling Chrome/Chromium via DevTools Protocol.

**Installation:**
```bash
npm install puppeteer
# or for lighter version without bundled browser
npm install puppeteer-core
```

## Basic Setup

### Standard Launch

```javascript
const puppeteer = require('puppeteer');

async function main() {
  const browser = await puppeteer.launch({
    headless: 'new', // or true for old headless, false for visible
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu'
    ]
  });

  const page = await browser.newPage();
  await page.goto('https://example.com');

  // ... operations ...

  await browser.close();
}
```

### With Custom User Agent

```javascript
const page = await browser.newPage();
await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
await page.setViewport({ width: 1920, height: 1080 });
```

## Navigation

### Page Navigation

```javascript
// Navigate with options
await page.goto('https://example.com', {
  waitUntil: 'networkidle0', // or 'load', 'domcontentloaded', 'networkidle2'
  timeout: 30000
});

// Wait for navigation after click
await Promise.all([
  page.waitForNavigation({ waitUntil: 'networkidle0' }),
  page.click('a.nav-link')
]);

// Go back/forward
await page.goBack();
await page.goForward();

// Reload
await page.reload({ waitUntil: 'networkidle0' });
```

### Wait Strategies

```javascript
// Wait for selector
await page.waitForSelector('#element', { visible: true, timeout: 5000 });

// Wait for XPath
await page.waitForXPath('//button[contains(text(), "Submit")]');

// Wait for function
await page.waitForFunction(() => document.querySelector('#data').innerText !== '');

// Wait for network idle
await page.waitForNetworkIdle({ idleTime: 500 });

// Wait for response
await page.waitForResponse(response =>
  response.url().includes('/api/data') && response.status() === 200
);
```

## Selectors and Interaction

### Element Selection

```javascript
// CSS selectors
const element = await page.$('#id');           // Single element
const elements = await page.$$('.class');      // All matching

// Evaluate in page context
const text = await page.$eval('#title', el => el.textContent);
const texts = await page.$$eval('.items', els => els.map(el => el.textContent));

// Check existence
const exists = await page.$('#element') !== null;
```

### User Interactions

```javascript
// Click
await page.click('#button');
await page.click('#button', { button: 'right', clickCount: 2 });

// Type
await page.type('#input', 'Hello World', { delay: 100 });

// Clear and type
await page.click('#input', { clickCount: 3 });
await page.type('#input', 'New text');

// Keyboard
await page.keyboard.press('Enter');
await page.keyboard.down('Shift');
await page.keyboard.press('ArrowDown');
await page.keyboard.up('Shift');

// Mouse
await page.mouse.move(100, 200);
await page.mouse.click(100, 200);
await page.mouse.wheel({ deltaY: 500 });

// Hover
await page.hover('#menu-item');
```

## Form Handling

### Input Types

```javascript
// Text input
await page.type('#name', 'John Doe');

// Select dropdown
await page.select('#country', 'US');
await page.select('#multi', 'opt1', 'opt2'); // Multiple

// Checkbox/Radio
await page.click('#agree-checkbox');
await page.click('input[name="gender"][value="male"]');

// File upload
const input = await page.$('input[type="file"]');
await input.uploadFile('/path/to/file.pdf');

// Date input
await page.$eval('#date', (el, value) => el.value = value, '2026-01-18');
```

### Form Submission

```javascript
// Submit form
await page.click('button[type="submit"]');

// Or trigger form submit
await page.$eval('form', form => form.submit());

// Wait for response after submit
const [response] = await Promise.all([
  page.waitForNavigation(),
  page.click('button[type="submit"]')
]);
```

## Screenshot and PDF

### Screenshots

```javascript
// Full page
await page.screenshot({
  path: 'fullpage.png',
  fullPage: true
});

// Specific element
const element = await page.$('#chart');
await element.screenshot({ path: 'chart.png' });

// With options
await page.screenshot({
  path: 'screenshot.png',
  type: 'png', // or 'jpeg', 'webp'
  quality: 80, // jpeg/webp only
  clip: { x: 0, y: 0, width: 800, height: 600 },
  omitBackground: true // transparent background
});

// As base64
const base64 = await page.screenshot({ encoding: 'base64' });
```

### PDF Generation

```javascript
await page.pdf({
  path: 'document.pdf',
  format: 'A4', // or 'Letter', 'Legal', etc.
  printBackground: true,
  margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
  displayHeaderFooter: true,
  headerTemplate: '<div style="font-size:10px;text-align:center;width:100%;">Header</div>',
  footerTemplate: '<div style="font-size:10px;text-align:center;width:100%;"><span class="pageNumber"></span>/<span class="totalPages"></span></div>'
});

// Custom page size
await page.pdf({
  path: 'custom.pdf',
  width: '8.5in',
  height: '11in'
});
```

## Cookie and Session Management

### Cookies

```javascript
// Get all cookies
const cookies = await page.cookies();

// Get specific cookie
const sessionCookie = cookies.find(c => c.name === 'session_id');

// Set cookies
await page.setCookie({
  name: 'auth_token',
  value: 'abc123',
  domain: '.example.com',
  path: '/',
  httpOnly: true,
  secure: true
});

// Delete cookies
await page.deleteCookie({ name: 'auth_token' });

// Save and restore cookies
const cookies = await page.cookies();
fs.writeFileSync('cookies.json', JSON.stringify(cookies));

const savedCookies = JSON.parse(fs.readFileSync('cookies.json'));
await page.setCookie(...savedCookies);
```

### Local/Session Storage

```javascript
// Set localStorage
await page.evaluate(() => {
  localStorage.setItem('key', 'value');
});

// Get localStorage
const value = await page.evaluate(() => localStorage.getItem('key'));

// Clear storage
await page.evaluate(() => {
  localStorage.clear();
  sessionStorage.clear();
});
```

## Request Interception

### Basic Interception

```javascript
await page.setRequestInterception(true);

page.on('request', request => {
  // Block images and CSS
  if (['image', 'stylesheet'].includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});

// Modify requests
page.on('request', request => {
  if (request.url().includes('/api/')) {
    request.continue({
      headers: {
        ...request.headers(),
        'Authorization': 'Bearer token123'
      }
    });
  } else {
    request.continue();
  }
});

// Mock responses
page.on('request', request => {
  if (request.url().endsWith('/api/data')) {
    request.respond({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ mocked: true })
    });
  } else {
    request.continue();
  }
});
```

### Response Handling

```javascript
page.on('response', async response => {
  if (response.url().includes('/api/data')) {
    const data = await response.json();
    console.log('API Response:', data);
  }
});
```

## Stealth Mode

### Using puppeteer-extra-plugin-stealth

```javascript
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

puppeteer.use(StealthPlugin());

const browser = await puppeteer.launch({ headless: true });
```

### Manual Evasion Techniques

```javascript
// Override webdriver property
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
  });
});

// Override plugins
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
  });
});

// Override languages
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en']
  });
});
```

## Performance Optimization

### Disable Unnecessary Features

```javascript
const browser = await puppeteer.launch({
  args: [
    '--disable-gpu',
    '--disable-dev-shm-usage',
    '--disable-setuid-sandbox',
    '--no-sandbox',
    '--disable-accelerated-2d-canvas',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images', // if images not needed
    '--blink-settings=imagesEnabled=false'
  ]
});

// Block resources
await page.setRequestInterception(true);
page.on('request', request => {
  const blocked = ['image', 'stylesheet', 'font', 'media'];
  if (blocked.includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});
```

## Error Handling

### Navigation Error Handling

```javascript
async function safeNavigate(page, url, options = {}) {
  try {
    const response = await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 30000,
      ...options
    });

    if (!response.ok()) {
      throw new Error(`HTTP ${response.status()}: ${response.statusText()}`);
    }

    return response;
  } catch (error) {
    if (error.message.includes('net::ERR_')) {
      throw new Error(`Network error: ${error.message}`);
    }
    if (error.message.includes('Timeout')) {
      throw new Error(`Page load timeout: ${url}`);
    }
    throw error;
  }
}
```

### Element Interaction Error Handling

```javascript
async function safeClick(page, selector, options = {}) {
  const { timeout = 5000, retries = 3 } = options;

  for (let i = 0; i < retries; i++) {
    try {
      await page.waitForSelector(selector, { visible: true, timeout });
      await page.click(selector);
      return true;
    } catch (error) {
      if (i === retries - 1) {
        throw new Error(`Failed to click ${selector}: ${error.message}`);
      }
      await page.waitForTimeout(1000);
    }
  }
}

async function safeExtract(page, selector, defaultValue = null) {
  try {
    await page.waitForSelector(selector, { timeout: 5000 });
    return await page.$eval(selector, el => el.textContent?.trim());
  } catch {
    return defaultValue;
  }
}
```

## Advanced Patterns

### Multi-Tab Handling

```javascript
// Detect new page from target="_blank"
const [newPage] = await Promise.all([
  new Promise(resolve => browser.once('targetcreated', target => resolve(target.page()))),
  page.click('a[target="_blank"]')
]);
await newPage.waitForLoadState();

// Switch between tabs
const pages = await browser.pages();
await pages[0].bringToFront();

// Close specific tab
await newPage.close();
```

### iFrame Handling

```javascript
const frameHandle = await page.waitForSelector('iframe#myframe');
const frame = await frameHandle.contentFrame();
await frame.click('#button-in-iframe');
```

### Dialog Handling

```javascript
page.on('dialog', async dialog => {
  console.log(dialog.message());
  await dialog.accept('Input value'); // or dialog.dismiss()
});
```

### Download Handling

```javascript
const downloadPath = '/tmp/downloads';
const client = await page.target().createCDPSession();
await client.send('Page.setDownloadBehavior', {
  behavior: 'allow',
  downloadPath
});

await page.click('#download-button');
// Wait for file...
```

### Mobile Emulation

```javascript
const puppeteer = require('puppeteer');
const iPhone = puppeteer.devices['iPhone 12'];

const page = await browser.newPage();
await page.emulate(iPhone);
await page.goto('https://example.com');
```

## Proxy Support

### Single Proxy

```javascript
const browser = await puppeteer.launch({
  args: ['--proxy-server=http://proxy.example.com:8080']
});

// With authentication
const page = await browser.newPage();
await page.authenticate({
  username: 'proxyuser',
  password: 'proxypass'
});
```

### Proxy Pool Rotation

```javascript
const proxies = [
  'http://proxy1.example.com:8080',
  'http://proxy2.example.com:8080',
  'http://proxy3.example.com:8080'
];

let proxyIndex = 0;

async function getNextProxy() {
  const proxy = proxies[proxyIndex];
  proxyIndex = (proxyIndex + 1) % proxies.length;
  return proxy;
}

async function createBrowserWithProxy() {
  const proxy = await getNextProxy();
  return puppeteer.launch({
    args: [`--proxy-server=${proxy}`]
  });
}
```
