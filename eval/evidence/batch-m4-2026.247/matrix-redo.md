
# Redo wave matrix (21-lane, run 2026.247.2345 — lock-clean verification of the cpu-1 fix)

Wave: systemd-run units redo-10139..redo-10229, 21 lanes, cpu-1 per VM (-smp 1). Start 23:45:19Z (ActiveEnter redo-10139/10215), last summary write 23:50:45Z → wall ≈ 5.4 min (326 s). All 21 exited; 0 lock errors ("database is locked" / "Failed to get shared" absent from all 21 run logs); no stall/no freeze (the r10fix 16-lane wave froze in deploy-add — this wave did not).

## Rows (PR | run | total_s | ok)
| PR | run | total_s | ok |
|---|---|---|---|
| 10139 | 2026.247.2345 | 236 | PASS |
| 10141 | 2026.247.2345 | 235 | PASS |
| 10146 | 2026.247.2345 | 231 | PASS |
| 10147 | 2026.247.2345 | 234 | PASS |
| 10148 | 2026.247.2345 | 229 | PASS |
| 10199 | 2026.247.2345 | 230 | PASS |
| 10200 | 2026.247.2345 | 228 | PASS |
| 10202 | 2026.247.2345 | 239 | PASS |
| 10205 | 2026.247.2345 | 236 | PASS |
| 10208 | 2026.247.2345 | 233 | PASS |
| 10210 | 2026.247.2345 | 235 | PASS |
| 10211 | 2026.247.2345 | 236 | PASS |
| 10212 | 2026.247.2345 | 230 | PASS |
| 10215 | 2026.247.2345 | 146 | **FAIL** (pr-apply tree-read) |
| 10217 | 2026.247.2345 | 228 | PASS |
| 10219 | 2026.247.2345 | 239 | PASS |
| 10222 | 2026.247.2345 | 144 | **FAIL** (pr-behavior-2 marker/content) |
| 10224 | 2026.247.2345 | 232 | PASS |
| 10225 | 2026.247.2345 | 231 | PASS |
| 10228 | 2026.247.2345 | 168 | **FAIL** (pr-apply tree-read) |
| 10229 | 2026.247.2345 | 238 | PASS |

Result: **18/21 PASS, 3/21 FAIL**.

## Per-phase means (18 PASS lanes)
| phase | mean_s | median_s |
|---|---|---|
| vm-build | 6.1 | 6 |
| vm-create | 22.2 | 22 |
| deploy-add | 87.9 | 88 |
| bring-up-members | 0 | 0 |
| check-live | 41.4 | 40 |
| gate-restart-stop | 10.4 | 11 |
| gate-restart-start | 9.6 | 9 |
| check-live-rebuild | 42.9 | 44 |
| cleanup | 12.7 | 13 |
| cleanup-members | 0 | 0 |
| **total** | **233.3** | **233** |

All-21 mean total (incl. FAIL lanes): 4658/21 = **221.8 s** → evals/min = 21 × 60 / 221.8 = **5.68**.

## Band vs the previous 12-lane sample (avg 228 s, deploy-add 84, check-live 43)
- total: 233.3 s (was 228) → **+5 s (+2%), same band — no speedup, no regression**
- deploy-add: 87.9 (was 84) → +4 s (github @github ref-resolution fanout unchanged; cpu-1 adds no deploy serialization)
- check-live: 41.4 (was 43) → −2 s
- verdict: the lock-clean redo wave is functionally clean (21/21 ran to exit, 0 lock errors) but the ≤60 s/eval target remains far off (current band ~4× target). The cpu-1 fix verified for locking; timing is a separate bottleneck (deploy-add @github fanout).

## FULL 32-lane cpu-1 set — does it verify? **NO (29/32)**
- 11 prior lanes (run 2026.247.2337, the 12-lane sample minus 1): 10115 218, 10116 215, 10123 222, 10125 230, 10129 215, 10130 250, 10134 248, 10136 218, 10138 257, 10140 223, 10144 209 — all PASS, mean 227.7 s (≈ the 228 s sample).
- 21 redo lanes (2026.247.2345): 18 PASS / 3 FAIL.
- Union: **29/32 PASS — NOT fully verified.** The expected 10215 redo PASS **did NOT happen**.

## FAIL RCA
| PR | failing step | one-line RCA |
|---|---|---|
| 10215 | check-live → pr-apply (then cascade pr-behavior/-2/-3) | **tree-read class STILL PRESENT**: `fatal: unable to read tree (6ebb7e1b…)` exit 128 — the ac047a8 checkout-fallback fix did NOT resolve this lane; PR head never applied, so the 3 behavior greps fail downstream. |
| 10228 | check-live → pr-apply (+ pr-behavior cascade) | same tree-read class: `fatal: unable to read tree (f0bc41fb…)` exit 128 — intermittent (2 of 21 lanes); 10222's pr-apply DID pass (exit 0), so the fix works when the tree object is present but does not fall back when the advertised ref's tree is unreadable. |
| 10222 | check-live → pr-behavior-2 | marker/content mismatch, NOT tree-read: assertion greps the installed sample's CONTENT for `power-source-change` → exit=1 (file present, no token; empty stderr, not a No-such-file exit 2); the oracle verified the token only in the diff's ADDED path line (config/omarchy/hooks/power-source-change.d/show-power-source-notification.sample) — plan's marker rule vs check assertion diverge. |

Note: on FAIL lanes the run stops after check-live (no gate-restart / rebuild / cleanup phases — VM left running by design); media steps on all 21 lanes completed (rec-* PASS incl. on FAIL lanes; rec-mp4 SKIP — verify-only mode).

Evidence: eval/evidence/batch-m4-2026.247/stats/redo-wave-rows.tsv; per-bed .check/check-omarchy-pr-<N>-vm/2026.247.2345/{summary.yml,check-live.log,deploy-add.log}.
