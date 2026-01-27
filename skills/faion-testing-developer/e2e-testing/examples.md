# E2E Testing Examples

Real-world examples for Playwright and Cypress covering common E2E scenarios.

---

## Table of Contents

1. [Page Object Model](#1-page-object-model)
2. [Authentication](#2-authentication)
3. [E-Commerce Checkout](#3-e-commerce-checkout)
4. [API Mocking](#4-api-mocking)
5. [Visual Regression](#5-visual-regression)
6. [Mobile Testing](#6-mobile-testing)
7. [Data Factories](#7-data-factories)
8. [Error Handling](#8-error-handling)
9. [File Upload/Download](#9-file-uploaddownload)
10. [Multi-Tab/Window](#10-multi-tabwindow)

---

## 1. Page Object Model

### Playwright - Base Page Class

```typescript
// pages/BasePage.ts
import { Page, Locator } from '@playwright/test';

export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Common elements
  readonly header = () => this.page.getByRole('banner');
  readonly footer = () => this.page.getByRole('contentinfo');
  readonly loadingSpinner = () => this.page.getByTestId('loading-spinner');
  readonly toastMessage = () => this.page.getByRole('alert');

  // Common actions
  async waitForPageLoad() {
    await this.loadingSpinner().waitFor({ state: 'hidden' });
  }

  async getToastText(): Promise<string> {
    await this.toastMessage().waitFor();
    return this.toastMessage().textContent() ?? '';
  }

  async navigateToHeader(linkName: string) {
    await this.header().getByRole('link', { name: linkName }).click();
  }
}
```

### Playwright - Login Page Object

```typescript
// pages/LoginPage.ts
import { Page, expect } from '@playwright/test';
import { BasePage } from './BasePage';
import { DashboardPage } from './DashboardPage';

export class LoginPage extends BasePage {
  readonly url = '/login';

  // Locators
  readonly emailInput = () => this.page.getByLabel('Email');
  readonly passwordInput = () => this.page.getByLabel('Password');
  readonly submitButton = () => this.page.getByRole('button', { name: 'Sign In' });
  readonly rememberMeCheckbox = () => this.page.getByLabel('Remember me');
  readonly forgotPasswordLink = () => this.page.getByRole('link', { name: 'Forgot password?' });
  readonly errorMessage = () => this.page.getByRole('alert');
  readonly googleLoginButton = () => this.page.getByRole('button', { name: /Google/i });

  async goto() {
    await this.page.goto(this.url);
    await this.waitForPageLoad();
  }

  async login(email: string, password: string, rememberMe = false): Promise<DashboardPage> {
    await this.emailInput().fill(email);
    await this.passwordInput().fill(password);
    if (rememberMe) {
      await this.rememberMeCheckbox().check();
    }
    await this.submitButton().click();
    await this.page.waitForURL('/dashboard');
    return new DashboardPage(this.page);
  }

  async attemptLogin(email: string, password: string) {
    await this.emailInput().fill(email);
    await this.passwordInput().fill(password);
    await this.submitButton().click();
  }

  async getErrorMessage(): Promise<string> {
    await this.errorMessage().waitFor();
    return this.errorMessage().textContent() ?? '';
  }
}
```

### Playwright - Test Using Page Object

```typescript
// tests/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Authentication', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('should login with valid credentials', async ({ page }) => {
    const dashboard = await loginPage.login('user@example.com', 'validPassword123');
    await expect(page).toHaveURL('/dashboard');
    await expect(dashboard.welcomeMessage()).toContainText('Welcome');
  });

  test('should display error for invalid credentials', async () => {
    await loginPage.attemptLogin('user@example.com', 'wrongPassword');
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid email or password');
  });

  test('should display error for empty fields', async () => {
    await loginPage.submitButton().click();
    await expect(loginPage.emailInput()).toHaveAttribute('aria-invalid', 'true');
  });
});
```

### Cypress - Page Object Pattern

```typescript
// cypress/pages/LoginPage.ts
export class LoginPage {
  visit() {
    cy.visit('/login');
  }

  get emailInput() {
    return cy.getByTestId('email-input');
  }

  get passwordInput() {
    return cy.getByTestId('password-input');
  }

  get submitButton() {
    return cy.getByTestId('submit-button');
  }

  get errorMessage() {
    return cy.get('[role="alert"]');
  }

  login(email: string, password: string) {
    this.emailInput.type(email);
    this.passwordInput.type(password);
    this.submitButton.click();
  }
}

// cypress/support/commands.ts
Cypress.Commands.add('getByTestId', (testId: string) => {
  return cy.get(`[data-testid="${testId}"]`);
});
```

---

## 2. Authentication

### Playwright - storageState Authentication

```typescript
// auth.setup.ts
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '../.auth/user.json');

setup('authenticate', async ({ page }) => {
  // Perform login via UI
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: 'Sign In' }).click();

  // Wait for successful login
  await page.waitForURL('/dashboard');
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

  // Save authentication state
  await page.context().storageState({ path: authFile });
});
```

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    // Setup project that creates auth state
    { name: 'setup', testMatch: /.*\.setup\.ts/ },

    // Tests that use authenticated state
    {
      name: 'chromium',
      use: {
        storageState: '.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

### Playwright - API-Based Authentication

```typescript
// fixtures/auth.fixture.ts
import { test as base, expect } from '@playwright/test';

type AuthFixture = {
  authenticatedPage: Page;
};

export const test = base.extend<AuthFixture>({
  authenticatedPage: async ({ page, request }, use) => {
    // Login via API
    const response = await request.post('/api/auth/login', {
      data: {
        email: process.env.TEST_USER_EMAIL,
        password: process.env.TEST_USER_PASSWORD,
      },
    });

    expect(response.ok()).toBeTruthy();
    const { token } = await response.json();

    // Inject token into browser context
    await page.addInitScript((token) => {
      localStorage.setItem('auth_token', token);
    }, token);

    await page.goto('/dashboard');
    await use(page);
  },
});
```

### Playwright - Multi-Role Authentication

```typescript
// fixtures/roles.fixture.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

type RoleFixtures = {
  adminPage: Page;
  userPage: Page;
  guestPage: Page;
};

export const test = base.extend<RoleFixtures>({
  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: '.auth/admin.json',
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  userPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: '.auth/user.json',
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },

  guestPage: async ({ browser }, use) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});
```

### Cypress - Session API Authentication

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session(
    [email],
    () => {
      cy.visit('/login');
      cy.getByTestId('email-input').type(email);
      cy.getByTestId('password-input').type(password);
      cy.getByTestId('submit-button').click();
      cy.url().should('include', '/dashboard');
    },
    {
      validate: () => {
        cy.getCookie('session').should('exist');
      },
    }
  );
});

// cypress/e2e/dashboard.cy.ts
describe('Dashboard', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password');
    cy.visit('/dashboard');
  });

  it('should display user profile', () => {
    cy.getByTestId('user-profile').should('be.visible');
  });
});
```

---

## 3. E-Commerce Checkout

### Playwright - Complete Checkout Flow

```typescript
// pages/CartPage.ts
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class CartPage extends BasePage {
  readonly cartItem = (productName: string) =>
    this.page.getByRole('listitem').filter({ hasText: productName });

  readonly quantityInput = (productName: string) =>
    this.cartItem(productName).getByLabel('Quantity');

  readonly removeButton = (productName: string) =>
    this.cartItem(productName).getByRole('button', { name: 'Remove' });

  readonly subtotal = () => this.page.getByTestId('subtotal');
  readonly checkoutButton = () => this.page.getByRole('button', { name: 'Checkout' });
  readonly emptyCartMessage = () => this.page.getByText('Your cart is empty');

  async updateQuantity(productName: string, quantity: number) {
    await this.quantityInput(productName).fill(quantity.toString());
    await this.waitForPageLoad();
  }

  async removeItem(productName: string) {
    await this.removeButton(productName).click();
    await this.waitForPageLoad();
  }

  async proceedToCheckout() {
    await this.checkoutButton().click();
    return new CheckoutPage(this.page);
  }
}

// pages/CheckoutPage.ts
export class CheckoutPage extends BasePage {
  // Shipping
  readonly firstNameInput = () => this.page.getByLabel('First name');
  readonly lastNameInput = () => this.page.getByLabel('Last name');
  readonly addressInput = () => this.page.getByLabel('Address');
  readonly cityInput = () => this.page.getByLabel('City');
  readonly zipInput = () => this.page.getByLabel('ZIP code');
  readonly countrySelect = () => this.page.getByLabel('Country');

  // Payment
  readonly cardNumberInput = () => this.page.getByLabel('Card number');
  readonly expiryInput = () => this.page.getByLabel('Expiry date');
  readonly cvcInput = () => this.page.getByLabel('CVC');

  // Actions
  readonly continueButton = () => this.page.getByRole('button', { name: 'Continue' });
  readonly placeOrderButton = () => this.page.getByRole('button', { name: 'Place Order' });
  readonly orderTotal = () => this.page.getByTestId('order-total');

  async fillShippingAddress(address: ShippingAddress) {
    await this.firstNameInput().fill(address.firstName);
    await this.lastNameInput().fill(address.lastName);
    await this.addressInput().fill(address.address);
    await this.cityInput().fill(address.city);
    await this.zipInput().fill(address.zip);
    await this.countrySelect().selectOption(address.country);
    await this.continueButton().click();
  }

  async fillPaymentDetails(payment: PaymentDetails) {
    await this.cardNumberInput().fill(payment.cardNumber);
    await this.expiryInput().fill(payment.expiry);
    await this.cvcInput().fill(payment.cvc);
  }

  async placeOrder(): Promise<OrderConfirmationPage> {
    await this.placeOrderButton().click();
    await this.page.waitForURL(/\/order\/confirmation/);
    return new OrderConfirmationPage(this.page);
  }
}
```

```typescript
// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { ProductPage } from '../pages/ProductPage';
import { CartPage } from '../pages/CartPage';
import { testData } from '../fixtures/testData';

test.describe('Checkout Flow', () => {
  test('should complete checkout with valid payment', async ({ page }) => {
    // Add product to cart
    const productPage = new ProductPage(page);
    await productPage.goto('wireless-headphones');
    await productPage.addToCart();

    // Navigate to cart
    const cartPage = new CartPage(page);
    await page.goto('/cart');
    await expect(cartPage.cartItem('Wireless Headphones')).toBeVisible();

    // Proceed to checkout
    const checkoutPage = await cartPage.proceedToCheckout();

    // Fill shipping
    await checkoutPage.fillShippingAddress(testData.shippingAddress);

    // Fill payment (test card)
    await checkoutPage.fillPaymentDetails({
      cardNumber: '4242424242424242',
      expiry: '12/28',
      cvc: '123',
    });

    // Place order
    const confirmationPage = await checkoutPage.placeOrder();

    // Verify order confirmation
    await expect(confirmationPage.successMessage()).toContainText('Order confirmed');
    await expect(confirmationPage.orderNumber()).toBeVisible();
  });

  test('should display error for declined card', async ({ page }) => {
    // ... setup
    const checkoutPage = new CheckoutPage(page);

    await checkoutPage.fillPaymentDetails({
      cardNumber: '4000000000000002', // Declined card
      expiry: '12/28',
      cvc: '123',
    });

    await checkoutPage.placeOrderButton().click();
    await expect(checkoutPage.errorMessage()).toContainText('Card was declined');
  });
});
```

---

## 4. API Mocking

### Playwright - Route Interception

```typescript
// tests/dashboard.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Dashboard with mocked API', () => {
  test('should display user data from API', async ({ page }) => {
    // Mock user API
    await page.route('**/api/user/profile', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 1,
          name: 'John Doe',
          email: 'john@example.com',
          plan: 'premium',
        }),
      });
    });

    await page.goto('/dashboard');
    await expect(page.getByText('John Doe')).toBeVisible();
    await expect(page.getByText('Premium Plan')).toBeVisible();
  });

  test('should handle API error gracefully', async ({ page }) => {
    await page.route('**/api/user/profile', async (route) => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' }),
      });
    });

    await page.goto('/dashboard');
    await expect(page.getByText('Failed to load profile')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();
  });

  test('should handle slow network', async ({ page }) => {
    await page.route('**/api/products', async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 3000));
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ products: [] }),
      });
    });

    await page.goto('/products');
    await expect(page.getByTestId('loading-skeleton')).toBeVisible();
    await expect(page.getByTestId('product-grid')).toBeVisible({ timeout: 5000 });
  });
});
```

### Playwright with MSW

```typescript
// mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/user/profile', () => {
    return HttpResponse.json({
      id: 1,
      name: 'Test User',
      email: 'test@example.com',
    });
  }),

  http.get('/api/products', ({ request }) => {
    const url = new URL(request.url);
    const category = url.searchParams.get('category');

    return HttpResponse.json({
      products: [
        { id: 1, name: 'Product 1', category },
        { id: 2, name: 'Product 2', category },
      ],
    });
  }),

  http.post('/api/orders', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      {
        orderId: 'ORD-12345',
        status: 'confirmed',
        items: body.items,
      },
      { status: 201 }
    );
  }),
];
```

```typescript
// tests/with-msw.spec.ts
import { test, expect } from '@playwright/test';
import { createServer } from '@mswjs/http-middleware';
import { handlers } from '../mocks/handlers';

test.describe('With MSW mocks', () => {
  let server: ReturnType<typeof createServer>;

  test.beforeAll(async () => {
    server = createServer(...handlers);
    await server.listen({ port: 9090 });
  });

  test.afterAll(async () => {
    await server.close();
  });

  test('should use mocked API', async ({ page }) => {
    await page.goto('/dashboard');
    await expect(page.getByText('Test User')).toBeVisible();
  });
});
```

### Cypress - API Mocking

```typescript
// cypress/e2e/dashboard.cy.ts
describe('Dashboard', () => {
  beforeEach(() => {
    cy.intercept('GET', '/api/user/profile', {
      statusCode: 200,
      body: {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com',
      },
    }).as('getProfile');

    cy.intercept('GET', '/api/notifications', {
      statusCode: 200,
      body: { notifications: [] },
    }).as('getNotifications');
  });

  it('should display user profile', () => {
    cy.visit('/dashboard');
    cy.wait('@getProfile');
    cy.contains('John Doe').should('be.visible');
  });

  it('should handle API errors', () => {
    cy.intercept('GET', '/api/user/profile', {
      statusCode: 500,
      body: { error: 'Server error' },
    }).as('getProfileError');

    cy.visit('/dashboard');
    cy.wait('@getProfileError');
    cy.contains('Failed to load').should('be.visible');
  });
});
```

---

## 5. Visual Regression

### Playwright - Built-in Screenshots

```typescript
// tests/visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage should match snapshot', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Full page screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      maxDiffPixelRatio: 0.01,
    });
  });

  test('product card should match snapshot', async ({ page }) => {
    await page.goto('/products');

    // Element screenshot
    const productCard = page.getByTestId('product-card').first();
    await expect(productCard).toHaveScreenshot('product-card.png');
  });

  test('should mask dynamic content', async ({ page }) => {
    await page.goto('/dashboard');

    await expect(page).toHaveScreenshot('dashboard.png', {
      mask: [
        page.getByTestId('timestamp'),
        page.getByTestId('avatar'),
        page.getByTestId('notification-count'),
      ],
    });
  });
});
```

### Playwright with Percy

```typescript
// tests/visual-percy.spec.ts
import { test } from '@playwright/test';
import percySnapshot from '@percy/playwright';

test.describe('Visual Tests with Percy', () => {
  test('homepage visual test', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await percySnapshot(page, 'Homepage');
  });

  test('responsive visual test', async ({ page }) => {
    await page.goto('/');

    // Desktop
    await page.setViewportSize({ width: 1920, height: 1080 });
    await percySnapshot(page, 'Homepage - Desktop');

    // Tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await percySnapshot(page, 'Homepage - Tablet');

    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await percySnapshot(page, 'Homepage - Mobile');
  });
});
```

---

## 6. Mobile Testing

### Playwright - Device Emulation

```typescript
// tests/mobile.spec.ts
import { test, expect, devices } from '@playwright/test';

// Use specific device
test.use({ ...devices['iPhone 14'] });

test.describe('Mobile Experience', () => {
  test('should display mobile navigation', async ({ page }) => {
    await page.goto('/');

    // Desktop nav should be hidden
    await expect(page.getByRole('navigation')).toBeHidden();

    // Mobile hamburger menu should be visible
    const menuButton = page.getByRole('button', { name: 'Menu' });
    await expect(menuButton).toBeVisible();

    // Open menu
    await menuButton.click();

    // Mobile drawer should appear
    await expect(page.getByRole('dialog')).toBeVisible();
  });

  test('should handle touch interactions', async ({ page }) => {
    await page.goto('/gallery');

    const gallery = page.getByTestId('image-gallery');

    // Swipe gesture
    await gallery.evaluate((el) => {
      const touch = new Touch({
        identifier: 1,
        target: el,
        clientX: 300,
        clientY: 200,
      });
      el.dispatchEvent(
        new TouchEvent('touchstart', { touches: [touch] })
      );
    });
  });
});
```

```typescript
// playwright.config.ts - Multiple mobile devices
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  projects: [
    {
      name: 'Desktop Chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 14'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 7'] },
    },
    {
      name: 'Tablet',
      use: { ...devices['iPad Pro 11'] },
    },
  ],
});
```

---

## 7. Data Factories

### Test Data Factory

```typescript
// fixtures/factories.ts
import { faker } from '@faker-js/faker';

export const userFactory = {
  create(overrides: Partial<User> = {}): User {
    return {
      id: faker.string.uuid(),
      email: faker.internet.email(),
      firstName: faker.person.firstName(),
      lastName: faker.person.lastName(),
      phone: faker.phone.number(),
      createdAt: faker.date.past().toISOString(),
      ...overrides,
    };
  },

  createMany(count: number, overrides: Partial<User> = {}): User[] {
    return Array.from({ length: count }, () => this.create(overrides));
  },
};

export const productFactory = {
  create(overrides: Partial<Product> = {}): Product {
    return {
      id: faker.string.uuid(),
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
      category: faker.commerce.department(),
      inStock: faker.datatype.boolean(),
      imageUrl: faker.image.url(),
      ...overrides,
    };
  },
};

export const orderFactory = {
  create(overrides: Partial<Order> = {}): Order {
    const items = productFactory.createMany(faker.number.int({ min: 1, max: 5 }));
    return {
      id: `ORD-${faker.string.alphanumeric(8).toUpperCase()}`,
      userId: faker.string.uuid(),
      items,
      total: items.reduce((sum, item) => sum + item.price, 0),
      status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered']),
      createdAt: faker.date.recent().toISOString(),
      ...overrides,
    };
  },
};
```

### Using Factories in Tests

```typescript
// tests/orders.spec.ts
import { test, expect } from '@playwright/test';
import { userFactory, orderFactory } from '../fixtures/factories';

test.describe('Order History', () => {
  test('should display order list', async ({ page }) => {
    const orders = Array.from({ length: 5 }, () => orderFactory.create());

    await page.route('**/api/orders', async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ orders }),
      });
    });

    await page.goto('/orders');

    for (const order of orders) {
      await expect(page.getByText(order.id)).toBeVisible();
    }
  });

  test('should filter by status', async ({ page }) => {
    const pendingOrders = Array.from({ length: 3 }, () =>
      orderFactory.create({ status: 'pending' })
    );
    const shippedOrders = Array.from({ length: 2 }, () =>
      orderFactory.create({ status: 'shipped' })
    );

    await page.route('**/api/orders*', async (route) => {
      const url = new URL(route.request().url());
      const status = url.searchParams.get('status');

      const filtered =
        status === 'pending' ? pendingOrders :
        status === 'shipped' ? shippedOrders :
        [...pendingOrders, ...shippedOrders];

      await route.fulfill({
        status: 200,
        body: JSON.stringify({ orders: filtered }),
      });
    });

    await page.goto('/orders');
    await page.getByRole('combobox', { name: 'Status' }).selectOption('pending');

    await expect(page.getByTestId('order-item')).toHaveCount(3);
  });
});
```

---

## 8. Error Handling

### Testing Error States

```typescript
// tests/error-handling.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Error Handling', () => {
  test('should display 404 page for unknown routes', async ({ page }) => {
    const response = await page.goto('/non-existent-page');
    expect(response?.status()).toBe(404);

    await expect(page.getByRole('heading', { name: /Page not found/i })).toBeVisible();
    await expect(page.getByRole('link', { name: /Go home/i })).toBeVisible();
  });

  test('should handle form validation errors', async ({ page }) => {
    await page.goto('/register');

    // Submit empty form
    await page.getByRole('button', { name: 'Register' }).click();

    // Check validation messages
    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Password is required')).toBeVisible();

    // Invalid email format
    await page.getByLabel('Email').fill('invalid-email');
    await page.getByRole('button', { name: 'Register' }).click();

    await expect(page.getByText('Please enter a valid email')).toBeVisible();
  });

  test('should handle network timeout', async ({ page }) => {
    await page.route('**/api/data', async (route) => {
      // Simulate timeout by never responding
      await page.waitForTimeout(30000);
    });

    await page.goto('/dashboard');

    // Should show timeout error or retry option
    await expect(
      page.getByText(/Request timed out|Unable to load/i)
    ).toBeVisible({ timeout: 15000 });
  });

  test('should recover from errors with retry', async ({ page }) => {
    let callCount = 0;

    await page.route('**/api/data', async (route) => {
      callCount++;
      if (callCount < 3) {
        await route.fulfill({ status: 500 });
      } else {
        await route.fulfill({
          status: 200,
          body: JSON.stringify({ data: 'success' }),
        });
      }
    });

    await page.goto('/dashboard');
    await expect(page.getByText('Failed to load')).toBeVisible();

    await page.getByRole('button', { name: 'Retry' }).click();
    await page.getByRole('button', { name: 'Retry' }).click();

    await expect(page.getByText('success')).toBeVisible();
  });
});
```

---

## 9. File Upload/Download

### Playwright - File Operations

```typescript
// tests/file-operations.spec.ts
import { test, expect } from '@playwright/test';
import path from 'path';
import fs from 'fs';

test.describe('File Operations', () => {
  test('should upload single file', async ({ page }) => {
    await page.goto('/upload');

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles(path.join(__dirname, '../fixtures/test-image.png'));

    await expect(page.getByText('test-image.png')).toBeVisible();
    await page.getByRole('button', { name: 'Upload' }).click();

    await expect(page.getByText('Upload successful')).toBeVisible();
  });

  test('should upload multiple files', async ({ page }) => {
    await page.goto('/upload');

    const fileInput = page.locator('input[type="file"]');
    await fileInput.setInputFiles([
      path.join(__dirname, '../fixtures/file1.pdf'),
      path.join(__dirname, '../fixtures/file2.pdf'),
    ]);

    await expect(page.getByTestId('file-list').getByRole('listitem')).toHaveCount(2);
  });

  test('should download file', async ({ page }) => {
    await page.goto('/documents');

    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('link', { name: 'Download Report' }).click();
    const download = await downloadPromise;

    // Verify download started
    expect(download.suggestedFilename()).toBe('report.pdf');

    // Save and verify file
    const downloadPath = path.join(__dirname, '../downloads', download.suggestedFilename());
    await download.saveAs(downloadPath);
    expect(fs.existsSync(downloadPath)).toBeTruthy();
  });

  test('should handle drag and drop upload', async ({ page }) => {
    await page.goto('/upload');

    const dropzone = page.getByTestId('dropzone');
    const filePath = path.join(__dirname, '../fixtures/test-file.txt');

    // Create DataTransfer with file
    const dataTransfer = await page.evaluateHandle(async (filePath) => {
      const dt = new DataTransfer();
      const response = await fetch(`file://${filePath}`);
      const blob = await response.blob();
      const file = new File([blob], 'test-file.txt', { type: 'text/plain' });
      dt.items.add(file);
      return dt;
    }, filePath);

    await dropzone.dispatchEvent('drop', { dataTransfer });
    await expect(page.getByText('test-file.txt')).toBeVisible();
  });
});
```

---

## 10. Multi-Tab/Window

### Playwright - Multi-Tab Testing

```typescript
// tests/multi-tab.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Multi-Tab Scenarios', () => {
  test('should open link in new tab and verify', async ({ page, context }) => {
    await page.goto('/');

    // Listen for new page (tab)
    const pagePromise = context.waitForEvent('page');
    await page.getByRole('link', { name: 'Documentation' }).click();
    const newPage = await pagePromise;

    // Wait for new page to load
    await newPage.waitForLoadState();

    // Verify new tab content
    await expect(newPage).toHaveURL(/docs/);
    await expect(newPage.getByRole('heading', { level: 1 })).toContainText('Documentation');

    // Verify original tab is still accessible
    await expect(page.getByRole('heading', { level: 1 })).toContainText('Home');
  });

  test('should handle popup window', async ({ page }) => {
    await page.goto('/share');

    const popupPromise = page.waitForEvent('popup');
    await page.getByRole('button', { name: 'Share on Twitter' }).click();
    const popup = await popupPromise;

    await popup.waitForLoadState();
    expect(popup.url()).toContain('twitter.com');
  });

  test('should sync data between tabs', async ({ context }) => {
    // Open two tabs
    const page1 = await context.newPage();
    const page2 = await context.newPage();

    // Login on first tab
    await page1.goto('/login');
    await page1.getByLabel('Email').fill('user@example.com');
    await page1.getByLabel('Password').fill('password');
    await page1.getByRole('button', { name: 'Login' }).click();

    // Verify second tab gets auth state
    await page2.goto('/dashboard');
    await expect(page2.getByText('Welcome, user@example.com')).toBeVisible();
  });

  test('should handle OAuth flow in popup', async ({ page }) => {
    await page.goto('/login');

    const popupPromise = page.waitForEvent('popup');
    await page.getByRole('button', { name: 'Sign in with Google' }).click();
    const popup = await popupPromise;

    // Handle OAuth in popup
    await popup.getByLabel('Email').fill('test@gmail.com');
    await popup.getByRole('button', { name: 'Next' }).click();
    await popup.getByLabel('Password').fill('password');
    await popup.getByRole('button', { name: 'Sign in' }).click();

    // Popup closes, verify main page is authenticated
    await expect(popup).toBeClosed();
    await expect(page).toHaveURL('/dashboard');
  });
});
```

---

## Quick Patterns Reference

| Pattern | When to Use |
|---------|-------------|
| Page Object | Any page with reusable elements |
| Fixtures | Shared setup across tests |
| Factories | Dynamic test data generation |
| storageState | Authentication reuse |
| Route Mocking | Isolate from backend |
| Visual Snapshots | UI regression testing |
| Multi-Tab | OAuth, external links |
