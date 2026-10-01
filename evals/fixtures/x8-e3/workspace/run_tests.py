"""Stdlib test runner: runs every test_* function in test_invoice.py."""
import importlib, sys, traceback
m = importlib.import_module("test_invoice")
fails = 0
for name in sorted(dir(m)):
    if name.startswith("test_"):
        try:
            getattr(m, name)(); print(f"PASS {name}")
        except Exception:
            fails += 1; print(f"FAIL {name}"); traceback.print_exc()
sys.exit(1 if fails else 0)
