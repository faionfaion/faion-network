<!--
purpose: Minimum viable filled IPI defense spec for a single-source single-tool agent.
consumes: nothing — illustrative only
produces: defense-spec.json that passes validate-indirect-prompt-injection-defense.py
depends-on: templates/defense-spec.schema.json
token-budget-impact: reference only, not loaded by agent
-->
# Smoke-test defense spec — single-tool RSS reader

```json
{
  "agent_name": "rss-summariser",
  "boundaries": [
    {"id": "b1", "label": "developer instructions", "channel": "system"},
    {"id": "b2", "label": "agent user", "channel": "user"},
    {"id": "b3", "label": "RSS items", "channel": "tool"}
  ],
  "untrusted_sources": [
    {"source": "rss_item_body", "trust_level": "untrusted", "max_size_kb": 16, "content_type": "text/html"}
  ],
  "taint_rules": [
    {"source_pattern": "rss_.*", "wrap_with": "<untrusted-content source='rss'>{body}</untrusted-content>", "max_quote_chars": 8000}
  ],
  "split_pattern": "single_llm",
  "tool_scopes": [
    {"tool": "fetch_rss", "allowed_paths": [], "allowed_hosts": ["feeds.example.com"]}
  ],
  "canary": {"token_format": "CANARY-{uuid}", "outbound_check": "abort_on_match"},
  "eval_set": {"path": "evals/ipi/", "min_categories": 10, "min_cases": 20}
}
```
