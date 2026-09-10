// purpose: Regex scrubber for HAR and log bodies
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-output-capture
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

// A header pattern must consume the header's WHOLE VALUE, to end of line. The
// previous `Authorization:\s*[^\s]+` stopped at the first whitespace, so
// `Authorization: Basic dXNlcjpzdXBlcnNlY3JldA==` became
// `Authorization: [REDACTED] dXNlcjpzdXBlcnNlY3JldA==` — the scheme redacted
// and the credential left in place, under a marker that tells a reviewer the
// file is safe. A scrubber that leaks is bad; a scrubber that leaks while
// labelling the leak REDACTED is worse than none.
const HEADERS = [
  'authorization',
  'proxy-authorization',
  'set-cookie',
  'cookie',
  'x-api-key',
  'x-auth-token',
  'x-csrf-token',
  'x-amz-security-token',
];

const PATTERNS: Array<[RegExp, string]> = [
  // whole header line, any of the names above, header value never survives
  [new RegExp(`^([ \\t]*(?:${HEADERS.join('|')}))[ \\t]*:[^\\r\\n]*`, 'gim'), '$1: [REDACTED]'],
  // the same names as JSON/HAR members: {"name": "authorization", "value": "…"}
  [new RegExp(`("name"\\s*:\\s*"(?:${HEADERS.join('|')})"\\s*,\\s*"value"\\s*:\\s*)"[^"]*"`, 'gi'),
    '$1"[REDACTED]"'],
  // secret-ish JSON keys wherever they appear
  [/("(?:api[_-]?key|access[_-]?token|refresh[_-]?token|client[_-]?secret|password|passwd|secret|session[_-]?id)"\s*:\s*)"[^"]*"/gi,
    '$1"[REDACTED]"'],
  // bearer tokens in a body rather than a header
  [/Bearer\s+[A-Za-z0-9._~+/-]+=*/g, 'Bearer [REDACTED]'],
  [/eyJ[A-Za-z0-9._-]+/g, '[JWT_REDACTED]'],
];

// Card numbers are 13-19 digits and are written with spaces or dashes as often
// as without, so `\b\d{16}\b` missed every formatted number and every 15-digit
// Amex. Luhn is what separates a card from an order id of the same length:
// over-redaction destroys the evidence the capture exists to preserve.
const CARD_CANDIDATE = /\b(?:\d[ -]?){12,18}\d\b/g;

function luhn(digits: string): boolean {
  let sum = 0;
  let double = false;
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = digits.charCodeAt(i) - 48;
    if (double) {
      d *= 2;
      if (d > 9) d -= 9;
    }
    sum += d;
    double = !double;
  }
  return sum % 10 === 0;
}

export function scrub(body: string): string {
  let out = body;
  for (const [re, rep] of PATTERNS) out = out.replace(re, rep);
  return out.replace(CARD_CANDIDATE, (match) => {
    const digits = match.replace(/[ -]/g, '');
    return digits.length >= 13 && digits.length <= 19 && luhn(digits)
      ? '[CARD_REDACTED]'
      : match;
  });
}
