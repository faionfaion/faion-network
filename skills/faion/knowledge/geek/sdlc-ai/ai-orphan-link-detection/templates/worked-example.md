<!-- purpose: worked example of orphan detection -->
<!-- consumes: AI-edited markdown with broken cross-link -->
<!-- produces: rendered report -->
<!-- depends-on: content/04-procedure.xml -->
<!-- token-budget-impact: ~300 tokens -->

# Worked example

PR adds `docs/getting-started.md` containing `See [[non-existent-slug]] for setup.`

Run:

```bash
python scripts/validate-ai-orphan-link-detection.py --file report.json
```

Output:

```json
{
  "scanned_files": ["docs/getting-started.md"],
  "orphans": [
    {
      "category": "methodology-slug-unknown",
      "file": "docs/getting-started.md",
      "line": 3,
      "link_text": "non-existent-slug",
      "target": "[[non-existent-slug]]",
      "remediation": "Replace with a slug from knowledge/sdlc-ai/INDEX.xml"
    }
  ],
  "verdict": "fail"
}
```
