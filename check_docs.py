import ast
import os

def has_docstring(node):
    return ast.get_docstring(node) is not None

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    tree = ast.parse(content)
    missing = []
    # Module docstring
    if not has_docstring(tree):
        missing.append(f"Module docstring missing in {filepath}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not has_docstring(node):
                name = node.name
                if isinstance(node, ast.FunctionDef):
                    missing.append(f"Function {name} missing docstring in {filepath}")
                else:
                    missing.append(f"Class {name} missing docstring in {filepath}")
    return missing

files = ['api.py', 'app.py', 'config.py', 'tasks.py', 'utils.py']
all_missing = []
for f in files:
    if os.path.exists(f):
        all_missing.extend(check_file(f))

if all_missing:
    for m in all_missing:
        print(m)
    print("TEST FAILED")
    exit(1)
else:
    print("TEST PASSED")
    exit(0)