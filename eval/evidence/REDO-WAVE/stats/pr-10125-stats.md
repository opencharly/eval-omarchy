# PR 10125 eval stats (REDO WAVE)

- calver: 2026.251.1419
- bed: check-omarchy-pr-10125-vm
- verdict line: probeExit=2 (known-red verified) evalExit=0 (pr-behavior found after apply) subject=PASS
- headSha: 399665b58a317c50ff134555a9d9188d10ab4c9e
- live-head drift at preflight: none (zero drift)

## eval phase rows (from summary.yml)
ROW	DURATION_S	OK
vm-build	2	true
vm-create	2	true
deploy-add	22	true
bring-up-members	0	true
check-live	24	true
gate-restart-stop	1	true
gate-restart-start	1	true
check-live-rebuild	24	true
cleanup	7	true
cleanup-members	0	true
total_seconds	81

## probe phase rows (from summary.yml)
vm-build	64	true
vm-create	2	true
deploy-add	18	true
bring-up-members	0	true
check-live	7	false
total_seconds	91

## ts values
probe-start	1788876988.452
probe-end	1788877113.135
orphan-clean	1788877133.639
eval-start	1788877139.962
eval-end	1788877272.275

## artifact sizes (media/pr-10125-2026.251.1419/)
pr-10125.cast	1209
pr-10125.gif	23738
pr-10125.mjpeg	1382844
pr-10125-screen.mp4	104379
pr-10125-screen.png	1251709
media5of5	true

## lock ledger
lockIncidents	0
