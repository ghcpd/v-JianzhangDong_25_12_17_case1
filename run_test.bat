@echo off
REM Run the minimal test runner using the repository venv's python
"%~dp0\.venv\Scripts\python" "%~dp0\test_runner.py"
exit /B %ERRORLEVEL%