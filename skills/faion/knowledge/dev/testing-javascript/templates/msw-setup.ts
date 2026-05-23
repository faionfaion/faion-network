// purpose: TBD-template-header
// consumes: input from methodology
// produces: output artefact
// depends-on: 01-core-rules.xml
// token-budget-impact: small

/**
 * MSW v2 setup — works for both test (Node) and browser (dev/storybook) environments.
 *
 * Usage:
 *   1. Add to vitest.config.ts: setupFiles: ['./tests/setup.ts']
 *   2. Import server in individual test files to override handlers per-test.
 */

// ---- handlers.ts ----
// Create a separate file: tests/mocks/handlers.ts

import { http, HttpResponse } from 'msw';

export const handlers = [
  // Example: mock a REST endpoint
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Test User',
      email: 'test@example.com',
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json() as Record<string, unknown>;
    return HttpResponse.json(
      { id: crypto.randomUUID(), ...body },
      { status: 201 }
    );
  }),

  http.delete('/api/users/:id', () => {
    return new HttpResponse(null, { status: 204 });
  }),
];

// ---- server.ts (Node — for tests) ----
// Create: tests/mocks/server.ts

import { setupServer } from 'msw/node';
// import { handlers } from './handlers';

export const server = setupServer(...handlers);

// ---- setup.ts (Vitest global setup) ----
// Add to your tests/setup.ts:

// import { server } from './mocks/server';
// import '@testing-library/jest-dom';

// beforeAll(() => {
//   server.listen({ onUnhandledRequest: 'error' });
// });

// afterEach(() => {
//   server.resetHandlers(); // remove per-test overrides
// });

// afterAll(() => {
//   server.close();
// });

// ---- Per-test handler override ----
// In a specific test file:

// import { http, HttpResponse } from 'msw';
// import { server } from '../mocks/server';

// it('shows error on 500', async () => {
//   server.use(
//     http.get('/api/users/1', () => {
//       return HttpResponse.json({ message: 'Server error' }, { status: 500 });
//     })
//   );
//   // ... rest of test
// });

// ---- browser.ts (Browser — for Storybook/dev) ----
// Create: src/mocks/browser.ts

import { setupWorker } from 'msw/browser';
// import { handlers } from './handlers';

export const worker = setupWorker(...handlers);

// In main.tsx or preview.ts (Storybook):
// if (import.meta.env.DEV) {
//   const { worker } = await import('./mocks/browser');
//   await worker.start({ onUnhandledRequest: 'bypass' });
// }
