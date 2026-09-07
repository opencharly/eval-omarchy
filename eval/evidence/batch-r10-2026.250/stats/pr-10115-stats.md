# pr-10115 eval stats (exact timings — revalidation on the migrated lane)

probe run calver: 2026.250.1856  (check-omarchy-pr-10115-vm-probe — expected red, exit 2)
eval run calver:  2026.250.1859  (check-omarchy-pr-10115-vm — PASS, exit 0)

probe verdict: ok false (the known red)
eval verdict:  ok true

eval total_seconds: 52
probe total_seconds: 29

## eval phases (summary-eval.yml)

| phase | seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 1 | true |
| deploy-add | 14 | true |
| bring-up-members | 0 | true |
| check-live | 17 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 0 | true |
| check-live-rebuild | 15 | true |
| cleanup | 2 | true |
| cleanup-members | 0 | true |

## probe phases (summary-probe.yml)

| phase | seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 1 | true |
| deploy-add | 14 | true |
| bring-up-members | 0 | true |
| check-live | 13 | false (exit 2 — the known red) |

## media-window rows (artifact mtimes, host)

- /tmp/pr-10115.cast     980 B    21:00 (eval pull)
- /tmp/pr-10115.gif      19,367 B 21:00
- /tmp/pr-10115.mjpeg    923,778 B 21:00 (10 SPICE frames)
- media/pr-10115-2026.250.1859/pr-10115.mp4 93,803 B 21:03 (assembly transcode)
- media/pr-10115-2026.250.1859/pr-10115-screen.png 1,299,328 B 1280x800

check-live inner (eval): 11 steps, 10 passed, 0 failed, 1 skipped (rec-mp4, verify-only).
check-live inner (probe): 10 steps, 8 passed, 1 failed (pr-behavior — the known red), 1 skipped (rec-mp4).
