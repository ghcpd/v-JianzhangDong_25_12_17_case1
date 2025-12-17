#!/usr/bin/env python3
"""Automatic test runner that detects the environment and runs the appropriate test script.

The script will run `run_test.sh` on Linux/macOS and `run_test.bat` on Windows, and it will
log the output (including a timestamp and final status) to logs/test_run.log.
"""

import platform
import subprocess
import os
from datetime import datetime

LOG_FILE = os.path.join("logs", "test_run.log")

def run_cmd(cmd):
    """Run a command and capture output, writing to the LOG_FILE."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"Running tests at {datetime.now().isoformat()}\n")
        log.write(f"Executing: {' '.join(cmd)}\n")
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log.write(proc.stdout)
        return proc.returncode


def main():
    os.makedirs("logs", exist_ok=True)
    # Clear or create the log file
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

    sys = platform.system()
    if sys == "Windows":
        cmd = ["cmd", "/c", "run_test.bat"]
    else:
        # Assume POSIX system; prefer run_test.sh
        cmd = ["bash", "./run_test.sh"]

    rc = run_cmd(cmd)
    # Append final status line
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        if rc == 0:
            log.write("TEST PASSED\n")
        else:
            log.write("TEST FAILED\n")

    # Exit with same status
    raise SystemExit(rc)

if __name__ == "__main__":
    main()
