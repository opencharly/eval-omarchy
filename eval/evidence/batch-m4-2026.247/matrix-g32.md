# matrix-g32 — 32-lane batch, restart-only update_gate (no recreate)

- **Date/window**: 2026-09-05 01:17:38 → 01:27:53 CEST (wall **615 s** = 10m15s)
- **Units**: systemd user units `ug3-*` (systemd-run --user, cwd = eval-omarchy, `--setenv=PATH=/usr/bin:/bin`, WorkingDirectory=eval-omarchy). Pre-batch failures recorded: `ugeval-*` (01:13:40) 32× unstamped-binary freshness gate; `ugeval2-*` (01:16:30) 32× wrong-cwd `no entity …-vm`; the live wave is the parent-started `ug3-*`. A momentary duplicate smoke (ugeval3-10115) was deduped.
- **Binary**: charly 2026.247.2250 (stamped, `task build:binary` at 01:16:23)
- **Gate**: `update_gate: restart-only` — vm stop/start instead of recreate

## Rows (PR | run | total_seconds | ok)

| PR | run | total_seconds | ok |
|---|---|---|---|
| 10115 | 2026.247.2317 | 329 | Y |
| 10116 | 2026.247.2318 | 333 | Y |
| 10123 | 2026.247.2317 | 319 | Y |
| 10125 | 2026.247.2317 | 330 | Y |
| 10129 | 2026.247.2317 | 332 | Y |
| 10130 | 2026.247.2317 | 326 | Y |
| 10134 | 2026.247.2317 | 323 | Y |
| 10136 | 2026.247.2318 | 332 | Y |
| 10138 | 2026.247.2317 | 328 | Y |
| 10139 | 2026.247.2318 | 331 | Y |
| 10140 | 2026.247.2317 | 332 | Y |
| 10141 | 2026.247.2317 | 314 | Y |
| 10144 | 2026.247.2317 | 334 | Y |
| 10146 | 2026.247.2317 | 335 | Y |
| 10147 | 2026.247.2317 | 330 | Y |
| 10148 | 2026.247.2317 | 329 | Y |
| 10199 | 2026.247.2317 | 337 | Y |
| 10200 | 2026.247.2317 | 334 | Y |
| 10202 | 2026.247.2317 | 324 | Y |
| 10205 | 2026.247.2318 | 331 | Y |
| 10208 | 2026.247.2317 | 334 | Y |
| 10210 | 2026.247.2317 | 337 | Y |
| 10211 | 2026.247.2317 | 326 | Y |
| 10212 | 2026.247.2317 | 308 | Y |
| 10215 | 2026.247.2317 | 237 | N |
| 10217 | 2026.247.2317 | 332 | Y |
| 10219 | 2026.247.2318 | 111 | Y |
| 10222 | 2026.247.2317 | 211 | N |
| 10224 | 2026.247.2318 | 329 | Y |
| 10225 | 2026.247.2318 | 332 | Y |
| 10228 | 2026.247.2317 | 213 | N |
| 10229 | 2026.247.2317 | 325 | Y |
| **Σ 32** | | **9978** | **29Y / 3N** |

## Verdict — decisive evals/min datapoint at 32 lanes, restart-only gate

- **total band (all 32): 111–337 s**; success band **308–337 s** (excl. 10219 warm outlier; the 3 N lanes stop at check-live, 211–237 s)
- avg total = **311.8 s** (Y-only 321.3 s; median 329.5 s)
- **evals/min = 6.16** (32 lanes × 60 / 311.8 s) — operator target ≤60 s/eval (≈32/min at 32 lanes): **NOT met, ~5–6× above target**
- wall-based throughput: 32 / 10m15s = **3.1 evals/min**
- **The restart-only gate did NOT clear ≤60 s**: long poles are `deploy-add` (@github ref-resolution fanout, 20–130 s; mean 101.5) and `check-live` (59–96 s; mean 72.3) — both gate-independent.

## Per-phase ledger (all 32 lanes, seconds)

| phase | mean | median | min | max |
|---|---|---|---|---|
| vm-build | 9.5 | 10 | 7 | 12 |
| vm-create | 33.7 | 33.5 | 29 | 38 |
| deploy-add | 101.5 | 111 | 20 | 130 |
| bring-up-members | 0 | 0 | Infinity | 0 |
| check-live | 72.3 | 71 | 19 | 96 |
| gate-restart-stop | 20.9 | 23.5 | 4 | 32 |
| gate-restart-start | 18 | 19 | 3 | 30 |
| check-live-rebuild | 40.8 | 43 | 16 | 65 |
| cleanup | 15.1 | 14.5 | 5 | 32 |
| cleanup-members | 0 | 0 | Infinity | 0 |

## Failures (3) — all at [check-live] exit 2

| PR | total | failed checks | cause |
|---|---|---|---|
| 10222 | 211 | 1/11: [pr-behavior-2] power-source-change hook example absent (exit 1) | **genuine behavior miss** (pr-apply + pr-behavior + media passed) |
| 10215 | 237 | 4/12: [pr-apply] exit 128 `fatal: unable to read tree (6ebb7e1…)` → 3 behavior cascades | **infra: git tree object unavailable at pr-apply** |
| 10228 | 213 | 2/10: [pr-apply] exit 128 `fatal: unable to read tree (f0bc41…)` → behavior cascade | **infra: git tree object unavailable at pr-apply** |

Note: failed lanes leave their VM running by design (FAIL-leaves-VM); destroy via `charly vm destroy omarchy-vm-clone-<N> --domain check-omarchy-pr-<N>-vm`. Media contract held on all 32 (cast/gif/spice recorded even on failures).

## Fast + slow lane phase profiles (deploy-add / check-live / gate-restart-stop / gate-restart-start / chk-live-rebuild / cleanup)

| PR | total | deploy-add | check-live | gate-restart-stop | gate-restart-start | chk-live-rebuild | cleanup |
|---|---|---|---|---|---|---|---|
| 10219 | 111 | 20 | 19 | 4 | 3 | 16 | 5 |  ← fast (111 s; warm-cache tail lane)
| 10199 | 337 | 92 | 81 | 19 | 26 | 58 | 19 |
| 10210 | 337 | 72 | 79 | 29 | 23 | 58 | 30 |
| 10215 | 237 | 127 | 65 | — | — | — | — |  ← slowest deploy-add (N, died at check-live)
| 10136 | 332 | 130 | 63 | 30 | 18 | 37 | 10 |  ← slowest deploy-add (Y)

## Anomalies

1. **10219 unphased stall**: 7m16s gap vm-create PASS (01:19:18) → [deploy-add] START (01:26:34); then all phases warm (deploy-add 20 s). Signature = M5 @github ref-resolution serialization; the tail lane pays the full wait.
2. **10115 run dir 2026.247.2317 momentarily shared** with the ugeval3-10115 smoke duplicate (killed on lock contention; parent lane ran clean).
3. **ugeval/ugeval2 pre-batch failures** (not in this matrix): 32× unstamped binary (01:13:40), 32× wrong-cwd no-entity (01:16:30).

## Next hill-climb candidates (evidence-backed)

- deploy-add @github ref-resolution fanout: 8/32 lanes ≥124 s (10115 125, 10136 130, 10144 124, 10146 129, 10205 128, 10211 124, 10217 124, 10224 128) → host-side shared resolution or bounded mutex, reproduced at 32 lanes.
- check-live 72.3 s mean: per-VM ssh check suite ≈ 1/4 of each lane.
- pr-apply `unable to read tree` (10215/10228): confirm the PR-checkout ref completeness before rerun.

*Collected by omarchy-eval supervisor lane monitor (01:17:38–01:27:53 CEST); rows from .check/check-omarchy-pr-<N>-vm/*/summary.yml (mtime ≥ 01:16:00), unit exits via journalctl ug3-*.*