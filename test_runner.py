"""Minimal test runner that imports tests.test_docs and runs functions named test_*.

This avoids needing pytest to be installed in the environment and keeps CI
lightweight and deterministic for this kata.
"""
import importlib
import sys
import traceback

try:
    mod = importlib.import_module("tests.test_docs")
except Exception:
    print("ERROR: Failed to import tests.test_docs")
    traceback.print_exc()
    sys.exit(2)

failed = []
count = 0
for name in dir(mod):
    if name.startswith("test_"):
        obj = getattr(mod, name)
        if callable(obj):
            count += 1
            try:
                obj()
                print(f"PASS: {name}")
            except AssertionError as e:
                print(f"FAIL: {name} - AssertionError: {e}")
                tb = traceback.format_exc()
                print(tb)
                failed.append(name)
            except Exception:
                print(f"ERROR: {name} - unexpected exception")
                traceback.print_exc()
                failed.append(name)

print(f"Ran {count} tests, failures: {len(failed)}")
if failed:
    sys.exit(1)
sys.exit(0)
