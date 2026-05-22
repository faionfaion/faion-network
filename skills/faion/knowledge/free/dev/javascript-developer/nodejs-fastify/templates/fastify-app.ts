// purpose: Fastify entry that registers plugins BEFORE routes, with setErrorHandler + graceful close
// consumes: Fastify service spec from nodejs-fastify AGENTS.md
// produces: runnable Fastify server
// depends-on: fastify >= 4, @fastify/helmet, @fastify/cors, @fastify/compress, @fastify/rate-limit
// token-budget-impact: ~280 tokens when loaded as context
import Fastify from 'fastify'
import helmet from '@fastify/helmet'
import cors from '@fastify/cors'
import compress from '@fastify/compress'
import rateLimit from '@fastify/rate-limit'

export async function buildApp() {
  const app = Fastify({ logger: true })

  // Plugins BEFORE routes
  await app.register(helmet)
  await app.register(cors)
  await app.register(compress)
  await app.register(rateLimit, { max: 120, timeWindow: '1 minute' })

  app.setErrorHandler((err, _req, reply) => {
    const status = err.statusCode ?? 500
    reply.status(status).send({ error: err.code ?? 'internal', message: status >= 500 ? 'internal' : err.message })
  })

  app.get('/health', { schema: { response: { 200: { type: 'object', properties: { ok: { const: true } } } } } }, async () => ({ ok: true as const }))

  // route plugins go here

  return app
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const app = await buildApp()
  await app.listen({ port: Number(process.env.PORT ?? 3000), host: '0.0.0.0' })
  const close = async () => { await app.close(); process.exit(0) }
  process.on('SIGINT', close); process.on('SIGTERM', close)
}
