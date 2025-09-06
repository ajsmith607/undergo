#!/bin/bash

# Path to Hugo site root (assumed to be the current dir, or passed as $1)
SITE_DIR="${1:-.}"
PYTHON_SCRIPT="compile-assets.sh"

ASSET_DIR="${ASSET_DIR:-content/_assets}"  # fallback if not set
WATCH_PATH="$SITE_DIR/$ASSET_DIR"

echo "📂 Watching directory: $WATCH_PATH"
echo "⚙️  Using config: $CONFIG_FILE"

# Check prerequisites
command -v inotifywait >/dev/null 2>&1 || {
  echo "❌ inotifywait not found. Please install inotify-tools." >&2
  exit 1
}

# Main loop
inotifywait -mq -e modify -e close_write --format '%w%f' -r "$WATCH_PATH" |
while read changed_file; do
  if [[ "$changed_file" == *.md ]]; then
    echo "🔄 Detected change: $changed_file"
    "$PYTHON_SCRIPT" --changed "$changed_file"
  fi
done
