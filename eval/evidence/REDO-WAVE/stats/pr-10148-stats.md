# PR 10148 eval stats (REDO-WAVE 2026-09-08)
- pr: 10148
- headSha: a68df9c8cac7a78925001006fe64d9f7bfbf9429 (live-head match verified)
- binary: /tmp/charly-r10-fixed/bin/charly 2026.251.1146 (plugin-vm v2026.251.1105 idempotent clone build)
- probeBed: check-omarchy-pr-10148-vm-probe  calver 2026.251.1426  exit 2 (know-RED verified)  total 25s
- evalBed: check-omarchy-pr-10148-vm      calver 2026.251.1427  exit 0 (PASS)  total 54s
- verdict: PASS — probe red (pr-behavior FAIL on golden), eval green (pr-apply landed the PR; pr-behavior found audient on the live system; media loop complete)
- probeExit: 2
- evalExit: 0

## Eval phase matrix (check-omarchy-pr-10148-vm / 2026.251.1427)
| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 2 | true |
| deploy-add | 14 | true |
| bring-up-members | 0 | true |
| check-live | 18 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 1 | true |
| check-live-rebuild | 16 | true |
| cleanup | 2 | true |
| cleanup-members | 0 | true |
| total_seconds | 54 | true |

## timestamps (ts lines from checkpoint)
- declare-lane-10148 1788877577.736
- regate 1788877577.882
- probe-start 1788877584.549
- probe-end 1788877642.497
- orphan-clean 1788877651.642
- eval-start 1788877655.344
- eval-end 1788877757.752

## media artifacts (media/pr-10148-2026.251.1427/)
- pr-10148.cast: 870 bytes (>= 200B OK)
- pr-10148.gif: 12343 bytes (>= 1KB OK)
- pr-10148.mjpeg: 1082133 bytes (>= 10KB OK)
- pr-10148-screen.mp4: 101056 bytes (>= 10KB OK)
- pr-10148-screen.png: 1255140 bytes (>= 1KB OK)
- media 5/5 PASS

## lock ledger
- lockIncidents: 0 (zero 'Failed to get' / 'database is locked' across probe+eval logs)
