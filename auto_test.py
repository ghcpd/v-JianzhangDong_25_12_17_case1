import subprocess
import platform
import datetime
import os

# Detect environment
if platform.system() == 'Windows':
    script = 'run_test.bat'
else:
    script = 'run_test.sh'

# Run the script
result = subprocess.run([script], capture_output=True, text=True)
output = result.stdout + result.stderr
status = 'TEST PASSED' if result.returncode == 0 else 'TEST FAILED'

# Timestamp
timestamp = datetime.datetime.now().isoformat()

# Log content
log_content = f"{timestamp}\n{output}\n{status}"

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Write to log
with open('logs/test_run.log', 'w') as f:
    f.write(log_content)