#!/usr/bin/env bash
# save-media.sh — copy the eval run's recordings/screenshots to media/<pr>-<calver>/
# and re-render the GIF with the trailing exit trimmed (the record: stop types
# "exit", so a naive render ends on the exit/blank screen instead of the last test
# output — see cast-render.sh/cast-trim-end.py).
#
# The record: + spice: check steps pull their artifacts to the HOST paths in the
# bed's plan (e.g. /tmp/pr-<N>.cast, /tmp/pr-<N>-screen.png).
# This script, run after the bed, saves every media artifact for the run into the
# gitignored eval-omarchy media directory (eval rule 6) with the optimal GIF.
#
# Usage: save-media.sh <pr-or-bed> <calver> [cast ...]
#   default: /tmp/$1.cast /tmp/$1-screen.png; additional casts are merged into
#   one GIF (record each command in its own session with a distinct record_name).

set -eu
name="$1"
calver="$2"
shift 2

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEDIA_DIR="$(cd "$HERE/.." && pwd)/media"
DEST="$MEDIA_DIR/$name-$calver"
mkdir -p "$DEST"

casts=("$@")
if (( ${#casts[@]} == 0 )); then
    casts=(/tmp/"$name".cast)
fi

# Re-render the GIF with the trailing exits trimmed (and casts merged if several).
if [[ -f "${casts[0]}" ]]; then
    "$HERE/cast-render.sh" "$DEST/$name.gif" "${casts[@]}" >/dev/null
    echo "rendered: $DEST/$name.gif (exit-trimmed)"
fi

# Save the raw artifacts beside the rendered GIF.
if [[ -f "${casts[0]}" ]]; then
    cp "${casts[0]}" "$DEST/"
    echo "saved: ${casts[0]} -> $DEST/$(basename "${casts[0]}")"
fi
for a in /tmp/"$name"-screen.png /tmp/"$name"-screen-*.png; do
    if [[ -f "$a" ]]; then
        cp "$a" "$DEST/"
        echo "saved: $a -> $DEST/$(basename "$a")"
    fi
done

# Encode the SPICE screen frames into a video (the screen-evidence mp4). The
# spice: screenshot steps capture the VM display at the hypervisor level (no
# guest Wayland session dependency); several frames at ~1 fps make a readable
# video of the eval run.
if compgen -G "$DEST/$name-screen-*.png" > /dev/null; then
    FIRST="$DEST/$(ls "$DEST/$name-screen-1.png" 2>/dev/null || ls "$DEST/$name-screen-"*.png | head -1 | xargs basename)"
    ffmpeg -y -framerate 1 -pattern_type glob -i "$DEST/$name-screen-*.png" -c:v libx264 -pix_fmt yuv420p "$DEST/$name-screen.mp4" >/dev/null 2>&1         && echo "encoded: $DEST/$name-screen.mp4 (SPICE frames -> video)"         || echo "note: ffmpeg unavailable or no SPICE frames — screen video skipped"
fi

echo "media saved: $DEST"
