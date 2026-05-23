// purpose: bun:test skeleton for the Bun service
// consumes: bun-service-skeleton.ts entry
// produces: passing test suite when `bun test` is run
// depends-on: Bun >= 1.1; bun:test built-in
// token-budget-impact: ~180 tokens when loaded as context
import { test, expect } from 'bun:test'
import app from './bun-service-skeleton'

test('health returns ok', async () => {
  const res = await app.fetch(new Request('http://localhost/health'))
  expect(res.status).toBe(200)
  expect(await res.json()).toEqual({ ok: true })
})

test('register hashes password', async () => {
  const res = await app.fetch(new Request('http://localhost/register', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ email: 'a@b.c', password: 'hunter2' }),
  }))
  expect(res.status).toBe(200)
  const body = await res.json()
  expect(body.ok).toBe(true)
})
