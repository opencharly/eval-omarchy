# pr-10144 lane stats (calver 2026.251.1427)

verdict: PASS (probe RED exit 2 known-red verified; eval exit 0; lockIncidents 0)

## eval summary.yml phase rows
| step | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | True |
| vm-create | 1 | True |
| deploy-add | 14 | True |
| bring-up-members | 0 | True |
| check-live | 17 | True |
| gate-restart-stop | 1 | True |
| gate-restart-start | 0 | True |
| check-live-rebuild | 19 | True |
| cleanup | 3 | True |
| cleanup-members | 0 | True |
| **total_seconds** | 57 | |

## timestamps (ts lines from checkpoint)

## artifact sizes
/tmp/redo-wave2/media/pr-10144-2026.251.1427/pr-10144.cast 1352
/tmp/redo-wave2/media/pr-10144-2026.251.1427/pr-10144.gif 27662
/tmp/redo-wave2/media/pr-10144-2026.251.1427/pr-10144.mjpeg 782829
/tmp/redo-wave2/media/pr-10144-2026.251.1427/pr-10144-screen.mp4 76364
/tmp/redo-wave2/media/pr-10144-2026.251.1427/pr-10144-screen.png 1255334

lockIncidents: 0
| regate ts=1788877556.756
| probe-start ts=1788877564.688
| probe-end ts=1788877622.907
| orphan-clean ts=1788877636.957 probeDomainGone=yes
| eval-start ts=1788877639.828
| eval-end ts=1788877739.025
| evidence-done ts=1788877771.100
