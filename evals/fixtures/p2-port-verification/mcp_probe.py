#!/usr/bin/env python3
"""Minimal MCP stdio probe: initialize, tools/list, one tools/call per server.
Reads server defs from a .mcp.json (mcpServers key). No model involved. $0.
Usage: mcp_probe.py <mcp.json> <cwd>
"""
import json, subprocess, sys, threading, queue, os, time

CALLS = {
    "sequential-thinking": ("sequentialthinking", {"thought": "probe", "nextThoughtNeeded": False, "thoughtNumber": 1, "totalThoughts": 1}),
    "filesystem-wiki": ("list_directory", {"path": "./wiki"}),
    "context7": ("resolve-library-id", {"libraryName": "react"}),
    "github": ("search_repositories", {"query": "mcp"}),
    "playwright": ("browser_navigate", {"url": "about:blank"}),
}

def reader(proc, q):
    for line in proc.stdout:
        q.put(line)

def rpc(proc, q, method, params, timeout=120):
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}) + "\n")
    proc.stdin.flush()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            line = q.get(timeout=max(1, deadline - time.time()))
        except queue.Empty:
            break
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") == 1:
            return msg
    return None

def notify(proc, method, params=None):
    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method, "params": params or {}}) + "\n")
    proc.stdin.flush()

def probe(name, cfg, cwd):
    env = dict(os.environ)
    for k, v in (cfg.get("env") or {}).items():
        env[k] = v
    cmd = [cfg["command"]] + cfg.get("args", [])
    out = {"server": name, "cmd": " ".join(cmd)}
    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True, cwd=cwd, env=env)
    except Exception as e:
        out["error"] = f"spawn failed: {e}"
        return out
    q = queue.Queue()
    threading.Thread(target=reader, args=(proc, q), daemon=True).start()
    try:
        r = rpc(proc, q, "initialize", {"protocolVersion": "2024-11-05",
                                        "capabilities": {}, "clientInfo": {"name": "pv-probe", "version": "0.1"}}, timeout=180)
        if not r or "result" not in r:
            out["error"] = f"initialize failed: {json.dumps(r)[:300] if r else 'timeout'}"
            err = proc.stderr.read(2000) if proc.poll() is not None else ""
            if err: out["stderr"] = err[-800:]
            return out
        out["serverInfo"] = r["result"].get("serverInfo", {})
        notify(proc, "notifications/initialized")
        r = rpc(proc, q, "tools/list", {}, timeout=60)
        tools = [t["name"] for t in r["result"]["tools"]] if r and "result" in r else []
        out["tools_count"] = len(tools)
        out["tools"] = tools[:12]
        if name in CALLS:
            tname, targs = CALLS[name]
            out["call_tool"] = tname
            if tname not in tools:
                out["call_error"] = f"tool {tname} not in tools/list"
            else:
                # playwright/github calls can hang; shorter timeout
                r = rpc(proc, q, "tools/call", {"name": tname, "arguments": targs}, timeout=90)
                if r and "result" in r:
                    res = r["result"]
                    txt = json.dumps(res)[:400]
                    out["call_isError"] = res.get("isError", False)
                    out["call_result"] = txt
                else:
                    out["call_error"] = f"no response: {json.dumps(r)[:300] if r else 'timeout'}"
    finally:
        try:
            proc.terminate(); proc.wait(timeout=5)
        except Exception:
            proc.kill()
    return out

def main():
    mcpjson, cwd = sys.argv[1], sys.argv[2]
    cfg = json.load(open(mcpjson))["mcpServers"]
    results = []
    for name, scfg in cfg.items():
        print(f"--- probing {name} ...", flush=True)
        res = probe(name, scfg, cwd)
        results.append(res)
        print(json.dumps(res, indent=1)[:1500], flush=True)
    print("=== SUMMARY ===")
    for r in results:
        print(r["server"], "| tools:", r.get("tools_count"), "| call:", r.get("call_tool"),
              "| isError:", r.get("call_isError"), "| err:", r.get("error") or r.get("call_error"))

if __name__ == "__main__":
    main()
