# PR 10146 — REDO-WAVE eval stats

- calver: 2026.251.1427
- bed: check-omarchy-pr-10146-vm
- probeCalver: 2026.251.1426
- verdict: PASS
- subject: PASS
- headSha: a3e951158dcac624ced50d4df9b0a33e68539468
- reGate: zero live omarchy domains; no sibling 10146 run; fuser on golden disk empty (read-only backing confirmed)
- probeExit: 2 (pr-behavior FAIL on golden = known-red verified)
- evalExit: 0

## Eval phase rows (from summary.yml 2026.251.1427)

| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 1 | true |
| deploy-add | 14 | true |
| bring-up-members | 0 | true |
| check-live | 18 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 0 | true |
| check-live-rebuild | 17 | true |
| cleanup | 3 | true |
| cleanup-members | 0 | true |

total_seconds: 55

## Per-check matrix (check-live)

- pr-apply: PASS exit=0
- pr-behavior: PASS exit=0
- rec-start: PASS
- rec-spice-start: PASS
- rec-drive: PASS
- rec-screen-spice: PASS (1280x800 native SPICE)
- rec-spice-stop: PASS (9 frames, 1036854 bytes)
- rec-stop: PASS (1047 bytes .cast)
- rec-gif: PASS (17845 bytes)
- rec-mp4: SKIP (verify-only mode, mutating step — host assembly transcodes)
- record-verb-dispatches: PASS

## Timestamps (ts ledger)

regate + probe-start/probe-end + orphan-clean + eval-start/eval-end + evidence-done in /tmp/redo-wave2-CHECKPOINT/pr-10146.md

## Media artifacts (media/pr-10146-2026.251.1427/)

- pr-10146.cast: 1013 bytes (>= 200 OK)
- pr-10146.gif: 17845 bytes (>= 1KB OK)
- pr-10146.mjpeg: 924606 bytes (>= 10KB OK)
- pr-10146-screen.mp4: 93974 bytes (>= 10KB OK)
- pr-10146-screen.png: 1299570 bytes (>= 1KB OK)
- media5of5: true

## Lock ledger

lockIncidents: 0 (zero 'Failed to get' / 'database is locked' across probe + eval logs)
