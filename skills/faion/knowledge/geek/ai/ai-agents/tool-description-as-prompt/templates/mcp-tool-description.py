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
