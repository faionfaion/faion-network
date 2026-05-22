// purpose: production-shape Express app entry with canonical middleware stack
// consumes: service spec from nodejs-express AGENTS.md Prerequisites
// produces: runnable Express server on PORT env
// depends-on: express, helmet, cors, compression, pino-http, express-rate-limit
// token-budget-impact: ~280 tokens when loaded as context
import express, { type NextFunction, type Request, type Response } from 'express'
import helmet from 'helmet'
import cors from 'cors'
import compression from 'compression'
import pinoHttp from 'pino-http'
import rateLimit from 'express-rate-limit'

export function createApp() {
  const app = express()
  app.use(helmet())
  app.use(cors())
  app.use(compression())
  app.use(pinoHttp())
  app.use(rateLimit({ windowMs: 60_000, max: 120 }))
  app.use(express.json({ limit: '1mb' }))

  app.get('/health', (_req, res) => res.json({ ok: true }))

  // routes go here

  // Central error handler MUST be last:
  app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
    res.status(err?.status ?? 500).json({ error: err?.code ?? 'internal' })
  })

  return app
}
