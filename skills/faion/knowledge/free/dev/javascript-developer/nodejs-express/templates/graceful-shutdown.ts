// purpose: SIGINT/SIGTERM graceful shutdown for Express server
// consumes: http server instance + DB pool close() callback
// produces: drained server + closed resources; exits 0
// depends-on: Node >= 20 http server
// token-budget-impact: ~160 tokens when loaded as context
import type { Server } from 'node:http'

export function wireGracefulShutdown(server: Server, opts: {
  dbClose?: () => Promise<void>
  drainTimeoutMs?: number
} = {}) {
  const drainTimeoutMs = opts.drainTimeoutMs ?? 30_000
  let shuttingDown = false

  async function shutdown(signal: string) {
    if (shuttingDown) return
    shuttingDown = true
    console.log(`[shutdown] ${signal} received; draining`)
    const t = setTimeout(() => {
      console.error('[shutdown] drain timeout exceeded; force exit')
      process.exit(1)
    }, drainTimeoutMs)
    server.close(async () => {
      try { await opts.dbClose?.() } catch (e) { console.error(e) }
      clearTimeout(t)
      process.exit(0)
    })
  }

  process.on('SIGINT', () => shutdown('SIGINT'))
  process.on('SIGTERM', () => shutdown('SIGTERM'))
}
