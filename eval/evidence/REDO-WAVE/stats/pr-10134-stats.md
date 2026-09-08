# pr-10134 stats
calver: 2026.251.1418
verdict: PASS (probe exit 2 known-red verified; eval exit 0; media 5/5; lockIncidents 0)

## eval phase rows (name, duration_seconds, ok)
- name: vm-build duration_seconds: 2 ok: true
- name: vm-create duration_seconds: 2 ok: true
- name: deploy-add duration_seconds: 17 ok: true
- name: bring-up-members duration_seconds: 0 ok: true
- name: check-live duration_seconds: 23 ok: true
- name: gate-restart-stop duration_seconds: 1 ok: true
- name: gate-restart-start duration_seconds: 1 ok: true
- name: check-live-rebuild duration_seconds: 22 ok: true
- name: cleanup duration_seconds: 3 ok: true
- name: cleanup-members duration_seconds: 0 ok: true
total_seconds: 72

## ts values
probe-start: 1788877000.284
probe-end: 1788877082.493
orphan-clean: 1788877102.887
eval-start: 1788877116.775
eval-end: 1788877235.780

## artifact sizes
cast: 988
gif: 14399
mjpeg: 1037421
mp4: 98234
screenPng: 1251704

## locks
lockIncidents: 0
