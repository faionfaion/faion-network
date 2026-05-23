// purpose: reference createApp() factory for a layered TS Express service
// consumes: config from ./config/env, routes from ./routes, errorHandler from ./middleware/errorHandler
// produces: an Express instance ready to listen — listen() lives in server.ts, not here
// depends-on: express, helmet, cors, compression, ./utils/logger
// token-budget-impact: ~350 tokens when loaded by an agent as a scaffold reference

import express, { type Express } from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import { config } from './config/env';
import { requestLogger } from './middleware/requestLogger';
import { authenticate } from './middleware/auth';
import { errorHandler } from './middleware/errorHandler';
import routes from './routes';

export function createApp(): Express {
  const app = express();

  // 1. Security headers
  app.use(helmet());
  app.use(cors({ origin: config.CORS_ORIGIN }));

  // 2. Parsers
  app.use(express.json({ limit: '10kb' }));
  app.use(express.urlencoded({ extended: true, limit: '10kb' }));

  // 3. Compression
  app.use(compression());

  // 4. Logging
  app.use(requestLogger);

  // 5. Auth (optional — remove the line when auth_mode == 'none')
  app.use('/api', authenticate);

  // 6. Routes
  app.use('/api/v1', routes);

  // 7. Health probe
  app.get('/health', (_req, res) => {
    res.json({ status: 'ok', ts: new Date().toISOString() });
  });

  // 8. Error handler — MUST be last.
  app.use(errorHandler);

  return app;
}
