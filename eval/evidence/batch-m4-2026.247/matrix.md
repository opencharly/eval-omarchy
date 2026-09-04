# M4 batch matrix (16-lane, 2026-09-04 — FINAL: 16/16 evals PASS)
| PR | class/marker (diff-added) | probe (known-red) | eval | total_s |
|---|---|---|---|---|
| 10115 | notifications `showCountdown` | FAIL 5 | PASS | 83 |
| 10116 | network `adapter` | FAIL 5 | PASS | 163 |
| 10123 | docs `tile` | FAIL 5 | PASS (run 2230) | 112 |
| 10125 | screenrecording `encoder` | FAIL 5 | PASS (run 2230) | 112 |
| 10129 | presentation `presentation` | FAIL 5 | PASS | 166 |
| 10130 | lock `blankArmed` | FAIL 5 | PASS | revalidated |
| 10134 | vscode-theme `_watch` | FAIL 5 red (fresh 1938, exit 2) | PASS 9st 79s (fresh 1940) | 79 |
| 10136 | zed `zed` | FAIL 5 | PASS | 164 |
| 10138 | clock `Wallclock` | FAIL 5 | PASS | 170 |
| 10139 | apple-sd `apple` | FAIL 5 | PASS | 107 |
| 10140 | usb `autosuspend` (migrations path) | FAIL 5 | PASS | revalidated |
| 10141 | brcmfmac `brcmfmac` | FAIL 5 | PASS | 116 |
| 10144 | launcher `launcher` | FAIL 5 | PASS | 139 |
| 10146 | notifications `group` | FAIL 5 | PASS | 168 |
| 10147 | vibecad `VibeCAD` | FAIL 5 | PASS | 84 (trimmed media) |
| 10148 | audient `audient` | FAIL 5 | PASS | 154 |

Every probe column shows FAIL exit 2 on the instrumented golden = the marker's red-by-construction proof per lane (the ORACLE marker rule, PR-EVAL-LANE.md). The 4 oracle-defective markers (pre-existing base words) were caught by the probe (RED-PROBE-BROKEN), fixed with diff-added tokens, and re-validated to PASS. Evals avg ≈ 150 s (was 437 s): update 61→28 s, cleanup 182→6 s (acpid + payload collapse).


### 10134 capstone (the final lane, fresh runs under the `_watch` plan)
- RED-PROBE run 2026.247.1938: **FAIL exit 2** at 5s check-live (the goldens carry no `_watch`) — probe total 25s. Stale pre-fix runs (GENERATED_THEME) superseded by 29f4bbd.
- EVAL run 2026.247.1940: **PASS steps=9** — phases 1/4/15/0/16/26/14/4/0s, total **79s**; 8/8 check-live PASS incl. the `_watch` grep; update-rebuild re-PASSed (PR behavior survives the cycle).
- Media: /tmp/pr-10134-{screen.png 1254615B, .cast 920B, .gif 14812B}.
- Orphan discipline: vm destroyed after both lanes; domstate domain-not-found.
- Worker-lane note: the lane's final subagent_wait child-tool request is unavailable to the worker agent def — the eval work itself completed; the worker tool list needs no subagent_wait (removed for future lanes).
