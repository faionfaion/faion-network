// purpose: centralised error mapping middleware for Express
// consumes: known error kinds enumerated by the service
// produces: deterministic JSON error responses; no stack leakage
// depends-on: express; pino for logging
// token-budget-impact: ~160 tokens when loaded as context
import type { ErrorRequestHandler } from 'express'

const STATUS_MAP: Record<string, number> = {
  ValidationError: 400,
  AuthError: 401,
  ForbiddenError: 403,
  NotFoundError: 404,
  ConflictError: 409,
  RateLimitError: 429,
}

export const errorMiddleware: ErrorRequestHandler = (err, req, res, _next) => {
  const status = STATUS_MAP[err?.name] ?? err?.status ?? 500
  const code = err?.code ?? err?.name ?? 'internal'
  req.log?.error({ err, status, code }, 'request failed')
  res.status(status).json({ error: code, message: status >= 500 ? 'internal' : err?.message })
}
