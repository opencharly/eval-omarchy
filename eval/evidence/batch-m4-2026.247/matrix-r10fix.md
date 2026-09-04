<!-- HISTORICAL: the R10 re-verification run (00:18–00:26, the ssh-fragment fix only, BEFORE the ResolveRef-TTL fix) — every lane stalled at deploy-add by the ref-resolution storm. Superseded by matrix-final.md (the post-TTL-fix runs, all lanes concluded). -->

# matrix-r10fix.md — R10 re-verification, 16-lane (2026-09-05 00:18:31 → 00:26:44, batch wall 493s)

ssh-fragment-race fix under test: sdk local tree HEAD **5ecea08** "fix(kit): serialize the managed ssh-fragment save" (kit/sshconfig.go +21/-3), binary /home/atrawog/Sync/Atrapub/coder/pi/opencharly/charly/bin/charly (mtime 00:08, buildinfo dep sdk => /home/atrawog/Sync/Atrapub/coder/pi/opencharly/sdk (devel)). Fresh binary, probes skipped (red-proven), 16 concurrent `charly check run check-omarchy-pr-<N>-vm` from eval-omarchy.

## Result: 0/16 evals completed — the 16-lane stall PERSISTS (deploy-add phase)

| PR | total_s | vm-build | vm-create | deploy-add | verdict |
|---|---|---|---|---|---|
| 10115 | ≥493 (frozen, no verdict) | 4.154 | 15.471 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10116 | ≥493 (frozen, no verdict) | 4.125 | 15.953 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10123 | ≥493 (frozen, no verdict) | 4.236 | 15.644 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10125 | ≥493 (frozen, no verdict) | 4.094 | 15.464 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10129 | ≥493 (frozen, no verdict) | 4.018 | 15.515 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10130 | ≥493 (frozen, no verdict) | 4.242 | 15.945 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10134 | ≥493 (frozen, no verdict) | 4.099 | 15.225 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10136 | ≥493 (frozen, no verdict) | 4.156 | 15.312 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10138 | ≥493 (frozen, no verdict) | 4.183 | 15.118 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10139 | ≥493 (frozen, no verdict) | 4.058 | 15.985 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10140 | ≥493 (frozen, no verdict) | 4.228 | 15.598 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10141 | ≥493 (frozen, no verdict) | 4.146 | 15.049 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10144 | ≥493 (frozen, no verdict) | 4.241 | 15.976 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10146 | ≥493 (frozen, no verdict) | 4.332 | 16.466 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10147 | ≥493 (frozen, no verdict) | 4.227 | 15.409 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |
| 10148 | ≥493 (frozen, no verdict) | 3.964 | 16.526 | STALL (≥340s, ref-resolution storm) | STALL — deploy-add hang |

## Batch numbers
- batch wall: **493 s** (00:18:31 → 00:26:44; terminated at freeze)
- evals/min: **0.0 completed** (0/16 lanes reached a verdict) — target 16 evals/min @ ≤60s avg not approachable while deploy-add hangs
- pre-fix 16-lane average: 535 s → this batch: **no lane finished even at 493 s**; totals NOT in the ~93–110 s band
- lane phases reached: vm-build ✓ (~seconds), vm-create ✓ (~15 s each, zero serialization), deploy-add ✗ (16/16 hung)

## Verdict: FIX DOES NOT RESOLVE THE 16-LANE STALL (STILL SLOW)

### Phase evidence (per the task's >200 s rule — every lane exceeded it)
- 16/16 lanes frozen in [deploy-add] (`charly fleet add`) with deploy-add.log at 42 B "status: RUNNING" from 00:19:42 → termination; no summary.yml in any 2026.247.2218 dir (verified).
- The `charly fleet add ... --dev-local-pkg` children sat in **futex_wait** (Go runtime waiting on subprocess completion), each with 10+ live `git ls-remote` children against github.com/opencharly/{layer-*,plugin-*}.git (152 concurrent at peak, host load 35; some ls-remotes aged >4 min; a 20 s-capped probe ls-remote timed out → GitHub throttling/fanout starvation).
- Wave behavior: git subprocess waves re-spawned across the whole window (fresh pids at 00:26); the stall is self-renewing, not a transient.
- The ssh-fragment SAVE fix itself demonstrably works: /home/atrawog/.config/charly/ssh_config contains all 16 host stanzas, written once at 00:19:25, coherent (no lost stanzas, no corruption) — the fix's target race is resolved; the remaining stall is the deploy-add ref-resolution fanout the fragment fix does not touch.

### R1 root-cause (narrative, evidence-backed)
The 535 s pre-fix stall was attributed to the managed ssh-fragment save race (concurrent executors hang; sdk 5ecea08). On the fixed binary the 16-lane run reproduces the SAME phase/signature (fleet-add futex_wait, deploy-add.log frozen) — but the contended resource is the **per-lane git ls-remote @github ref-resolution fanout** (each lane resolves every @github layer/plugin ref live, ~10+ concurrent ls-remote per lane × 16 lanes; github.com throttles → every lane blocks for minutes). The 00:08 pre-run batch (same phase, same signature, found orphaned at handover) matches this same mechanism. The fix neither regresses nor resolves the stall. Next hill-climb candidate: cache/pin the @github ref resolution (single host-side resolution shared across lanes) or serialize the resolution phase with a bounded mutex.

### Hygiene after termination
- 16 lane run procs + 16 fleet-add children + all ls-remote waves killed (SIGTERM then SIGKILL); 0 leftover batch procs.
- 16 lane VMs destroyed via `charly vm destroy check-omarchy-pr-<N>-vm --keep-deploy --if-exists` (disposable beds; oracle-generated per-PR configs preserved).
- Host left with only the pre-existing paused `charly-check-snap-probe` VM (different bed — untouched).
