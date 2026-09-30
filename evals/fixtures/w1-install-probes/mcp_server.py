#!/usr/bin/env python3
"""Minimal MCP stdio server: one tool w1_ping -> W1MCPMARKER. No deps."""
import sys, json
def send(o):
    sys.stdout.write(json.dumps(o)+"\n"); sys.stdout.flush()
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    try: req=json.loads(line)
    except Exception: continue
    mid=req.get("id"); method=req.get("method","")
    if method=="initialize":
        send({"jsonrpc":"2.0","id":mid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"w1mcp","version":"0.1.0"}}})
    elif method=="tools/list":
        send({"jsonrpc":"2.0","id":mid,"result":{"tools":[{"name":"w1_ping","description":"Returns the W1 MCP marker token.","inputSchema":{"type":"object","properties":{}}}]}})
    elif method=="tools/call":
        send({"jsonrpc":"2.0","id":mid,"result":{"content":[{"type":"text","text":"W1MCPMARKER"}],"isError":False}})
    elif mid is not None:
        send({"jsonrpc":"2.0","id":mid,"result":{}})
