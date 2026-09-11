#!/usr/bin/env bash
# Verify the five direct-write media artifacts for one acceptance bed.
# The bed's rec-wrap steps land media/<calver>/<bed>/<bed>.{cast,gif,mjpeg,mp4,png}
# straight from the check-live steps (Cutover G-direct-write) — this script is
# the ONE verify implementation (R3); the matrix media stage and the suite
# aggregate stage both delegate here. Usage: verify-media.sh <bed> <calver>
set -u

[ $# -eq 2 ] || { echo "verify-media: usage: verify-media.sh <bed> <calver>" >&2; exit 1; }
bed=$1
calver=$2
d="media/$calver/$bed"

[ -d "$d" ] || { echo "verify-media: missing artifact dir $d for $bed (the direct-write run did not publish)" >&2; exit 1; }

fail=0
for spec in "cast 200" "gif 1024" "mjpeg 4096" "mp4 4096" "png 1024"; do
    set -- $spec
    f=$1
    m=$2
    p="$d/$bed.$f"
    if [ ! -s "$p" ]; then
        echo "verify-media: missing $p" >&2
        fail=1
        continue
    fi
    bytes=$(wc -c < "$p")
    if [ "$bytes" -lt "$m" ]; then
        echo "verify-media: $p is $bytes bytes, min is $m" >&2
        fail=1
    fi
done

if [ "$fail" -ne 0 ]; then
    echo "verify-media: FAILED assertions for $d" >&2
    exit 1
fi

echo "verify-media: OK $d ($(wc -c < "$d/$bed.cast")/$(wc -c < "$d/$bed.gif")/$(wc -c < "$d/$bed.mjpeg")/$(wc -c < "$d/$bed.mp4")/$(wc -c < "$d/$bed.png") bytes cast/gif/mjpeg/mp4/png)"
