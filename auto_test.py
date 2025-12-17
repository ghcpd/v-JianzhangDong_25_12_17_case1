"""Automatic test runner.

Detect environment (Windows/Linux/macOS/Docker) and execute the appropriate test
script (run_test.bat for Windows, run_test.sh for Linux/macOS). Writes full
output to logs/test_run.log including a timestamp and a final status line.
"""
import os
import subprocess
import platform
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "test_run.log"

# Detect environment
system = platform.system()
is_docker = Path("/.dockerenv").exists() or os.environ.get("DOTNET_RUNNING_IN_CONTAINER")

if system == "Windows":
    cmd = ["cmd.exe", "/c", "run_test.bat"]
else:
    # Treat Docker like Linux/macOS and run the shell script
    cmd = ["/bin/bash", "./run_test.sh"]

start_ts = datetime.utcnow().isoformat() + "Z"
with LOG_FILE.open("a", encoding="utf-8") as f:
    f.write(f"===== Test run started at {start_ts} (system={system}, docker={is_docker}) =====\n")
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
        f.write(proc.stdout)
        if proc.stderr:
            f.write("\nSTDERR:\n")
            f.write(proc.stderr)
        status = "TEST PASSED" if proc.returncode == 0 else "TEST FAILED"
    except subprocess.TimeoutExpired as e:
        f.write("Test execution timed out.\n")
        status = "TEST FAILED"
    except Exception as e:
        f.write(f"Error running tests: {e}\n")
        status = "TEST FAILED"

    end_ts = datetime.utcnow().isoformat() + "Z"
    f.write(f"===== Test run finished at {end_ts} - {status} =====\n\n")

# Also print summary to stdout
print(f"{status}: logs written to {LOG_FILE}")
if status == "TEST FAILED":
    raise SystemExit(1)
