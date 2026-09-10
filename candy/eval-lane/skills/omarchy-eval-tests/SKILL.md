# omarchy-eval-tests

The omarchy test-corpus map — the Config Oracle's guide to the charly-native
equivalents of omarchy's own tests. The oracle consults this skill to SELECT
the corpus surfaces that make sense for a PR; the lane runs them against the
eval VM.

## The corpus registry

The charly-native equivalents live in `candy/omarchy-corpus/` :

- `charly.yml` — the check plans: the declarative translations of the
  omarchy test files, one step per upstream assertion, grouped by feature
  (`omarchy:`, `wl:`, `quickshell:`, `dbus:`, `file:`, `package:`, `unit:`,
  `service:`, `process:`, `command:`, `spice:`, `libvirt:` send-key, `record:`,
  `wl: ocr`).
- `registry.yaml` — the equivalence manifest: the mapped omarchy test files →
  their covering steps, with the coverage counters recording the honest state
  (the translation is INCREMENTAL — each wave maps a batch). A mapped entry's
  steps are exercised by the corpus beds; the counters make an unmapped file
  visible.

## The lane's gap surface

- A SETUP_DEFECT is recorded when the ORACLE selects a corpus bed the registry
  does not carry — the oracle's real gap mode.
- A NEW upstream test file with no covering bed is visible in the registry's
  coverage counters — the translation-batch todo, never a faked pass.
- The hardware-bound and nested-VM classes are PARTIAL rows with the recorded
  reason — mapped, honestly not runnable on this venue.

## The selection heuristic ("if it makes sense")

1. ALWAYS include the PR's own changed test files (the existing contract,
   unchanged).
2. ADD the corpus beds by changed-file adjacency:
   - a PR touching `bin/omarchy-*` → the matching `check-omarchy-cli-*` beds;
   - `config/`/`shell/` changes → the shell-corpus beds whose feature name
     matches the changed paths;
   - migration PRs → their named migration beds;
   - visual PRs → the acceptance beds (the screenshots flow into the media
     lane).
3. NEVER select hardware-bound beds (`hw-*`, `t2-*`, `brcmfmac-*`) or
   nested-VM beds (`windows-vm-*`) unless the venue truly has the hardware —
   record PARTIAL instead (the tiers skill).
4. NEVER run the whole corpus per PR — full-corpus runs are the CALIBRATION
   bed's job.
5. A PR with no sensible corpus surface has an EMPTY corpus — `corpus_note`
   says why. Empty is legal; an unexplained empty is not.

## The invocation contract

- The selected beds run against the eval VM via the lane's existing
  check-live surface, filtered per bed; results are structured
  PASS/FAIL/skip — never parsed prose.
- Corpus beds run AFTER the oracle-authored checks and BEFORE the drive
  recording; the acceptance beds run LAST (they open/close apps and mutate
  desktop config).
- No mock, ever: the beds run against the installed product
  (`/usr/share/omarchy` after pr-apply).
- knownRed stays oracle-checks-only: corpus beds are upstream's own contract,
  never negated into the control bed.
- One failing bed never masks the rest: per-bed results are evidence
  (keep-going semantics).
