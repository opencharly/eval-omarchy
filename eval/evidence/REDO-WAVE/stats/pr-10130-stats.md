# pr-10130 lane stats (REDO WAVE)

- pr: 10130
- headSha: 21992f03f72c2b15bdeb135e9ae8e8bb21274e95
- calver: 2026.251.1418
- verdict: PASS (probe exit 2 known-red verified; eval exit 0)
- bed pin == live PR head: yes (zero drift)

## Eval phase rows (from eval summary.yml — .check/check-omarchy-pr-10130-vm/2026.251.1418/summary.yml)

| phase | duration_seconds | ok |
|---|---|---|
| vm-build | 1 | true |
| vm-create | 2 | true |
| deploy-add | 15 | true |
| bring-up-members | 0 | true |
| check-live | 20 | true |
| gate-restart-stop | 1 | true |
| gate-restart-start | 1 | true |
| check-live-rebuild | 24 | true |
| cleanup | 6 | true |
| cleanup-members | 0 | true |
| **total_seconds** | **70** | **ok: true** |

## check-live per-step evidence
- pr-apply: PASS exit=0 ('pr-apply 10130 21992f03f72c2b15bdeb135e9ae8e8bb21274e95 shell/plugins/lock/Service.qml test/shell.d/fixtures/lock-activity-reblank/shell.qml test/shell.d/lock-activity-reblank-test.sh')
- pr-behavior: PASS exit=0 (grep -qi blankArmed /usr/share/omarchy/shell/plugins/lock/Service.qml — diff-ADDED marker, proven-landing path)
- rec-start: PASS (asciinema, output /tmp/charly-recordings/pr-10130.cast)
- rec-spice-start: PASS (fps 5)
- rec-drive: PASS (drove 'grep -n blankArmed .../Service.qml; echo pr-10130-done')
- rec-screen-spice: PASS (1280x800, native SPICE decode)
- rec-spice-stop: PASS (frames: 10, bytes: 1152270)
- rec-stop: PASS (969 bytes /tmp/pr-10130.cast)
- rec-gif: PASS (15499 bytes /tmp/pr-10130.gif)
- record-verb-dispatches (non-PR-specific sanity): PASS

## Timeline (epoch ms)
- declare: 1788876970.641
- ssh-pre-drop: 1788876970.718
- regate: 1788876970.944
- probe-start: 1788876977.988
- probe-end: 1788877084.950 (probe ran ~107s)
- orphan-clean: 1788877094.646
- eval-start: 1788877097.728
- eval-end: 1788877218.197 (eval ran ~120s)

## Artifacts (media/pr-10130-2026.251.1418/)
- pr-10130.cast: 952 B (>= 200B)
- pr-10130.gif: 15499 B (>= 1KB)
- pr-10130.mjpeg: 1267420 B (>= 10KB)
- pr-10130-screen.mp4: 102304 B (>= 10KB)
- pr-10130-screen.png: 1251711 B (>= 1KB)
- media5of5: true

## Lock ledger
- lockIncidents: 0 ('Failed to get' / 'database is locked' in probe+eval logs: 0)
- reGate inventory: no wave VMs live at gate; sibling probes 10129/10115 in flight; golden fuser empty (no holder); zero lock strings.
