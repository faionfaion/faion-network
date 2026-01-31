# Accessibility Templates

Copy-paste templates for common accessibility patterns.

## Skip Navigation Links

```html
<!-- Place at the very beginning of body -->
<a href="#main-content" class="skip-link">Skip to main content</a>
<a href="#navigation" class="skip-link">Skip to navigation</a>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: #fff;
  padding: 8px 16px;
  text-decoration: none;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
</style>
```

## Accessible Button Patterns

### Icon Button with Label

```tsx
<button aria-label="Close dialog">
  <CloseIcon aria-hidden="true" />
</button>
```

### Toggle Button

```tsx
<button
  aria-pressed={isPressed}
  onClick={() => setPressed(!isPressed)}
>
  {isPressed ? 'Mute' : 'Unmute'}
</button>
```

### Button with Loading State

```tsx
<button disabled={loading} aria-busy={loading}>
  {loading ? (
    <>
      <span className="visually-hidden">Loading...</span>
      <Spinner aria-hidden="true" />
    </>
  ) : (
    'Submit'
  )}
</button>
```

## Modal Dialog

```tsx
import { useEffect, useRef } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;

    // Store previous focus
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus first focusable element
    const focusable = dialogRef.current?.querySelector<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    focusable?.focus();

    // Trap focus
    const trapFocus = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      const focusableElements = dialogRef.current?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (!focusableElements || focusableElements.length === 0) return;

      const first = focusableElements[0];
      const last = focusableElements[focusableElements.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    // Handle Escape key
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      } else {
        trapFocus(e);
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    // Prevent body scroll
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = '';

      // Restore focus
      previousFocusRef.current?.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <>
      <div
        className="modal-backdrop"
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="modal"
      >
        <h2 id="modal-title">{title}</h2>
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </>
  );
}
```

## Accessible Form

```tsx
import { useState, useRef } from 'react';

interface FormData {
  email: string;
  password: string;
  agreeToTerms: boolean;
}

interface FormErrors {
  email?: string;
  password?: string;
  agreeToTerms?: string;
}

export function AccessibleForm() {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    agreeToTerms: false,
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);
  const errorSummaryRef = useRef<HTMLDivElement>(null);

  const validate = (): FormErrors => {
    const newErrors: FormErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms';
    }

    return newErrors;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      errorSummaryRef.current?.focus();
    } else {
      setErrors({});
      setSubmitted(true);
      // Submit form
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      {/* Error Summary */}
      {Object.keys(errors).length > 0 && (
        <div
          ref={errorSummaryRef}
          role="alert"
          tabIndex={-1}
          className="error-summary"
        >
          <h2>There are {Object.keys(errors).length} errors in the form</h2>
          <ul>
            {Object.entries(errors).map(([field, message]) => (
              <li key={field}>
                <a href={`#${field}`}>{message}</a>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Success Message */}
      {submitted && (
        <div role="status" aria-live="polite" className="success-message">
          Form submitted successfully!
        </div>
      )}

      {/* Email Field */}
      <div className="form-group">
        <label htmlFor="email">
          Email Address
          <span aria-hidden="true">*</span>
          <span className="visually-hidden">(required)</span>
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
          aria-required="true"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : 'email-hint'}
          autoComplete="email"
        />
        <span id="email-hint" className="hint">
          We'll never share your email
        </span>
        {errors.email && (
          <span id="email-error" className="error" role="alert">
            {errors.email}
          </span>
        )}
      </div>

      {/* Password Field */}
      <div className="form-group">
        <label htmlFor="password">
          Password
          <span aria-hidden="true">*</span>
          <span className="visually-hidden">(required)</span>
        </label>
        <input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
          aria-required="true"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : 'password-hint'}
          autoComplete="new-password"
        />
        <span id="password-hint" className="hint">
          At least 8 characters
        </span>
        {errors.password && (
          <span id="password-error" className="error" role="alert">
            {errors.password}
          </span>
        )}
      </div>

      {/* Checkbox */}
      <div className="form-group">
        <input
          id="agreeToTerms"
          type="checkbox"
          checked={formData.agreeToTerms}
          onChange={(e) => setFormData({ ...formData, agreeToTerms: e.target.checked })}
          required
          aria-required="true"
          aria-invalid={!!errors.agreeToTerms}
          aria-describedby={errors.agreeToTerms ? 'terms-error' : undefined}
        />
        <label htmlFor="agreeToTerms">
          I agree to the <a href="/terms">terms and conditions</a>
          <span aria-hidden="true">*</span>
        </label>
        {errors.agreeToTerms && (
          <span id="terms-error" className="error" role="alert">
            {errors.agreeToTerms}
          </span>
        )}
      </div>

      {/* Submit Button */}
      <button type="submit">Submit</button>
    </form>
  );
}
```

## Tabs Component

```tsx
import { useState, useRef, useEffect } from 'react';

interface Tab {
  id: string;
  label: string;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
}

export function Tabs({ tabs, defaultTab }: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0].id);
  const [focusIndex, setFocusIndex] = useState(0);
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);

  useEffect(() => {
    tabRefs.current = tabRefs.current.slice(0, tabs.length);
  }, [tabs]);

  const handleKeyDown = (e: React.KeyboardEvent, index: number) => {
    let newIndex = index;

    switch (e.key) {
      case 'ArrowRight':
        newIndex = (index + 1) % tabs.length;
        break;
      case 'ArrowLeft':
        newIndex = (index - 1 + tabs.length) % tabs.length;
        break;
      case 'Home':
        newIndex = 0;
        break;
      case 'End':
        newIndex = tabs.length - 1;
        break;
      default:
        return;
    }

    e.preventDefault();
    setFocusIndex(newIndex);
    setActiveTab(tabs[newIndex].id);
    tabRefs.current[newIndex]?.focus();
  };

  return (
    <div className="tabs">
      <div role="tablist" aria-label="Content tabs">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            ref={(el) => (tabRefs.current[index] = el)}
            role="tab"
            aria-selected={activeTab === tab.id}
            aria-controls={`panel-${tab.id}`}
            id={`tab-${tab.id}`}
            tabIndex={activeTab === tab.id ? 0 : -1}
            onClick={() => {
              setActiveTab(tab.id);
              setFocusIndex(index);
            }}
            onKeyDown={(e) => handleKeyDown(e, index)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map((tab) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`panel-${tab.id}`}
          aria-labelledby={`tab-${tab.id}`}
          hidden={activeTab !== tab.id}
          tabIndex={0}
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

## Accordion Component

```tsx
import { useState } from 'react';

interface AccordionItem {
  id: string;
  title: string;
  content: React.ReactNode;
}

interface AccordionProps {
  items: AccordionItem[];
  allowMultiple?: boolean;
}

export function Accordion({ items, allowMultiple = false }: AccordionProps) {
  const [expanded, setExpanded] = useState<Set<string>>(new Set());

  const toggle = (id: string) => {
    const newExpanded = new Set(expanded);

    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      if (!allowMultiple) {
        newExpanded.clear();
      }
      newExpanded.add(id);
    }

    setExpanded(newExpanded);
  };

  return (
    <div className="accordion">
      {items.map((item) => {
        const isExpanded = expanded.has(item.id);

        return (
          <div key={item.id} className="accordion-item">
            <h3>
              <button
                id={`accordion-button-${item.id}`}
                aria-expanded={isExpanded}
                aria-controls={`accordion-panel-${item.id}`}
                onClick={() => toggle(item.id)}
              >
                <span>{item.title}</span>
                <span aria-hidden="true">{isExpanded ? '−' : '+'}</span>
              </button>
            </h3>
            <div
              id={`accordion-panel-${item.id}`}
              role="region"
              aria-labelledby={`accordion-button-${item.id}`}
              hidden={!isExpanded}
            >
              {item.content}
            </div>
          </div>
        );
      })}
    </div>
  );
}
```

## Live Region for Dynamic Content

```tsx
import { useEffect, useRef } from 'react';

interface LiveRegionProps {
  message: string;
  priority?: 'polite' | 'assertive';
  atomic?: boolean;
}

export function LiveRegion({ message, priority = 'polite', atomic = true }: LiveRegionProps) {
  const regionRef = useRef<HTMLDivElement>(null);

  return (
    <div
      ref={regionRef}
      role={priority === 'assertive' ? 'alert' : 'status'}
      aria-live={priority}
      aria-atomic={atomic}
      className="visually-hidden"
    >
      {message}
    </div>
  );
}

// Usage example
export function StatusUpdater() {
  const [status, setStatus] = useState('');

  const updateStatus = (newStatus: string) => {
    setStatus(newStatus);
  };

  return (
    <>
      <button onClick={() => updateStatus('Data loaded successfully')}>
        Load Data
      </button>
      <LiveRegion message={status} priority="polite" />
    </>
  );
}
```

## Tooltip with Accessible Pattern

```tsx
import { useState, useRef } from 'react';

interface TooltipProps {
  content: string;
  children: React.ReactNode;
}

export function Tooltip({ content, children }: TooltipProps) {
  const [visible, setVisible] = useState(false);
  const tooltipId = useRef(`tooltip-${Math.random().toString(36).substr(2, 9)}`);

  return (
    <span className="tooltip-wrapper">
      <button
        aria-describedby={visible ? tooltipId.current : undefined}
        onMouseEnter={() => setVisible(true)}
        onMouseLeave={() => setVisible(false)}
        onFocus={() => setVisible(true)}
        onBlur={() => setVisible(false)}
      >
        {children}
      </button>
      {visible && (
        <span
          id={tooltipId.current}
          role="tooltip"
          className="tooltip-content"
        >
          {content}
        </span>
      )}
    </span>
  );
}
```

## CSS Utilities

```css
/* Visually Hidden (accessible to screen readers) */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focusable when navigated to via keyboard */
.visually-hidden:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}

/* Focus Styles */
:focus {
  outline: none;
}

:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* High Contrast Mode */
@media (prefers-contrast: high) {
  :root {
    --color-text: #000000;
    --color-background: #ffffff;
    --color-primary: #0000cc;
  }
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #ffffff;
    --color-background: #1a1a1a;
    --color-primary: #6b9eff;
  }
}
```

## Jest + Testing Library Tests

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Modal } from './Modal';

expect.extend(toHaveNoViolations);

describe('Modal Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(
      <Modal isOpen={true} onClose={() => {}} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should trap focus within modal', async () => {
    const user = userEvent.setup();
    render(
      <Modal isOpen={true} onClose={() => {}} title="Test Modal">
        <button>First</button>
        <button>Second</button>
        <button>Third</button>
      </Modal>
    );

    const firstButton = screen.getByRole('button', { name: 'First' });
    const thirdButton = screen.getByRole('button', { name: 'Third' });

    // Focus should wrap from last to first
    thirdButton.focus();
    await user.tab();
    expect(firstButton).toHaveFocus();

    // Focus should wrap from first to last with Shift+Tab
    await user.tab({ shift: true });
    expect(thirdButton).toHaveFocus();
  });

  it('should close on Escape key', async () => {
    const user = userEvent.setup();
    const onClose = jest.fn();
    render(
      <Modal isOpen={true} onClose={onClose} title="Test Modal">
        <p>Content</p>
      </Modal>
    );

    await user.keyboard('{Escape}');
    expect(onClose).toHaveBeenCalled();
  });

  it('should restore focus on close', () => {
    const trigger = document.createElement('button');
    document.body.appendChild(trigger);
    trigger.focus();

    const { rerender } = render(
      <Modal isOpen={true} onClose={() => {}} title="Test Modal">
        <p>Content</p>
      </Modal>
    );

    // Close modal
    rerender(
      <Modal isOpen={false} onClose={() => {}} title="Test Modal">
        <p>Content</p>
      </Modal>
    );

    expect(document.activeElement).toBe(trigger);
  });
});
```

## Playwright E2E Tests

```typescript
import { test, expect } from '@playwright/test';

test.describe('Accessibility Tests', () => {
  test('should navigate with keyboard', async ({ page }) => {
    await page.goto('/');

    // Tab through navigation
    await page.keyboard.press('Tab');
    await expect(page.locator('a:focus')).toHaveText('Home');

    await page.keyboard.press('Tab');
    await expect(page.locator('a:focus')).toHaveText('About');

    // Test skip link
    await page.goto('/');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter');
    await expect(page.locator('main')).toBeFocused();
  });

  test('should work with screen reader', async ({ page }) => {
    await page.goto('/form');

    // Check ARIA labels
    const emailInput = page.getByRole('textbox', { name: /email/i });
    await expect(emailInput).toHaveAttribute('aria-required', 'true');

    // Check error announcements
    await page.getByRole('button', { name: /submit/i }).click();
    const alert = page.getByRole('alert');
    await expect(alert).toBeVisible();
    await expect(alert).toContainText('Email is required');
  });

  test('should meet contrast requirements', async ({ page }) => {
    await page.goto('/');

    // Check button contrast
    const button = page.getByRole('button', { name: /submit/i });
    const color = await button.evaluate((el) => {
      const styles = window.getComputedStyle(el);
      return {
        color: styles.color,
        backgroundColor: styles.backgroundColor,
      };
    });

    // You would use a contrast checker library here
    // expect(getContrastRatio(color.color, color.backgroundColor)).toBeGreaterThan(4.5);
  });
});
```
