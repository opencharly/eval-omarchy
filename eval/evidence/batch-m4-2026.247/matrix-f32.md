# Matrix — f32 FINAL confirmation wave (32 lanes, complete fix stack)

- **Wave**: systemd user units `f32-<PR>.service`, launched 2026-09-05 03:00:08–11 CEST, run via `charly check run check-omarchy-pr-<N>-vm` from `eval-omarchy`; all 32 concluded by 03:05:27 CEST (wave wall ≈ 5.3 min)
- **Fix stack under test**: hardened golden (sshd MaxStartups + pr-apply pre-seed + guest-warm, captured 00:58Z) · sdk #207 fanout-0 @github resolution · beds' media waits (eventually 90s on rec-spice-start/rec-screen-spice) + pull retries (rec-stop/rec-gif eventually 60s) · 1vCPU · restart-only gate · content markers · head-freshness
- **Run dir**: `.check/check-omarchy-pr-<N>-vm/2026.248.0100` (fresh summaries, mtime < 12 min all)
- **Fanout samples** (`pgrep -af 'git ls-remote' | grep -v pgrep | wc -l`): 16 at 01:01Z (launch transient, initial resolution) → 0 at 01:02:55Z → 0 at 01:04:10Z → 0 at 01:05:59Z — steady-state 0 ✓

## Result rows — PR | run | total(s) | ok

| PR | run | total | ok | failing step / note |
|---|---|---|---|---|
| 10115 | 2026.248.0100 | 153 | **PASS** | — |
| 10116 | 2026.248.0100 | 129 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10123 | 2026.248.0100 | 151 | **PASS** | — |
| 10125 | 2026.248.0100 | 154 | **PASS** | — |
| 10129 | 2026.248.0100 | 53 | **PASS** | serialized tail lane (~3m53s pre-deploy-add wait; phase time 53s) |
| 10130 | 2026.248.0100 | 147 | **PASS** | — |
| 10134 | 2026.248.0100 | 142 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10136 | 2026.248.0100 | 142 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10138 | 2026.248.0100 | 146 | **PASS** | — |
| 10139 | 2026.248.0100 | 54 | **PASS** | serialized tail lane |
| 10140 | 2026.248.0100 | 53 | **PASS** | serialized tail lane |
| 10141 | 2026.248.0100 | 143 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10144 | 2026.248.0100 | 151 | **PASS** | — |
| 10146 | 2026.248.0100 | 54 | **PASS** | serialized tail lane |
| 10147 | 2026.248.0100 | 156 | **PASS** | — |
| 10148 | 2026.248.0100 | 149 | **PASS** | — |
| 10199 | 2026.248.0100 | 155 | **PASS** | — |
| 10200 | 2026.248.0100 | 137 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual; torn-YAML class GONE) |
| 10202 | 2026.248.0100 | 126 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10205 | 2026.248.0100 | 135 | **PASS** | — |
| 10208 | 2026.248.0100 | 53 | **PASS** | serialized tail lane |
| 10210 | 2026.248.0100 | 52 | **PASS** | serialized tail lane |
| 10211 | 2026.248.0100 | 135 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10212 | 2026.248.0100 | 133 | **PASS** | — |
| 10215 | 2026.248.0100 | 140 | **PASS** | head-freshness PR; content checks PASS |
| 10217 | 2026.248.0100 | 131 | **PASS** | — |
| 10219 | 2026.248.0100 | 124 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10222 | 2026.248.0100 | 139 | **PASS** | content-marker PR; marker checks PASS |
| 10224 | 2026.248.0100 | 151 | **PASS** | — |
| 10225 | 2026.248.0100 | 134 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (residual) |
| 10228 | 2026.248.0100 | 138 | **PASS** | — (head-freshness PR) |
| 10229 | 2026.248.0100 | 137 | **PASS** | — |

**23/32 PASS, 9/32 FAIL — all 9 fails are the SAME single class** (verified by grep 'uniformly one color' = 1 in all 9 check-live-rebuild.logs).

## The residual fail class (9×) — rec-spice-stop uniform-frame

`FAIL check stop the SPICE capture and pull the MJPEG stream [rec-spice-stop] spice: record: artifact "/tmp/pr-<N>.mjpeg" is uniformly one color (RGBA=0,0,0,255 / 17,17,17,255) — likely a blank/black/white capture`

RCA (beds pr-beds/pr-<N>/charly.yml): the 90s media waits are wired to **rec-spice-start** (line ~60) and **rec-screen-spice** (line ~50) only; **rec-spice-stop has NO `eventually`/`retry_interval`** (single-shot pull with `artifact_min_bytes: 10000, artifact_not_uniform: true`). The still-screenshot (spice: screenshot, native decode) passes while the MJPEG **video** stream returns uniform-black frames — post-reboot capture window too short for 9/32 1vCPU guests. Artifacts prove it: /tmp/pr-10116.mjpeg = 250881 B, pr-10202 = 217205 B (many all-black frames) vs PASS lane pr-10115 = 47 frames / 780065 B. Decisive control: the 6 serialized tail lanes (10129/10139/10140/10146/10208/10210) waited ~3m53s before deploy-add, their guests fully rendered, and rec-spice-stop PASSED instantly at check-live-rebuild 14–15 s. The uniform-frame class is therefore a **residual timing issue, not a new class** — the retry fix landed on the wrong check. Next hill-climb: add `eventually: 90s` + `retry_interval: 5s` to **rec-spice-stop** itself (or a pre-stop frame-count wait on the recording session).

## Fixed classes this wave (c32 → f32)

| c32 class | c32 fails | f32 fails | status |
|---|---|---|---|
| rec-spice-stop uniform-frame | 12 | 9 | RESIDUAL (waits not wired to the stop pull) |
| rec-stop sshd kex reset (.cast pull) | 1 | 0 | GONE (eventually 60s + sshd MaxStartups golden) |
| gate-restart-start domain not found | 1 | 0 | GONE (restart-only gate) |
| cleanup destroy domain not found | 1 | 0 | GONE |
| torn project charly.yml read (10200) | 1 | 0 | GONE |
| deploy-add @github ref-resolution stall (8/32 ≥124s, ls-remote storm) | — | 0 | GONE → clean serialized tail (FAN stays 0) |

## Phase band (seconds; n=32 lanes, all fresh summaries)

| phase | n | min | med | max |
|---|---|---|---|---|
| vm-build | 32 | 1 | 2 | 2 |
| vm-create | 32 | 5 | 6 | 7 |
| deploy-add | 32 | 13 | 43.5 | 50 |
| bring-up-members | 32 | 0 | 0 | 0 |
| check-live | 32 | 14 | 41.5 | 57 |
| gate-restart-stop | 32 | 1 | 2 | 3 |
| gate-restart-start | 32 | 0 | 2 | 3 |
| check-live-rebuild | 32 | 14 | 35 | 44 |
| cleanup | 23 | 2 | 6 | 12 |
| cleanup-members | 23 | 0 | 0 | 0 |

## Band + throughput

- total per eval: min 52 s, median 137.5 s, max 156 s, **avg 124.9 s** (sum 3997 / 32)
- **evals/min = lanes × 60 / avg_eval_seconds = 32 × 60 / 124.9 ≈ 15.4** (c32 was ≈ 13.2; operator target ≤60 s avg not yet met — residual class and 1vCPU boot dominate)
- Wave wall: 03:00:11 → 03:05:27 CEST ≈ 5.3 min for all 32 lanes (c32: ≈ 5.5 min)
- 23 PASS lanes ran 124–156 s; 6 serialized tail lanes ran 52–54 s of phase time

## Cleanup + hygiene

- 9 FAIL-leaves-VMs destroyed via `charly vm destroy check-omarchy-pr-<N>-vm --keep-deploy --if-exists` all reported "Destroyed VM" — only the pre-existing paused charly-check-snap-probe remains (untouched; not part of this wave)
- Media contract: all 32 lanes produced .cast/.gif/screen.png; rec-mp4 is verify-only (skipped); fails' .mjpeg artifacts recorded (uniform-black) but kept as evidence
- No processes killed; units f32-* exited naturally (systemd GC'd dead units); no staged files

*Collected by omarchy-eval lane monitor (01:01–01:06Z); rows from .check/check-omarchy-pr-<N>-vm/2026.248.0100/summary.yml (all mtime < 12 min)*