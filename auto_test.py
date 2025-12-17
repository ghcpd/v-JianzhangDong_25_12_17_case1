"""Auto test runner that detects the environment and runs the project tests.

Behavior:
 - Detects Windows vs POSIX vs Docker
 - Runs run_test.bat on Windows, run_test.sh on POSIX (including Docker)
 - Captures output and writes logs/test_run.log with a timestamp and a final
   status line: TEST PASSED or TEST FAILED
"""
import os
import sys
import subprocess
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "test_run.log")


def detect_environment():
    if os.name == "nt":
        return "windows"
    # basic docker detection
    if os.path.exists("/.dockerenv") or os.environ.get("DOCKER", "") != "":
        return "docker"
    return "posix"


def run_tests_and_capture(env):
    if env == "windows":
        cmd = ["cmd", "/c", "run_test.bat"]
    else:
        # posix and docker use the shell script
        cmd = ["/bin/bash", "run_test.sh"]

    proc = subprocess.run(cmd, cwd=os.path.dirname(__file__), capture_output=True, text=True)
    combined = proc.stdout + proc.stderr
    return proc.returncode, combined


def main():
    os.makedirs(LOG_DIR, exist_ok=True)
    env = detect_environment()
    code, output = run_tests_and_capture(env)

    timestamp = datetime.utcnow().isoformat() + "Z"
    status = "TEST PASSED" if code == 0 else "TEST FAILED"

    with open(LOG_FILE, "a", encoding="utf-8") as fh:
        fh.write(f"-----\nTIME: {timestamp}\nENV: {env}\n")
        fh.write(output)
        fh.write(f"\n{status}\n")

    print(f"Wrote test log to: {LOG_FILE} (status: {status})")
    # mirror exit code
    sys.exit(code)


if __name__ == "__main__":
    main()
