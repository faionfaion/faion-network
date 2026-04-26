# YAML Frontmatter Checklist

Step-by-step guide for adding and validating YAML frontmatter in SDD documents.

---

## Pre-Flight Checklist

Before writing frontmatter, confirm:

- [ ] Document type identified (spec, design, task, etc.)
- [ ] Required fields list available (see [templates.md](templates.md))
- [ ] Project conventions checked (constitution.md)
- [ ] Date in ISO format ready (YYYY-MM-DD)

---

## Writing Frontmatter

### Step 1: Start with Delimiters

```yaml
---

---
```

Place at the **very top** of the file. Nothing should precede it (no whitespace, no BOM).

### Step 2: Add Required Fields

Check document type and add required fields:

| Document Type | Required Fields |
|---------------|-----------------|
| constitution | type, version, status, created, updated, author |
| roadmap | type, version, status, created, updated |
| spec | type, feature_id, version, status, priority, created, updated |
| design | type, feature_id, version, status, created, updated |
| implementation-plan | type, feature_id, version, status, created, updated |
| task | type, task_id, feature_id, status, priority, created |
| methodology | type, id, title, category, difficulty |

### Step 3: Add Optional Fields

Based on document needs:

- [ ] `depends_on` - List of dependencies
- [ ] `blocks` - List of blocked items
- [ ] `tags` - Classification tags
- [ ] `author` - Document author
- [ ] `language` - Content language (en, uk)

### Step 4: Quote Sensitive Values

Always quote:

- [ ] Version numbers: `version: "1.0.0"`
- [ ] IDs with special chars: `feature_id: "02-landing-page"`
- [ ] Values starting with special YAML chars: `title: "--- Introduction"`

### Step 5: Validate Syntax

Check for common YAML errors:

- [ ] No tabs (use spaces only)
- [ ] Consistent indentation (2 spaces recommended)
- [ ] Colons followed by space: `key: value`
- [ ] Arrays properly formatted: `tags: [a, b, c]` or multiline
- [ ] Dates unquoted: `created: 2026-01-25`

---

## Validation Checklist

### Syntax Validation

- [ ] Valid YAML (use online validator if unsure)
- [ ] Proper delimiter placement (`---` on own lines)
- [ ] No trailing spaces after values
- [ ] Proper escaping of special characters

### Schema Validation

- [ ] All required fields present
- [ ] Field types correct (string, number, date, array)
- [ ] Enum values valid (status, priority, difficulty)
- [ ] Version follows semver format (X.Y.Z)
- [ ] Date follows ISO format (YYYY-MM-DD)

### Semantic Validation

- [ ] `type` matches document purpose
- [ ] `feature_id` matches folder name
- [ ] `task_id` follows naming convention
- [ ] `status` reflects actual state
- [ ] `priority` appropriate for context
- [ ] `depends_on` references valid IDs

---

## Status Values Reference

### Document Status

| Status | When to Use |
|--------|-------------|
| `draft` | Work in progress |
| `review` | Under review |
| `approved` | Approved, ready for use |
| `active` | Currently in use |
| `final` | Finalized |
| `archived` | No longer active |

### Feature/Task Status

| Status | When to Use |
|--------|-------------|
| `backlog` | Not yet scheduled |
| `todo` | Scheduled for work |
| `in-progress` | Currently working |
| `done` | Completed |
| `blocked` | Waiting on dependency |

---

## Priority Values Reference

| Priority | Meaning | Use Case |
|----------|---------|----------|
| `P0` | Blocker | Must be done first |
| `P1` | Critical | High business value |
| `P2` | Nice-to-have | Can be deferred |

---

## Version Increment Guide

| Change Type | Action | Example |
|-------------|--------|---------|
| Breaking change | Bump MAJOR | 1.0.0 -> 2.0.0 |
| New section added | Bump MINOR | 1.0.0 -> 1.1.0 |
| Typo/small fix | Bump PATCH | 1.0.0 -> 1.0.1 |

---

## Quick Validation Commands

### Python (python-frontmatter)

```bash
python -c "import frontmatter; print(frontmatter.load('doc.md').keys())"
```

### Node.js (gray-matter)

```bash
npx gray-matter doc.md --json | jq '.data'
```

### YAML Syntax Only

```bash
head -n 20 doc.md | sed '1d;/^---$/,$d' | python -c "import yaml,sys; yaml.safe_load(sys.stdin)"
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| `version: 1.0.0` | Parsed as number | `version: "1.0.0"` |
| `date: 01-25-2026` | Invalid format | `date: 2026-01-25` |
| `tags: a, b, c` | Invalid YAML | `tags: [a, b, c]` |
| Tab indentation | YAML error | Use 2 spaces |
| `key:value` | Missing space | `key: value` |
| Empty frontmatter | No metadata | Add required fields |

---

## Migration Checklist

When migrating from inline metadata to frontmatter:

1. [ ] Identify existing metadata in document
2. [ ] Map to frontmatter fields
3. [ ] Create frontmatter block at top
4. [ ] Remove inline metadata section
5. [ ] Validate new frontmatter
6. [ ] Update document title (if duplicated)
7. [ ] Test with parsers/tools

---

## Integration Checklist

### For Static Site Generators

- [ ] Frontmatter fields match template expectations
- [ ] Required fields for layouts present
- [ ] Dates parseable by SSG
- [ ] Taxonomies/tags properly formatted

### For CI/CD Validation

- [ ] Schema file created/updated
- [ ] Validation action configured
- [ ] All content files pass validation
- [ ] Error messages actionable

### For LLM Processing

- [ ] Document type clearly specified
- [ ] Status accurately reflects state
- [ ] Dependencies explicit
- [ ] No ambiguous values

---

## Review Checklist

Before committing document with frontmatter:

- [ ] Required fields complete
- [ ] Status accurate
- [ ] Version appropriate
- [ ] Dates current
- [ ] Dependencies valid
- [ ] No syntax errors
- [ ] Schema validation passes
- [ ] Renders correctly in target system

---

*yaml-frontmatter/checklist.md v1.0.0 - 2026-01-25*
