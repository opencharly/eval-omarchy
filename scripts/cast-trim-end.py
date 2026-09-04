#!/usr/bin/env python3
"""Trim the trailing exit sequence from an asciinema .cast.

The record: stop types "exit" at the very end of the terminal session (to end
asciinema gracefully — verified in plugin-record methods.go: send-keys exit
Enter). The .cast therefore ends with the shell exiting: the last meaningful
content (the command output + the trailing prompt) precedes the exit, separated
by the final idle gap (the settle before the stop).

This script writes a trimmed .cast ending right after the content, so any
render (agg) ends on the test-output screen instead of the exit/blank screen.

Generic: the idle-gap threshold (0.5s) marks the content/exit boundary — a
longer or shorter command adapts automatically.

Usage: cast-trim-end.py <in.cast> <out.cast>
"""
import json
import sys

IDLE_THRESHOLD = 0.5  # seconds; an idle gap >= this separates content from the exit tail
MARGIN = 0.3          # seconds past the last content so the output is fully visible

t = 0.0
events = []
with open(sys.argv[1]) as f:
    header = f.readline().strip()
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        # asciinema v2/v3: [delta, "o"|"x"|..., data]
        if isinstance(ev, list) and len(ev) >= 3:
            t += float(ev[0])
            events.append((t, line))

last_content_t = events[-1][0] if events else 0
# The exit keystroke sits after the FINAL idle gap (the settle between the
# command output and the record: stop). Scan backwards for that gap.
for i in range(len(events) - 1, 0, -1):
    delta = events[i][0] - events[i - 1][0]
    if delta >= IDLE_THRESHOLD:
        last_content_t = events[i - 1][0]
        break

with open(sys.argv[2], "w") as out:
    out.write(header + "\n")
    for et, line in events:
        if et <= last_content_t + MARGIN:
            out.write(line + "\n")
        else:
            break
