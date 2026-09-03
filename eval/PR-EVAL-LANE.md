# PR-eval lane — per-channel snapshot bases

**Status:** DESIGNED — declared in the plan (plan/omarchy-pr-eval-alignment.md rev 3); VM bases and the experiment are **pending** and land with the channel-base cutover (distro-omarchy). Nothing here is claimed as run.

## Goal

Evaluate omacom/omarchy PRs the way **another user would** — apply the PR to a real
omarchy system, use it, and report what happened — on disposable test environments,
without a fresh install (~20-30 min) per PR: one base VM per omarchy update channel
(stable / rc / edge / dev), each clean-snapshotted, per-PR revert → apply → check →
evidence → revert.

## Standing rules (every PR evaluation)

1. **Test like a user, not a validator.** Reports and posted comments are first-person:
   what I did, what worked, what did not, what I could not do and why. The evidence
   rigor stays (step matrix, per-check matrix, findings tied to evidence) — only the
   framing changes. Every report is rendered from `eval/PR-EVAL-TEMPLATE.md`.
2. **Assisted-by footer on every posted comment.** Every PR comment ends with
   `*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*`
   (e.g. `*Assisted-by: pi ollama-cloud/deepseek-v4-flash:0731 (fully tested and validated)*`).
3. **Install missing software in the test environment.** When a check fails or a test
   environment cannot complete because a tool/package is missing, install it (extra
   software package / install step, or the system's own package installer) and re-run
   BEFORE declaring "couldn't be tested". Only a genuinely impossible install (package
   in no reachable repository) stays untested — with the exact blocker documented.
   (Canonical case: pr-9332's cardwire gap — try to install it first.)
4. **Test to the maximum extent possible.** Run every applicable test environment
   (container, virtual machine, visual, GPU when hardware is available), exercise the
   PR's own "## Verification" claims, and probe edge cases (idempotence/double-run,
   failure paths, clean-install vs upgrade). Do not stop at the first green check.
5. **Record every evaluation — both lanes.** Every PR evaluation produces a terminal
   asciinema `.cast` AND a full-screen video (desktop recording or VM display
   recording), saved to the gitignored `media/<pr>-<calver>/`. Check output must be
   surfaced on the system's desktop and visible in the recording frames (the
   checks-visible-in-recordings rule below).
6. **Create reusable software packages when software is missing.** When a PR needs
   software or tooling that does not exist yet, create a small reusable package for it
   — following the established rules (scaffold with the scaffolding tool; every package
   needs a description + at least one automated check; one generic package per concern,
   no duplication) — so future PR evaluations reuse it instead of re-installing ad hoc.
   Candidates that fall out of the first PR evals: `omarchy-pr-apply` (generic
   PR-apply package), `omarchy-eval-record` (recording tools), `cardwire` (a
   PR-required tool the omarchy package repository does not ship yet).

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
id — no faked freshness.

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
