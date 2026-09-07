# PR-eval lane — per-channel snapshot bases

**Status:** OPERATIONAL — the stable hand-authored `charly.yml` holds only the VM
template + golden bases + the shared clone; per-PR evals are oracle-generated
(`pr-beds/pr-<N>/`): RED-PROBE (must FAIL) then the eval (linked-disk lane on the
instrumented golden; NO `--anchor`, NO snapshot; the clone overlay dies with the
run). Channel bases for rc/edge/dev follow the same instrumented-golden seam.

## Goal

Evaluate omacom/omarchy PRs the way **another user would** — apply the PR to a real
omarchy system, use it, and report what happened — on disposable test environments,
without a fresh install (~20-30 min) per PR: one base VM per omarchy update channel
(stable / rc / edge / dev), each clean-snapshotted, per-PR revert → apply → check →
evidence → revert.

## The lane state machine (all reuse — no new tooling)

- **Base:** the omarchy VM is built from the latest omarchy installer + create/start +
  settle; VM deployments already take a clean snapshot when they finish — *that snapshot IS the clean base*.

- **Channels:** rc/edge/dev bases are the stable base + switch the update channel +
  run the update; the dev base additionally hosts the `~/omarchy` source checkout (the
  channel binds the OS to it) — the PRIMARY upstream-code lane: a PR is applied by
  checking out its head there.
- **Per PR:** `charly check run check-omarchy-pr-<N>-vm-probe` (RED-PROBE: same checks,
  NO apply — must FAIL, exit 2) then `charly check run check-omarchy-pr-<N>-vm` (the
  eval — linked-disk lane from the channel INSTRUMENTED golden; NO `--anchor`, NO
  snapshot on eval beds; the clone overlay dies with the run). The runner recovers
  orphans between them. Nothing is reverted because the golden is never written.
- **Parallel batch (lean PRs):** lean evals launch CONCURRENTLY (one per PR, each its
  own .check lock + domain + COW overlay); the only host limits are RAM (4G/VM) and
  vCPU (4/VM). The GPU-class eval runs alone (SERIAL).

Hardware-class VM configs + the full golden mechanics: `references/golden-mechanics.md`.
Batch/concurrency sequencing: `references/lane-sequencing.md`.

## Standing rules (every PR evaluation)

1. **NEVER mock anything — ever.** A check that substitutes a fake tool for the real
   one proves nothing about the PR. Every check must exercise the REAL tool, the REAL
   system state, the REAL behavior; a behavior not testable with the current tier's
   real tools must be tested on the live VM tier (Tier-2) — or not claimed at all. An
   evaluation that mocks is not an evaluation.
2. **Test like a user, not a validator.** Reports and posted comments are first-person:
   what I did, what worked, what did not, what I could not do and why — with the full
   evidence rigor kept (step matrix, per-check matrix, findings tied to evidence).
   Every report is rendered from `eval/PR-EVAL-TEMPLATE.md`.
3. **Assisted-by footer on every posted comment.**
   `*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*`.
4. **Install missing software in the test environment.** When a check fails or a test
   environment cannot complete because a tool/package is missing, install it (extra
   software package / install step, or the system's own package installer) and re-run
   BEFORE declaring "couldn't be tested". Only a genuinely impossible install (package
   in no reachable repository) stays untested — with the exact blocker documented.
   (Canonical case: pr-9332's cardwire gap — the install is tried first.)
5. **Test to the maximum extent possible — on a live system.** Run every applicable
   test environment (container, VM, visual, GPU when hardware is available), exercise
   the PR's own "## Verification" claims, and probe edge cases (idempotence, failure
   paths, clean-install vs upgrade). A PR whose core behavior is system-level
   (hardware switching, filesystem/snapshot behavior, session environment, network
   state, keybindings, service behavior) MUST be tested on a live omarchy VM (Tier-2),
   never only in a container — a wrong-tier eval is a HARD FAIL, never a soft pass. Do
   not stop at the first green check.
6. **Record every evaluation — both lanes.** Every PR evaluation produces a terminal
   asciinema `.cast` AND a full-screen video, saved to the gitignored
   `media/<pr>-<calver>/`. Check output must be surfaced on the system's desktop AND
   visible in the recording frames (checks-visible-in-recordings rule). Media
   contract: `references/media-contract.md`.
7. **Create reusable software packages when software is missing.** When a PR needs
   software or tooling that does not exist yet, create a small reusable package for it
   — scaffold with the scaffolding tool; a description + at least one automated check
   each; one generic package per concern — so future evaluations reuse it instead of
   re-installing ad hoc.
8. **Triage before authoring a validation.** Before creating a per-PR test
   environment, decide whether the PR is worth evaluating at all:
   - **Is the PR useful?** Does it fix a real, user-visible problem (PR body + linked
     issues), or is it trivial, duplicative, superseded, or WIP / "do not merge"? A PR
     that is not useful gets a short triage note, not a validation.
   - **New insights?** Would the checks tell us something we do not already know? If
     the behavior is already covered with nothing new to measure, skip (or minimize).
   - **Testable on the available hardware?** Hardware-bound classes (GPU passthrough,
     laptop hardware, fingerprint readers, and similar) that cannot be exercised are
     recorded as "couldn't be tested" with the reason — never a faked test
     environment, and no validation is authored for them.
   - **Which tier proves the behavior?** A system-behavior PR must be routed to the
     live VM tier; if the live tier cannot run (no base VM), the PR gets a scoped
     partial eval or a triage note — never a container-only claim of live behavior.
9. **Every PR-specific check must fail without the PR (the known-red fixture).** A
   check that passes on the base image without the PR proves nothing about the PR.
   Each PR-specific check must be red (fail) when the PR is not applied — by
   construction (it asserts a string, file, or behavior that only exists in the PR)
   or by verification (run the checks against the base image without the PR candy and
   confirm they fail). General sanity checks are allowed but must be labeled
   non-PR-specific and never counted as PR proof.
10. **Every evaluation result is validated by a cold reader against the criteria.**
    Before a report is finalized or a comment is posted, a fresh reader who did NOT
    author the evaluation validates it: never mock, known-red (every PR-specific check
    fails without the PR), tier compliance (system-behavior PRs on the live VM;
    wrong-tier = FAIL), claims scoped to the tier, recordings non-empty and showing
    the actual commands, Assisted-by footer present, disclaimer verbatim, triage
    applied. The verdict is recorded in the report; a report that fails the cold read
    is fixed, not posted. Rubric: `references/cold-reader.md`.

## The ONE eval lane — golden-backed VM (mandatory, R5)

- **The ONLY PR eval lane is the golden-backed VM**: a linked-disk clone of the
  channel INSTRUMENTED golden (or the eval-base-inst golden), with the PR applied at
  runtime via the single pr-apply seam + the record/spice evidence loop. GPU
  passthrough is added ONLY for GPU-class PRs (requires_exclusive: [nvidia-gpu],
  serial). Everything else is cut: no fresh ISO installs per PR (S6), no pod-only
  evals for system-behavior PRs. A system-behavior PR without the live VM lane gets
  NO VALIDATION, never a container-claimed pass.
- Base provenance is the GOLDEN SNAPSHOT (channel + snapshot id/sha256), not the
  installer version — the template's "Who ran this" reflects it (see
  PR-EVAL-TEMPLATE.md).
- Provision/re-provision, keeper-run protocol, per-PR clone + RED-PROBE twins, head
  freshness: `references/golden-mechanics.md`.

## NO VALIDATION semantics

The validation's purpose is binary: does it actually work? The only valid verdicts
are PASS (verified working on a live system) and FAIL (verified not working on a
live system). NO VALIDATION means the validation itself failed — it could not answer
the question because the core behavior could not be tested on a live system.

**Strict prohibition:** any "might work" / "mostly works" / "it works" evaluation
that is NOT verified on a live system is **STRICTLY FORBIDDEN** — it fakes success
for something the validation could not test. A pod-only eval is NOT a validation: the
container tier cannot test live system behavior, so a container run of a
system-behavior PR proves nothing about the PR and must never be presented as a
validation. If the validation cannot test the thing on a live system, the validation
itself FAILS — the result is NO VALIDATION, and no report is produced. A container
run never becomes a live-behavior claim, and an untested live behavior never becomes
a pass or a fail — it becomes nothing.

NO VALIDATION is a **LAST RESORT — never the default**: before that verdict is ever
written, the exhaustion ladder must be run (the PR's own test suites on the live
system, try to install the missing software for real, test the real behavior with the
real tools, and record a PARTIAL with the real evidence):
`references/oracle-rules.md`.

## The ORACLE rules and tier routing (condensed — full detail in references/)

- **ORACLE marker rule (mandatory):** a PR-specific check marker MUST be a
  **diff-ADDED token** (a string in the PR's added lines, never a word that
  pre-exists in the base), verified against the base before the bed ships: a probe
  that does NOT fail (exit 2) on the golden = **RED-PROBE-BROKEN = a PROCESS block** —
  no eval is valid from that bed (S7).
- **ORACLE path rule (mandatory):** a check path must be from a **PROVEN-LANDING
  class** (`bin/`, `shell/`, `migrations/` — verified by pr-apply) or verified
  against the post-apply tree.
- **Tier routing rule:** a PR whose core behavior is system-level (hardware switching,
  filesystem/snapshot behavior, session environment, network state, keybindings,
  service behavior) MUST be evaluated on a live VM (Tier-2), not just the container —
  the container tier alone is insufficient for these classes.
- Full detail: the apply seam + ORACLE TEMPLATE (§Template) + check-plan contract +
  NO VALIDATION ladder → `references/oracle-rules.md`; tier semantics + strict
  prohibition + honesty about testing → `references/tiers.md`.

## The publication gate

No report is finalized and no comment is posted until ALL hold:

- **Cold-read validation passed** (standing rule 10): the verdict is recorded in the
  report; a report that fails the cold read is fixed, not posted.
- **Process cleanliness:** any process defect (non-red probe, wrong tier, claim
  scoped beyond the tier, media missing/empty or not showing the commands, footer or
  disclaimer missing) = **REDO-PROCESS** (setup update + full re-run), never a posted
  report.
- **Evidence persisted:** `eval/evidence/<pr>-<calver>/summary.yml` + per-check logs
  committed; recordings assembled in `media/<pr>-<calver>/` (gitignored).

## Index — where every topic lives

| Topic | File |
|---|---|
| Standing rules 1–10 | this file |
| Tier semantics, routing rule, strict prohibition, honesty about testing | `references/tiers.md` |
| The apply seam (pr-apply), ORACLE TEMPLATE (§Template), ORACLE marker/path rules, check-plan contract, NO VALIDATION ladder | `references/oracle-rules.md` |
| Orphan sequencing, HARD lane-sequencing gate, launch sequencing, run preflight, concurrency guidance (16/32-lane), host/guest responsibility split, expected-phase budget | `references/lane-sequencing.md` |
| Checks-visible-in-recordings, THREE-artifact media contract, media-density rule, media assembly, media directory contract | `references/media-contract.md` |
| ONE golden-backed lane mechanics, provision/re-provision dual-state, keeper-run protocol, per-PR clone + RED-PROBE twins, head freshness | `references/golden-mechanics.md` |
| COLD-READER RUBRIC, vision-deterministic cross-check (GNOME trap), adversarial self-test, calibration, judge rule, per-eval stats contract, RCA stats-signature discipline, deep-eval tool protocol | `references/cold-reader.md` |
| Dated RCA narratives, experiments, measurements (archived) | `CHANGELOG/2026.250.1700.md` |
