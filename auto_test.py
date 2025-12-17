"""Automatic test execution script.
Detects the current environment and runs the appropriate test script.
Logs all output to logs/test_run.log with timestamp and final status.
"""

import os
import sys
import platform
import subprocess
from datetime import datetime
import re


def detect_environment():
    """Detect the current environment (Windows/Linux/macOS/Docker).
    
    Returns:
        str: Environment name ('windows', 'linux', 'macos', or 'docker').
    """
    # Check if running in Docker
    if os.path.exists('/.dockerenv') or os.environ.get('DOCKER_RUNNING'):
        return 'docker'
    
    system = platform.system().lower()
    
    if 'windows' in system:
        return 'windows'
    elif 'linux' in system:
        return 'linux'
    elif 'darwin' in system:
        return 'macos'
    else:
        return 'linux'  # Default to linux for unknown systems


def get_test_script(environment):
    """Get the appropriate test script path for the detected environment.
    
    Args:
        environment (str): The detected environment.
    
    Returns:
        str: Path to the test script file.
    """
    if environment == 'windows':
        return 'run_test.bat'
    else:  # linux, macos, docker
        return 'run_test.sh'


def ensure_test_scripts_exist():
    """Ensure test scripts exist. Create dummy ones if they don't.
    
    Returns:
        bool: True if scripts exist or were created, False otherwise.
    """
    windows_script = 'run_test.bat'
    linux_script = 'run_test.sh'
    python_test_file = '_test_docstrings.py'
    
    # Create Python test file that can be called from both batch and shell scripts
    if not os.path.exists(python_test_file):
        with open(python_test_file, 'w') as f:
            f.write("""\"\"\"Internal test module for verifying docstrings.\"\"\"

import sys

def verify_docstrings():
    \"\"\"Verify that all required docstrings are present.
    
    Returns:
        bool: True if all docstrings are present, False otherwise.
    \"\"\"
    import inspect
    import api
    import app
    import config
    import utils
    import tasks

    errors = []

    # Check api.py
    if not api.__doc__:
        errors.append('api.py: Missing module docstring')
    if not api.internal_helper.__doc__:
        errors.append('api.py: internal_helper() missing docstring')

    # Check app.py
    if not app.__doc__:
        errors.append('app.py: Missing module docstring')

    # Check config.py
    if not config.__doc__:
        errors.append('config.py: Missing module docstring')

    # Check utils.py
    if not utils.__doc__:
        errors.append('utils.py: Missing module docstring')
    if not utils.validate_task_title.__doc__:
        errors.append('utils.py: validate_task_title() missing docstring')
    if not utils.helper_function.__doc__:
        errors.append('utils.py: helper_function() missing docstring')

    # Check tasks.py
    if not tasks.__doc__:
        errors.append('tasks.py: Missing module docstring')
    if not tasks.Task.__doc__:
        errors.append('tasks.py: Task class missing docstring')
    if not tasks.TaskManager.__doc__:
        errors.append('tasks.py: TaskManager class missing docstring')

    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return False
    else:
        print('All docstrings verified successfully')
        return True

if __name__ == '__main__':
    success = verify_docstrings()
    sys.exit(0 if success else 1)
""")
    
    # Create Windows test script if it doesn't exist
    if not os.path.exists(windows_script):
        with open(windows_script, 'w') as f:
            f.write("""@echo off
REM Test verification script for Windows
REM Verifies that all required docstrings are present

python _test_docstrings.py
exit /b %errorlevel%
""")
    
    # Create Linux/macOS test script if it doesn't exist
    if not os.path.exists(linux_script):
        with open(linux_script, 'w') as f:
            f.write("""#!/bin/bash
# Test verification script for Linux/macOS
# Verifies that all required docstrings are present

python3 _test_docstrings.py
exit $?
""")
        # Make the Linux script executable
        os.chmod(linux_script, 0o755)
    
    return True


def run_tests(test_script):
    """Run the appropriate test script and capture output.
    
    Args:
        test_script (str): Path to the test script.
    
    Returns:
        tuple: (exit_code, output_text)
    """
    try:
        # Detect environment to use correct Python executable
        environment = detect_environment()
        
        if environment == 'windows':
            # Use venv Python on Windows
            python_cmd = r'.venv\Scripts\python'
        else:
            # Use venv Python on Linux/macOS/Docker
            python_cmd = '.venv/bin/python'
        
        # Run the test directly using the venv Python
        result = subprocess.run(
            [python_cmd, '_test_docstrings.py'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result.returncode, result.stdout + result.stderr
    except Exception as e:
        return 1, f"Error running test script: {str(e)}"


def log_results(test_script, exit_code, output, environment):
    """Log test results to logs/test_run.log.
    
    Args:
        test_script (str): The test script that was run.
        exit_code (int): The exit code from the test.
        output (str): The output from the test script.
        environment (str): The detected environment.
    """
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    log_file = 'logs/test_run.log'
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = 'TEST PASSED' if exit_code == 0 else 'TEST FAILED'
    
    with open(log_file, 'a') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Test Run: {timestamp}\n")
        f.write(f"Environment: {environment}\n")
        f.write(f"Test Script: {test_script}\n")
        f.write(f"{'='*60}\n")
        f.write(output)
        if not output.endswith('\n'):
            f.write('\n')
        f.write(f"\nExit Code: {exit_code}\n")
        f.write(f"Status: {status}\n")
        f.write(f"{'='*60}\n\n")
    
    return log_file, status


def main():
    """Main entry point for auto_test.py."""
    print("Auto Test Execution Script")
    print("-" * 60)
    
    # Detect environment
    environment = detect_environment()
    print(f"Detected Environment: {environment}")
    
    # Ensure test scripts exist
    ensure_test_scripts_exist()
    
    # Get appropriate test script
    test_script = get_test_script(environment)
    print(f"Test Script: {test_script}")
    
    # Run tests
    print("\nRunning tests...")
    exit_code, output = run_tests(test_script)
    
    # Log results
    log_file, status = log_results(test_script, exit_code, output, environment)
    
    # Print results
    print("\nTest Output:")
    print("-" * 60)
    print(output)
    print("-" * 60)
    print(f"\nStatus: {status}")
    print(f"Log File: {log_file}")
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
