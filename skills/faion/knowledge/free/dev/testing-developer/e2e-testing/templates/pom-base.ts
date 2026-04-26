import { type Page, type Locator } from '@playwright/test';

/**
 * Abstract base class for Page Objects.
 * Extend this for every page or major feature section.
 */
export abstract class BasePage {
  protected readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  abstract readonly url: string;

  async navigate(params?: Record<string, string>): Promise<void> {
    const searchParams = params ? '?' + new URLSearchParams(params).toString() : '';
    await this.page.goto(this.url + searchParams);
  }

  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  /** Convenience: wait for a locator to be visible */
  async waitForVisible(locator: Locator, timeout = 5000): Promise<void> {
    await locator.waitFor({ state: 'visible', timeout });
  }

  /** Returns current page title */
  async title(): Promise<string> {
    return this.page.title();
  }
}

// Example concrete Page Object:
//
// export class LoginPage extends BasePage {
//   readonly url = '/login';
//   readonly emailInput = this.page.getByLabel('Email');
//   readonly passwordInput = this.page.getByLabel('Password');
//   readonly submitButton = this.page.getByRole('button', { name: 'Sign in' });
//
//   async login(email: string, password: string): Promise<void> {
//     await this.emailInput.fill(email);
//     await this.passwordInput.fill(password);
//     await this.submitButton.click();
//   }
// }
