# M4-batch matrix — c12 wave (12 lanes, sdk #206 materialized-tree cache, 2026-09-05 ~01:57:44–02:05 CEST)

Bed set: `charly check run check-omarchy-pr-<N>-vm` per PR; systemd user units **c12-<N>**
(run dir calver **2026.247.2357**; launched 01:57:44, MainPID sequence 3520942→3521077).
Binary: charly 2026.247.2250, rebuilt 01:57 with local sdk @ **a01cdb2** carrying
`27b90d6 feat(loaderkit): cache the materialized merged deploy tree across CLI-subcommand
children (#206)` — the 32-lane stall's designated root fix under test. Observed read-only
except the one FAIL lane's VM cleanup (10130).

## Verdict

- **11/12 PASS** (eval ok=true, all steps green) — mean total **369.4 s** (band 365–374 s).
- **1/12 FAIL** — 10130 (deploy-add; below).
- **KEY MEASURE — deploy-add did NOT drop, it ~4x'ed**: PASS lanes flat **324–326 s**
  (mean 325.5 s) vs the vc1 cpu-1 baseline mean **84.0 s** (band 78–92). No later-lane
  windfall: all 11 finished deploy-add inside a 2.4 s window (deploy-add.log mtimes
  02:03:39.36–02:03:41.76) regardless of start order. The FAIL lane 10130 died at 135 s.
- evals/min: 11 PASS × 60 / 369.4 ≈ **1.79 at 12 lanes** vs vc1's realized 1.7 (which had
  19 lock-failed lanes) — no net gain; per-eval cost is *worse* end to end.

## The comparison the operator asked for (cpu-1 waves vs this cache wave)

| metric | vc1 cpu-1 (no cache) | c12 (sdk #206 cache) | delta |
|---|---|---|---|
| deploy-add mean | 84.0 s | **325.5 s** (PASS) | **+287 % (worse)** |
| deploy-add band | 78–92 | 324–326 | 4× |
| check-live mean | 42.9 s | 18.5 s | −57 % |
| check-live-rebuild mean | 29.7 s | 17.6 s | −41 % |
| cleanup mean | 9.7 s | 3.1 s | −68 % |
| total mean | 228.3 s | 369.4 s | +62 % |

## Rows (12)

| PR | run | deploy-add_s | check-live_s | chk-live-rebuild_s | cleanup_s | total_s | ok | note |
|---|---|---|---|---|---|---|---|---|
| 10115 | 2357 | 326 | 17 | 19 | 3 | 370 | PASS | |
| 10116 | 2357 | 325 | 18 | 17 | 3 | 368 | PASS | |
| 10123 | 2357 | 326 | 19 | 18 | 3 | 370 | PASS | |
| 10125 | 2357 | 324 | 15 | 17 | 4 | 365 | PASS | |
| 10129 | 2357 | 324 | 15 | 17 | 4 | 365 | PASS | |
| 10130 | 2357 | 135 | — | — | — | 138 | **FAIL** | deploy-add: ls-remote exit 128 (below) |
| 10134 | 2357 | 326 | 17 | 18 | 4 | 369 | PASS | |
| 10136 | 2357 | 326 | 24 | 16 | 2 | 374 | PASS | |
| 10138 | 2357 | 326 | 17 | 19 | 3 | 370 | PASS | |
| 10139 | 2357 | 326 | 24 | 17 | 2 | 374 | PASS | |
| 10140 | 2357 | 326 | 16 | 18 | 3 | 368 | PASS | |
| 10141 | 2357 | 325 | 18 | 19 | 3 | 370 | PASS | |

## Per-phase ledger (11 PASS lanes, calver 2357)

| phase | mean_s | vs vc1 |
|---|---|---|
| vm-build | 1.0 | 9.0 → −89 % |
| vm-create | 2.6 | 37.1 → −93 % |
| **deploy-add** | **325.5** | 84.0 → **+287 %** |
| bring-up-members | 0 | |
| check-live | 18.5 | 42.9 → −57 % |
| gate-restart-stop | 1.0 | 8.0 |
| gate-restart-start | 1.0 | 8.0 |
| check-live-rebuild | 17.6 | 29.7 → −41 % |
| cleanup | 3.1 | 9.7 |
| cleanup-members | 0 | |
| **total** | **369.4** | 228.3 → +62 % |

## Why the cache did not cut the later lanes (observed mechanism)

- The #206 key is **per-lane by design**: a SHA-256 over the walk envelope, which embeds the
  bed's deploy target (`vm:check-omarchy-pr-<N>-vm` visible inside the cached json at
  ~/.cache/charly/materialized/*.json). 12 distinct beds ⇒ 12 distinct keys ⇒ **zero
  cross-lane reuse**; lane 2+ never sees lane 1's materialization.
- The deploy-add long pole is the **@github latest-tag resolution fanout**, which the
  materialize cache does not cover: during deploy-add, each of the 11 `charly fleet add
  ... --dev-local-pkg` procs spawned ~10 concurrent `git ls-remote` (layer-*, plugin-*,
  plugin-deploy-vm) → **90–94 concurrent ls-remote procs at peak**, waves respawned every
  ~2 min (observed etime resets 00:41 → 00:35/00:36), loader ~26 then drifted down to ~6.7.
  Every lane pays the full throttled wait; all 11 unblocked in the same ~2 s window.
- Net: vm-build/vm-create/check-live/cleanup all got *faster* (low contention, warm images),
  but deploy-add's fanout dominates and regressed; the cache neither created a warm-lane
  effect nor touched the actual bottleneck.

## Failed lane → RCA (one line each)

- **10130** [deploy-add] after 135 s: `charly: error: command "fleet": scan deploy plugins:
  deploy add_candy: cannot resolve latest tag for github.com/opencharly/plugin-deploy-vm:
  git ls-remote --tags https://github.com/opencharly/plugin-deploy-vm.git: exit status 128`
  → transient github ls-remote failure (exit 128, likely throttling) inside the 90+ proc
  burst at 01:58–02:00; a direct probe succeeded minutes later (rc=0). Env/network-flavored,
  not PR-content (deploy-add precedes any PR-apply). FAIL-leaves-VM cleaned up:
  `charly vm destroy omarchy-vm-clone-10130 --domain check-omarchy-pr-10130-vm --if-exists`
  → destroyed; `virsh list` confirms no 10130 domain remains.

*Collected by omarchy-eval supervisor lane monitor (01:57:44–02:05:16 CEST); rows from
.check/check-omarchy-pr-<N>-vm/2026.247.2357/summary.yml + deploy-add.log mtimes; unit
exits via systemctl --user show c12-*. No c12 lane, process, or bed was modified beyond the
mandated FAIL-VM cleanup.*
