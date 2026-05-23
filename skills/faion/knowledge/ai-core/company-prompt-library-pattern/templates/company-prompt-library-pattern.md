<!--
purpose: Markdown skeleton for a Company Prompt Library Pattern spec.
consumes: inventory.csv, namespace_map.json, OWNERS.yaml.
produces: a Markdown spec consumable by humans + indexable by CI.
depends-on: content/02-output-contract.xml schema.
token-budget-impact: ~200 tokens.
-->

# Company Prompt Library Spec — &lt;spec_id&gt;

- **spec_id**: &lt;org-slug&gt;-prompt-library
- **owner**: &lt;handle or email — single named human, never "team"&gt;
- **version**: 1.0.0
- **last_reviewed**: 2026-05-22
- **status**: active

## Namespace map

| Namespace | Consumer | Count |
|---|---|---|
| `prompts/role/pm/` | PM agents | 12 |
| `prompts/role/dev/` | dev agents | 18 |
| `prompts/task/code-review/` | code-review agents | 7 |

## Override layers (resolution order — fixed)

1. `faion-defaults` (upstream)
2. `role-pack`
3. `company-override`
4. `repo-override` (wins)

## Eval gate

- Scorers: `rubric-judge`, `json-schema`
- Threshold: 0.85
- Block on fail: **true**
- Schedule: on every PR + nightly drift check

## Role packs

| Pack | Owner | Count |
|---|---|---|
| pm | alex@acme.com | 12 |
| dev | kim@acme.com | 18 |
| qa | sam@acme.com | 9 |

## Rollout plan

1. Migrate inline prompts into namespaced files (CI grep gate).
2. Wire eval gate to PR pipeline.
3. Assign owners; archive orphans.
4. Announce 2-week window; declare cutover.

## Notes

&lt;Supersedes &lt;old_spec_id&gt;; or "ready for owner review"; or open questions.&gt;
