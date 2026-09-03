# PR-eval lane — per-channel snapshot bases

**Status:** DESIGNED — declared in the plan (plan/omarchy-pr-eval-alignment.md rev 3); VM bases and the spike are **pending** and land with the channel-keepers cutover (distro-omarchy). Nothing here is claimed as run.

## Goal

Evaluate omacom/omarchy PRs the way **another user would** — apply the PR to a real
omarchy system, use it, and report what happened — on disposable beds, without a fresh
ISO install (~20-30 min) per PR: one base VM per omarchy update channel (stable / rc /
edge / dev), each clean-snapshotted, per-PR revert → apply → check → evidence → revert.

## Standing rules (every PR evaluation)

1. **Test like a user, not a validator.** Reports and posted comments are first-person:
   what I did, what worked, what did not, what I could not do and why. The evidence
   rigor stays (step matrix, per-check matrix, findings tied to evidence) — only the
   framing changes. Every report is rendered from `eval/PR-EVAL-TEMPLATE.md`.
2. **Assisted-by footer on every posted comment.** Every PR comment ends with
   `*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*` (org contract
   form, e.g. `*Assisted-by: pi ollama-cloud/deepseek-v4-flash:0731 (fully tested and validated)*`).
3. **Install missing software in the bed.** When a check fails or a bed cannot complete
   because a tool/package is missing in the venue, install it (per-PR candy add_candy /
   run step, or in-venue pacman / omarchy-pkg-add) and re-run BEFORE declaring
   NOT-EVALUABLE. Only a genuinely impossible install (package in no reachable repo)
   becomes NOT-EVALUABLE — with the exact blocker documented. (Canonical case: pr-9332's
   cardwire gap — try to install it first.)
4. **Test to the maximum extent possible.** Run every applicable tier (Tier-1 pod,
   Tier-2 VM, visual, hybrid-GPU when hardware is available), exercise the PR's own
   "## Verification" claims, and probe edge cases (idempotence/double-run, failure
   paths, clean-install vs upgrade). Do not stop at the first green check.
5. **Record every evaluation — both lanes.** Every PR evaluation produces a terminal
   asciinema `.cast` AND a full-screen video (desktop `record: {record_mode: desktop}`
   or SPICE `spice: record` on VM venues), saved to the gitignored
   `media/<pr>-<calver>/`. Check output must be surfaced on the venue's desktop and
   visible in the recording frames (the checks-visible-in-recordings rule below).
6. **Create reusable candies when software is missing.** When a PR needs software or
   tooling that does not exist yet, create a candy for it — following the established
   rules (`charly box new candy`; non-empty `description:` + ≥1 deterministic
   `check:` step, enforced by `charly box validate`; one generic candy per concern,
   R3) — so future PR evaluations reuse it instead of re-installing ad hoc. Candidates
   that fall out of the first PR evals: `omarchy-pr-apply` (generic PR-apply candy),
   `omarchy-eval-record` (recording layers: tmux + asciinema + wf-recorder/pixelflux),
   `cardwire` (a PR-required tool the omarchy package repo does not ship yet).

## Mechanics (all reuse — no new charly surface)

- **Base:** `charly vm build omarchy-vm` (latest omarchy ISO) + create/start + settle;
  vm deploys already carry `snapshot: {on_finalize: golden, keep_venue: true}`
  (check-charly-omarchy-vm) — the golden snapshot IS the clean base.
- **Channels:** rc / edge / dev bases are the stable base + `omarchy-channel-set <ch>`
  + `omarchy update`; the dev base additionally hosts the `~/omarchy` source checkout
  (the channel binds the OS to it) — the PRIMARY upstream-code lane: a PR is applied by
  checking out its head there.
- **Per PR (serial):** `libvirt: run snapshot/revert (target: clean)` → apply the PR at
  the channel seam → `charly check live <keeper>` the runtime checks → persist evidence
  (`eval/evidence/<pr>-<calver>/`) → revert clean.

### The apply seam — a `local:` candy install on the snapshot VM

The PR is applied to the snapshot-reverted VM via a **`kind: local` template nested
under the vm bed** (the canonical `check-arch-vm` → `arch-host` shape in
`charly/box/arch/charly.yml` — the child `local:` node carries NO `host:` and runs on
NestedExecutor over the guest SSHExecutor; every write stays in the guest):

```yaml
check-omarchy-pr-<N>-vm:
    vm:
        from: omarchy-vm
        disposable: true
        lifecycle: dev
        snapshot: {on_finalize: golden, keep_venue: true}
        # … vm hardware/plan …
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

- The apply candy fetches pull/<N>/head SHA-pinned and installs ONLY the changed files
  over the installed tree, then proves application with a pr-applied check (the known-red
  fixture surfaces a missed apply per-check).
- Alternative (non-bed): a top-level `local:` deploy with `host: charly-<vmname>`
  (SSHExecutor via the managed ssh_config fragment) — valid, but nesting is the
  bed-shaped way (the enclosing bed owns the lifecycle).
- **RDD:** this `local:` apply leg is the lane's named high-risk unknown — prove it on a
  real base VM (spike) before claiming the lane.

- **Batch:** SHA-keyed cache in `scripts/omarchy-rollup.py` (unchanged heads skipped);
  reports rendered from `eval/PR-EVAL-TEMPLATE.md` with channel + base provenance.

## R10 honesty

Bases are disposable deploys rebuilt fresh on ISO/channel calver bumps; every PR apply
is fresh (revert + re-apply); one full fresh-install R10 anchor run stays per batch;
lane-only evals report the `analysed on a live system` tier unless the anchor ran;
every report records channel + ISO calver + snapshot id — no faked freshness.

## Spike (2026-09-02 — run with a real base VM; results honest, run vs NOT-RUN)

**RAN (measured on a live omarchy-vm base, ISO 4.0.1 unattended install):**
- **Base build+start:** the official-ISO install completed unattended and the guest
  reached a running state within the spike window.
- **`omarchy update -y` is NOT fully scriptable.** The update progressed through its
  phases (mise upgrade to node 26.7.0, "Update system packages", migration stages) and
  then **stalled without exit at the "Orphan system packages" review stage** — killed
  by timeout after 8 min (`UPDATE_Y_EXIT=KILLED-BY-TIMEOUT`). Keepers must pre-resolve
  orphans or pipe the answer; a bare `-y` does not suffice.
- **CRITICAL — the update's migration disabled AND stopped sshd mid-run** (migration
  1788124236; persistent across reboot), cutting remote access mid-flight. The qemu
  guest agent was NOT connected (no fallback path in the stock guest). Lane rule: never
  kill an update mid-flight; every keeper base must ship an ENABLED qemu-guest-agent as
  a console fallback; updates run with pre-resolved inputs.
- **Halt state:** the base VM was stopped after the spike (GPU freed; host clean —
  stale leftover check-* domains from earlier crashed runs were also undefined).

**NOT-RUN with documented blockers (no fabrication):**
- `omarchy-channel-set` presence/get/set/idempotence probes — access was lost to the
  sshd-disabling migration before they ran; scheduled with the keeper base build.
- pacman `-Syu` guard probe — same blocker.
- Autologin desktop + checks-on-screen — **DONE (2026-09-02, vision-verified)**: the
  logged-in desktop shot and the checks-on-screen shot were produced on a fresh
  keeper base (omarchy-autologin composed, distro-omarchy v2026.245.1421) via the
  SPICE display head, and BOTH vision-verified (extensions.vision_ask):
  desktop.png = logged-in Hyprland session (bar, workspaces, clock, tray — no greeter);
  checks-on-screen.png = the same desktop with the running eval check output surfaced
  as on-screen notification cards ("[eval] omarchy-autologin-configured: PASS ...").
  Artifacts at /tmp/d4-shots/{desktop,checks-on-screen}.png.

## Checks visible to the user AND in screen recordings (lane rule)

Whenever an eval runs on a real venue, the check output MUST be surfaced live on the
venue's desktop (notify-send cards and/or a visible terminal) AND captured in the
recording/screenshot frames — what the operator sees is what the recording shows.
Recordings and screenshots are graded (ADE) for containing the on-screen check output
verbatim. Proven on the C1 recording lane (notify cards visible in the h264 frame) and
the D4 screenshot lane (eval cards in the SPICE framebuffer).
- Footprint (free/disk) exact values recorded in the spike session log; qualitative:
  one 8G-RAM VM runs comfortably; VM lanes must SERIALIZE on this vfio-flipped host
  (GPU hostdev collides with concurrent VM creates — measured).

**Open spike items (carry into the keepers cutover):** channel-set + guard semantics;
snapshot-survives-recreate; revert-and-start usability; dev-checkout rebuild; footprint
for 4 keepers. The lane is NOT claimed until those land.
## Phase B decision (2026-09-02 — gated OFF, recorded per plan LEG 5)

The spike and the anchor runs showed NO measured need for new charly surface, so
Phase B is gated off with this evidence:
- Snapshot create/revert/list/delete: ALREADY EXISTS via the `libvirt: snapshot/*`
  verb (plugin-vm) + the vm-deploy `snapshot: on_finalize: golden` capability — no
  new verbs/cli needed for the lane.
- Per-PR apply: the per-PR candy seam (build-time + deploy-time) is the ONE apply
  mechanism (R3) — no second mechanism added.
- Batch orchestration: scripts/omarchy-rollup.py (SHA-keyed cache) covers the
  batch loop; the keepers+twins cover the per-channel bases. A `pr-eval`
  orchestration plugin remains a candidate ONLY if batch throughput is measured
  insufficient later — not the case today.
- Host mechanics (measured): the VM-lane fresh-rebuild tail (`charly update`) does
  not conclude on this host (re-exec churn; dev-worktree binary hypothesis) and
  VM lanes must serialize on the vfio-flipped host — those are HOST issues to
  resolve (installed binary / org CI), not plugin gaps.
- `source.kind: clone` / host `charly vm snapshot` CLI: no measured need (the golden
  snapshot + libvirt verbs cover the lane) — gated off.
