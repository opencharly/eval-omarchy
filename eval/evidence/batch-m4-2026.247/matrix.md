# M4 batch matrix (16-lane, 2026-09-04 — FINAL: 16/16 evals PASS)
| PR | class/marker (diff-added) | probe (known-red) | eval | total_s |
|---|---|---|---|---|
| 10115 | notifications `showCountdown` | FAIL 5 | PASS | 137 |
| 10116 | network `adapter` | FAIL 5 | PASS | 163 |
| 10123 | docs `tile` | FAIL 5 | PASS | 166 |
| 10125 | screenrecording `encoder` | FAIL 5 | PASS | 171 |
| 10129 | presentation `presentation` | FAIL 5 | PASS | 166 |
| 10130 | lock `blankArmed` | FAIL 5 | PASS | revalidated |
| 10134 | vscode-theme `GENERATED_THEME` | FAIL 5 | PASS | 82 |
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
