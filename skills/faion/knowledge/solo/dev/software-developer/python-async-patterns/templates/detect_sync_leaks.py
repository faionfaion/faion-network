"""
detect_sync_leaks.py — find blocking calls inside async def functions.

Usage: python detect_sync_leaks.py [path]
Exit 1 if blocking calls found; suitable as pre-commit hook.
"""
import ast
import sys
import pathlib

BLOCKING = {
    "requests.get", "requests.post", "requests.put", "requests.delete", "requests.request",
    "urllib.request.urlopen", "urllib3.PoolManager",
    "time.sleep",
    "psycopg2.connect",
    "sqlalchemy.create_engine",
    "boto3.client", "boto3.resource",
    "open",  # use aiofiles instead
}


def name_of(node: ast.expr) -> str:
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value  # type: ignore[assignment]
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def scan(path: str) -> list[tuple[str, int, str]]:
    issues = []
    for f in pathlib.Path(path).rglob("*.py"):
        try:
            tree = ast.parse(f.read_text(), filename=str(f))
        except SyntaxError:
            continue
        async_funcs = [n for n in ast.walk(tree) if isinstance(n, ast.AsyncFunctionDef)]
        for fn in async_funcs:
            for node in ast.walk(fn):
                if isinstance(node, ast.Call):
                    n = name_of(node.func)
                    if any(n.startswith(b) for b in BLOCKING):
                        issues.append((str(f), node.lineno, n))
    return issues


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    found = scan(target)
    for filepath, line, name in found:
        print(f"{filepath}:{line}: blocking call '{name}' inside async def")
    sys.exit(1 if found else 0)
