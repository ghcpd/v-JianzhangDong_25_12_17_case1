import os
import sys
from datetime import datetime

LOG_FILE = os.path.join("logs", "test_run.log")
FILES = ["utils.py", "api.py", "tasks.py", "config.py"]

os.makedirs("logs", exist_ok=True)

with open(LOG_FILE, "w", encoding="utf-8") as log:
    log.write(f"Running tests at {datetime.now().isoformat()}\n")

    status = 0

    def check_module_docstring(f):
        with open(f, encoding="utf-8") as fh:
            first_lines = [next(fh) for _ in range(3)]
        if not any('"""' in line for line in first_lines):
            log.write(f"Missing module docstring in {f}\n")
            return 1
        return 0

    def check_function_docstrings(f):
        with open(f, encoding="utf-8") as fh:
            lines = fh.readlines()
        for i, line in enumerate(lines):
            if line.lstrip().startswith("def "):
                block = lines[i + 1 : i + 6]
                if not any('"""' in b for b in block):
                    log.write(f"Missing docstring for function in {f} at line {i + 1}\n")
                    return 1
        return 0

    def check_class_docstrings(f):
        with open(f, encoding="utf-8") as fh:
            lines = fh.readlines()
        for i, line in enumerate(lines):
            if line.lstrip().startswith("class "):
                block = lines[i + 1 : i + 6]
                if not any('"""' in b for b in block):
                    log.write(f"Missing docstring for class in {f} at line {i + 1}\n")
                    return 1
        return 0

    for f in FILES:
        status |= check_module_docstring(f)
        status |= check_function_docstrings(f)
        status |= check_class_docstrings(f)

    if status == 0:
        log.write("TEST PASSED\n")
    else:
        log.write("TEST FAILED\n")

sys.exit(0 if status == 0 else 1)
