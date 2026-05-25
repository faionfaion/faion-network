// purpose: error class hierarchy for the layered Express service
// consumes: nothing (foundational)
// produces: AppError + four typed subclasses used by controllers and the error handler
// depends-on: built-in Error; no third-party imports
// token-budget-impact: ~250 tokens

export class AppError extends Error {
  constructor(
    message: string,
    public readonly statusCode: number = 500,
    public readonly code: string = 'INTERNAL_ERROR',
    public readonly isOperational: boolean = true,
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
  }
}

export class ValidationError extends AppError {
  constructor(
    message = 'Validation failed',
    public readonly fields: Record<string, string[]> = {},
  ) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}
