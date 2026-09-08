# Lane 10139 — eval stats

- pr: 10139
- headSha: 38c07810ee3d06e22eaa069c630d7a33fbbf3475
- calver: 2026.251.1428
- verdict: PASS (RED-PROBE exit 2 known-red verified on golden; EVAL exit 0 with pr-behavior found after apply; media 5/5)
- probeExit: 2
- evalExit: 0

## Eval phase rows (from /tmp/redo-wave2/eval/evidence/REDO-WAVE/runs/pr-10139-eval-summary.yml)
| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 2 | true |
| deploy-add | 15 | true |
| bring-up-members | 0 | true |
| check-live | 18 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 0 | true |
| check-live-rebuild | 15 | true |
| cleanup | 3 | true |
| cleanup-members | 0 | true |
| **total_seconds** | **55** | |

## Probe phase rows (from pr-10139-probe-summary.yml): vm-build PASS 1.938s, vm-create PASS 2.038s, deploy-add PASS 13.431s, bring-up-members PASS 0s, check-live FAIL 5.108s (exit 2, pr-behavior known-red) — steps=5, run FAIL exit 2.

## ts values
- regate: 1788877552.135
- probe-start: 1788877663.649
- probe-end: 1788877663.650
- orphan-clean: 1788877679.375 (domstate error = domain gone)
- eval-start: 1788877778.583
- eval-end: 1788877778.584
- evidence-done: (see below append)

## Media artifacts (media/pr-10139-2026.251.1428/)
- pr-10139.cast: 820 B (threshold >= 200)
- pr-10139.gif: 11253 B (threshold >= 1024)
- pr-10139.mjpeg: 1202290 B (threshold >= 10240)
- pr-10139-screen.mp4: 103129 B (threshold >= 10240, host transcode from MJPEG via ffmpeg libx264)
- pr-10139-screen.png: 1255145 B (threshold >= 1024)
- media5of5: true

## Lock incidents
- lockIncidents (grep -m 5 'Failed to get' probe+eval logs | wc -l): 0
