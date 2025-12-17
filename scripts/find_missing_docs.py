"""Scan Python files and report missing module/class/function docstrings.

Writes results to reference_link.txt in workspace root.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reference_link.txt"

py_files = list(ROOT.glob("*.py"))
ignore_names = {"auto_test.py", "run_test.sh", "run_test.bat"}

results = []
count = 1
for p in sorted(py_files):
    if p.name in ignore_names:
        continue
    if p.name.startswith("test_"):
        continue
    with p.open("r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            continue
    module_doc = ast.get_docstring(tree)
    if not module_doc:
        results.append((p.name, f"Missing module docstring (line 1)"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node)
            if not doc:
                results.append((p.name, f"Missing class docstring for {node.name} (line {node.lineno})"))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip functions starting with '_' (private) to reduce noise
            if node.name.startswith("_"):
                continue
            parent = getattr(node, "parent", None)
            doc = ast.get_docstring(node)
            if not doc:
                results.append((p.name, f"Missing function docstring for {node.name}() (line {node.lineno})"))

# Write to file in specified numbered format
with OUTPUT.open("w", encoding="utf-8") as out:
    if not results:
        out.write("No missing docstrings found.\n")
    else:
        for i, (fname, msg) in enumerate(results, start=1):
            out.write(f"({i}) {fname}: {msg}\n")

print(f"Found {len(results)} missing docstrings. Written to {OUTPUT}")
