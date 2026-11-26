#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STATE="$SCRIPT_DIR/.monthly-last-run"

CURRENT_MONTH=$(date +%Y-%m)
LAST_MONTH=$(cat "$STATE" 2>/dev/null || echo "")

if [ "$LAST_MONTH" = "$CURRENT_MONTH" ]; then
    echo "Already executed birthday post generator this month. Skipping."
    exit 0
fi

echo "Running monthly birthday post generator: $(date)"

# Run Python script in parent directory
PYTHON="$SCRIPT_DIR/../venv/bin/python"
if "$PYTHON" "$SCRIPT_DIR/../script.py" -gdrive; then
    echo "$CURRENT_MONTH" > "$STATE"
    echo "Birthday post generator completed successfully."
else
    echo "Birthday post generator failed."
    exit 1
fi
