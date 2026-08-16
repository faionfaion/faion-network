# Puppeteer Output Capture (Screenshots, PDFs, HAR)

## Summary

**One-sentence:** Produces a Puppeteer capture script that takes screenshots (jpeg/webp quality 80 for high volume), PDFs (printBackground true + waitForSelector before pdf), and HAR (with secret scrubber).

**One-paragraph:** Capturing artifacts from Puppeteer has a small set of recurring traps: PDF generation called before the page finished rendering, screenshots wasting storage by defaulting to PNG, and HAR files leaking session tokens. This methodology produces a capture module exposing screenshot(page, opts), pdf(page, opts), and har(page, opts) — each enforcing the correct defaults: jpeg/webp quality 80 for bulk pipelines, printBackground=true + waitForSelector anchor for PDFs, and HAR piped through a secret scrubber before persistence.

**Ефективно для:**

- Bulk screenshot pipeline storing/transmitting many images (size matters).
- PDF generation from rendered dashboards or invoices.
- HAR capture for downstream replay or audit.
- Adding consistent artifact discipline to an existing worker.

## Applies If (ALL must hold)

- Worker uses Puppeteer 22+ with the new headless mode.
- Output artifacts are persisted to disk or object storage.
- Volume is high enough that PNG > JPEG cost difference matters.
- PDF/HAR outputs may contain secrets that need scrubbing.

## Skip If (ANY kills it)

- One-off debugging screenshots in dev; defaults are fine.
- Visual-regression testing where lossless PNG is required (use playwright-automation with toHaveScreenshot).
- Targets that already export PDFs server-side — let the backend do it.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Output type | screenshot | pdf | har | task brief |
| Volume estimate | low | medium | high | ops capacity plan |
| Secrets policy | scrub patterns + retention rules | secret policy |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[puppeteer-launch-setup]] | the page handed in came from the safe launch wrapper |
| [[puppeteer-agent-workflow]] | artifacts get scrubbed before persistence |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure | 900 |
| `content/06-decision-tree.xml` | essential | Routing tree → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-capture-format` | haiku | lookup by output type + volume |
| `emit-capture-module` | sonnet | render screenshot/pdf/har helpers with correct defaults |
| `verify-scrubber` | haiku | scan HAR persistence path for direct write without scrub |

## Templates

| File | Purpose |
|------|---------|
| `templates/capture.ts` | Capture helpers: screenshot, pdf, har with safe defaults |
| `templates/scrubber.ts` | Regex scrubber for HAR and log bodies |
| `templates/artefact.json` | Sample artefact metadata for validator |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-puppeteer-output-capture.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; agent self-check |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[puppeteer-agent-workflow]]
- [[puppeteer-launch-setup]]
- [[puppeteer-page-interaction]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, environment context, risk level) to a concrete conclusion, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which rule applies to the current context.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/capture.ts`

```typescript
import { Page } from 'puppeteer';
import fs from 'node:fs';

export async function screenshot(page: Page, outPath: string, opts: { fullPage?: boolean } = {}) {
  await page.screenshot({
    path: outPath,
    type: 'jpeg',
    quality: 80,
    fullPage: opts.fullPage ?? false,
  });
}

export async function pdf(page: Page, anchorSelector: string, outPath: string) {
  await page.waitForSelector(anchorSelector);
  await page.evaluate(() => (document as any).fonts?.ready);
  await page.pdf({
    path: outPath,
    printBackground: true,
    preferCSSPageSize: true,
    format: 'A4',
  });
}
```

### `templates/scrubber.ts`

```typescript
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
```

### `templates/artefact.json`

```json
{
  "output_type": "mixed",
  "screenshot_format": "jpeg",
  "screenshot_quality": 80,
  "pdf_print_background": true,
  "uses_correct_format": true,
  "applies_scrub": true,
  "waits_before_pdf": true,
  "bounded_artifact_path": true,
  "artifact_dir": "/tmp/agent-run/job-42"
}
```
