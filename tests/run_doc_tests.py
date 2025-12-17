"""Run checks to verify that documented missing docstrings were added.

Reads reference_link_before.txt (the original missing-doc list) and ensures each
item now has a docstring. Exits with code 0 if all checks pass, otherwise 1.
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reference_link_before.txt"

if not REF.exists():
    print("reference_link_before.txt not found; cannot run tests.")
    sys.exit(2)

pattern = re.compile(r"\)\s*(?P<file>[^:]+):\s*(?P<msg>.+)\s*\(line (?P<line>\d+)\)")

failed = []
for line in REF.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    m = pattern.search(line)
    if not m:
        print(f"Unrecognized line format: {line}")
        failed.append(line)
        continue
    fname = m.group("file").strip()
    msg = m.group("msg").strip()
    fpath = ROOT / fname
    if not fpath.exists():
        print(f"File missing during test: {fname}")
        failed.append(line)
        continue
    tree = ast.parse(fpath.read_text(encoding="utf-8"))
    if msg.startswith("Missing module docstring"):
        if ast.get_docstring(tree):
            print(f"PASS: module docstring present in {fname}")
        else:
            print(f"FAIL: module docstring missing in {fname}")
            failed.append(line)
    elif msg.startswith("Missing class docstring for"):
        cls_name = msg.split("for",1)[1].strip().split()[0]
        found = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == cls_name:
                if ast.get_docstring(node):
                    print(f"PASS: class docstring present for {cls_name} in {fname}")
                else:
                    print(f"FAIL: class docstring missing for {cls_name} in {fname}")
                    failed.append(line)
                found = True
                break
        if not found:
            print(f"FAIL: class {cls_name} not found in {fname}")
            failed.append(line)
    elif msg.startswith("Missing function docstring for"):
        func_part = msg.split("for",1)[1].strip()
        func_name = func_part.split("(")[0].strip()
        found = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == func_name:
                # skip private functions
                if ast.get_docstring(node):
                    print(f"PASS: function docstring present for {func_name} in {fname}")
                else:
                    print(f"FAIL: function docstring missing for {func_name} in {fname}")
                    failed.append(line)
                found = True
                break
        if not found:
            print(f"FAIL: function {func_name} not found in {fname}")
            failed.append(line)
    else:
        print(f"Unrecognized message type: {msg}")
        failed.append(line)

if failed:
    print(f"\nTEST FAILED: {len(failed)} item(s) failed")
    sys.exit(1)
else:
    print("\nAll documented missing docstrings are present. TEST PASSED")
    sys.exit(0)
