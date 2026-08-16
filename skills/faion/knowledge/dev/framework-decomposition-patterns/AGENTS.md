# Framework Decomposition Patterns

## Summary

**One-sentence:** Cap framework files at 150-200 lines per type via extraction patterns (service layer, selectors, DTOs, query objects, actions, custom hooks) so a single LLM Read fits in &lt;20K tokens.

**One-paragraph:** Fat controllers and God models are the LLM-context killer of legacy codebases. A 500-line Django view forces a coding agent to load 50K tokens to make a 2-line edit; the agent then mis-references, drops imports, and slows. The fix is per-framework decomposition: extract the right pattern (service layer for Rails / Django, query objects + selectors for React, DTOs for Laravel, actions + hooks for SPA frontends). This methodology produces a decomposition report per fat file: current LoC, proposed extraction pattern, target LoC after, AI-context savings, and the test set that proves equivalence. The script `find-fat-files.sh` surfaces candidates; the JS variant `find-fat-components.mjs` does the same for React.

**Ефективно для:**

- Solo dev preparing a legacy codebase for Claude Code / Cursor — files over 200 lines defeat AI-pair coding.
- Refactor sprint targeting LLM-context efficiency rather than micro-perf.
- Onboarding LLM agent into a fat-model Rails / Django repo.
- DRY audit: surface candidates whose churn justifies the decomposition.

## Applies If (ALL must hold)

- Existing codebase using Django, Rails, Laravel, React (or close equivalents).
- One or more files exceed 150 lines AND change-frequency is non-trivial (≥5 commits in 90 days).
- LLM-assisted dev is part of the workflow OR planned.
- Test coverage exists OR characterization tests will be added (see `characterization-test-recipes`).

## Skip If (ANY kills it)

- Tiny scripts, one-off Lambdas, files already under 100 lines.
- Prototypes being thrown away weekly (YAGNI).
- Frameworks with opinionated structure already enforcing the boundary (Phoenix contexts, NestJS modules).
- Microservices where one service = one concern; extra layers duplicate boundaries.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target file path(s) | string | `find-fat-files.sh` output |
| Framework | string | repo config |
| Change-frequency data | git log | repo |
| Test coverage (or characterization plan) | report / plan | tests/ + roadmap |
| AI-context budget target | tokens | team handbook |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `solo/dev/characterization-test-recipes` | Pre-refactor safety net for behavior-preserving decomposition. |
| `solo/dev/context-window-curation-for-coding-agents` | Downstream: bounded files feed bounded context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 14 rules: per-framework patterns, LoC caps, naming, run + skip | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the decomposition report + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: extract-then-re-merge, wrong-pattern-per-framework, untested-refactor, LoC-only metric | 700 |
| `content/04-procedure.xml` | medium | 5-step procedure: identify → choose-pattern → write-characterization → extract → verify | 700 |
| `content/06-decision-tree.xml` | essential | Tree: framework? file-type? recommended pattern → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `find-fat-files` | haiku | Mechanical LoC + change-freq scan. |
| `propose-pattern` | sonnet | Bounded judgment: which extraction pattern fits this fat file. |
| `verify-equivalence` | sonnet | Run characterization tests; compare pre/post. |

## Templates

| File | Purpose |
|------|---------|
| `templates/framework-decomposition-patterns.json` | JSON Schema for the decomposition report. |
| `templates/find-fat-files.sh` | Bash helper to surface fat files by LoC + change-freq. |
| `templates/find-fat-components.mjs` | JS helper to surface fat React components by LoC + jsx-depth. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-framework-decomposition-patterns.py` | Validate a decomposition report against the schema + pattern-framework consistency. | After proposal; before extraction. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[characterization-test-recipes]] — safety net for the extraction.
- [[context-window-curation-for-coding-agents]] — bounded files = bounded context.
- [[tech-debt-management]] — sibling for picking which fat files to fix first.

## Decision tree

See `content/06-decision-tree.xml`. The tree first determines the framework (django / rails / laravel / react / generic). It then routes the fat-file type (view / controller / model / component / route) to the recommended extraction pattern. Then verifies test coverage exists OR characterization-test plan attached. Leaves emit `propose-extraction`, `block-no-coverage`, or `block-pattern-not-applicable`. Each leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/framework-decomposition-patterns.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/framework-decomposition-patterns.json",
  "type": "object",
  "required": [
    "artefact_id",
    "file_path",
    "framework",
    "file_type",
    "current_loc",
    "proposed_pattern",
    "target_loc",
    "coverage_or_plan",
    "verdict",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^fdp-[a-z0-9-]{6,}$"
    },
    "file_path": {
      "type": "string",
      "minLength": 1
    },
    "framework": {
      "enum": [
        "django",
        "rails",
        "laravel",
        "react",
        "nextjs",
        "generic"
      ]
    },
    "file_type": {
      "enum": [
        "view",
        "controller",
        "model",
        "component",
        "route",
        "service",
        "form"
      ]
    },
    "current_loc": {
      "type": "integer",
      "minimum": 100
    },
    "proposed_pattern": {
      "enum": [
        "service-layer",
        "selector",
        "dto",
        "query-object",
        "action",
        "custom-hook",
        "extract-helper",
        "split-by-domain"
      ]
    },
    "target_loc": {
      "type": "integer",
      "minimum": 1,
      "maximum": 200
    },
    "coverage_or_plan": {
      "type": "string",
      "minLength": 5
    },
    "ai_context_savings_tokens": {
      "type": "integer",
      "minimum": 0
    },
    "verdict": {
      "enum": [
        "propose-extraction",
        "block-no-coverage",
        "block-pattern-not-applicable",
        "skip-already-small"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    }
  }
}
```

### `templates/find-fat-files.sh`

```bash
# find-fat-files.sh — top-20 longest Python app files (excludes tests/migrations)
# Usage: ./find-fat-files.sh [repo-path]
cd "${1:-.}"
git ls-files '*.py' | grep -Ev 'tests?/|migrations?/' \
  | xargs wc -l 2>/dev/null | sort -rn | head -20
```

### `templates/find-fat-components.mjs`

```javascript
// find-fat-components.mjs — list React components over 150 LOC for hook extraction
// Usage: node find-fat-components.mjs [src-dir]
// Output: LOC and file path, sorted descending

import { readFileSync } from 'node:fs';
import { globSync } from 'glob';

const srcDir = process.argv[2] || 'src';
const threshold = 150;

const results = [];
for (const f of globSync(`${srcDir}/**/*.{tsx,jsx}`)) {
  const loc = readFileSync(f, 'utf8').split('\n').length;
  if (loc > threshold) results.push({ loc, file: f });
}
results.sort((a, b) => b.loc - a.loc);
for (const { loc, file } of results) console.log(loc, file);
```
