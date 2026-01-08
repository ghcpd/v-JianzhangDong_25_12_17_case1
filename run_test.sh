#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="logs/test_run.log"
mkdir -p logs

# Log timestamp
echo "Running tests at $(date)" > "$LOG_FILE"

# Files to check
FILES=(utils.py api.py tasks.py config.py)
STATUS=0

check_module_docstring() {
  local file="$1"
  # Ensure there is a triple-quote in the first 3 lines
  if ! head -n 3 "$file" | grep -q '"""'; then
    echo "Missing module docstring in $file" >> "$LOG_FILE"
    STATUS=1
  fi
}

# Check functions in file for docstrings
check_function_docstrings() {
  local file="$1"
  # For each def, check the next 5 lines for triple-quote
  grep -n '^def ' "$file" | while IFS=: read -r line rest; do
    start=$((line + 1))
    end=$((line + 5))
    # Use sed to get lines after def
    if ! sed -n "${start},${end}p" "$file" | grep -q '"""'; then
      echo "Missing docstring for function in $file at line $line" >> "$LOG_FILE"
      STATUS=1
    fi
  done
}

check_class_docstrings() {
  local file="$1"
  # For each class, check the next 5 lines for triple-quote
  grep -n '^class ' "$file" | while IFS=: read -r line rest; do
    start=$((line + 1))
    end=$((line + 5))
    if ! sed -n "${start},${end}p" "$file" | grep -q '"""'; then
      echo "Missing docstring for class in $file at line $line" >> "$LOG_FILE"
      STATUS=1
    fi
  done
}

for f in "${FILES[@]}"; do
  check_module_docstring "$f"
  check_function_docstrings "$f"
  check_class_docstrings "$f"
done

if [ $STATUS -eq 0 ]; then
  echo "TEST PASSED" >> "$LOG_FILE"
else
  echo "TEST FAILED" >> "$LOG_FILE"
fi

exit $STATUS
