// purpose: Domain error classes shared across layers
// consumes: See content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1000 tokens when loaded as context
import { ErrorRequestHandler } from 'express';
import { ZodError } from 'zod';

export class AppError extends Error {
  constructor(
    message: string,
    public statusCode = 500,
    public code = 'INTERNAL_ERROR',
    public isOperational = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') { super(message, 404, 'NOT_FOUND'); }
}

export class ConflictError extends AppError {
  constructor(message = 'Resource conflict') { super(message, 409, 'CONFLICT'); }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') { super(message, 401, 'UNAUTHORIZED'); }
}

export class ValidationError extends AppError {
  constructor(message = 'Validation failed', public errors: Record<string, string[]> = {}) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

export const errorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  if (err instanceof ZodError) {
    return res.status(400).json({ error: 'Validation failed', code: 'VALIDATION_ERROR',
      details: err.flatten().fieldErrors });
  }
  if (err instanceof AppError && err.isOperational) {
    return res.status(err.statusCode).json({ error: err.message, code: err.code });
  }
  return res.status(500).json({ error: 'Internal server error', code: 'INTERNAL_ERROR' });
};
