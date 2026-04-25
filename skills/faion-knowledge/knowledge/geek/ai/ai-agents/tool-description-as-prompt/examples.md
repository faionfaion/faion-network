# Examples — Tool Description as Prompt

## Example 1: Anthropic SWE-bench gain

Anthropic reported that the leap to SOTA on SWE-bench came largely from rewriting tool descriptions, not from a new model. Specifically: replacing terse one-liners with structured "use this when / do NOT use this when / output shape" descriptions cut wrong-tool selection errors and improved end-to-end task success.

The model didn't change. The eval changed because the prompt-shaped-as-tool-defs got better.

## Example 2: Disambiguating two read tools

Before:
```
read_file: "Read a file."
grep: "Search files."
```

The model alternated between them roughly randomly when the user said "find the auth handler".

After:
```
read_file: "Use when you know the file path. Returns full content. Do NOT use for cross-file search."
grep: "Use when you don't know the file path or need cross-file matches. Returns line matches. Do NOT use for reading a known file."
```

Tool selection error rate dropped to near zero.

## Example 3: Side-effect surfacing

Before:
```
delete_branch: "Delete a branch."
```
Model would call this on the working branch by accident.

After:
```
delete_branch: "MUTATING. Deletes a remote branch. Do NOT use on the current working branch. Use `archive_branch` instead if you want to preserve history."
```

The MUTATING marker + explicit forbiddance fixed the bug.

## Example 4: Latency hint

```
batch_train_model: "Submit a model training job. Returns a job_id. LATENCY: 5-30 minutes; the agent should NOT poll; the job will emit completion via webhook."
```

The latency hint + "do not poll" instruction prevents the agent from spinning waiting for results.

## Example 5: Output cap

```
search_docs: "Returns up to 10 results. If you need more, narrow your query first; do NOT call repeatedly with offsets."
```

Without this cap, agents call `search_docs` 5x trying to enumerate the corpus.

## Example 6: Validate-then-apply pair

```
dry_run_patch: "Preview a patch's effect without writing. Returns conflicts and changed files. Always call before `apply_patch`."

apply_patch: "MUTATING. Applies the patch. Use AFTER `dry_run_patch` returned no conflicts. Do NOT call on a dirty tree."
```

The pairing makes the correct sequence ("dry first, apply second") obvious from the descriptions alone.

## Example 7: Project-mining catch (faion-cli)

We had:
```
generate_implementation: "Generate code"
```
The agent often called this for refactor tasks where it should have been `refactor_code`. After splitting and adding when-to/when-not lines, mis-selection dropped.

## Example 8: Anti-example — marketing prose

Don't:
```
description: "Our powerful, AI-driven, enterprise-grade search powered by cutting-edge embeddings and a state-of-the-art reranker"
```

The model has no use for any of those words. They take prompt budget and add zero discrimination signal.

Do:
```
description: "Hybrid search over the docs corpus. Keyword + semantic. Returns top 10 passages with paths."
```
