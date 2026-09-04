# pr-10123 eval stats (exact timings)

bed: check-omarchy-pr-10123-vm | run calver: 2026.247.2043
verdict ok: False | total_seconds: 505

| phase | seconds | ok |
|---|---|---|
| vm-build | 9 | True |
| vm-create | 33 | True |
| deploy-add | 117 | True |
| bring-up-members | 0 | True |
| check-live | 53 | True |
| update | 244 | True |
| check-live-rebuild | 49 | False |

## media window (inner-step evidence, artifact-mtime) ##
spice-record→gif window: 3s (mjpeg 1788556602 → gif 1788556605)
cast: 23:16:44 982B
