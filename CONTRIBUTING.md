# Contributing to eval-omarchy

This repo runs evaluations of omacom/omarchy PRs on disposable golden-VM
environments — read `VISION.md` for what that is and `README.md` for how it works.

## What you need

- A **charly binary** (schema v2026.244+). The eval beds are charly `kind: check`
  runs; `charly check run <bed>` performs the full disposable sequence
  (build → check image → deploy → check live → fresh update → teardown).
- A **libvirt user-session daemon** (`systemctl --user enable --now virtqemud.service`)
  for the Tier-2 VM lanes, and the host GPU in vfio mode for GPU classes
  (`charly vm gpu status`).
- The **omarchy distro import** (`omarchy: '@github.com/opencharly/distro-omarchy:…'`)
  resolved via the charly binary — no manual checkout needed.
- The **golden chain** provisioned once per channel: `charly check run check-omarchy-eval-base`
  then `check-omarchy-eval-base-inst` / `-edge-inst` / `-rc-inst` / `-dev-inst`
  (see `docs/golden-vm.md`).

## How the lane works

The lane is the `eval-pr-plan` `kind: pipeline` entity in `charly.yml`, running on
the `plugin-pipeline` engine. There is **no GitHub Action** in the eval path. The
binding lane contract is the `omarchy-eval` skill entity (with its
`omarchy-eval-oracle` and `omarchy-eval-cold-reader` siblings) in
`candy/eval-pr/charly.yml`, generated to `marketplace/distros/skills/`; the record
template is the inline `report.template` block of the `eval-pr-plan` pipeline in
`charly.yml`.

The lane grades each PR against the **org-wide `pr-validator` criteria** — the
`pr-validator-agent` `skill:` entity in `opencharly/layer-charly-internals-extra`
(projection: `marketplace/internals/agents/pr-validator.md`), scoped to an upstream
PR by the applicability map in the entry `omarchy-eval` skill. The one difference from
that spec: the pr-validator ASSUMES the author ran R10 and pasted the evidence, whereas
this lane RUNS the R10 itself and feeds its ledger facts (the `gate` stage) to the
`validate` grading stage. The pr-validator PASS/BLOCK verdict and the packet cold-read
verdict are SEPARATE record fields.

## Running one evaluation

```sh
charly pipeline run eval-pr-plan --pr <N>       # oracle → render → control → eval → gate → validate → report → cold-read → record
```

or, to run a single rendered bed by hand:

```sh
charly check run check-omarchy-pr-<N>-vm         # the eval bed (apply + checks + evidence)
charly check run check-omarchy-pr-<N>-control    # the control twin (negated checks, must PASS)
```

`eval/pr-<N>/charly.yml` (both beds) is **rendered by the pipeline's `render` stage** —
never hand-edit it; re-run the oracle (or delete the cached `eval/pr-<N>/eval.yml` to
force fresh triage). The oracle stage caches its reply in `eval/pr-<N>/eval.yml` keyed
on the PR head sha, so a re-run at an unchanged head reuses the plan.

## The publication gate

The record is rendered from the inline `report.template` of the `eval-pr-plan` pipeline
in `charly.yml` (user-testing voice, the `*Assisted-by:*` footer).
**Nothing posts to omacom/omarchy without explicit operator approval.** Every posted
comment is the operator's call, outside the repo's automated flows.

## Landing changes to this repo

- Work on a `feat/` branch; the org-wide `charly/pr-validator` gates the merge;
  `tag-on-merge` writes `CHANGELOG/<calver>.md` from the PR body.
- PR body contract: `## Summary`, `## How tested` (pasted evidence), `## Rulebook
  compliance`, `## Change classification`, and the `*Assisted-by:*` footer.
- Catch up with `origin/main` before finalizing (`git fetch origin main` + diff
  against current main). This repo is a submodule of the umbrella — a dirty
  checkout fails the umbrella's `verify`; the umbrella records the gitlink after
  the merge.
- R10: verify from the final committed tree; a docs/config change that touches
  beds or the golden chain re-runs the affected bed and pastes the per-step
  output.

## Which skills to load

The lane instructions are the `omarchy-eval` skill entity and its
`omarchy-eval-oracle` and `omarchy-eval-cold-reader` siblings in
`candy/eval-pr/charly.yml` (generated to `marketplace/distros/skills/`) — see
the entry `omarchy-eval` and AGENTS.md R0. Load the entry + the skill your
task touches (oracle for triage, cold-reader for grading) before any eval
work.
