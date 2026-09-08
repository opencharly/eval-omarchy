# pr-10129 eval stats (REDO WAVE, fixed stack)

- PR: 10129
- headSha: 0681cadf28aae14f9cc46271ecb2af76e5958a36
- eval calver: 2026.251.1418
- probe calver: 2026.251.1416
- VERDICT: PASS (probeExit=2 known-red, evalExit=0)

## Probe phases (check-omarchy-pr-10129-vm-probe, exit 2)
| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 40 | true |
| vm-create | 2 | true |
| deploy-add | 14 | true |
| bring-up-members | 0 | true |
| check-live | 7 | false (known-red: pr-behavior absent on golden) |

## Eval phases (check-omarchy-pr-10129-vm, exit 0)
| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 3 | true |
| vm-create | 2 | true |
| deploy-add | 17 | true |
| bring-up-members | 0 | true |
| check-live | 18 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 1 | true |
| check-live-rebuild | 25 | true |
| cleanup | 7 | true |
| cleanup-members | 0 | true |

- total_seconds: 72

## Timestamps (epoch)
- regate: 1788876968.255
- probe-start: 1788876968.310
- probe-end: 1788877068.211
- orphan-clean: 1788877089.796
- eval-start: 1788877093.119
- eval-end: 1788877210.488

## Media artifacts (media/pr-10129-2026.251.1418/)
- pr-10129.cast: 1049 B
- pr-10129.gif: 17775 B
- pr-10129.mjpeg: 1443300 B
- pr-10129-screen.mp4: 107024 B
- pr-10129-screen.png: 1255219 B
- media5of5: true

## Lock ledger
- lockIncidents: 0
