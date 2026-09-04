# M4 batch matrix (16-lane, 2026-09-04)
| PR | class | probe (must FAIL) | eval | total_s |
|---|---|---|---|---|
| 10115 | notifications countdown | BROKEN->fixed | PASS / revalidating | |
| 10116 | network adapter | FAIL 5 | PASS | 163 |
| 10123 | docs | FAIL 5 | PASS | 166 |
| 10125 | screenrecording | FAIL 5 | PASS | 171 |
| 10129 | presentation terminal | FAIL 5 | PASS | 166 |
| 10130 | lock reblank | BROKEN->fixed | FAIL reblank->fixed / revalidating | |
| 10134 | vscode theme | FAIL 5 (marker weak?) | FAIL->fixed / revalidating | |
| 10136 | zed theme | FAIL 5 | PASS | 164 |
| 10138 | wallclock | FAIL 5 | PASS | 170 |
| 10139 | apple sd | FAIL 5 | PASS | 107 |
| 10140 | usb autosuspend | FAIL 5 | FAIL path->fixed / revalidating | |
| 10141 | brcmfmac | FAIL 5 | PASS | 116 |
| 10144 | launcher rename | FAIL 5 | PASS | 139 |
| 10146 | notification group | FAIL 5 | PASS | 168 |
| 10147 | vibecad | FAIL 5 | PASS | 164 |
| 10148 | audient | FAIL 5 | PASS | 154 |

Passing evals avg total ~150s (update 61s + cleanup 6s — the acpid + payload collapse; was 437s). REDO-PROCESS findings: 10115 (marker not red), 10130 (marker not in PR code), 10134 (marker/path), 10140 (etc/ path) — 4 oracle marker defects, fixed with diff-added tokens, re-running.
