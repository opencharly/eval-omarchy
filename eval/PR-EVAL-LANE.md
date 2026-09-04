# PR-eval lane — per-channel snapshot bases

**Status:** OPERATIONAL — the stable INSTRUMENTED golden is provisioned and captured (check-omarchy-eval-base-inst; the 1210/1251 runs PASS, all three golden checks green; durability verified — the golden must survive every re-provision, RCA #7) and the STABLE hand-authored charly.yml holds only the VM template + golden bases + the shared clone. Per-PR evals are oracle-generated (pr-beds/pr-<N>/): RED-PROBE (must FAIL) then the eval (linked-disk lane on the instrumented golden; NO --anchor, NO snapshot; the clone overlay dies with the run). Channel bases for rc/edge/dev follow the same instrumented-golden seam.

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
   omarchy VM (Tier-2), never only in a container. A system-behavior PR evaluated
   only in a container is a HARD FAIL (wrong tier) — never a soft pass. Do not stop
   at the first green check.
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
10. **Every evaluation result is validated by a cold reader against the criteria.**
    Before a report is finalized or a comment is posted, a fresh reader who did NOT
    author the evaluation validates the report against the validation criteria:
    never mock (no mocked checks), known-red (every PR-specific check fails without
    the PR), tier compliance (system-behavior PRs tested on the live VM; wrong-tier =
    FAIL), claims scoped to the tier (no live-behavior claims from container runs),
    recordings non-empty and showing the actual commands, Assisted-by footer present,
    disclaimer verbatim, triage applied. The cold reader's verdict is recorded in the
    report; a report that fails the cold read is fixed, not posted.

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
The container tier alone is insufficient for these classes.

**The validation's purpose is binary: does it actually work?** The only valid
verdicts are PASS (verified working on a live system) and FAIL (verified not
working on a live system). NO VALIDATION means the validation itself failed — it
could not answer the question because the core behavior could not be tested on a
live system.

**Strict prohibition:** any "might work" / "mostly works" / "it works" evaluation
that is NOT verified on a live system is **STRICTLY FORBIDDEN** — it fakes
success for something the validation could not test. A pod-only eval is NOT a
validation: the container tier cannot test live system behavior, so a container
run of a system-behavior PR proves nothing about the PR and must never be
presented as a validation. If the validation cannot test the thing on a live
system, the validation itself FAILS — the result is NO VALIDATION, and no report
is produced. A container run never becomes a live-behavior claim, and an untested
live behavior never becomes a pass or a fail — it becomes nothing.

## Mechanics (all reuse — no new tooling)

- **Base:** build the omarchy VM from the latest omarchy installer + create/start +
  settle; VM deployments already take a clean snapshot when they finish — that snapshot
  IS the clean base.
- **Channels:** rc / edge / dev bases are the stable base + switch the update channel +
  run the update; the dev base additionally hosts the `~/omarchy` source checkout (the
  channel binds the OS to it) — the PRIMARY upstream-code lane: a PR is applied by
  checking out its head there.

### Purpose-built VM configs — match the PR's hardware class (MANDATORY)

An eval of a HARDWARE-dependent PR on a box WITHOUT that hardware is useless — the
eval config must match what the PR exercises. Every PR is classified BEFORE its bed is
chosen:

| PR | Subject | Hardware class | VM config |
|---|---|---|---|
| #9332 | hybrid GPU switching (supergfxctl → cardwire) | **GPU — the REAL cardwire GPU switching needs the passed-through GPU** | `omarchy-vm-clone-gpu` (clone + `requires_exclusive: [nvidia-gpu]`, SERIAL — one GPU) |
| #9893 | low-space update errors (Btrfs snapshot boot detection) | software | `omarchy-vm-clone` (lean) |
| #9894 | Tailscale panel reconnect | software | `omarchy-vm-clone` (lean) |
| #9906 | Flatpak desktop entries | software | `omarchy-vm-clone` (lean) |
| #9912 | `omarchy pkg add` group-aware | software | `omarchy-vm-clone` (lean) |
| #9917 | terminal launch speed | software | `omarchy-vm-clone` (lean) |
| #9921 | SUPER+A select-all keybinding | software | `omarchy-vm-clone` (lean) |
| #9923 | network panel split-brain | software | `omarchy-vm-clone` (lean) |

- **Lean class (software PRs):** `omarchy-vm-clone` — the clone (COW overlay on the
  golden), **no GPU**, 4G RAM — runs MANY in PARALLEL (≈ 16 evals on a 64G host; each
  VM starts from the golden, no rebuild). A GPU-less eval of a software PR is correct
  AND the fastest possible.
- **GPU class (GPU PRs):** `omarchy-vm-clone-gpu` — the same clone PLUS the NVIDIA
  GPU passthrough (`requires_exclusive: [nvidia-gpu]`, the whole-IOMMU-group hostdev
  auto-allocated by `charly vm create`). The REAL cardwire GPU switching is only
  meaningful here. SERIAL — one GPU, one such eval at a time. Classify the PR first;
  NEVER evaluate a GPU PR on a lean box (the behavior is hardware-bound → the eval is
  worthless).
- **Per PR:** `charly check run check-omarchy-pr-<N>-vm-probe` (RED-PROBE: same checks, NO
  apply — must FAIL, exit 2) then `charly check run check-omarchy-pr-<N>-vm` (the eval —
  linked-disk lane from the channel INSTRUMENTED golden; NO --anchor, NO snapshot on eval
  beds; the clone overlay dies with the run). The runner recovers orphans between them.
  The VM is a COW overlay on the immutable golden — vm-create ≈ 3-4 s vs the fresh ISO
  install ≈ 20-30 min; nothing is reverted because the golden is never written.
- **Parallel batch (lean PRs):** launch the lean evals CONCURRENTLY (one per PR, each
  its own .check lock + domain + COW overlay); the only host limits are RAM (4G/VM) and
  vCPU (4/VM). The GPU eval runs alone.
- **Media (every run):** the record: and spice: check steps pull every artifact onto the
  host (`.cast`, `.gif` via the record plugin's gif method, SPICE frames/video); the EVAL RUNNER agent then assembles them into the gitignored `media/<pr>-<calver>/` (pi file tools — no scripts) and the COLD READER grades them (vision_ask on the frames + the deterministic .cast text). Eval rule 6: every evaluation produces a terminal .cast AND a screen recording.

### The apply seam — the ONE runtime seam (pr-apply), no nested templates

The PR is applied at RUNTIME by the single helper `pr-apply <pr> <sha> <changed-files...>`
(candy/omarchy-pr-apply — the git-fetch block lives THERE and nowhere else; S9 guard:
`grep 'git fetch .* pull/'` matches only that candy). The helper is baked into the
instrumented golden, so the eval bed's apply step is exactly one line. Mutation lives in
candies (bed-plan `run:` steps are dead code in VM beds — RCA #2); the eval/probe beds
carry only `check:` steps.

#### ORACLE TEMPLATE (§Template) — the canonical per-PR config the config-oracle agent authors

`pr-beds/pr-<N>/charly.yml` (gate: `charly box validate`; NO hand-edits; no `run:` steps):

```yaml
# Generated by the config-oracle agent from pr-plans/eval-plan-<N>.json (§Template) — DO NOT hand-edit.
omarchy-vm-clone-<N>:
    vm:
        source: {kind: clone, from_vm: check-omarchy-eval-base-inst, from_snapshot: golden}
        disk_size: 40G
        ram: 4G
        cpu: 4
        machine: q35
        firmware: uefi-insecure
        network: {mode: user}
        ssh: {user: user, port_auto: true, key_source: generate}
        backend: libvirt
        libvirt:
            devices:
                channels: [{type: spicevmc, name: com.redhat.spice.0}]
                graphics: [{type: spice, listen: [{type: socket}]}]
                video: [{model: virtio, vram: 65536, heads: 1, accel3d: false}]
                rng: [{model: virtio, backend: /dev/urandom}]
                memballoon: {model: virtio}
            snippets:
                - "<channel type='unix'><target type='virtio' name='org.qemu.guest_agent.0'/></channel>"
check-omarchy-pr-<N>-vm:
    vm:
        from: omarchy-vm-clone-<N>
        disposable: true
        lifecycle: dev
        add_candy:              # ONLY the plugin provider candies (verbs register at check-run time)
            - '@github.com/opencharly/plugin-record/candy/plugin-record:v2026.246.1624'
            - '@github.com/opencharly/plugin-spice/candy/plugin-spice:v2026.245.1508'
        plan:
            - check: apply PR #<N> via the single apply seam
              id: pr-apply
              context: [runtime]
              command: 'pr-apply <N> <sha> <file...>'
            # … the PR-specific behavior checks (every one known-red; ids unique) …
            # … the record:/spice: evidence loop (record: start/run/stop/gif + spice: screenshot) …
check-omarchy-pr-<N>-vm-probe:   # RED-PROBE twin: same checks, NO apply — must FAIL (exit 2)
    vm:
        from: omarchy-vm-clone-<N>
        disposable: true
        lifecycle: dev
        add_candy: [plugin-record, plugin-spice pins]
        plan:
            # … the SAME PR-specific checks, no pr-apply step …
```

The probe proves known-red (S7) AND golden freshness; a probe that passes = stale golden
or a non-red check → re-provision the golden (delete-before-recapture; the golden must
survive — RCA #7: a failed capture run must not destroy it, the runner verifies golden
presence post-run). Class routing, channel choice, vCPU/RAM sizing and the expected-phase
budget belong to the oracle (Tier-0 venue ladder; GPU class SERIAL `requires_exclusive:
[nvidia-gpu]`; a system-behavior PR evaluated only in a container is a HARD FAIL).

- **Batch:** the SUPERVISOR agent maintains the verdict ledger (the `.check/` summaries ARE the data; the golden sha256 sidecar keys staleness — a re-provisioned golden invalidates every older verdict). Unchanged heads are skipped by the supervisor's ledger; reports render from `eval/PR-EVAL-TEMPLATE.md` with channel + base provenance. No scripts — the agents read the native artifacts directly.

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
- Batch orchestration: the supervisor agent's ledger + the per-channel base VMs
  cover the batch loop (the SHA-keyed skip now lives in the agent's ledger, keyed
  bed+calver+golden-sha256). A dedicated orchestration tool remains a candidate
  ONLY if batch throughput is measured insufficient later — not the case today.
- Host mechanics (measured): the VM-lane fresh-rebuild tail does
  not conclude on this host (a host issue with the development build) and
  VM lanes must serialize on the GPU-passthrough host — those are HOST issues to
  resolve, not tooling gaps.
- Clone-based sources / a snapshot command: no measured need (the clean
  snapshot + snapshot tooling cover the lane) — not pursued.

## NO VALIDATION is a LAST RESORT — never the default

A report that says NO VALIDATION is an admission that the evaluation itself
failed. Before that verdict is ever written, ALL of these must have been
exhausted, in order:

1. **Run the PR's own test suites** (`test/cli`, `test/shell`, `test/shell.d/*`)
   on the live system — the PR's own "## Verification" claims are the first
   thing to measure, and they are almost always runnable.
2. **Try to install the missing software for real** (rule 4): the package
   repository, AUR, the project's own releases. A tool that exists on AUR is
   installable — "not in the omarchy repo" is NOT a blocker when AUR has it.
3. **Test the real behavior with the real tools** on the live VM (Tier-2):
   real pacman, real df/findmnt, real config trees, real services. Script-level
   logic (detection, fallbacks, error paths, install paths) is testable even
   when the full hardware cycle is not.
4. **Record what WAS tested** — a PARTIAL verdict with the real evidence
   (which suites passed, which real behaviors were measured, which branches
   were not triggered and why) is always better than NO VALIDATION.

Only a genuinely impossible test (hardware the machine does not have, a
credential the environment does not have, a package in no reachable
repository) stays untested — with the exact blocker documented. The canonical
counter-example: pr-9332 was reported NO VALIDATION because "cardwire is not
in the omarchy package repository" — but cardwire IS on AUR, the PR's own
test suites run, and the scripts' real behavior (detection fallback,
install-path failure) is measurable. The re-evaluation found all of it.


## M4 findings — permanent guidance (16-lane batch, 2026-09-04)

### The ORACLE marker rule (mandatory)
A PR-specific check marker MUST be a **diff-ADDED token** (a string in the PR's added lines, never a word that pre-exists in the base). Verified against the base before the bed ships: a probe that does NOT fail (exit 2) on the golden = **RED-PROBE-BROKEN = a PROCESS block — no eval is valid from that bed** (S7). Caught live: 10115 `countdown` (base theme token), 10130 `reblank` (the PR uses re-arm/rearmed), 10134 `vscode` (base `VS_CODE_THEME_DESCRIPTOR`) — all fixed with diff-added tokens (`showCountdown`, `blankArmed`, `_watch`).

### The ORACLE path rule (mandatory)
A check path must be from a PROVEN-LANDING class (`bin/`, `shell/`, `migrations/` — verified by pr-apply) or verified against the post-apply tree. `etc/` (10140) failed to land at `/usr/share/omarchy/etc/...` — the check path was wrong by construction.

### The RUNNER orphan-sequencing rule (mandatory)
A FAILED probe leaves the VM running "for debugging"; `charly check stop` releases the flock but does NOT destroy the VM — the eval's clone vm-build collides on the overlay write-lock (caught: 10116/10125/10129 eval-attempt-1). Sequence: probe verdict → `charly check stop` → `charly vm destroy <entity> --domain <bed>` → eval.

### Concurrency guidance (16-lane)
- Golden-lock: NEVER start a batch while a golden-provisioning run is active (the 21:00 attempts crashed on the held golden).
- The shared `~/.config/charly/ssh_config` rewrite across 16 parallel lanes raced (10134 deploy-add "Could not resolve hostname") — a charly shared-state observation; the lane retry after the config settled succeeded. Recorded as an upstream candidate.

### Measured speed profile (folded into the hill-climb baseline)
- update 61 s → 28 s (payload baked; var.), cleanup 182 s → 4–8 s (acpid), evals avg ≈ 150 s (was 437 s); 10134 @ 82 s with the trimmed media (settle_ms 300, single frame). Remaining levers: update-gate change-class (operator decision), deploy-add resolver+staging (~30 s), boot floor.


## The ONE eval lane — golden-backed VM (mandatory, R5)

- **The ONLY PR eval lane is the golden-backed VM**: a linked-disk clone of the channel INSTRUMENTED golden (or the eval-base-inst golden), with the PR applied at runtime via the single pr-apply seam + the record/spice evidence loop. GPU passthrough is added ONLY for GPU-class PRs (requires_exclusive: [nvidia-gpu], serial). Everything else is cut: no fresh ISO installs per PR (S6), no pod-only evals for system-behavior PRs. A system-behavior PR without the live VM lane gets NO VALIDATION, never a container-claimed pass.
- Base provenance is the GOLDEN SNAPSHOT (channel + snapshot id/sha256), not the installer version — the template's "Who ran this" reflects it (see PR-EVAL-TEMPLATE.md).


## COLD-READER RUBRIC (M6, permanent) — the grading contract for every eval result

A cold read is a FRESH-CONTEXT validation of the eval evidence (the report + the media + the ledger) against the criteria. It issues TWO verdicts:

- **SUBJECT** (about the PR): PASS (verified working on a live system) / FAIL (verified not working) / NO VALIDATION. Any "might work" framing for untested live behavior is STRICTLY FORBIDDEN.
- **PROCESS** (about the eval itself): every PR-specific check known-red (probe FAIL exit 2 observed), tier compliance (system PRs on the live VM), claims scoped to the tier, media non-empty AND showing the commands, footer + disclaimer verbatim. Any process defect = REDO-PROCESS (setup update + full re-run), never a posted report.

### The vision-deterministic cross-check (mandatory, the GNOME trap)
The vision model can mislabel the desktop (measured: Hyprland+Quickshell repeatedly called "GNOME"). Every material vision claim MUST be corroborated by a deterministic source: the .cast text, the wl:/spice:/record: verb outputs, or the config. A vision claim without corroboration is a PROCESS finding. Reading lanes: vision_ask/pi.read on SPICE frames + the GIF; ffmpeg frames from screen.mp4; the .cast text (the terminal lane truth).

### The adversarial self-test (performed at M6 and whenever the rubric changes)
Feed the reader deliberately MISLABELED frames (e.g., a real GNOME-desktop screenshot labeled as the omarchy eval output, or the Hyprland desktop labeled "boot failure") + verify the reader flags the mismatch via the deterministic cross-check. A reader that accepts a mislabeled frame without a PROCESS finding FAILS the self-test.

### Calibration (one past-report re-audit)
Re-audit one previously finalized eval (from eval/) with the current rubric; the audit's verdict (PASS/FAIL-of-process) is recorded in the findings ledger as the calibration baseline.


### The THREE-artifact media contract (mandatory, every eval)
Every eval lane produces ALL THREE artifacts — no exceptions:
1. **`.cast`** — the ascii screencast of the checks: `record: {method: start, record_mode: terminal, record_name: <pr>}` → the drive step → `record: {method: stop, artifact: …/pr-<N>.cast, artifact_min_bytes: 200}`.
2. **`.gif`** — the screencast rendered to an animated GIF (the record verb render method).
3. **`screen.mp4`** — the SPICE OUTPUT as video via the shipped `spice: record` method (plugin-spice v2026.245.1508+: the host-side MJPEG capture polls the display at fps, default 5): `spice: {method: record, action: start, fps: 5}` BEFORE the drive, the drive steps, then `spice: {method: record, action: stop, artifact: /tmp/pr-<N>.mjpeg, artifact_min_bytes: 10000, artifact_not_uniform: true}` (an empty/static stream honest-fails the validators). ONE `run:` step transcodes the MJPEG to MP4 (`ffmpeg -y -loglevel error -i /tmp/pr-<N>.mjpeg -c:v libx264 -pix_fmt yuv420p /tmp/pr-<N>-screen.mp4`). Charly-native: no frame-assembly workarounds — the capture IS the spice video stream; the ffmpeg step only relabels containers.

### The judge rule (cold-reader)
- **ALWAYS** read the `.cast` (the terminal-lane truth: exact commands, exit codes, timestamps).
- **MP4 review ON DEMAND only**: review the `screen.mp4` (frames via ffmpeg + vision_ask) ONLY when the plan's `visual:` flag is true (the PR's diff touches the desktop UI — panels, notifications, themes, overlays, animations) or the diff clearly implies visual change. A non-visual PR (config/scripts/docs) never needs the mp4 — the .cast + check results suffice.
- Every material vision claim is corroborated by a deterministic source (the .cast/wl/spice text) — the GNOME-mislabel trap applies to mp4 frames too.


### Head-freshness rule (RCA 2026-09-04: PR 10147's branch was force-pushed upstream — the pinned head became orphaned and pr-apply failed with `unable to read tree`)
The plan's headSha must equal the LIVE PR head (gh api repos/omacom/omarchy/pulls/<N>) — checked BEFORE any run. On drift (the branch was rebased/force-pushed), REGENERATE the plan + bed to the live head FIRST (verify the marker is still in the new head's added lines via the diff), never run a stale pin. A fetch-by-PR-ref only brings the live head's objects — an orphaned pinned commit's tree is unreachable in the guest. The oracle re-validates head freshness at authoring; the runner re-checks the triple (plan ↔ bed ↔ live head) at launch.
