// purpose: Server-runtime Sentry config skeleton with Supabase scrubbing + baseline ignore list.
// consumes: see content/02-output-contract.xml inputs
// produces: artefact conforming to content/02-output-contract.xml
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-600 tokens when loaded as context

/* eslint-disable @typescript-eslint/no-explicit-any */
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.2,
  beforeSend(event: any) {
    if (event?.request?.headers) {
      delete event.request.headers.authorization;
      delete event.request.headers.cookie;
    }
    if (event?.extra) {
      for (const k of ["access_token", "refresh_token", "provider_token"]) {
        if (k in event.extra) event.extra[k] = "[Filtered]";
      }
    }
    return event;
  },
  ignoreErrors: [
    "ResizeObserver loop limit exceeded",
    "AbortError",
    "NextRouter was not mounted",
    "Hydration failed",
  ],
});
