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
- The **golden chain** provisioned once: `charly check run check-omarchy-eval-base`
  then `check-omarchy-eval-base-inst` (see `docs/golden-vm.md`).

## How the lane works

The pipeline is a set of **pi agents** committed in the opencharly umbrella
(`.pi/agents/omarchy-{config-oracle,eval-runner,eval-supervisor,cold-reader}.md`)
plus the `pi-omarchy-eval` package (skills + prompts). There is **no GitHub Action**
in the eval path. The binding lane contract is `eval/PR-EVAL-LANE.md` (+ its
`references/`); the report template is `eval/PR-EVAL-TEMPLATE.md`.

## Running one evaluation

```sh
pi -p "<supervisor prompt> /eval-pr <N>"   # or invoke the agents directly
```

or, to run a single generated bed by hand:

```sh
charly check run check-omarchy-pr-<N>-vm        # the eval bed (apply + checks + evidence)
charly check run check-omarchy-pr-<N>-vm-probe  # the RED-PROBE twin (must FAIL exit 2)
```

The bed files under `pr-beds/pr-<N>/` are **oracle-generated** — never hand-edit
them; regenerate via the config-oracle. Before any run, the head-freshness
preflight compares the plan's headSha with the live PR head.

## The publication gate

Reports are rendered from `eval/PR-EVAL-TEMPLATE.md` (user-testing voice, the
the `*Assisted-by:*` footer).
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

The lane instructions are the proper skills under `skills/` — see the index in
`skills/omarchy-eval-lane/SKILL.md` (entry) and AGENTS.md R0. Load the entry + the
skills your task touches (oracle for authoring beds, golden for provisioning, media
for evidence, cold-reader for grading, full-loop for the redo contract) before any
eval work.
