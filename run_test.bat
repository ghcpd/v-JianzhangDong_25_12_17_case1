@echo off
python -u tests\run_doc_tests.py
exit /b %ERRORLEVEL%
