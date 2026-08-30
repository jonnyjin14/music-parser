#!/usr/bin/env bash
# bob-setup.sh
# Copies the .bob configuration (custom modes, skills, and rules) into a target repository.
# Usage:
#   ./bob-setup.sh /path/to/other-repo
#   ./bob-setup.sh          # defaults to current directory

TARGET="${1:-.}"
SOURCE="$(dirname "$0")/.bob"

if [ ! -d "$SOURCE" ]; then
  echo "Error: Source .bob directory not found at: $SOURCE" >&2
  exit 1
fi

if [ ! -d "$TARGET" ]; then
  echo "Error: Target directory does not exist: $TARGET" >&2
  exit 1
fi

DEST="$TARGET/.bob"
echo "Copying .bob configuration to: $DEST"
cp -r "$SOURCE" "$TARGET/"

echo ""
echo "Done. Files installed:"
find "$DEST" -type f | sed "s|$TARGET/||"

echo ""
echo "Note: The rules files in .bob/rules-agent/, .bob/rules-ask/, and .bob/rules-plan/"
echo "      contain project-specific notes for this repo. Edit them for your new project."
