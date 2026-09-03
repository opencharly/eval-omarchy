# PR-eval lane — per-channel snapshot bases

**Status:** DESIGNED — declared in the plan (plan/omarchy-pr-eval-alignment.md rev 3); VM bases and the experiment are **pending** and land with the channel-base cutover (distro-omarchy). Nothing here is claimed as run.

## Goal

Evaluate omacom/omarchy PRs the way **another user would** — apply the PR to a real
omarchy system, use it, and report what happened — on disposable test environments,
without a fresh install (~20-30 min) per PR: one base VM per omarchy update channel
(stable / rc / edge / dev), each clean-snapshotted, per-PR revert → apply → check →
evidence → revert.

## Standing rules (every PR evaluation)

1. **NEVER mock anything — ever.** A check that substitutes a fake tool for the real
   one proves nothing about the PR. Every check must exercise the REAL tool, the REAL
   system state, the REAL behavior. If a behavior cannot be tested with the real
   tools available in the current tier (e.g. real cardwire, real btrfs snapshots, a
   real flatpak session), it must be tested on the live VM tier (Tier-2) — or not
   claimed at all. A mocked check is not evidence; a report built on mocks is
   useless. This rule is first because it is the whole point: an evaluation that
   mocks is not an evaluation.
2. **Test like a user, not a validator.** Reports and posted comments are first-person:
   what I did, what worked, what did not, what I could not do and why. The evidence
   rigor stays (step matrix, per-check matrix, findings tied to evidence) — only the
   framing changes. Every report is rendered from `eval/PR-EVAL-TEMPLATE.md`.
3. **Assisted-by footer on every posted comment.** Every PR comment ends with
   `*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*`
   (e.g. `*Assisted-by: pi ollama-cloud/deepseek-v4-flash:0731 (fully tested and validated)*`).
4. **Install missing software in the test environment.** When a check fails or a test
   environment cannot complete because a tool/package is missing, install it (extra
   software package / install step, or the system's own package installer) and re-run
   BEFORE declaring "couldn't be tested". Only a genuinely impossible install (package
   in no reachable repository) stays untested — with the exact blocker documented.
   (Canonical case: pr-9332's cardwire gap — try to install it first.)
5. **Test to the maximum extent possible — on a live system.** Run every applicable
   test environment (container, virtual machine, visual, GPU when hardware is
   available), exercise the PR's own "## Verification" claims, and probe edge cases
   (idempotence/double-run, failure paths, clean-install vs upgrade). A PR whose core
   behavior is system-level (hardware switching, filesystem/snapshot behavior, session
   environment, network state, keybindings, service behavior) MUST be tested on a live
   omarchy VM (Tier-2), never only in a container. Do not stop at the first green
   check.
6. **Record every evaluation — both lanes.** Every PR evaluation produces a terminal
   asciinema `.cast` AND a full-screen video (desktop recording or VM display
   recording), saved to the gitignored `media/<pr>-<calver>/`. Check output must be
   surfaced on the system's desktop and visible in the recording frames (the
   checks-visible-in-recordings rule below).
7. **Create reusable software packages when software is missing.** When a PR needs
   software or tooling that does not exist yet, create a small reusable package for it
   — following the established rules (scaffold with the scaffolding tool; every package
   needs a description + at least one automated check; one generic package per concern,
   no duplication) — so future PR evaluations reuse it instead of re-installing ad hoc.
   Candidates that fall out of the first PR evals: `omarchy-pr-apply` (generic
   PR-apply package), `omarchy-eval-record` (recording tools), `cardwire` (a
   PR-required tool the omarchy package repository does not ship yet).
8. **Triage before authoring a validation.** Before creating a per-PR test
   environment, decide whether the PR is worth evaluating at all:
   - **Is the PR useful?** Does it fix a real, user-visible problem (check the PR
     body and linked issues)? Is it a meaningful change, or trivial, duplicative,
     superseded, or marked WIP / "do not merge"? A PR that is not useful gets a
     short triage note, not a validation.
   - **Would the evaluation add new insights?** Would the checks tell us something
     we do not already know? If the PR is trivial or its behavior is already fully
     covered by its own tests with nothing new to measure, the evaluation adds no
     insight — skip it (or keep it to a minimal check).
   - **Can the PR be tested on the available hardware?** Hardware-bound classes
     (GPU passthrough, specific laptop hardware, fingerprint readers, and similar)
     where the core behavior cannot be exercised on this machine are recorded as
     "couldn't be tested" with the reason — never a faked test environment, and no
     validation is authored for them.
   - **Which tier proves the behavior?** A system-behavior PR (hardware switching,
     filesystem/snapshot behavior, session environment, network state, keybindings,
     services) must be routed to the live VM tier. If the live tier cannot run (no
     base VM), the PR gets a scoped partial eval or a triage note — never a
     container-only claim of live behavior.
9. **Every PR-specific check must fail without the PR (the known-red fixture).** A
   check that passes on the base image without the PR proves nothing about the PR.
   Each PR-specific check must be red (fail) when the PR is not applied — by
   construction (it asserts a string, file, or behavior that only exists in the PR)
   or by verification (run the checks against the base image without the PR candy and
   confirm they fail). General sanity checks (e.g. "bash is installed") are allowed
   but must be labeled non-PR-specific and never counted as PR proof.

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

**Routing rule:** a PR whose core behavior is system-level (hardware switching,
filesystem/snapshot behavior, session environment, network state, keybindings,
service behavior) MUST be evaluated on a live VM (Tier-2), not just the container.
The container tier alone is insufficient for these classes. If the live tier cannot
run (no base VM), the report must say "live behavior not tested — requires the
Tier-2 VM lane" and the verdict is capped accordingly — a container run never
becomes a live-behavior claim.

## Mechanics (all reuse — no new tooling)

- **Base:** build the omarchy VM from the latest omarchy installer + create/start +
  settle; VM deployments already take a clean snapshot when they finish — that snapshot
  IS the clean base.
- **Channels:** rc / edge / dev bases are the stable base + switch the update channel +
  run the update; the dev base additionally hosts the `~/omarchy` source checkout (the
  channel binds the OS to it) — the PRIMARY upstream-code lane: a PR is applied by
  checking out its head there.
- **Per PR (serial):** restore the clean snapshot → apply the PR at the channel seam →
  run the checks on the live system → persist evidence (`eval/evidence/<pr>-<calver>/`)
  → restore the clean snapshot again.

### The apply seam — a local software template on the snapshot VM

The PR is applied to the snapshot-reverted VM via a **local software template nested
under the VM test environment** (the same pattern used for the Arch test VM — the child
template carries no host and runs inside the guest; every write stays in the guest):

```yaml
check-omarchy-pr-<N>-vm:
    vm:
        from: omarchy-vm
        disposable: true
        lifecycle: dev
        snapshot: {on_finalize: golden, keep_venue: true}
        # … VM hardware/plan …
    omarchy-pr-apply:
        local:
            disposable: true
            lifecycle: dev
            add_candy: [omarchy-pr-apply-<N>, omarchy-eval-record]
            plan:
                - check: the PR files are applied over the installed tree
                  id: pr-applied
                  context: [deploy]
                  command: "…"
                # … recording steps (record: start/cmd/stop, spice: record) …
```

- The apply package fetches the PR head (locked to a specific version) and installs ONLY
  the changed files over the installed tree, then proves application with a check that
  fails if the PR was not applied.
- Alternative (non-test-environment): a top-level local deployment that connects to the
  VM over SSH — valid, but nesting is the test-environment-shaped way (the enclosing
  test environment owns the lifecycle).
- **Prove it first:** this apply step is the lane's named high-risk unknown — prove it
  on a real base VM (a time-boxed experiment) before claiming the lane.

- **Batch:** result cache in `scripts/omarchy-rollup.py` (unchanged heads skipped);
  reports rendered from `eval/PR-EVAL-TEMPLATE.md` with channel + base provenance.

## Honesty about testing

Bases are disposable test systems rebuilt fresh on installer/channel version bumps;
every PR apply is fresh (revert + re-apply); one full fresh-install verification run
stays per batch; lane-only evals report the "tested on a real system" level unless the
fresh-install run happened; every report records channel + installer version + snapshot
id — no faked freshness. A report's claims are scoped to the tier that produced them:
a container run proves script logic and file application, never live system behavior.
A system-behavior PR whose live tier has not run is reported as "mostly works — script
logic verified; live behavior not yet tested", never as a live-behavior pass.

## Experiment (2026-09-02 — run with a real base VM; results honest, run vs NOT-RUN)

**RAN (measured on a live omarchy VM base, installer 4.0.1 unattended install):**
- **Base build+start:** the official installer completed unattended and the guest
  reached a running state within the experiment window.
- **`omarchy update -y` is NOT fully scriptable.** The update progressed through its
  phases (mise upgrade to node 26.7.0, "Update system packages", migration stages) and
  then **stalled without exit at the "Orphan system packages" review stage** — killed
  by timeout after 8 min (`UPDATE_Y_EXIT=KILLED-BY-TIMEOUT`). Keepers must pre-resolve
  orphans or pipe the answer; a bare `-y` does not suffice.
- **CRITICAL — the update's migration disabled AND stopped sshd mid-run** (migration
  1788124236; persistent across reboot), cutting remote access mid-flight. The guest
  agent was NOT connected (no fallback path in the stock guest). Lane rule: never
  kill an update mid-flight; every channel base must ship an ENABLED guest agent as
  a console fallback; updates run with pre-resolved inputs.
- **Halt state:** the base VM was stopped after the experiment (GPU freed; host clean —
  stale leftover test VMs from earlier crashed runs were also undefined).

**NOT-RUN with documented blockers (no fabrication):**
- `omarchy-channel-set` presence/get/set/idempotence probes — access was lost to the
  sshd-disabling migration before they ran; scheduled with the channel-base build.
- pacman `-Syu` guard probe — same blocker.
- Autologin desktop + checks-on-screen — **DONE (2026-09-02, vision-verified)**: the
  logged-in desktop shot and the checks-on-screen shot were produced on a fresh
  channel base (omarchy-autologin composed, distro-omarchy v2026.245.1421) via the
  VM display, and BOTH checked by an AI vision model:
  desktop.png = logged-in Hyprland session (bar, workspaces, clock, tray — no greeter);
  checks-on-screen.png = the same desktop with the running eval check output surfaced
  as on-screen notification cards ("[eval] omarchy-autologin-configured: PASS ...").
  Artifacts at /tmp/d4-shots/{desktop,checks-on-screen}.png.

## Checks visible to the user AND in screen recordings (lane rule)

Whenever an eval runs on a real test system, the check output MUST be surfaced live on
the system's desktop (desktop notifications and/or a visible terminal) AND captured in
the recording/screenshot frames — what the operator sees is what the recording shows.
Recordings and screenshots are graded (by an AI) for containing the on-screen check
output verbatim. Proven on the recording test (notify cards visible in the video frame)
and the screenshot test (eval cards in the VM display).
- Footprint (free/disk) exact values recorded in the experiment session log; qualitative:
  one 8G-RAM VM runs comfortably; VM lanes must SERIALIZE on this GPU-passthrough host
  (the GPU can only be used by one system at a time — measured).

**Open experiment items (carry into the channel-base cutover):** channel-set + guard semantics;
snapshot-survives-recreate; revert-and-start usability; dev-checkout rebuild; footprint
for 4 channel bases. The lane is NOT claimed until those land.

## Phase B decision (2026-09-02 — not pursued, recorded per plan step 5)

The experiment and the anchor runs showed NO measured need for new tooling, so
Phase B is not pursued with this evidence:
- Snapshot create/revert/list/delete: ALREADY EXISTS via the snapshot tooling + the
  VM deployment's snapshot capability — no new commands needed for the lane.
- Per-PR apply: the per-PR package seam (build-time + deploy-time) is the ONE apply
  mechanism (no duplication) — no second mechanism added.
- Batch orchestration: scripts/omarchy-rollup.py (result cache) covers the
  batch loop; the per-channel base VMs cover the bases. A dedicated
  orchestration tool remains a candidate ONLY if batch throughput is measured
  insufficient later — not the case today.
- Host mechanics (measured): the VM-lane fresh-rebuild tail does
  not conclude on this host (a host issue with the development build) and
  VM lanes must serialize on the GPU-passthrough host — those are HOST issues to
  resolve, not tooling gaps.
- Clone-based sources / a snapshot command: no measured need (the clean
  snapshot + snapshot tooling cover the lane) — not pursued.
