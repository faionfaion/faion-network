# article-pipeline

## Purpose
Produce one longform article from an editorial brief and ship it in two languages: outline, draft the sections in parallel, assemble, edit against a validation gate, translate, then repair the translation against its source.

## Invoke
```
faion workflow build {recipe.json} --var brief={file} --var article={out.md} --var language={name} --var target={out.lang.md} [--var style_guide={file}] [--var rules={file}] [--var gates={cmds}] [--target claude|codex|both] [--out-dir {dir}]
```

## Inputs
- `brief` — editorial brief every stage is grounded in; nothing outside it may be invented. Required.
- `article` — target path of the finished source-language article. Required.
- `language` — target language of the translation. Required: the pipeline always produces exactly one.
- `target` — target path of the translated article. Required.
- `style_guide` — style guide the outliner and the editor enforce. Optional, default empty.
- `rules` — language-rules file for the translator and the language reviewer. Optional, default empty.
- `gates` — validation command templates, one per line; `{file}` is replaced with the file under verification. Optional, default empty — empty gates clean.

## Outputs
- Files: `.claude/workflows/article-pipeline.js`, `article-pipeline.codex.sh`, `article-pipeline.lock.json`.
- Six stages: `outline` (JSON, 6-14 sections) → `sections` (fan-out, ≤8 concurrent) → `assemble` → `review` (gated, ≤2 rounds) → `translate` → `language_review`.
- The run writes `{run:dir}/section-NN.md` per section, then `{article}` and `{target}`.
- The command gate runs on `{article}` only. The translation gets a language review that edits in place, not a command gate — point `gates` at file-agnostic commands and re-run them on `{target}` if you need one.

## When NOT to use
- Anything touching code, docs-in-repo, or a build: every fragment here is forbidden to leave the article paths. Use `sdd-feature`.
- Short-form copy — an outline of 6-14 sections is the floor, and the fan-out costs more than the piece is worth.
- Single-language output: `translate` and `language_review` are not optional stages, they are the last two.

## Cost
One model call per stage plus one per section and per gate round, so cost scales with the outline's section count; `sections` and `translate` dominate. The translation doubles the article's token volume.
