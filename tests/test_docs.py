"""Tests that verify presence of module/class/function docstrings by parsing source files.

Using AST parsing avoids importing modules that may require third-party packages
(like fastapi) and keeps tests lightweight and deterministic.
"""
import ast
import os

ROOT = os.path.dirname(os.path.dirname(__file__))


def get_tree(filename):
    path = os.path.join(ROOT, filename)
    with open(path, "r", encoding="utf-8") as fh:
        return ast.parse(fh.read())


def find_def(tree, name):
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == name:
            return node
    return None


def test_utils_docs_present():
    tree = get_tree("utils.py")
    # module docstring
    assert ast.get_docstring(tree) and ast.get_docstring(tree).strip() != ""
    # functions
    fn = find_def(tree, "validate_task_title")
    assert fn is not None and ast.get_docstring(fn) and ast.get_docstring(fn).strip() != ""
    fn2 = find_def(tree, "helper_function")
    assert fn2 is not None and ast.get_docstring(fn2) and ast.get_docstring(fn2).strip() != ""


def test_tasks_docs_present():
    tree = get_tree("tasks.py")
    assert ast.get_docstring(tree) and ast.get_docstring(tree).strip() != ""
    cls = find_def(tree, "TaskManager")
    assert cls is not None and ast.get_docstring(cls) and ast.get_docstring(cls).strip() != ""
    add_fn = find_def(cls, "add_task") or next((n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "add_task"), None)
    assert add_fn is not None and ast.get_docstring(add_fn) and ast.get_docstring(add_fn).strip() != ""
    list_fn = next((n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "list_tasks"), None)
    assert list_fn is not None and ast.get_docstring(list_fn) and ast.get_docstring(list_fn).strip() != ""
    rem_fn = next((n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "remove_task"), None)
    assert rem_fn is not None and ast.get_docstring(rem_fn) and ast.get_docstring(rem_fn).strip() != ""


def test_api_and_config_docs_present():
    tree = get_tree("api.py")
    assert ast.get_docstring(tree) and ast.get_docstring(tree).strip() != ""
    fn = find_def(tree, "create_task")
    assert fn is not None and ast.get_docstring(fn) and ast.get_docstring(fn).strip() != ""
    fn2 = find_def(tree, "internal_helper")
    assert fn2 is not None and ast.get_docstring(fn2) and ast.get_docstring(fn2).strip() != ""

    tree2 = get_tree("config.py")
    assert ast.get_docstring(tree2) and ast.get_docstring(tree2).strip() != ""

    tree3 = get_tree("app.py")
    assert ast.get_docstring(tree3) and ast.get_docstring(tree3).strip() != ""
