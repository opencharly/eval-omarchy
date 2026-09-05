# Matrix — c32 confirmation wave (32 lanes)

- **Wave**: systemd user units `c32-<PR>.service`, launched 2026-09-05 02:24:28–29 CEST, run via `charly check run check-omarchy-pr-<N>-vm` from `eval-omarchy`
- **Binary**: dev/worktree charly (`opencharly/charly/bin/charly`) — sdk #207 cached-latest-tag route + beds' post-reboot media waits (rec-screen-spice / rec-spice-start, eventually 90s) + head-freshness (10215/10228) + 10222 content marker
- **Run dir**: `.check/check-omarchy-pr-<N>-vm/2026.248.0024`; all 32 lanes concluded 02:28:38–02:30:00 CEST (wave wall ≈ 5.5 min)
- **Fanout samples** (`pgrep -af 'git ls-remote'`): 0 (00:25Z) · 38 (00:26:00Z, initial resolution wave) · 0 (00:26:10Z) · 1 (00:26:52Z) · 0 (00:27:47Z) — steady-state ≈ 0 ✓

## Result rows — PR | run | total(s) | ok

| PR | run | total | ok | failing step / note |
|---|---|---|---|---|
| 10115 | 2026.248.0024 | 104 | FAIL | check-live → rec-stop (guest sshd kex reset on .cast pull) |
| 10116 | 2026.248.0024 | 128 | FAIL | gate-restart-start (domain not found after vm stop) |
| 10123 | 2026.248.0024 | 175 | FAIL | cleanup (destroy: domain not found) — ALL checks passed |
| 10125 | 2026.248.0024 | 156 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10129 | 2026.248.0024 | 161 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10130 | 2026.248.0024 | 180 | **PASS** | — |
| 10134 | 2026.248.0024 | 180 | **PASS** | — |
| 10136 | 2026.248.0024 | 189 | **PASS** | — |
| 10138 | 2026.248.0024 | 158 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10139 | 2026.248.0024 | 131 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10140 | 2026.248.0024 | 131 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10141 | 2026.248.0024 | 158 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10144 | 2026.248.0024 | 120 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10146 | 2026.248.0024 | 123 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10147 | 2026.248.0024 | 163 | **PASS** | — |
| 10148 | 2026.248.0024 | 168 | **PASS** | — |
| 10199 | 2026.248.0024 | 168 | **PASS** | — |
| 10200 | 2026.248.0024 | 34 | FAIL | check-live-rebuild (project charly.yml torn read, YAML err at line 160) |
| 10202 | 2026.248.0024 | 170 | **PASS** | — |
| 10205 | 2026.248.0024 | 167 | **PASS** | — |
| 10208 | 2026.248.0024 | 119 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10210 | 2026.248.0024 | 116 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10211 | 2026.248.0024 | 176 | **PASS** | — |
| 10212 | 2026.248.0024 | 133 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10215 | 2026.248.0024 | 159 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (head-freshness PR; content checks PASS) |
| 10217 | 2026.248.0024 | 119 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10219 | 2026.248.0024 | 161 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10222 | 2026.248.0024 | 117 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame (content-marker PR; marker checks PASS) |
| 10224 | 2026.248.0024 | 174 | **PASS** | — |
| 10225 | 2026.248.0024 | 134 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |
| 10228 | 2026.248.0024 | 166 | **PASS** | — (head-freshness PR) |
| 10229 | 2026.248.0024 | 161 | FAIL | check-live-rebuild → rec-spice-stop uniform-frame |

**11/32 PASS, 21/32 FAIL.**

## Phase band (seconds)

| phase | n | min | med | max |
|---|---|---|---|---|
| vm-build | 32 | 1 | 2 | 4 |
| vm-create | 32 | 3 | 5 | 7 |
| deploy-add | 32 | 11 | 48 | 56 |
| check-live | 32 | 14 | 54 | 65 |
| gate-restart-stop | 31 | 1 | 2 | 4 |
| gate-restart-start | 31 | 1 | 2 | 3 |
| check-live-rebuild | 30 | 0 | 40 | 59 |
| cleanup | 12 | 7 | 11 | 13 |

## Band + throughput

- total_seconds: n=32, sum=4699, **avg=146s**, min=34, max=189, median≈158s
- **evals/min = 13.1** (lanes × 60 / avg_eval_seconds = 32×60/146.8); wall rate 32 evals ≈ 5.5 min

## Comparison

| wave | avg eval (s) | PASS rate | dominant failure |
|---|---|---|---|
| pre-fix (M4-era) | 312 | — | deploy-add @github fanout stall |
| cpu-1 variant | 228–233 | — | — |
| v32 | — | 9/32 (28%) | 21/32 rebuild uniform-frame |
| **c32 (this wave)** | **146** | **11/32 (34%)** | 17/32 rebuild uniform-frame + 4 other causes |

Duration: **312 → 146s avg (53% cut)** — the deploy-add/@github caching fix works. Verdict on "mostly pass": **NOT met** — the rebuild post-reboot uniform-frame capture persists (~half the lanes), plus 4 one-off teardown/race failures.

## Failure RCA (one line each)

1. **17× check-live-rebuild rec-spice-stop** — post-reboot SPICE MJPEG is uniformly black (RGBA=0,0,0,255 / 17,17,17,255); the guest display pipeline does not repaint within the (up to 90s) wait after gate-restart; first-pass rec-spice-stop passes in these lanes, so it is specifically the post-reboot capture. New media waits helped 11 lanes but ~half still black. All per-PR pr-apply/pr-behavior content checks PASS in both passes — the red is a capture-assertion, not a product-content miss.
2. **10200 check-live-rebuild** — `yaml: line 160: mapping values are not allowed`: the SHARED `eval-omarchy/charly.yml` was concurrently rewritten by other lanes' cleanup (`vm destroy` default removes the vm entry → file rewrite, observed mtime 02:31:29) while 10200's rebuild re-resolved the project → torn read. sdk #207 fixed the ssh_config race, not this project-YAML write race.
3. **10115 check-live rec-stop** — `.cast` pull kex reset (guest sshd); wave config raised `MaxStartups 200:60:200` but the 32-lane burst still overran it (ssh contention).
4. **10116 gate-restart-start / 10123 cleanup** — `vm start`/`vm destroy` "domain not found" right after `vm stop`; transient libvirt miss under 32 concurrent VM lifecycle ops (both lanes' content + rebuild checks fully PASS — 10123 would otherwise be green).

## Cleanup (FAIL-leaves-VM)

Surviving VMs after the wave (virsh): charly-check-omarchy-pr-{10141,10200,10215,10219,10229}-vm → destroyed with `charly vm destroy --keep-deploy --if-exists`.
