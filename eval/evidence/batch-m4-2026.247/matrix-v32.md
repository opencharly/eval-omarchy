# Batch M4-2026.247 — 32-lane wave v32 (sdk #207 cached latest-tag route)

**Wave**: 32 systemd units `v32-*` (`charly check run check-omarchy-pr-<N>-vm`), launched 02:15:34–02:16:30, all 32 exited by 02:21:37.
**Run calvers pinned**: 2026.248.0015 (10141) / 2026.248.0016 (all others) — a later full re-run wave (calver 0024) wrote into the same bed dirs; see the reproducibility note below. All v32-phase numbers below are read from the pinned calvers only.
**Binary**: `/home/atrawog/Sync/Atrapub/coder/pi/opencharly/charly/bin/charly` — local-sdk build carrying sdk #207 (cached-latest-tag route replacing version-less `git ls-remote` ref-resolution fanout).
**Verdict on the fanout fix: WORKS.** deploy-add collapsed to a mean of **38.1 s** (median 41 s) from 84–104 s (cpu-1 wave) / 325 s (c12 wave). Sampled concurrent `git ls-remote` was **0 across the bulk window** (pre-fix: 90–94 sustained); a single tail spike of **20** while the last 2 lanes cold-fetched their uncached 43-repo metadata set — the bounded residual of the warm 1h cache.

## Per-lane rows (ledger = summary.yml of the pinned v32 calver)

| PR | run | ok | total | vm-build | vm-create | deploy-add | check-live | cl-rebuild | failing step |
|---|---|---|---|---|---|---|---|---|---|
| 10115 | 0016 | false | 120s | 1 | 6 | 40 | 38 | 29 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10116 | 0016 | false | 153s | 2 | 5 | 43 | 54 | 44 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10123 | 0016 | false | 159s | 1 | 5 | 44 | 62 | 42 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10125 | 0016 | false | 156s | 2 | 4 | 43 | 64 | 38 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10129 | 0016 | false | 147s | 2 | 5 | 41 | 59 | 34 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10130 | 0016 | false | 158s | 2 | 6 | 45 | 61 | 39 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10134 | 0016 | false | 148s | 1 | 5 | 41 | 55 | 42 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10136 | 0016 | false | 126s | 2 | 5 | 39 | 41 | 35 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10138 | 0016 | false | 150s | 3 | 4 | 40 | 60 | 38 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10139 | 0016 | false | 155s | 2 | 6 | 42 | 55 | 45 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10140 | 0016 | false | 160s | 1 | 5 | 41 | 58 | 49 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10141 | 0015 | true | 83s | 0 | 1 | 11 | 15 | 32 | - |
| 10144 | 0016 | false | 135s | 2 | 5 | 43 | 46 | 35 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10146 | 0016 | false | 108s | 1 | 5 | 30 | 37 | 29 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10147 | 0016 | false | 159s | 1 | 5 | 39 | 56 | 51 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10148 | 0016 | true | 50s | 3 | 5 | 11 | 14 | 13 | - |
| 10199 | 0016 | true | 160s | 1 | 5 | 43 | 55 | 41 | - |
| 10200 | 0016 | true | 156s | 1 | 5 | 39 | 60 | 36 | - |
| 10202 | 0016 | true | 49s | 1 | 6 | 11 | 14 | 13 | - |
| 10205 | 0016 | false | 137s | 1 | 6 | 41 | 43 | 42 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10208 | 0016 | false | 116s | 2 | 5 | 36 | 37 | 30 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10210 | 0016 | false | 147s | 1 | 5 | 41 | 58 | 38 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10211 | 0016 | true | 143s | 1 | 6 | 40 | 45 | 39 | - |
| 10212 | 0016 | false | 129s | 1 | 5 | 46 | 41 | 32 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10215 | 0016 | true | 155s | 1 | 5 | 40 | 52 | 43 | - |
| 10217 | 0016 | false | 162s | 1 | 5 | 53 | 51 | 45 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10219 | 0016 | true | 170s | 1 | 5 | 44 | 59 | 44 | - |
| 10222 | 0016 | false | 74s | 1 | 3 | 33 | 37 | - | check-live |
| 10224 | 0016 | true | 167s | 1 | 6 | 42 | 62 | 44 | - |
| 10225 | 0016 | false | 115s | 2 | 6 | 35 | 36 | 30 | rec-screen-spice/rec-spice-stop (blank SPICE) |
| 10228 | 0016 | true | 121s | 1 | 5 | 38 | 36 | 31 | - |
| 10229 | 0016 | true | 161s | 1 | 5 | 43 | 57 | 40 | - |

## Fanout samples (`ps aux | grep -c '[g]it ls-remote'`)

| ts | concurrent ls-remote | notes |
|---|---|---|
| 02:16:25 | 1 | baseline (vm-build/vm-create phase; observation start) |
| 02:19:37 | 0 | bulk lanes past deploy-add (check-live/rebuild), load1=58.3 |
| 02:19:46 | 0 | load1=57.4 |
| 02:20:17 | 0 | 28/32 have summary.yml; 10148+10202 still in vm-create; load1=57.6 |
| 02:20:48 | 20 | tail spike: 10148+10202 in deploy-add, uncached 43-repo metadata fetch; load1=36.2 |
| 02:21:10 | 0 | |
| 02:21:20 | 0 | |
| 02:21:30 | 0 | |
| 02:22:08 | 0 | post-wave baseline |

Pre-fix comparator: 90–94 concurrent for the WHOLE deploy-add window of the 16-lane wave (futex-stuck lane children, GitHub throttling, deploy-add 84–325 s). Per-lane logs under the fix show `Resolved @github.com/opencharly/{plugin,layer}-* -> (latest tag)` + `charly: git metadata cached` (e.g. deploy-add.log of 10148: the 43-repo fetch completed inside an 11 s deploy-add).

## The band

- Launch: 02:15:34 (10141) → 02:16:30 (remaining 31).
- First lane done: **02:17:32** (10141, 83 s). Last lane done: **02:21:37** (10148).
- Completion band (first→last summary.yml): **245 s (4m05s)**; wave wall from first launch to last done: **363 s (6m03s)**.
- Tail bottleneck shifted from deploy-add to **vm-create queue serialization** at 32-lane oversubscription: 10148+10202 sat in vm-create ~02:16→02:20 (phase snapshots, host load1 57–58 on 16c) while 30 other lanes finished; their own deploy-add then took 11 s from the warm cache. vm-create queue = new longest-pole candidate.

## Headline numbers (ledger-based)

- Mean total **135.3 s** (median 147.5 s) · mean deploy-add **38.1 s** (median 41 s) · mean check-live 47.4 s · mean check-live-rebuild 37.7 s (31 lanes).
- **evals/min = 32×60/135.3 = 14.2** (ledger convention) — under the 16/min target because 32 lanes oversubscribe a 16c host 2×. Wall throughput: 32 evals / 363 s ≈ 5.3/min. Host load1 57–58 during bulk → 36 after; RAM 123 GiB, 57 GiB available; disk 35%.
- **Lock errors: 0** across every v32 run log ('database is locked' / 'Failed to get shared' — none).
- Results: **11/32 PASS, 21/32 FAIL** (verify-only mode — rec-mp4 transcode skipped by design).

## FAILs — failing step + one-line RCA

| PRs (n) | step | RCA (one line) |
|---|---|---|
| 10115 10116 10123 10125 10129 10130 10134 10136 10138 10139 10144 10146 10147 (13) | check-live-rebuild → rec-screen-spice | SPICE screenshot uniform near-black RGBA 17,17,17 — display not yet rendered in the rebuild phase after gate-restart; visual-capture race, independent of the ref-resolution fix. |
| 10140 10205 10208 10210 10212 10217 10225 (7) | check-live-rebuild → rec-spice-stop | SPICE MJPEG artifact uniform black RGBA 0,0,0 — same family: blank display capture during rebuild bring-up (all frames pre-render). |
| 10222 (1) | check-live → pr-behavior-2 | grep exit 2: expected hook sample `/usr/share/omarchy/config/omarchy/hooks/power-source-change.d/show-power-source-notification.sample` absent — plan↔PR-content mismatch (PR 10222 ships the sample at a different path or not at all). |

RCA grouping: the 20 rebuild-phase visual fails are ONE defect family (blank SPICE display after guest display-stack restart), not per-PR regressions, and not related to sdk #207 (deploy-add resolution was clean/cached). 10222 is plan/PR drift, not infrastructure.

## Reproducibility: 0024 re-run wave (observed, NOT part of v32 data)

A second full 32-lane wave (calver 2026.248.0024, ~02:24→02:30) re-ran the same PRs immediately after v32: **11 PASS / 21 FAIL — the identical split**, mean total 146.8 s, evals/min 13.1. The 21 failures replicated (same families: 13+7 visual rebuild-capture + 10222 pr-behavior-2), i.e. the failure set is deterministic, not transient. Sample: 10115 re-failed ok=false total=104 s da=49 s at 0024.

## Cleanup + hygiene

- FAIL-leaves-VM cleanup: **21/21 FAIL-lane VMs destroyed** (`charly vm destroy check-omarchy-pr-<N>-vm --keep-deploy --if-exists`, RC=0 each, verified against `charly vm list`). Destroy targets the **entity** name (charly maps to the `charly-`-prefixed domain). All 0024-wave FAIL leftovers were the same domains and are gone too — 0 FAIL-lane VMs running post-cleanup.
- Note: my first destroy attempt batch used the `charly-`-prefixed domain name (no-op) and an earlier `charly vm list | head -45` truncated the running set (appeared to show PASS lanes cleaned); both corrected before remediation — no wrong VM touched, no in-flight run disrupted (2024 redo summaries all predate the destroy batches; latest FAIL-lane redo summary 02:29:09 < first destroy ~02:29:30).
- Remaining running (neither wave cleaned them): PASS-lane VMs 10141, 10200, 10215, 10219, 10229 + pre-existing paused `charly-check-snap-probe` (untouched by design). PASS-lane VMs linger after BOTH waves → runner guidance item: the cleanup step does not reliably destroy the VM on PASS; verify/force teardown before the next wave.
- No processes killed, nothing SIGQUIT'd, no subagents spawned; 0 `v32-*` units and 0 `charly check run` processes remain. Observation data: /tmp/v32-wave.log (per-snapshot phase/fanout log), /tmp/v32-snap.sh (snapshot script).
