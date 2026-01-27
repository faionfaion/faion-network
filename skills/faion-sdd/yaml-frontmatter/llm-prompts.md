# LLM Prompts for YAML Frontmatter

Effective prompts for LLM-assisted frontmatter generation, validation, and migration.

---

## Generation Prompts

### Generate SDD Specification

```
Generate a spec.md file for {FEATURE_NAME} with proper YAML frontmatter.

Requirements:
- Feature ID: "{NNN}-{feature-name}"
- Status: backlog
- Priority: P1
- Include depends_on array (empty or with dependencies)

Frontmatter must include:
- type: spec
- feature_id
- version: "1.0.0"
- status
- priority
- created: {TODAY_DATE}
- updated: {TODAY_DATE}

After frontmatter, include sections:
- Overview
- Problem Statement
- Requirements (FR-1, FR-2, etc.)
- Success Criteria
- Out of Scope
```

### Generate Design Document

```
Generate a design.md for feature "{FEATURE_ID}" based on this specification:

{PASTE_SPEC_CONTENT}

Frontmatter must include:
- type: design
- feature_id: "{FEATURE_ID}"
- version: "1.0.0"
- status: draft
- created: {TODAY_DATE}
- updated: {TODAY_DATE}
- spec_version: "1.0.0"

Include sections:
- Architecture Overview
- Component Design
- Data Model
- API Contracts
- Security Considerations
- Testing Strategy
```

### Generate Implementation Plan

```
Generate an implementation-plan.md for feature "{FEATURE_ID}" based on this design:

{PASTE_DESIGN_CONTENT}

Frontmatter must include:
- type: implementation-plan
- feature_id: "{FEATURE_ID}"
- version: "1.0.0"
- status: draft
- created: {TODAY_DATE}
- updated: {TODAY_DATE}
- design_version: "1.0.0"
- total_tasks: {CALCULATED_COUNT}

Include:
- Task breakdown (WBS)
- Dependency graph
- Wave-based parallelization
- Files to change per task
- Estimated tokens per task (no time estimates)
```

### Generate Task File

```
Generate a task file TASK_{NNN}_{slug}.md for this work:

Feature: {FEATURE_ID}
Task Description: {TASK_DESCRIPTION}
Priority: {P0|P1|P2}

Frontmatter must include:
- type: task
- task_id: "TASK_{NNN}"
- feature_id: "{FEATURE_ID}"
- status: todo
- priority: {PRIORITY}
- created: {TODAY_DATE}
- depends_on: [{DEPENDENCIES}]
- blocks: [{BLOCKED_BY_THIS}]
- complexity: {low|medium|high}
- estimated_tokens: {NUMBER}

Include sections:
- SDD References (links to spec, design)
- Requirements Coverage (FR-X)
- Acceptance Criteria (Given-When-Then)
- Files to Change (CREATE/MODIFY table)
- Subtasks (numbered checkboxes)
- Implementation (empty, filled during work)
- Summary (empty, filled after completion)
```

### Generate Blog Post Frontmatter

```
Generate MDX frontmatter for a blog post about: {TOPIC}

Include:
- type: blog-post
- title: "{COMPELLING_TITLE}"
- slug: {kebab-case-slug}
- description: "{SEO-OPTIMIZED_DESCRIPTION}" (150-160 chars)
- pubDate: {TODAY_DATE}
- author: {AUTHOR_NAME}
- tags: [{RELEVANT_TAGS}] (3-5 tags)
- category: {CATEGORY}
- readingTime: {ESTIMATED_MINUTES}
- draft: true
- featured: false
- image.src: /images/blog/{suggested-image-name}.png
- image.alt: "{DESCRIPTIVE_ALT_TEXT}"

SEO section:
- seo.title: "{TITLE} | {SITE_NAME}" (under 60 chars)
- seo.description: "{META_DESCRIPTION}" (150-160 chars)
- seo.keywords: [{KEYWORDS}]
```

### Generate Methodology Frontmatter

```
Generate frontmatter for a methodology document about: {METHODOLOGY_TOPIC}

Determine:
- id: {kebab-case-id} (e.g., "chain-of-thought-prompting")
- title: "{Human Readable Title}"
- category: {SDD|Development|DevOps|ML|Marketing|Product|BA|UX|PM}
- difficulty: {beginner|intermediate|advanced}
- tags: [{relevant}, {technical}, {tags}]
- read_time_minutes: {ESTIMATED_BASED_ON_CONTENT}

If advanced, include:
- prerequisites: [{required-methodologies}]
- related: [{related-methodologies}]
```

---

## Validation Prompts

### Validate Frontmatter Against Schema

```
Validate this frontmatter against SDD standards:

```yaml
{PASTE_FRONTMATTER}
```

Check:
1. All required fields for type "{TYPE}" are present
2. Field types are correct (string, number, date, array)
3. Enum values are valid (status, priority, difficulty)
4. Version follows semver format (X.Y.Z)
5. Dates follow ISO format (YYYY-MM-DD)
6. Arrays are properly formatted
7. No YAML syntax errors

Report:
- Missing fields
- Invalid values
- Suggested fixes
```

### Validate Task Dependencies

```
Validate task dependencies in this frontmatter:

```yaml
{PASTE_FRONTMATTER}
```

Given these existing tasks:
{LIST_OF_TASK_IDS}

Check:
1. depends_on references valid task IDs
2. blocks references valid task IDs
3. No circular dependencies
4. Dependencies are logically correct
```

### Check Frontmatter Consistency

```
Check frontmatter consistency across these documents:

Spec:
```yaml
{SPEC_FRONTMATTER}
```

Design:
```yaml
{DESIGN_FRONTMATTER}
```

Implementation Plan:
```yaml
{IMPL_PLAN_FRONTMATTER}
```

Verify:
1. feature_id matches across all documents
2. spec_version in design matches spec version
3. design_version in impl-plan matches design version
4. Status progression is logical
5. Dates are consistent (created <= updated)
```

---

## Migration Prompts

### Migrate Inline Metadata to Frontmatter

```
Convert this document with inline metadata to proper YAML frontmatter:

```markdown
{PASTE_DOCUMENT}
```

Rules:
1. Extract all metadata from ## Metadata section or similar
2. Map to appropriate frontmatter fields based on document type
3. Add any missing required fields with sensible defaults
4. Remove the inline metadata section from body
5. Ensure proper YAML formatting
6. Keep document title as first heading after frontmatter
```

### Batch Migrate Multiple Files

```
Generate a migration script for converting these files to frontmatter format:

File patterns: {GLOB_PATTERN}
Document type: {TYPE}
Default values:
- status: draft
- author: {DEFAULT_AUTHOR}

Script should:
1. Read each matching file
2. Detect existing metadata (inline or partial frontmatter)
3. Generate proper frontmatter
4. Preserve document content
5. Write back with frontmatter
6. Report any files that couldn't be migrated
```

### Upgrade Frontmatter Schema

```
Upgrade frontmatter from schema v1 to v2:

Old format (v1):
```yaml
{OLD_FRONTMATTER}
```

New schema changes:
- Rename "date" to "created"
- Add "updated" field (copy from "date" if missing)
- Change "status" values: "wip" -> "draft", "complete" -> "done"
- Add "type" field based on file location/naming
- Convert "tags" from comma-separated to array

Generate:
1. New frontmatter
2. Explanation of changes
```

---

## Transformation Prompts

### Extract Frontmatter to JSON

```
Extract frontmatter from this markdown file and output as JSON:

```markdown
{PASTE_MARKDOWN}
```

Output format:
{
  "frontmatter": { ... },
  "content_preview": "first 200 chars of content",
  "word_count": N,
  "has_code_blocks": true/false
}
```

### Generate Frontmatter from Content

```
Analyze this markdown content and generate appropriate frontmatter:

```markdown
{PASTE_CONTENT_WITHOUT_FRONTMATTER}
```

Infer:
- type (based on content structure and keywords)
- title (from first heading or content summary)
- tags (from content topics)
- difficulty (based on technical depth)
- reading time (based on word count)

Generate complete frontmatter with inferred values.
```

### Normalize Inconsistent Frontmatter

```
Normalize this frontmatter to follow SDD standards:

```yaml
{PASTE_INCONSISTENT_FRONTMATTER}
```

Apply:
1. Standardize field names (created_at -> created)
2. Fix date formats (all to YYYY-MM-DD)
3. Standardize status values to SDD enum
4. Quote version numbers
5. Convert string tags to array
6. Add missing required fields with defaults
7. Remove deprecated/unknown fields
```

---

## Query Prompts

### Generate Collection Query

```
Generate an Astro content collection query for:

Collection: {COLLECTION_NAME}
Filter by: {FILTER_CRITERIA}
Sort by: {SORT_FIELD}
Limit: {N}

Query should:
1. Get entries from collection
2. Apply filters based on frontmatter fields
3. Sort by specified field (descending)
4. Limit results
5. Return typed data
```

### Find Documents by Criteria

```
Given these frontmatter extracts from multiple files:

{LIST_OF_FRONTMATTER_OBJECTS}

Find all documents where:
- status = "{STATUS}"
- priority = "{PRIORITY}"
- created >= {DATE}

Return:
- Matching document IDs
- Their key frontmatter fields
- Total count
```

---

## Schema Generation Prompts

### Generate Zod Schema from Examples

```
Generate a Zod schema based on these frontmatter examples:

Example 1:
```yaml
{EXAMPLE_1}
```

Example 2:
```yaml
{EXAMPLE_2}
```

Example 3:
```yaml
{EXAMPLE_3}
```

Generate:
1. TypeScript Zod schema
2. All required vs optional fields
3. Appropriate Zod types
4. Default values where sensible
5. String validations (max length, patterns)
6. Enum values from examples
```

### Generate JSON Schema

```
Generate a JSON Schema for document type "{TYPE}" with these requirements:

Required fields:
{LIST_REQUIRED_FIELDS}

Optional fields:
{LIST_OPTIONAL_FIELDS}

Constraints:
- version: semver pattern
- status: enum [{STATUS_VALUES}]
- dates: ISO format
- priority: enum [P0, P1, P2]

Output complete JSON Schema draft-07.
```

---

## Debugging Prompts

### Fix YAML Syntax Error

```
Fix the YAML syntax error in this frontmatter:

```yaml
{PASTE_BROKEN_YAML}
```

Error message: {ERROR_MESSAGE}

Provide:
1. Identified error
2. Fixed YAML
3. Explanation of what was wrong
```

### Explain Parsing Failure

```
This frontmatter fails to parse with gray-matter:

```yaml
{PASTE_FRONTMATTER}
```

Error: {ERROR}

Explain:
1. Why parsing failed
2. Which line/character caused the issue
3. How to fix it
4. Best practices to avoid this in future
```

---

## Prompt Best Practices

### For Claude

1. **Be explicit about frontmatter structure** - Show the exact format expected
2. **Provide context** - Include document type, project context
3. **Use templates** - Reference templates.md for consistency
4. **Request validation** - Ask Claude to validate after generation

### For GPT-4

1. **System prompt** - Set frontmatter expert role
2. **Few-shot examples** - Provide 2-3 good examples
3. **JSON mode** - Use for extraction tasks
4. **Structured output** - Request specific format

### For Copilot

1. **Comment-driven** - Start with comment describing frontmatter
2. **Template starter** - Begin with `---` and let it complete
3. **Context window** - Keep related files open
4. **Accept suggestions** - Copilot learns from accepted completions

---

*yaml-frontmatter/llm-prompts.md v1.0.0 - 2026-01-25*
