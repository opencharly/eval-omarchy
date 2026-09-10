# omarchy-eval-tests

The omarchy test-corpus map — the Config Oracle's guide to the charly-native
equivalents of omarchy's own tests. The oracle consults this skill to SELECT
the corpus surfaces that make sense for a PR; the lane runs them against the
eval VM.

## The corpus lives in charly.yml — ONE source, CUE-validated

The corpus is the `omarchy-corpus` candy in this repo's `charly.yml`
(`candy/omarchy-corpus/charly.yml`, flattened into the project charly.yml by
the box load). There is NO side manifest file: **charly.yml is the single
source** and `charly box validate` CUE-validates it. The mapping data is the
plan itself:

- every check step's `id:` is the corpus bed identity the oracle selects;
- the step's section comment names the upstream test file
  (`# === test/shell.d/<feature>-test.sh - ... ===`) — the PROVENANCE
  convention, greppable from charly.yml;
- the coverage is DERIVED, never authored: the count of the corpus steps in
  the candy's plan vs the upstream corpus size (the config-audit computes it
  from charly.yml — no side file to drift).

## The selection heuristic ("if it makes sense")

1. ALWAYS include the PR's own changed test files (the existing contract,
   unchanged).
2. ADD the corpus beds by changed-file adjacency:
   - a PR touching `bin/omarchy-*` → the matching `cli-*` bed steps;
   - `config/`/`shell/` changes → the shell-corpus steps whose feature name
     matches the changed paths;
   - migration PRs → their named migration steps;
   - visual PRs → the acceptance steps (the screenshots flow into the media
     lane).
3. NEVER select hardware-bound surfaces (`hw-*`, `t2-*`, `brcmfmac-*`) or
   nested-VM surfaces (`windows-vm-*`) unless the venue truly has the
   hardware — record PARTIAL instead (the tiers skill).
4. NEVER run the whole corpus per PR — full-corpus runs are the CALIBRATION
   bed's job.
5. A PR with no sensible corpus surface has an EMPTY corpus — `corpus_note`
   says why. Empty is legal; an unexplained empty is not.

## The invocation contract

- The selected steps run against the eval VM via the lane's existing
  check-live surface; results are structured PASS/FAIL/skip — never parsed
  prose.
- Corpus steps run AFTER the oracle-authored checks and BEFORE the drive
  recording; the acceptance surfaces run LAST (they open/close apps and
  mutate desktop config).
- No mock, ever: the surfaces run against the installed product
  (`/usr/share/omarchy` after pr-apply).
- knownRed stays oracle-checks-only — corpus surfaces are upstream's own
  contract, never negated into the control bed.
- One failing surface never masks the rest: per-surface results are evidence
  (keep-going semantics).

## The lane's gap surface

- A SETUP_DEFECT is recorded when the ORACLE selects a corpus step the candy's
  plan does not carry — the triage's validate gate rejects the selection
  (every selected id must exist as a step `id:` in charly.yml), and the
  informed redo re-authors.
- A NEW upstream test file with no covering corpus step is visible to the
  oracle reading charly.yml — the translation-batch todo, never a faked pass.
- The hardware-bound and nested-VM classes are PARTIAL with the recorded
  reason — mapped, honestly not runnable on this venue.
