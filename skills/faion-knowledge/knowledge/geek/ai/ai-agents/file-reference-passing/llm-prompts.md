# LLM Prompts — File-Reference Passing

## Prompt 1: Scanner

```
You will be given a MANIFEST of {n} items, each with id, path, and one-line description. Your job is to select at most {k} ids most relevant to: {goal}.

Return STRICT JSON:
{
  "rationale": "one sentence",
  "relevant_ids": [int, ...]
}

Do NOT return content from the items. Only ids.

MANIFEST:
{manifest}
```

## Prompt 2: Subagent reporter

```
After completing your investigation, return STRICT JSON:
{
  "summary": "3-5 sentences. What you found, what matters.",
  "interesting_refs": ["path-or-url", ...],
  "follow_up_questions": ["question", ...]   // optional, only if relevant
}

The PARENT agent will re-read any path you list. Do NOT paste file contents into your summary — paths are enough.
```

## Prompt 3: Tree-descender

```
You are at directory: {path}
Children: {children_listing}

Goal: {goal}

Pick the ONE child most likely to contain what we need. Return:
{
  "rationale": "one sentence",
  "next": "<child name>"
}
```

## Prompt 4: Ref-validator wrapper (post-LLM)

After the LLM emits refs, run this code-side prompt back to a small model only if validation fails:

```
The previous response listed refs that don't exist:
{bad_refs}

Available refs are:
{valid_refs}

Pick the closest matches from the valid list, or say "no match" if none apply. Return STRICT JSON:
{ "corrected": [str, ...], "rejected": [str, ...] }
```

## Prompt 5: Don't-quote rule

Add to system prompt of any reference-emitting agent:

```
You will analyze content. When reporting findings:
- Quote NO MORE than 10 words verbatim from any source
- Identify sources by their REF (path/URL/id) so the orchestrator can re-read them
- Your output should be at most 500 words; refs do the heavy lifting
```
