@echo off
REM Test verification script for Windows
REM Verifies that all required docstrings are present

python _test_docstrings.py
exit /b %errorlevel%
