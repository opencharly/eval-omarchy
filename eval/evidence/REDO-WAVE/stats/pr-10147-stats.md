# PR 10147 — eval stats (REDO-WAVE lane, B2)

- calver: 2026.251.1427
- verdict: PASS (probeExit 2 = known-red verified; evalExit 0 = pr-behavior found after apply; media 5/5; lockIncidents 0)
- bed: check-omarchy-pr-10147-vm
- probe bed: check-omarchy-pr-10147-vm-probe (PROBE_EXIT=2)
- headSha: 65fa55975f6e54757d3a087534f107b28005077b
- binary: /tmp/charly-r10-fixed/bin/charly (2026.251.1146)

## Eval phase rows (from eval summary.yml)

| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 2 | true |
| vm-create | 2 | true |
| deploy-add | 16 | true |
| bring-up-members | 0 | true |
| check-live | 17 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 1 | true |
| check-live-rebuild | 15 | true |
| cleanup | 3 | true |
| cleanup-members | 0 | true |
| **total_seconds** | **55** | **ok: true** |

## check-live internals (all steps)

pr-apply PASS (exit=0) → pr-behavior PASS (exit=0, VibeCAD grep on installed menu)

media loop: rec-start PASS, rec-spice-start PASS, rec-drive PASS (grep -n VibeCAD ... ; echo pr-10147-done),
rec-screen-spice PASS (1280x800), rec-spice-stop PASS (6 frames, 691146 bytes),
rec-stop PASS (cast 1114B), rec-gif PASS (19960B), rec-mp4 SKIP (verify-only — runner assembly transcodes)

## ts values (epoch seconds)

- declare: 1788877591
- ssh-fragment-pre-drop: 1788877591
- regate: 1788877591
- probe-start: 1788877598
- probe-end: 1788877656
- orphan-clean: 1788877672
- eval-start: 1788877677
- eval-end: 1788877773

## Media artifacts (media/pr-10147-2026.251.1427/)

| artifact | bytes | threshold | pass |
|---|---|---|---|
| pr-10147.cast | 1097 | >= 200 | yes |
| pr-10147.gif | 19960 | >= 1024 | yes |
| pr-10147.mjpeg | 721740 | >= 10240 | yes |
| pr-10147-screen.mp4 | 92541 | >= 10240 | yes |
| pr-10147-screen.png | 1255310 | >= 1024 | yes |

media 5/5: true

## Lock ledger

lockIncidents: 0 (grep -m 5 'Failed to get' probe.log eval.log → 0)
