#!/usr/bin/env bash
# save-media.sh — copy the eval run's recordings/screenshots to media/<pr>-<calver>/.
#
# The record: + spice: check steps pull their artifacts to the HOST paths in the
# bed's plan (e.g. /tmp/pr-<N>.cast, /tmp/pr-<N>.gif, /tmp/pr-<N>-screen.png).
# This script, run after the bed, saves every media artifact for the run into the
# gitignored eval-omarchy media directory (eval rule 6).
#
# Usage: save-media.sh <pr-or-bed> <calver> [artifact ...]
#   default artifacts: /tmp/$1.cast /tmp/$1.gif /tmp/$1-screen.png

set -eu
name="$1"
calver="$2"
shift 2

MEDIA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/media"
DEST="$MEDIA_DIR/$name-$calver"
mkdir -p "$DEST"

artifacts=("$@")
if (( ${#artifacts[@]} == 0 )); then
    artifacts=(/tmp/"$name".cast /tmp/"$name".gif /tmp/"$name"-screen.png)
fi

copied=0
for a in "${artifacts[@]}"; do
    if [[ -f "$a" ]]; then
        cp "$a" "$DEST/"
        echo "saved: $a -> $DEST/$(basename "$a")"
        copied=$((copied + 1))
    fi
done

echo "media saved: $copied artifact(s) to $DEST"
