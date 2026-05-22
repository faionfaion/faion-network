// purpose: Hono HTTP server template running on Bun.serve.
// consumes: project repo; see the methodology AGENTS.md for input contract.
// produces: the working artifact described above; placement: Place under src/server.ts.
// depends-on: the tooling pinned in the methodology's AGENTS.md.
// token-budget-impact: zero — local-only template; build/CI time is the only cost.
// src/index.ts — Hono server with middleware, Zod validation, JWT-protected routes
import { Hono } from "hono"
import { cors } from "hono/cors"
import { logger } from "hono/logger"
import { jwt } from "hono/jwt"
import { zValidator } from "@hono/zod-validator"
import { z } from "zod"

const app = new Hono()

// Middleware
app.use("*", logger())
app.use("/api/*", cors())

// Public routes
app.get("/health", (c) => c.json({ status: "ok" }))

// Auth routes
app.post(
  "/api/auth/login",
  zValidator(
    "json",
    z.object({
      email: z.string().email(),
      password: z.string().min(8),
    })
  ),
  async (c) => {
    const { email, password } = c.req.valid("json")
    // Replace with real auth logic
    const token = "jwt-token"
    return c.json({ token })
  }
)

// Protected routes
const api = new Hono()
api.use("*", jwt({ secret: Bun.env.JWT_SECRET! }))

api.get("/users", async (c) => {
  return c.json({ data: [] })
})

api.post(
  "/users",
  zValidator(
    "json",
    z.object({
      email: z.string().email(),
      name: z.string().min(1),
    })
  ),
  async (c) => {
    const data = c.req.valid("json")
    return c.json({ data }, 201)
  }
)

app.route("/api", api)

// Start server — Hono adapter for Bun.serve
export default {
  port: Bun.env.PORT || 3000,
  fetch: app.fetch,
}
