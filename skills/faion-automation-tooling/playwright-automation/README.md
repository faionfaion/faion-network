# Playwright Browser Automation

**Layer:** Technical reference
**Used by:** faion-browser-agent

## Overview

Playwright is Microsoft's cross-browser automation library supporting Chromium, Firefox, and WebKit.

**Installation:**
```bash
npm install playwright
# Install browsers
npx playwright install
```

## Basic Setup

### Standard Launch

```javascript
const { chromium, firefox, webkit } = require('playwright');

async function main() {
  // Choose browser
  const browser = await chromium.launch({
    headless: true,
    slowMo: 50 // slow down operations
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Custom User Agent'
  });

  const page = await context.newPage();
  await page.goto('https://example.com');

  await browser.close();
}
```

### Browser Contexts

```javascript
// Isolated context with storage state
const context = await browser.newContext({
  storageState: 'auth.json', // saved login state
  locale: 'en-US',
  timezoneId: 'America/New_York',
  geolocation: { longitude: -73.935242, latitude: 40.730610 },
  permissions: ['geolocation']
});

// Save storage state
await context.storageState({ path: 'auth.json' });
```

## Auto-Waiting

Playwright automatically waits for elements. No explicit waits needed for most operations.

```javascript
// These auto-wait for element to be actionable
await page.click('#button');      // waits for element, enabled, stable
await page.fill('#input', 'text'); // waits for element, enabled, editable
await page.check('#checkbox');    // waits for element, enabled, stable

// Explicit waits when needed
await page.waitForSelector('#dynamic-element');
await page.waitForLoadState('networkidle');
await page.waitForURL('**/dashboard');
await page.waitForFunction(() => window.dataLoaded === true);
```

## Selectors

### Selector Types

```javascript
// CSS
await page.click('#button');
await page.click('.class');

// Text
await page.click('text=Click me');
await page.click('text=/submit/i'); // regex

// XPath
await page.click('xpath=//button[@type="submit"]');

// Role (accessibility)
await page.click('role=button[name="Submit"]');
await page.click('role=link[name="Learn more"]');

// Chained selectors
await page.click('.parent >> .child');
await page.click('.form >> text=Submit');

// Has-text filter
await page.click('article:has-text("Breaking News")');

// Nth match
await page.click('.item >> nth=0'); // first
await page.click('.item >> nth=-1'); // last
```

### Locators (Recommended)

```javascript
// Create reusable locators
const submitButton = page.locator('button[type="submit"]');
const emailInput = page.locator('#email');

// Chain locators
const form = page.locator('form.login');
const username = form.locator('#username');
const password = form.locator('#password');

// Filter locators
const activeItems = page.locator('.item').filter({ hasText: 'Active' });
const specificRow = page.locator('tr').filter({ has: page.locator('td', { hasText: 'John' }) });

// Use locators
await emailInput.fill('user@example.com');
await submitButton.click();
```

## Form Handling

### Input Types

```javascript
// Text
await page.fill('#name', 'John Doe');

// Select
await page.selectOption('#country', 'US');
await page.selectOption('#multi', ['opt1', 'opt2']);

// Checkbox/Radio
await page.check('#agree');
await page.uncheck('#newsletter');
await page.setChecked('#terms', true);

// File upload
await page.setInputFiles('#upload', 'file.pdf');
await page.setInputFiles('#upload', ['file1.pdf', 'file2.pdf']);
await page.setInputFiles('#upload', []); // clear

// Date
await page.fill('#date', '2026-01-18');

// Content editable
await page.fill('[contenteditable]', 'Rich text content');
```

### Focus and Blur

```javascript
await page.focus('#input');
await page.blur('#input');

// Dispatch events
await page.dispatchEvent('#input', 'change');
```

## Screenshot and PDF

### Screenshots

```javascript
// Full page
await page.screenshot({ path: 'full.png', fullPage: true });

// Element
await page.locator('#chart').screenshot({ path: 'chart.png' });

// Options
await page.screenshot({
  path: 'screenshot.png',
  type: 'png',
  clip: { x: 0, y: 0, width: 800, height: 600 },
  omitBackground: true,
  animations: 'disabled', // wait for animations
  caret: 'hide', // hide text cursor
  scale: 'css' // or 'device'
});

// As buffer
const buffer = await page.screenshot();
```

### PDF Generation

```javascript
await page.pdf({
  path: 'document.pdf',
  format: 'A4',
  printBackground: true,
  margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' },
  displayHeaderFooter: true,
  headerTemplate: '<div>Header</div>',
  footerTemplate: '<div><span class="pageNumber"></span></div>'
});
```

## Network Interception

### Route Handling

```javascript
// Block resources
await page.route('**/*.{png,jpg,jpeg}', route => route.abort());

// Modify requests
await page.route('**/api/**', route => {
  route.continue({
    headers: {
      ...route.request().headers(),
      'Authorization': 'Bearer token'
    }
  });
});

// Mock responses
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([{ id: 1, name: 'Mock User' }])
  });
});

// Modify response
await page.route('**/api/data', async route => {
  const response = await route.fetch();
  const json = await response.json();
  json.modified = true;
  route.fulfill({ response, json });
});
```

### Request/Response Events

```javascript
// Listen to requests
page.on('request', request => {
  console.log('>>', request.method(), request.url());
});

page.on('response', response => {
  console.log('<<', response.status(), response.url());
});

// Wait for specific response
const responsePromise = page.waitForResponse('**/api/data');
await page.click('#load-data');
const response = await responsePromise;
const data = await response.json();
```

## Video Recording

```javascript
const context = await browser.newContext({
  recordVideo: {
    dir: 'videos/',
    size: { width: 1280, height: 720 }
  }
});

const page = await context.newPage();
// ... perform actions ...

// Save video (closes page)
await page.close();
const video = await page.video();
const path = await video.path();
```

## Tracing

```javascript
// Start tracing
await context.tracing.start({
  screenshots: true,
  snapshots: true,
  sources: true
});

// ... perform actions ...

// Stop and save
await context.tracing.stop({ path: 'trace.zip' });

// View trace: npx playwright show-trace trace.zip
```

## Testing Framework

### Basic Test Structure

```javascript
// tests/example.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display title', async ({ page }) => {
    await expect(page).toHaveTitle(/Example/);
  });

  test('should navigate to about', async ({ page }) => {
    await page.click('text=About');
    await expect(page).toHaveURL(/.*about/);
  });
});
```

### Fixtures

```javascript
// fixtures/auth.js
const { test: base } = require('@playwright/test');

exports.test = base.extend({
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: 'auth.json'
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('/admin/login');
    await page.fill('#username', 'admin');
    await page.fill('#password', 'adminpass');
    await page.click('button[type="submit"]');
    await use(page);
    await context.close();
  }
});
```

### Assertions

```javascript
const { test, expect } = require('@playwright/test');

test('assertions', async ({ page }) => {
  // Page assertions
  await expect(page).toHaveTitle('My App');
  await expect(page).toHaveURL(/dashboard/);

  // Element assertions
  await expect(page.locator('h1')).toHaveText('Welcome');
  await expect(page.locator('h1')).toContainText('Welc');
  await expect(page.locator('.item')).toHaveCount(5);
  await expect(page.locator('#button')).toBeVisible();
  await expect(page.locator('#button')).toBeEnabled();
  await expect(page.locator('#input')).toHaveValue('test');
  await expect(page.locator('#input')).toHaveAttribute('placeholder', 'Enter...');
  await expect(page.locator('.active')).toHaveClass(/selected/);

  // Soft assertions (continue on failure)
  await expect.soft(page.locator('h1')).toHaveText('Title');
  await expect.soft(page.locator('h2')).toHaveText('Subtitle');
});
```

## Advanced Patterns

### Multi-Tab Handling

```javascript
// Open new tab
const [newPage] = await Promise.all([
  context.waitForEvent('page'),
  page.click('a[target="_blank"]')
]);
await newPage.waitForLoadState();

// Switch between tabs
const pages = context.pages();
await pages[0].bringToFront();

// Close specific tab
await newPage.close();
```

### iFrame Handling

```javascript
// Playwright
const frame = page.frameLocator('iframe#myframe');
await frame.locator('#button-in-iframe').click();

// Multiple nested iframes
const nestedFrame = page
  .frameLocator('#outer-frame')
  .frameLocator('#inner-frame');
await nestedFrame.locator('#deep-button').click();
```

### Dialog Handling

```javascript
// Auto-accept
page.on('dialog', dialog => dialog.accept());

// Handle specific dialog
const dialogPromise = page.waitForEvent('dialog');
await page.click('#trigger-alert');
const dialog = await dialogPromise;
await dialog.accept();
```

### Download Handling

```javascript
const downloadPromise = page.waitForEvent('download');
await page.click('#download-button');
const download = await downloadPromise;

// Save to specific path
await download.saveAs('/path/to/save/file.pdf');

// Get suggested filename
const filename = download.suggestedFilename();

// Get download stream
const stream = await download.createReadStream();
```

### Geolocation and Permissions

```javascript
// Set geolocation
const context = await browser.newContext({
  geolocation: { longitude: -122.4194, latitude: 37.7749 },
  permissions: ['geolocation']
});

// Grant permissions
await context.grantPermissions(['geolocation', 'notifications'], {
  origin: 'https://example.com'
});

// Clear permissions
await context.clearPermissions();
```

### Mobile Emulation

```javascript
const { devices } = require('playwright');
const iPhone12 = devices['iPhone 12'];

const context = await browser.newContext({
  ...iPhone12
});

// Custom device
const context = await browser.newContext({
  viewport: { width: 375, height: 812 },
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0...',
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true
});
```

## Proxy Support

```javascript
const browser = await chromium.launch({
  proxy: {
    server: 'http://proxy.example.com:8080',
    username: 'user',
    password: 'pass'
  }
});
```

## Page Object Model

### Page Object Class

```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = '#username';
    this.passwordInput = '#password';
    this.submitButton = 'button[type="submit"]';
    this.errorMessage = '.error-message';
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username, password) {
    await this.page.fill(this.usernameInput, username);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }

  async getErrorMessage() {
    return await this.page.textContent(this.errorMessage);
  }

  async isLoggedIn() {
    return await this.page.isVisible('.dashboard');
  }
}

module.exports = { LoginPage };
```

### Using Page Objects

```javascript
const { LoginPage } = require('./pages/LoginPage');

describe('Login', () => {
  let loginPage;

  beforeEach(async () => {
    loginPage = new LoginPage(page);
    await loginPage.navigate();
  });

  test('successful login', async () => {
    await loginPage.login('user@example.com', 'password123');
    expect(await loginPage.isLoggedIn()).toBe(true);
  });

  test('invalid credentials', async () => {
    await loginPage.login('wrong@example.com', 'wrongpass');
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
  });
});
```
