@echo off
REM Run Python test runner and capture logs
set "LOG_FILE=logs\test_run.log"
if not exist logs mkdir logs

echo Running tests at %date% %time% > "%LOG_FILE%"

python run_test.py

REM Append final status from run_test.py output
IF %ERRORLEVEL% EQU 0 (
  echo TEST PASSED >> "%LOG_FILE%"
) ELSE (
  echo TEST FAILED >> "%LOG_FILE%"
)
