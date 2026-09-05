# M4-batch matrix — vc1 wave (32 lanes, cpu-1/VM restart-only, 2026-09-05 ~01:36–01:43 local)

Bed set: `charly check run check-omarchy-pr-<N>-vm` per PR; systemd user units vc1-<N>
(run dir calver **2026.247.2337**). Observed read-only; no lane touched, nothing killed.

## Verdict

- **12/32 PASS** (eval ok=true, all 10 steps) — mean total **228 s** (band 209–257 s).
- **1/32 eval FAIL** — 10215 (check-live; details below).
- **19/32 launch-FAIL** — charly concurrent-run guard at bed start: a leftover wave
  (16 `charly check run` procs launched 01:31:51, calver 2332, NOT vc1-* units) still held
  those beds' `.check/check-omarchy-pr-<N>-vm/.lock` when wave vc1 started 01:36:35.
  All 19 exited in 35–47 s (mean 41.8 s) with `refusing a concurrent run (lock: …)`.
  The leftover wave finished on its own by ~01:42 (observed exiting; not killed).
- Wave wall: 01:36:35 → ~01:43:30 ≈ **7.0 min**; 12 real evals → 1.7 evals/min realized
  (19 lanes never ran).

## Rows (32)

| PR | run | deploy-add_s | check-live_s | total_s | ok | note |
|---|---|---|---|---|---|---|
| 10115 | 2337 | 84 | 34 | 218 | PASS | |
| 10116 | 2337 | 86 | 33 | 215 | PASS | |
| 10123 | 2337 | 87 | 37 | 222 | PASS | |
| 10125 | 2337 | 83 | 42 | 230 | PASS | |
| 10129 | 2337 | 79 | 34 | 215 | PASS | |
| 10130 | 2337 | 84 | 61 | 250 | PASS | |
| 10134 | 2337 | 83 | 60 | 248 | PASS | |
| 10136 | 2337 | 81 | 33 | 218 | PASS | |
| 10138 | 2337 | 85 | 63 | 257 | PASS | |
| 10140 | 2337 | 92 | 37 | 223 | PASS | |
| 10144 | 2337 | 78 | 32 | 209 | PASS | |
| 10208 | 2337 | 86 | 49 | 234 | PASS | |
| 10215 | 2337 | 79 | 34 | 159 | **FAIL** | check-live: pr-apply git tree read err 128 + 3 dependent calendar checks |
| 10139 | — | — | — | 46.1 | FAIL-lock | launch: bed lock held by leftover 01:31:51 wave |
| 10141 | — | — | — | 46.9 | FAIL-lock | same |
| 10146 | — | — | — | 41.7 | FAIL-lock | same |
| 10147 | — | — | — | 39.7 | FAIL-lock | same |
| 10148 | — | — | — | 46.4 | FAIL-lock | same |
| 10199 | — | — | — | 43.7 | FAIL-lock | same |
| 10200 | — | — | — | 41.1 | FAIL-lock | same |
| 10202 | — | — | — | 41.6 | FAIL-lock | same |
| 10205 | — | — | — | 34.5 | FAIL-lock | same |
| 10210 | — | — | — | 47.2 | FAIL-lock | same |
| 10211 | — | — | — | 39.6 | FAIL-lock | same |
| 10212 | — | — | — | 47.1 | FAIL-lock | same |
| 10217 | — | — | — | 41.2 | FAIL-lock | same |
| 10219 | — | — | — | 44.1 | FAIL-lock | same |
| 10222 | — | — | — | 35.2 | FAIL-lock | same |
| 10224 | — | — | — | 38.5 | FAIL-lock | same |
| 10225 | — | — | — | 44.9 | FAIL-lock | same |
| 10228 | — | — | — | 39.2 | FAIL-lock | same |
| 10229 | — | — | — | 35.0 | FAIL-lock | same |

## Per-phase numbers (12 PASS lanes, calver 2337)

| phase | mean_s | vs cpu-2 32-lane |
|---|---|---|
| vm-build | 9.0 | |
| vm-create | 37.1 | |
| **deploy-add** | **84.0** | was **104 s → −19%** |
| bring-up-members | 0 | |
| **check-live** | **42.9** | was **73 s → −41%** |
| gate-restart-stop | 8.0 | |
| gate-restart-start | 8.0 | |
| check-live-rebuild | 29.7 | |
| cleanup | 9.7 | |
| cleanup-members | 0 | |
| **total** | **228.3** | was **312 s → −27%** |

## The comparison the operator asked for

- **deploy-add dropped: yes** — mean 104 s (cpu-2 wave) → **84.0 s** (this wave), and all 13
  measured lanes ≤ 92 s (band 78–92) with 79–87 typical. No 100 s+ stragglers.
- evals/min: at the improved per-eval cost, 32 × 60 / 228.3 ≈ **8.4 evals/min** projected
  (vs 6.16). Realized this wave: 1.7/min because 19 lanes were lock-guarded at launch.
- Caveat: this wave's check-live ran while the leftover 01:31:51 wave was still finishing on
  the same host (16 procs down to 0 by ~01:42), so timings are measured under residual
  contention — the drop is real but the clean-room number needs a lock-free re-run.

## Failed lanes → RCA (one line each)

- 19× lock: at 01:36:35 launch, charly found the bed's `.lock` held by the STILL-RUNNING
  leftover wave from 01:31:51 (16 procs observed; calver-2332 run dirs) → `refusing a
  concurrent run` → exit 1. Fix belongs to launch sequencing (verify no earlier wave's
  procs/locks before launching), not to this wave's code. Needs REDO re-run of the 19.
- 10215: [check-live] FAIL after 34 s, exit 2 — 4 checks failed, root = [pr-apply]
  `fatal: unable to read tree (6ebb7e1b319a9f477d8242d02fefa62e886339bb)` (git exit 128)
  → patch never applied → 3 dependent calendar/planner checks missing files
  (`omarchy-calendar` bin, PlannerModel.js, calendar cmd group). Env-flavored git-tree
  read failure in the guest, not a PR-content failure; VM left running for debug by charly.
  Needs REDO re-run to confirm.

*Observed passively by the monitoring lane; no vc1-* lane, process, or bed was modified.
Leftover-wave exit was its own; nothing was killed.*
