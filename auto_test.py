import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "test_run.log"


def is_docker():
    # Common Docker indicators
    if os.path.exists("/.dockerenv"):
        return True
    try:
        with open("/proc/1/cgroup", "r") as f:
            content = f.read()
            if "docker" in content or "kubepods" in content:
                return True
    except Exception:
        pass
    return False


def run_script(cmd, shell=False):
    proc = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    system = platform.system()
    if is_docker():
        env = "docker"
    elif system == "Windows":
        env = "windows"
    else:
        env = "linux"

    if env == "windows":
        script = ["cmd", "/c", "run_test.bat"]
    else:
        script = ["bash", "run_test.sh"]

    start_ts = datetime.utcnow().isoformat() + "Z"
    rc, out, err = run_script(script)

    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(f"=== Test run at {start_ts} (env={env}) ===\n")
        fh.write(out)
        if err:
            fh.write("\n--- STDERR ---\n")
            fh.write(err)
        final = "TEST PASSED" if rc == 0 else "TEST FAILED"
        fh.write(f"\n{final}\n\n")

    print(out)
    print(err)
    print(final)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
