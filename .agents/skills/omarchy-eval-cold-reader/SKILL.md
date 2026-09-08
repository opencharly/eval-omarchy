---
name: omarchy-eval-cold-reader
description: |-
  The cold-reader rubric: artifacts-only grading, SUBJECT + PROCESS verdicts, the deep-eval tool protocol. Use before finalizing any eval result.
---

## COLD-READER RUBRIC (M6, permanent) — the grading contract for every eval result

A cold read is a FRESH-CONTEXT validation of the eval evidence (the report + the media
+ the ledger) against the criteria. It issues TWO verdicts:

- **SUBJECT** (about the PR): PASS (verified working on a live system) / FAIL
  (verified not working) / NO VALIDATION. Any "might work" framing for untested live
  behavior is STRICTLY FORBIDDEN.
- **PROCESS** (about the eval itself): every PR-specific check known-red (probe FAIL
  exit 2 observed), tier compliance (system PRs on the live VM), claims scoped to the
  tier, media non-empty AND showing the commands, Assisted-by footer present. Any
  process defect = REDO-PROCESS (setup update + full re-run), never a posted report.

### The vision-deterministic cross-check (mandatory, the GNOME trap)

The vision model can mislabel the desktop (Hyprland+Quickshell repeatedly called
"GNOME"). Every material vision claim MUST be corroborated by a deterministic source:
the .cast text, the wl:/spice:/record: verb outputs, or the config. A vision claim
without corroboration is a PROCESS finding.

### The deep-eval tool protocol (the reading lanes)

The reader walks FOUR lanes for every eval:

- **PR code lane:** pi.read/pi.grep on the PR diff — markers are diff-added, paths
  proven-landing, the visual/class decision holds.
- **Check-results lane:** the run's summary.yml phases + per-check verdicts — the
  evidence for every process criterion.
- **.cast lane (the terminal-lane truth):** ALWAYS read — exact commands, exit codes,
  timestamps.
- **Vision lane:** vision_ask/pi.read on SPICE frames + the GIF; ffmpeg frames from
  screen.mp4 — every material vision claim corroborated by the .cast/wl/spice text,
  never trusted alone.

### The adversarial self-test (performed whenever the rubric changes)

Feed the reader deliberately MISLABELED frames (e.g., a real GNOME-desktop screenshot
labeled as the omarchy eval output, or the Hyprland desktop labeled "boot failure") +
verify the reader flags the mismatch via the deterministic cross-check. A reader that
accepts a mislabeled frame without a PROCESS finding FAILS the self-test.

### Calibration (one past-report re-audit)

Re-audit one previously finalized eval (from eval/) with the current rubric; the
audit's verdict (PASS/FAIL-of-process) is recorded in the findings ledger as the
calibration baseline.

### The judge rule (cold-reader) — the media review scope

- **ALWAYS** read the `.cast` (the terminal-lane truth: exact commands, exit codes,
  timestamps).
- **MP4 review ON DEMAND only:** review the `screen.mp4` (frames via ffmpeg +
  vision_ask) ONLY when the plan's `visual:` flag is true (the PR's diff touches the
  desktop UI — panels, notifications, themes, overlays, animations) or the diff clearly
  implies visual change. A non-visual PR (config/scripts/docs) never needs the mp4 —
  the .cast + check results suffice.
- Every material vision claim is corroborated by a deterministic source (the
  .cast/wl/spice text) — the GNOME-mislabel trap applies to mp4 frames too.

The three-artifact media contract that produces .cast/.gif/screen.mp4:
`references/media-contract.md`.

### Per-eval stats contract (every batch, every lane)

Every eval run gets a DEDICATED stats file — exact measurements, one file per eval:

- Path: `eval/evidence/batch-<batch>/stats/<pr>-stats.md` (the matrix is the
  aggregate; the stats files are the per-run records).
- Content: run calver, the verdict line verbatim, EVERY phase (name + duration_seconds
  + ok) from the run's summary.yml, total_seconds, plus timestamps (the run dir mtimes
  / log times).
- The supervisor/batch owner EMITS the file when each run concludes (before the
  aggregate matrix) — never after a batch restart that would blur the runs.

### RCA stats-signature discipline

Whatever is suspected MUST show up in the per-eval stats:

- Every hypothesis declares its STATS SIGNATURE before testing (e.g. 'the media steps
  are the cost' ⇒ the stats' media-window rows must sum large; 'the deploy machinery
  serializes' ⇒ deploy-add grows with the concurrent lane count in the A/B; 'the update
  recreate is the cost' ⇒ the update+rebuild rows dominate).
- The stats files carry BOTH the phase rows (summary.yml) AND the media-window rows
  (artifact mtimes — currently the only precise inner-step timing source) until the
  charly enhancement lands (summary.yml gains the check-live inner step durations —
  queued in the plugin-check pipeline).
- A hypothesis without its signature in the stats is NOT a finding.
