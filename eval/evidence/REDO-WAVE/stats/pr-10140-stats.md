# PR 10140 stats (REDO WAVE, fixed stack)

- calver: 2026.251.1427
- verdict: PASS
- headSha: d06853a760955a09ef5a014a4f28584c6d1f0ec9
- binary: /tmp/charly-r10-fixed/bin/charly = 2026.251.1146

## Eval phase rows (check-omarchy-pr-10140-vm, summary 2026.251.1427)

| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 1 | true |
| deploy-add | 15 | true |
| bring-up-members | 0 | true |
| check-live | 17 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 1 | true |
| check-live-rebuild | 17 | true |
| cleanup | 3 | true |
| cleanup-members | 0 | true |

total_seconds: 55

## Probe phase rows (check-omarchy-pr-10140-vm-probe, summary 2026.251.1426)

| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 2 | true |
| deploy-add | 16 | true |
| bring-up-members | 0 | true |
| check-live | 6 | false (pr-behavior known-red, exit 2) |

total_seconds: 26

## ts values

- config-audit: 1788877574.726
- head-fresh: 1788877574.726
- binary: 1788877574.726
- ssh-pre-drop: 1788877574.726
- regate: 1788877565.021
- probe-start: 1788877578.265
- probe-end: 1788877632.970
- orphan-clean: 1788877649.786
- eval-start: 1788877649.786
- eval-end: 1788877747.898
- evidence-done: 1788877777.043

## Artifact sizes (media/pr-10140-2026.251.1427)

- pr-10140.cast: 1262 bytes (>= 200)
- pr-10140.gif: 28248 bytes (>= 1KB)
- pr-10140.mjpeg: 1082184 bytes (>= 10KB)
- pr-10140-screen.mp4: 100993 bytes (>= 10KB)
- pr-10140-screen.png: 1255146 bytes (>= 1KB)
- media 5/5

## Lock ledger

- lockIncidents: 0 (0 = clean; any >0 = FAIL-HARD LOCK)
