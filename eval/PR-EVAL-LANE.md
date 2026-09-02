# PR-eval lane — per-channel snapshot bases

**Status:** DESIGNED — declared in the plan (plan/omarchy-pr-eval-alignment.md rev 3); VM bases and the spike are **pending** and land with the channel-keepers cutover (distro-omarchy). Nothing here is claimed as run.

## Goal

Multi-PR evaluation without a fresh ISO install (~20-30 min) per PR: one base VM per
omarchy update channel (stable / rc / edge / dev), each clean-snapshotted, per-PR
revert → apply → check → evidence → revert.

## Mechanics (all reuse — no new charly surface)

- **Base:** `charly vm build omarchy-vm` (latest omarchy ISO) + create/start + settle;
  vm deploys already carry `snapshot: {on_finalize: golden, keep_venue: true}`
  (check-charly-omarchy-vm) — the golden snapshot IS the clean base.
- **Channels:** rc / edge / dev bases are the stable base + `omarchy-channel-set <ch>`
  + `omarchy update`; the dev base additionally hosts the `~/omarchy` source checkout
  (the channel binds the OS to it) — the PRIMARY upstream-code lane: a PR is applied by
  checking out its head there.
- **Per PR (serial):** `libvirt: run snapshot/revert (target: clean)` → apply the PR at
  the channel seam (dev: checkout in ~/omarchy + update; edge/rc/stable: deploy-time
  per-PR candy) → `charly check live <keeper>` the runtime checks → persist evidence
  (`eval/evidence/<pr>-<calver>/`) → revert clean.
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
  phases (mise upgrade to node 26.7.0, “Update system packages”, migration stages) and
  then **stalled without exit at the “Orphan system packages” review stage** — killed
  by timeout after 8 min (`UPDATE_Y_EXIT=KILLED-BY-TIMEOUT`). Keepers must pre-resolve
  orphans or pipe the answer; a bare `-y` does not suffice.
- **CRITICAL — the update’s migration disabled AND stopped sshd mid-run** (migration
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
- Autologin desktop + both screenshots (plain desktop + checks-on-screen) — wedged,
  unreachable guest; to be produced on the clean keeper base (autologin composed) as
  part of the keepers’ real proof.
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
