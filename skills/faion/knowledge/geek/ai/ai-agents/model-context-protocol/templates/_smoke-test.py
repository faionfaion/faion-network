#!/usr/bin/env python3
# purpose: Minimum viable smoke test for an MCP server scaffolded from python-server-stdio.py.
# consumes: a `server.py` path on disk.
# produces: exit 0 on green, 1 on red, with a one-line trace per tool call.
# depends-on: stdlib + `pip install mcp`.
# token-budget-impact: zero LLM tokens; pure protocol-level handshake.
"""Run as: python _smoke-test.py /srv/mcp/faion-internal/server.py"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path


async def main(server_path: Path) -> int:
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        str(server_path),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None

    handshake = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2026-07-28", "clientInfo": {"name": "smoke", "version": "1"}},
    }
    proc.stdin.write((json.dumps(handshake) + "\n").encode())
    await proc.stdin.drain()
    line = await proc.stdout.readline()
    resp = json.loads(line)
    assert "result" in resp, f"handshake failed: {resp}"
    print(f"[handshake] ok, server={resp['result'].get('serverInfo', {}).get('name')}")

    ping = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "ping", "arguments": {}}}
    proc.stdin.write((json.dumps(ping) + "\n").encode())
    await proc.stdin.drain()
    line = await proc.stdout.readline()
    resp = json.loads(line)
    body = json.loads(resp["result"]["content"][0]["text"])
    assert body["payload"]["status"] == "ok", f"ping failed: {body}"
    print(f"[ping] ok, server_version={body['server_version']}")

    proc.terminate()
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("usage: python _smoke-test.py <server.py>\n")
        sys.exit(2)
    sys.exit(asyncio.run(main(Path(sys.argv[1]))))
