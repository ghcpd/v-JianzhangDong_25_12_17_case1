#!/usr/bin/env bash
# Run the minimal test runner using the repository venv's python
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$DIR/.venv/bin/python" "$DIR/test_runner.py"
exit $?