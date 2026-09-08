# PR #10138 eval stats — REDO WAVE (fixed stack)
- pr: 10138
- headSha: 87f2bf1e72e60de3a49531f0e65aeb7c5d4f5f02
- evalCalver: 2026.251.1419 (eval summary /tmp/redo-wave2/eval/evidence/REDO-WAVE/runs/pr-10138-eval-summary.yml)
- probeCalver: 2026.251.1417 (probe summary /tmp/redo-wave2/eval/evidence/REDO-WAVE/runs/pr-10138-probe-summary.yml)
- verdict: PASS (probe exit 2 = known-red verified on golden; eval exit 0 = pr-behavior found live after apply; media loop complete)
- subject: PASS

## ts ledger
ts regate 1788877022
  regate-inventory:
1788877022.425 probe-start
1788877108.069 probe-end
ts orphan-clean 1788877132
1788877141.166 eval-start
1788877268.086 eval-end
ts evidence-done 1788877297


## eval phases (check-omarchy-pr-10138-vm, calver 2026.251.1419)
- vm-build: duration 2s ok=true
- vm-create: duration 2s ok=true
- deploy-add: duration 22s ok=true
- bring-up-members: duration 0s ok=true
- check-live: duration 23s ok=true
- gate-restart-stop: duration 1s ok=true
- gate-restart-start: duration 1s ok=true
- check-live-rebuild: duration 23s ok=true
- cleanup: duration 6s ok=true
- cleanup-members: duration 0s ok=true
- total_seconds: 79
- bed overall: ok=true (exit 0)

## probe phases (check-omarchy-pr-10138-vm-probe, calver 2026.251.1417) — known-red
- vm-build 24s ok, vm-create 2s ok, deploy-add 19s ok, bring-up-members 0s ok, check-live 7s ok=FALSE (pr-behavior fails on golden by construction), total_seconds 52, bed ok=false (exit 2)

## media artifacts (media/pr-10138-2026.251.1419/)
- pr-10138.cast 1075B (>=200)
- pr-10138.gif 19084B (>=1K)
- pr-10138.mjpeg 1443817B (>=10K)
- pr-10138-screen.mp4 107236B (>=10K, ffmpeg transcode)
- pr-10138-screen.png 1255287B (>=1K)
- media 5/5

## locks
- lockIncidents: 0 (Failed-to-get count across probe+eval run logs = 0)
