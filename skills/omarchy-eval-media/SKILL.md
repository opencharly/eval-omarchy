---
name: omarchy-eval-media
description: |-
  The mandatory record:/spice: evidence loop, media assembly into media/<pr>-<calver>/, and the three-artifact media contract. Use when running or grading eval evidence.
---

# Media contract — recordings, artifacts, density, assembly

## Checks visible to the user AND in screen recordings (lane rule)

Whenever an eval runs on a real test system, the check output MUST be surfaced live on
the system's desktop (desktop notifications and/or a visible terminal) AND captured in
the recording/screenshot frames — what the operator sees is what the recording shows.
Recordings and screenshots are graded (by an AI) for containing the on-screen check
output verbatim.

### The THREE-artifact media contract (mandatory, every eval)

Every eval lane produces ALL THREE artifacts — no exceptions:

1. **`.cast`** — the ascii screencast of the checks: `record: {method: start, record_mode:
   terminal, record_name: <pr>}` → the drive step → `record: {method: stop, artifact:
   …/pr-<N>.cast, artifact_min_bytes: 200}`.
2. **`.gif`** — the screencast rendered to an animated GIF (the record verb render
   method).
3. **`screen.mp4`** — the SPICE OUTPUT as video via the shipped `spice: record` method
   (plugin-spice v2026.245.1508+: the host-side MJPEG capture polls the display at fps,
   default 5): `spice: {method: record, action: start, fps: 5}` BEFORE the drive, the
   drive steps, then `spice: {method: record, action: stop, artifact: /tmp/pr-<N>.mjpeg,
   artifact_min_bytes: 10000, artifact_not_uniform: true}` (an empty/static stream
   honest-fails the validators). ONE `run:` step transcodes the MJPEG to MP4
   (`ffmpeg -y -loglevel error -i /tmp/pr-<N>.mjpeg -c:v libx264 -pix_fmt yuv420p
   /tmp/pr-<N>-screen.mp4`). Charly-native: no frame-assembly workarounds — the capture
   IS the spice video stream; the ffmpeg step only relabels containers.

The record:/spice: check steps pull every artifact onto the host (the `.cast`, the
`.gif` via the record plugin's gif method, SPICE frames/video); the EVAL RUNNER agent
then assembles them into the gitignored `media/<pr>-<calver>/` (pi file tools — no
scripts) and the COLD READER grades them (vision_ask on the frames + the deterministic
.cast text). Standing rule 6: every evaluation produces a terminal .cast AND a screen
recording.

### Media-density rule (visual-class only)

The SPICE-VIDEO artifacts (spice: record start/stop + the mp4 transcode) are produced
ONLY for `visual: true` plans (the judge rule). NON-visual beds keep the .cast + .gif
+ the SPICE screenshot + the deterministic checks — the mp4 is reviewable on demand for
visual PRs only. The probe beds carry NO media loop at all (red-by-construction needs
the greps only).

### The media assembly (the artifacts land in /tmp, the mp4 transcode is an assembly step)

The launch chain MUST assemble the media after every run:

`charly check run <bed> && mkdir -p media/<pr>-<calver> && cp /tmp/pr-<N>.{cast,gif,mjpeg,screen.png} media/<pr>-<calver>/ && ffmpeg -y -loglevel error -i media/<pr>-<calver>/pr-<N>.mjpeg -c:v libx264 -pix_fmt yuv420p media/<pr>-<calver>/pr-<N>.mp4`

The mp4 is produced by the ASSEMBLY (the in-plan rec-mp4 run: step is skipped in
verify-only mode by design). media/ is gitignored; the cold-reader reads the .cast
always + the mp4 for visual-class PRs.

### The media directory contract (gitignored, creation-validated, used for validation)

- **Location:** `eval-omarchy/media/<pr>-<calver>/` — GITIGNORED (the evidence lives on
  disk, never in the tree; the PR carries the matrices + the stats, not the binaries).
- **Contents** (the three-artifact contract): `pr-<N>.cast` (the ascii screencast),
  `pr-<N>.gif` (the cast render), `pr-<N>.mjpeg` (the spice-record MJPEG),
  `pr-<N>.mp4` (the ffmpeg transcode), `pr-<N>-screen.png` (the SPICE frame).
- **Assembly:** the launch chain runs the assembly chain above; the in-plan rec-mp4 run:
  step is verify-only-skipped — the transcode belongs in the assembly.
- **CREATION-VALIDATED by the runner:** after every run the runner verifies the 5
  artifacts exist + are non-empty (`test -s` each; the .cast >= 200B, the .gif >= 1KB,
  the .mjpeg >= 10KB, the .mp4 >= 10KB, the screen.png >= 1KB) — a missing/empty
  artifact = a PROCESS finding (the media contract broken), reported with the run.
- **USED FOR VALIDATION by the cold-reader:** the .cast is ALWAYS read (the terminal-lane
  truth); the mp4 frames (ffmpeg + vision_ask) are reviewed for visual-class PRs (the
  plan's `visual:` flag); the gif/mjpeg corroborate the visual claims. A media artifact
  that contradicts the checks = a finding.
