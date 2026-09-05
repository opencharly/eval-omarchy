# batch-m4-2026.247 / final4 wave — 2026-09-05 03:31–03:38

## Result: 3 PASS + 1 WEDGE — NOT the closure (32/32 NOT achieved)

| PR | run | total | ok |
|---|---|---|---|
| 10219 | final4-10219.service | 97s (systemd wall) | PASS (10/10 steps ok) |
| 10116 | final4-10116.service | 78s (systemd wall) | PASS (10/10 steps ok) |
| 10211 | final4-10211.service | 77s (systemd wall) | PASS (10/10 steps ok) |
| 10225 | final4-10225.service | >336s (frozen 5:48, killed) | WEDGE (hang recurred) |

Spec #94 git-op timeout+retry (spec HEAD bf10f96, PR #94 merged) HELD on the git-op path:
3 lanes completed in 77–97s with zero ls-remote storms / no deploy-add stalls — the dead-socket git-op hang did NOT recur.

## Wedge forensics — lane 10225

- Frozen >5 min: journal last movement = "[vm-create] PASS" 03:32:02; at 03:37:38 (5:48 elapsed)
  unit still active/running, proc 3759403 in futex_wait, zero children (no ssh probes, no git), CPU parked
  (utime 217→221 across 2 samples 10 s apart), bed .lock + vm-domain lock held, NO deploy-add.log created.
- Failing step: vm-create → pre-deploy SSH-readiness gate (runner never started deploy-add).
- One-line RCA: **stale ssh_config port vs fresh passt forward** — ssh_config stanza for
  charly-check-omarchy-pr-10225-vm carried Port 34281 (= the port of the PREVIOUS run 2026.248.0100,
  proven by its check-live.log "ssh user@127.0.0.1:34281"), while the live run's passt forward was
  LISTENING on 127.0.0.1:41351:22 (passt pid 3760880) → configured SSH endpoint refused, readiness
  wait has no timeout, lane parks forever.
- Guest itself booted fine (serial.log: login prompt 03:32:35, sshd OK, Network Online) — not a guest
  failure; the runner never even attempted an ssh probe.
- Cleanup done: systemctl stop final4-10225.service (Result=success), runner gone,
  charly vm destroy check-omarchy-pr-10225-vm --keep-deploy --if-exists rc=0, no stray procs,
  vm-domain lock released (zero-byte flock file remains, holder gone).

## Next-action pointer (not this task's scope)

Fix charly's ssh-fragment lifecycle: when a VM is recreated in a fresh check run, the existing
ssh_config host stanza must be UPDATED to the run's actual passt forward port (or the port must be
pinned per VM record so re-runs reuse it) — append-if-missing leaves a stale-port dead end on re-runs.
This is a NEW wedge phase (pre-deploy readiness), distinct from the spec-#94 git-op hang.
