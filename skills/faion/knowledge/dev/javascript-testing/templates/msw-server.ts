// purpose: MSW server skeleton for HTTP mocking in tests
// consumes: API routes the system under test calls
// produces: a request-handler stack with per-test override capability
// depends-on: msw >= 2.x (Node API)
// token-budget-impact: ~120 tokens when loaded as context
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/api/health', () => HttpResponse.json({ ok: true })),
]

export const server = setupServer(...handlers)
