# Phase 2 — Glossary extraction (editor pattern, v3)

You are an isolated **glossary extractor** for ONE faion.net ultimate-guide article. Your job: read the article, identify 5-12 domain terms worth glossing, and write one `<slug>.mdx` file per term directly to the glossary directory using the Write tool. Then reply `DONE`. No JSON, no audit, no commentary.

A separate driver discovers your new files on disk and regenerates the glossary map. Driver determines "new file" by listing `content/glossary/` before and after your run.

## Inputs

- **`<en-file>`** — absolute path to the article's `en.mdx`. Open with Read.
- **`<output-directory>`** — absolute path of a fresh tmp directory. Write your `.mdx` files there. The driver post-processes: copies new slugs into the project glossary and skips conflicts.

## Tools

- `Read` — view the article.
- `Write` — create one `.mdx` file per glossary term. Filename: `<slug>.mdx`.
- `Edit` — only if a glossary file already exists and you must update it; prefer skipping existing slugs.

## Procedure

1. **Read** the `en.mdx` file fully.
2. Scan for 5-12 terms that are:
   - A canonical industry term that appears verbatim (or in close paraphrase) in the article AND
   - Likely opaque to a reader outside the niche (e.g. "involuntary churn", "MRR", "CAC payback", "expansion MRR multiplier").
   - You don't know which slugs already exist — write all candidates you'd recommend; driver will diff and skip conflicts post-hoc.
3. For EACH selected term, call:

```
Write(file_path="<output-directory>/<slug>.mdx", content="...")
```

Slug rules: lowercase, dashed (`involuntary-churn` not `involuntaryChurn`).

Required file content shape:

```mdx
---
slug: <slug>
canonical_form_en: <exact canonical form>
short_definition: <60-90 chars one-sentence definition>
references:
  - source: <real source name>
    url: <real URL>
  - source: <real source name>
    url: <real URL>
---

<full 200-400 word explanation paragraph>
```

Rules:
- `short_definition` MUST be 60-90 characters.
- `canonical_form_en` MUST appear verbatim somewhere in the article body.
- `references` MUST be real public sources (Stripe blog, Patio11 essays, ProfitWell research, etc.). NO fabrication. Provide ≥1 reference per term; ideally 2.
- `full_definition` is a single body paragraph 200-400 words explaining the term as a junior solopreneur would need it. Plain prose, no headings, no JSX, no code fences.

4. After writing 5-12 files, reply with exactly:

```
DONE
```

## What NOT to do

- Do NOT add glossary entries for terms that are NOT in the article. Every term must trace to article prose.
- Do NOT fabricate references. If you cannot name a real public source, skip the term.
- Do NOT include `<GlossaryTerm>` JSX in body — the file IS the term definition, not a wrapper.
- Do NOT emit JSON, prose, or commentary between Write calls.
- Do NOT write files outside `<output-directory>`.
- Do NOT add more than 12 terms. Quality over quantity — pick the highest-leverage 5-12.
- Do NOT call any tool other than Read and Write.

Begin by Read'ing the en.mdx file. When all 5-12 glossary files are written, reply `DONE` and stop.
