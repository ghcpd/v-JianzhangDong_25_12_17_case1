import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "reference_link.txt"

failures = []

line_re = re.compile(r"^\(\d+\)\s+(?P<path>[^:]+):\s+Missing\s+(?P<kind>module|function|class)\s+docstring(?:\s+for\s+(?P<name>[^\(]+?)(?:\(\))?)?", re.I)

with REF.open(encoding="utf-8") as fh:
    for ln in fh:
        ln = ln.strip()
        if not ln:
            continue
        # Parse lines like: (1) utils.py: Missing function docstring for validate_task_title() (line 1)
        prefix, _, rest = ln.partition(":")
        file_part = prefix.split(")", 1)[1].strip() if ")" in prefix else prefix.strip()
        path = ROOT / file_part
        if not path.exists():
            failures.append(f"File not found: {path}")
            continue
        kind = None
        name = None
        if "Missing module docstring" in rest:
            kind = "module"
        elif "Missing class docstring" in rest:
            kind = "class"
        elif "Missing function docstring" in rest:
            kind = "function"
        # extract optional name between 'for ' and ' (line'
        if " for " in rest:
            start = rest.find(" for ") + len(" for ")
            end = rest.rfind(" (line")
            if end == -1:
                end = len(rest)
            name = rest[start:end].strip()
            if name.endswith("()"):
                name = name[:-2]

        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        if kind == "module":
            doc = ast.get_docstring(tree)
            if not doc:
                failures.append(f"Missing module docstring in {path}")
        elif kind == "class":
            found = False
            for node in tree.body:
                if isinstance(node, ast.ClassDef) and node.name == name:
                    found = True
                    if not ast.get_docstring(node):
                        failures.append(f"Missing class docstring for {name} in {path}")
                    break
            if not found:
                failures.append(f"Class {name} not found in {path}")
        elif kind == "function":
            # function may be top-level or method (ClassName.func)
            if name and "." in name:
                clsname, funcname = name.split(".")
                found = False
                for node in tree.body:
                    if isinstance(node, ast.ClassDef) and node.name == clsname:
                        for mem in node.body:
                            if isinstance(mem, ast.FunctionDef) and mem.name == funcname:
                                found = True
                                if not ast.get_docstring(mem):
                                    failures.append(f"Missing function docstring for {name} in {path}")
                                break
                        break
                if not found:
                    failures.append(f"Method {name} not found in {path}")
            else:
                found = False
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef) and node.name == name:
                        found = True
                        if not ast.get_docstring(node):
                            failures.append(f"Missing function docstring for {name} in {path}")
                        break
                if not found:
                    failures.append(f"Function {name} not found in {path}")

if failures:
    print("Some checks failed:")
    for f in failures:
        print(" -", f)
    sys.exit(1)
else:
    print("All documentation checks passed.")
    sys.exit(0)
