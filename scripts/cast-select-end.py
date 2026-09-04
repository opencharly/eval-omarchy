#!/usr/bin/env python3
"""Compute the agg --select end that cuts the trailing exit sequence.

The record: stop types "exit" at the very end of the terminal session (the
asciinema .cast ends with the shell exiting). The last meaningful content (the
command output + the trailing prompt) precedes the exit, which is separated by
the settle idle — the FINAL idle gap. The select end = the last event before
that final idle gap, plus a small margin, so the rendered GIF ends on the test
output screen instead of the blank screen after the exit.

Generic: works for any .cast — the threshold (an idle gap of >= 0.5s) marks the
content/exit boundary, so a longer or shorter command adapts automatically.

Usage: cast-select-end.py <file.cast>   -> prints the select end in seconds
"""
import json
import sys

IDLE_THRESHOLD = 0.5  # seconds; an idle gap >= this separates content from the exit tail
MARGIN = 0.3          # seconds past the last content so the output is fully visible

t = 0.0
events = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            ev = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        # asciinema v2: [delta, "o"|"x", text]
        if isinstance(ev, list) and len(ev) >= 3:
            t += float(ev[0])
            events.append((t, ev[1]))

if not events:
    print("0.0")
    sys.exit(0)

total = events[-1][0]

# The exit keystroke sits at the very end, after the final idle gap (the settle
# between the command output and the record: stop). Scan backwards for that gap.
last_content = total
for i in range(len(events) - 1, 0, -1):
    delta = events[i][0] - events[i - 1][0]
    if delta >= IDLE_THRESHOLD:
        last_content = events[i - 1][0]
        break

select_end = min(last_content + MARGIN, total)
print(f"{select_end:.2f}")
