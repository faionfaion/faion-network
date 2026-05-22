// purpose: Fastify route + TypeBox schema reference example
// consumes: route + body + reply contract from nodejs-fastify AGENTS.md
// produces: type-safe route handler with auto-validated request and serialized response
// depends-on: fastify >= 4, @sinclair/typebox
// token-budget-impact: ~200 tokens when loaded as context
import { Type, type Static } from '@sinclair/typebox'
import type { FastifyInstance } from 'fastify'

const Body = Type.Object({
  amount_cents: Type.Integer({ minimum: 1 }),
  currency: Type.String({ pattern: '^[A-Z]{3}$' }),
})

const Reply = Type.Object({ id: Type.String() })

export default async function invoiceRoutes(f: FastifyInstance) {
  f.post<{ Body: Static<typeof Body>; Reply: Static<typeof Reply> }>(
    '/invoices',
    { schema: { body: Body, response: { 200: Reply } } },
    async (req) => ({ id: `inv-${req.id}` }),
  )
}
