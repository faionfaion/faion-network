// purpose: Regex scrubber for HAR and log bodies
// consumes: input artefacts described in AGENTS.md ## Prerequisites
// produces: artefact conforming to content/02-output-contract.xml for puppeteer-output-capture
// depends-on: content/01-core-rules.xml
// token-budget-impact: ~200-1200 tokens when loaded as context

const PATTERNS: Array<[RegExp, string]> = [
  [/Bearer [A-Za-z0-9._\-]+/g, 'Bearer [REDACTED]'],
  [/Authorization:\s*[^\s]+/gi, 'Authorization: [REDACTED]'],
  [/Set-Cookie:[^\n]+/gi, 'Set-Cookie: [REDACTED]'],
  [/eyJ[A-Za-z0-9._\-]+/g, '[JWT_REDACTED]'],
  [/\b\d{16}\b/g, '[CARD_REDACTED]'],
];

export function scrub(body: string): string {
  let out = body;
  for (const [re, rep] of PATTERNS) out = out.replace(re, rep);
  return out;
}
