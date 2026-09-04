#!/usr/bin/env bash
# cast-render.sh — render one or more asciinema .cast recordings into an
# animated GIF, cutting the trailing exit sequences and (for multiple casts)
# merging them into a single GIF.
#
# WHY: the record: stop types "exit" at the very end of the asciinema session
# (plugin-record methods.go) so the shell can end gracefully. The .cast
# therefore ends with the exit keystroke + the shell closing, and a naive
# render's LAST FRAME shows that exit/blank screen instead of the final test
# output. cast-trim-end.py cuts the trailing exit (the content/exit boundary is
# the final idle gap — the settle before the stop), so the GIF ends on the
# test-output screen. For a PR eval with several commands, record EACH command
# in its own session (record: start → run → stop, distinct record_name per
# command), trim each, and this script merges them with asciinema cat into one
# GIF.
#
# Usage: cast-render.sh <out.gif> <cast1> [cast2 ...]
# Requires: python3 (cast-trim-end.py), asciinema (merge), agg (render).
set -eu
OUT="$1"
shift

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

MERGE="$TMP/merged.cast"
first=""
for cast in "$@"; do
    [[ -f "$cast" ]] || { echo "cast-render: missing cast $cast" >&2; exit 1; }
    TRIM="$TMP/$(basename "$cast").trimmed"
    python3 "$HERE/cast-trim-end.py" "$cast" "$TRIM"
    if [[ -z "$first" ]]; then
        cp "$TRIM" "$MERGE"
        first=1
    else
        # asciinema cat concatenates recordings (timestamps shift naturally);
        # each trimmed cast is: prompt → command → output → prompt.
        asciinema cat "$MERGE" "$TRIM" > "$TMP/next.cast"
        mv "$TMP/next.cast" "$MERGE"
    fi
done

# Render the (merged) trimmed recording. idle_time_limit compresses the settle
# gaps; last_frame_duration holds the final output frame so it is readable.
agg --idle-time-limit 1 --last-frame-duration 2 "$MERGE" "$OUT"
echo "cast-render: $OUT ($(identify "$OUT" 2>/dev/null | wc -l | tr -d ' ') frames)"
