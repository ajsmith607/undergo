#!/bin/bash

# Start time in milliseconds
start=$(date +%s%3N)



SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/compile-assets.py" "$@"



# End time in milliseconds
end=$(date +%s%3N)

# Calculate duration
duration=$((end - start))

# Extract seconds and milliseconds
seconds=$((duration / 1000))
millis=$((duration % 1000))

echo "Execution time: ${seconds}.${millis}s"

