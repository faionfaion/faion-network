# purpose: MCP @mcp.tool decorator with structured docstring
# consumes: tool name + function signature + side-effect class
# produces: tool definition (Python dict) conforming to content/02-output-contract.xml schema constraints
# depends-on: 01-core-rules.xml (structured-description-required, under-200-tokens, anti-trigger-required-on-overlap, mutating-marker-required, latency-and-pagination-caps, description-matches-schema)
# token-budget-impact: ~80-180 tokens per tool description
@mcp.tool()
def query_warehouse(sql: str) -> list[dict]:
    """
    Execute a read-only SQL query against the warehouse.

    Use this when the user asks for analytics that require SQL.
    Do NOT use this for transactional or write operations.
    Returns up to 1000 rows; truncate with LIMIT if larger sets are needed.

    Side effect: none (read-only, sandboxed read-replica).
    Latency: 1-30s depending on query.
    """
    ...
