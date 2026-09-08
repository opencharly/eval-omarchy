# pr-10123 stats (REDO WAVE — idempotent clone build, plugin-vm v2026.251.1105, charly 2026.251.1146)

- calver (eval): 2026.251.1419
- calver (probe): 2026.251.1416
- verdict: PASS (probe known-red exit 2, eval exit 0, pr-behavior green after apply)
- pr: 10123 | headSha: 51c4cf8148922ccb6f213f6f399856ace93bff32 (matches live head)

## Probe (check-omarchy-pr-10123-vm-probe) — exit 2 (expected known-red)
| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 54 | true |
| vm-create | 2 | true |
| deploy-add | 20 | true |
| bring-up-members | 0 | true |
| check-live | 7 | false (pr-behavior FAIL: grep exit=2, marker absent on golden) |

## Eval (check-omarchy-pr-10123-vm) — exit 0
| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 2 | true |
| deploy-add | 21 | true |
| bring-up-members | 0 | true |
| check-live | 22 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 1 | true |
| check-live-rebuild | 24 | true |
| cleanup | 6 | true |
| cleanup-members | 0 | true |

- total_seconds: 78
- diagnostics: errors 0, warnings 0 (only allowlisted dev-worktree-binary-notice)

## Timestamps (ts label epoch)
- regate 1788876997.588
- probe-start 1788876997.591
- probe-end 1788877112.000 (probe-log mtime; script aborted before writing due to set -e on expected exit 2)
- orphan-clean 1788877135.734
- eval-start 1788877146.176
- eval-end 1788877274.242
- evidence-done 1788877301.224

## Media artifacts (media/pr-10123-2026.251.1419/)
| artifact | bytes | min | ok |
|---|---|---|---|
| pr-10123.cast | 1392 | 200 | true |
| pr-10123.gif | 30159 | 1000 | true |
| pr-10123.mjpeg | 1612812 | 10000 | true |
| pr-10123-screen.mp4 | 107348 | 10000 | true |
| pr-10123-screen.png | 1251622 | 1000 | true |

media 5/5.

## Lock ledger
- lockIncidents: 0 (grep 'Failed to get|database is locked' on probe+eval logs = 0)
