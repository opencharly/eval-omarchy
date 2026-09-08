---
name: omarchy-eval-tiers
description: |-
  undefined
---

## What each tier proves (honest semantics)

A claim in a report is only as strong as the tier that produced it. Never claim
live-system behavior from a container run.

- **Tier-1 container (pod):** proves the PR's files are applied to the installed
  tree, and the script-level logic with the container's REAL tools (e.g. real
  pacman, real commands, real file state). It does NOT prove live system behavior:
  real hardware switching, real filesystem/snapshot behavior, a real session
  environment, real network state, real keypresses, real service behavior. No
  mocked tools, ever — a behavior that cannot be tested with the container's real
  tools is tested on the live VM or not claimed.
- **Tier-2 live VM (omarchy-vm):** proves the PR's behavior on a real omarchy
  system — real cardwire, real btrfs snapshots, real flatpak, real network, real
  desktop. This is the tier for system-behavior claims.
- **Tier-2 visual / L3 GPU:** desktop evidence and hardware-bound classes
  (PARTIAL/NOT-EVALUABLE when the hardware is unavailable — never a faked bed).

## Routing rule

A PR whose core behavior is system-level (hardware switching, filesystem/snapshot
behavior, session environment, network state, keybindings, service behavior) MUST
be evaluated on a live VM (Tier-2), not just the container. The container tier
alone is insufficient for these classes.

## The validation's purpose is binary: does it actually work?

The only valid verdicts are PASS (verified working on a live system) and FAIL
(verified not working on a live system). NO VALIDATION means the validation itself
failed — it could not answer the question because the core behavior could not be
tested on a live system.

## Strict prohibition

Any "might work" / "mostly works" / "it works" evaluation that is NOT verified on a
live system is **STRICTLY FORBIDDEN** — it fakes success for something the
validation could not test. A pod-only eval is NOT a validation: the container tier
cannot test live system behavior, so a container run of a system-behavior PR proves
nothing about the PR and must never be presented as a validation. If the validation
cannot test the thing on a live system, the validation itself FAILS — the result is
NO VALIDATION, and no report is produced. A container run never becomes a
live-behavior claim, and an untested live behavior never becomes a pass or a fail —
it becomes nothing.

## Honesty about testing

Bases are disposable test systems rebuilt fresh on installer/channel version bumps;
every PR apply is fresh (revert + re-apply); one full fresh-install verification run
stays per batch; lane-only evals report the "tested on a real system" level unless
the fresh-install run happened; every report records channel + installer version +
snapshot id — no faked freshness. A report's claims are scoped to the tier that
produced them: a container run proves script logic and file application, never live
system behavior. A system-behavior PR whose live tier has not run is reported as
"mostly works — script logic verified; live behavior not yet tested", never as a
live-behavior pass.
