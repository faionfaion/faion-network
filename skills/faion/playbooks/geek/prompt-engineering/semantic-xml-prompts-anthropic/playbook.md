---
name: semantic-xml-prompts-anthropic
description: Structure Anthropic prompts with semantic XML tags, Jinja2 templates, and SemVer versioning so Claude parses intent unambiguously at scale.
tier: geek
group: prompt-engineering
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a versioned, Jinja2-templated XML prompt system for Claude that uses Anthropic's recommended tag vocabulary (`<role>`, `<context>`, `<instructions>`, `<examples>`, `<task>`, `<output_format>`), applies SemVer so output-schema changes trigger a major bump, and ships a real working Python call verified against `claude-sonnet-4-6`.

## Prerequisites

- Python 3.11+, `pip install anthropic>=0.51 jinja2>=3.1 pydantic>=2.0`.
- `ANTHROPIC_API_KEY` exported in the environment.
- Familiarity with the Anthropic Messages API shape (`system` string + `messages` list).
- Read [semantic-xml-content](../../../knowledge/geek/ai/llm-integration/semantic-xml-content) to understand why XML tags carry structural meaning for Claude beyond mere formatting.
- Optional but useful: [prompt-techniques](../../../knowledge/geek/ai/llm-integration/prompt-techniques) for versioning and A/B testing background.

## Steps

1. **Understand why XML beats Markdown in long prompts.**

   Claude's training data contains XML-tagged documents (code, structured APIs, internal tooling). Tags create unambiguous scope boundaries. A heading like `## Instructions` can appear inside quoted user content and confuse the model; `<instructions>` cannot — Claude treats the tag as a structural delimiter, not content. The gain is most visible above ~500 tokens where Markdown headings blur into prose. Anthropic's prompt-engineering guide explicitly recommends XML for complex prompts with multiple sections.

2. **Establish the canonical six-tag vocabulary.**

   | Tag | Role in prompt | Notes |
   |-----|---------------|-------|
   | `<role>` | Persona / behavioral contract | One per system prompt; sets tone and authority |
   | `<context>` | Background the model needs but shouldn't invent | Dynamic: inject per-request data here |
   | `<instructions>` | Ordered steps / rules | Numbering inside the tag is fine |
   | `<examples>` | Few-shot demonstrations | Each wrapped in `<example>` child tag |
   | `<task>` | The specific request for this call | Keep concise; context lives above |
   | `<output_format>` | Schema + constraints on the reply | JSON schema, field names, length limits |

   Tags nest: `<examples><example>...</example></examples>`. Do not invent new top-level tags — Claude treats unrecognised tags as opaque delimiters, which is fine, but canonical tags carry training-time signal.

3. **Create the prompt template file** using Jinja2.

   ```
   mkdir -p prompts/v1
   ```

   Write `prompts/v1/classify_issue.xml.j2`:

   ```xml
   <role>
   You are a senior support triage engineer. You classify incoming GitHub issues into exactly one category and assign a severity score. You never refuse to classify; you always return valid JSON.
   </role>

   <context>
   Repository: {{ repo_name }}
   Open issue count: {{ open_count }}
   Labels available: {{ labels | join(", ") }}
   </context>

   <instructions>
   1. Read the issue title and body in <task>.
   2. Choose the best-fit category from: bug, feature-request, question, docs, security.
   3. Assign severity 1 (critical) – 5 (trivial) based on user impact.
   4. If severity is 1 or 2, set escalate to true.
   5. Return only the JSON object described in <output_format>. No prose.
   </instructions>

   <examples>
   <example>
   <input>Title: Login fails with 500 on password reset | Body: Happens every time for all users since deploy 2.4.1.</input>
   <output>{"category": "bug", "severity": 1, "escalate": true, "summary": "Login broken for all users post-deploy"}</output>
   </example>
   <example>
   <input>Title: Add dark mode toggle | Body: Would be nice to have.</input>
   <output>{"category": "feature-request", "severity": 4, "escalate": false, "summary": "Dark mode toggle requested"}</output>
   </example>
   </examples>

   <task>
   Title: {{ issue_title }}
   Body: {{ issue_body }}
   </task>

   <output_format>
   Return a single JSON object with exactly these keys:
   - category: string, one of bug | feature-request | question | docs | security
   - severity: integer 1–5
   - escalate: boolean
   - summary: string, ≤80 chars, action-leading
   No markdown fences, no trailing text.
   </output_format>
   ```

4. **Define the output schema with Pydantic v2.**

   ```python
   # schemas/v1.py
   from pydantic import BaseModel, Field
   from typing import Literal

   PROMPT_VERSION = "1.0.0"

   class IssueClassification(BaseModel):
       category: Literal["bug", "feature-request", "question", "docs", "security"]
       severity: int = Field(ge=1, le=5)
       escalate: bool
       summary: str = Field(max_length=80)
   ```

5. **Write the prompt loader with version tracking.**

   ```python
   # prompts/loader.py
   import json
   from pathlib import Path
   from jinja2 import Environment, FileSystemLoader
   import anthropic
   from schemas.v1 import IssueClassification, PROMPT_VERSION

   PROMPTS_DIR = Path(__file__).parent
   _env = Environment(loader=FileSystemLoader(str(PROMPTS_DIR)), autoescape=False)


   def render_classify_issue(
       repo_name: str,
       open_count: int,
       labels: list[str],
       issue_title: str,
       issue_body: str,
       prompt_version: str = PROMPT_VERSION,
   ) -> str:
       """Render the versioned XML prompt for issue classification."""
       major = prompt_version.split(".")[0]
       template = _env.get_template(f"v{major}/classify_issue.xml.j2")
       return template.render(
           repo_name=repo_name,
           open_count=open_count,
           labels=labels,
           issue_title=issue_title,
           issue_body=issue_body,
       )


   def classify_issue(
       repo_name: str,
       open_count: int,
       labels: list[str],
       issue_title: str,
       issue_body: str,
   ) -> IssueClassification:
       client = anthropic.Anthropic()
       system_prompt = render_classify_issue(
           repo_name=repo_name,
           open_count=open_count,
           labels=labels,
           issue_title=issue_title,
           issue_body=issue_body,
       )
       response = client.messages.create(
           model="claude-sonnet-4-6",
           max_tokens=256,
           system=system_prompt,
           messages=[{"role": "user", "content": "Classify the issue."}],
       )
       raw = response.content[0].text.strip()
       data = json.loads(raw)
       return IssueClassification(**data)
   ```

6. **Apply SemVer to the prompt itself.**

   Treat each `classify_issue.xml.j2` as a versioned artifact:

   | Change type | Bump | Example |
   |-------------|------|---------|
   | New tag or rename a key in `<output_format>` | **major** (output schema changed; callers must update Pydantic model) | `1.x.x` → `2.0.0`, create `prompts/v2/` |
   | New `<example>`, reword `<instructions>`, expand `<context>` fields | **minor** (semantics improved, output schema unchanged) | `1.0.x` → `1.1.0` |
   | Typo fix, punctuation, whitespace | **patch** | `1.0.0` → `1.0.1` |

   Track the version in `schemas/v1.py` as `PROMPT_VERSION = "1.0.0"`. When you bump major, create `schemas/v2.py` + `prompts/v2/classify_issue.xml.j2` and update the loader. Old callers stay on v1 until they opt in.

7. **Run the working end-to-end call.**

   ```python
   # run.py
   from prompts.loader import classify_issue

   result = classify_issue(
       repo_name="acme/platform",
       open_count=47,
       labels=["bug", "enhancement", "security", "docs"],
       issue_title="SQL injection in user search endpoint",
       issue_body=(
           "The /api/users?q= parameter is not sanitised. "
           "Tested: /api/users?q=1' OR '1'='1 returns all rows. "
           "Discovered in staging during pentest 2026-04-30."
       ),
   )
   print(result.model_dump_json(indent=2))
   ```

   Expected output shape:

   ```json
   {
     "category": "security",
     "severity": 1,
     "escalate": true,
     "summary": "SQL injection in user search allows full table dump"
   }
   ```

## Verify

Run the script and confirm Pydantic parses without error and `escalate` is `true`:

```bash
python run.py
```

A valid run exits 0 and prints a JSON object where `category` is `"security"`, `severity` is `1`, and `escalate` is `true`. If Claude returns prose instead of JSON, the `<output_format>` tag is missing or the template failed to render — check `render_classify_issue()` output before the API call.

To confirm the template renders correctly without calling the API:

```python
from prompts.loader import render_classify_issue
print(render_classify_issue("acme/platform", 47, ["bug", "security"], "Test", "Body"))
```

The output must start with `<role>` and contain all six XML tags.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `json.JSONDecodeError` on `response.content[0].text` | Claude wrapped JSON in markdown fences (` ```json `) | Add `"Do not use markdown fences."` to `<output_format>`; or strip fences with `re.sub(r"^```json\n?|```$", "", raw, flags=re.M)` |
| Template renders with empty `{{ issue_body }}` | Jinja2 variable name mismatch or whitespace in key | Print `template.render(**kwargs)` directly and compare variable names |
| `ValidationError` for `severity` out of range 1–5 | Model returned `"severity": 0` or `"severity": 6` | Add explicit range reminder in `<instructions>`: `"Severity must be an integer from 1 (critical) to 5 (trivial), inclusive."` |
| Switching to `v2/` template silently uses `v1/` | `major` parsed from `PROMPT_VERSION` string, but `PROMPT_VERSION` not updated | Update `PROMPT_VERSION` in `schemas/v2.py` to `"2.0.0"` before wiring the loader |
| Prompt cache miss on every call | Dynamic fields (`open_count`, `issue_title`) inside the `<context>` block bust cache | Move high-churn fields to the `messages` list (user turn), keep `<role>` + `<instructions>` + `<examples>` in system for caching; see [claude-best-practices](../../../knowledge/geek/ai/llm-integration/claude-best-practices) |

## Next

- Add Anthropic prompt caching: annotate `<role>` + `<instructions>` + `<examples>` as `cache_control: {"type": "ephemeral"}` in the system array form to cache the static 80% of the prompt — see [claude-best-practices](../../../knowledge/geek/ai/llm-integration/claude-best-practices).
- A/B test template versions by routing 10% of traffic to `v2/` and comparing Pydantic parse-failure rate — see [prompt-techniques](../../../knowledge/geek/ai/llm-integration/prompt-techniques) for the PromptLibrary pattern.
- Extend the output schema with a `confidence` float and bump to `1.1.0` (minor — no key removed or renamed).

## References

- [knowledge/geek/ai/llm-integration/semantic-xml-content](../../../knowledge/geek/ai/llm-integration/semantic-xml-content) — establishes the XML-as-semantic-delimiter principle that backs every tag in the six-tag vocabulary used in Step 2 and the template in Step 3
- [knowledge/geek/ai/llm-integration/prompt-techniques](../../../knowledge/geek/ai/llm-integration/prompt-techniques) — covers PromptLibrary versioning and A/B testing patterns that the SemVer scheme in Step 6 extends to the file-level template artifact
- [knowledge/geek/ai/llm-integration/claude-best-practices](../../../knowledge/geek/ai/llm-integration/claude-best-practices) — production Anthropic API patterns: prompt caching for static XML blocks, model ID selection (`claude-sonnet-4-6`), and max_tokens discipline used in Step 5
