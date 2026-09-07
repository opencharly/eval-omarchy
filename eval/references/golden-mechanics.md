# Golden mechanics — the ONE golden-backed lane, provision, keepers, clones

## The ONE eval lane — golden-backed VM (mandatory, R5)

The ONLY PR eval lane is the golden-backed VM: a linked-disk clone of the channel
INSTRUMENTED golden (or the eval-base-inst golden), with the PR applied at runtime via
the single pr-apply seam + the record/spice evidence loop. GPU passthrough is added
ONLY for GPU-class PRs (`requires_exclusive: [nvidia-gpu]`, serial). Everything else
is cut: no fresh ISO installs per PR (S6), no pod-only evals for system-behavior PRs.
A system-behavior PR without the live VM lane gets NO VALIDATION, never a
container-claimed pass. Base provenance is the GOLDEN SNAPSHOT (channel + snapshot
id/sha256), not the installer version.

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

## The per-PR clone + RED-PROBE twins

Per PR: `charly check run check-omarchy-pr-<N>-vm-probe` (RED-PROBE: same checks, NO
apply — must FAIL, exit 2) then `charly check run check-omarchy-pr-<N>-vm` (the eval —
linked-disk lane from the channel INSTRUMENTED golden; NO `--anchor`, NO snapshot on
eval beds; the clone overlay dies with the run). The runner recovers orphans between
them. The VM is a COW overlay on the immutable golden — vm-create ≈ 3-4 s vs the fresh
ISO install ≈ 20-30 min; nothing is reverted because the golden is never written.

The clone entity + the eval/probe bed shape (the one-line pr-apply step, the
plugin-provider-only `add_candy`, the unique known-red check ids) are authored by the
config-oracle from the ORACLE TEMPLATE (§Template) — see `references/oracle-rules.md`.

## Provision / re-provision — the dual state (charly store snapshot + libvirt metadata)

The golden exists in TWO states that must BOTH be verified:

- The **charly store snapshot** (channel + snapshot id/sha256): the golden sha256
  sidecar keys staleness — a re-provisioned golden invalidates every older verdict.
- The **libvirt external-snapshot metadata**: `snapshots/golden/disk.qcow2` +
  `meta.json`. Destroying the VM that holds the only external golden removes the
  disk — only meta.json survives.

Re-provision = **delete-before-recapture**: the old golden is deleted, then recaptured
capture-declared (~2 min). The golden must SURVIVE a failed capture run — a failed
capture run must not destroy it (RCA #7); the runner verifies golden presence post-run.

### Golden keeper-run protocol (obligatory after any golden refresh)

1. Verify the capture: `snapshots/golden/disk.qcow2` EXISTS with a nonzero size.
2. THEN `charly check stop` + destroy the base-inst VM — a refresh run that leaves its
   VM running holds a WRITE LOCK on the fresh golden (stop-domain-after-capture); the
   external goldens are re-capturable (~2 min).
3. BATCH PREFLIGHT: before ANY batch, verify the golden disk's presence — a missing
   golden fails every clone's vm-create with 'Failed to get shared write lock'.
   **Missing golden = BLOCK: no batch starts.**
4. Never destroy a VM while it holds the only external golden without re-capturing
   first.

### Head-freshness rule (mandatory)

The plan's headSha must equal the LIVE PR head (`gh api repos/omacom/omarchy/pulls/<N>`)
— checked BEFORE any run. On drift (the branch was rebased/force-pushed), REGENERATE
the plan + bed to the live head FIRST (verify the marker is still in the new head's
added lines via the diff), never run a stale pin. A fetch-by-PR-ref only brings the
live head's objects — an orphaned pinned commit's tree is unreachable in the guest
(`unable to read tree`). The oracle re-validates head freshness at authoring; the
runner re-checks the triple (plan ↔ bed ↔ live head) at launch.
