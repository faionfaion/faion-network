// purpose: Testing Library + MSW setup file loaded by Vitest before each test
// consumes: msw-server.ts handler list
// produces: a clean handler stack per test + Testing Library matchers
// depends-on: @testing-library/jest-dom, msw, vitest
// token-budget-impact: ~140 tokens when loaded as context
import '@testing-library/jest-dom/vitest'
import { afterAll, afterEach, beforeAll } from 'vitest'
import { server } from './msw-server'

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
