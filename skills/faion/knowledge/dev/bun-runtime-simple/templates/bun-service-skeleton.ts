// purpose: hello-world Bun + Hono service skeleton
// consumes: route list from bun-runtime-simple AGENTS.md Prerequisites
// produces: runnable Bun service; bun run index.ts
// depends-on: Bun >= 1.1; hono package
// token-budget-impact: ~250 tokens when loaded as context
import { Hono } from 'hono'

const app = new Hono()

app.get('/health', (c) => c.json({ ok: true }))

app.post('/register', async (c) => {
  const { email, password } = await c.req.json<{ email: string; password: string }>()
  const hash = await Bun.password.hash(password)
  return c.json({ ok: true, email, hash_prefix: hash.slice(0, 8) })
})

export default {
  port: Number(Bun.env.PORT ?? 3000),
  fetch: app.fetch,
}
