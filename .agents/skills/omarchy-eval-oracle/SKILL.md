---
name: omarchy-eval-oracle
description: |-
  The per-PR config the config-oracle authors: class/lean sizing, per-channel goldens, the ORACLE TEMPLATE, pr-apply seam, marker/path rules, known-red contract. Use before authoring a pr-beds/pr-<N>/charly.yml.
---

# Oracle rules — the apply seam, the ORACLE TEMPLATE, the check-plan contract

## The apply seam — the ONE runtime seam (pr-apply), no nested templates

The PR is applied at RUNTIME by the single helper `pr-apply <pr> <sha> <changed-files...>`
(candy/omarchy-pr-apply — the git-fetch block lives THERE and nowhere else; S9 guard:
`grep 'git fetch .* pull/'` matches only that candy). The helper is baked into the
instrumented golden, so the eval bed's apply step is exactly one line. Mutation lives in
candies (bed-plan `run:` steps are dead code in VM beds — RCA #2); the eval/probe beds
carry only `check:` steps.

## The check-plan contract (known-red + golden freshness)

The probe proves known-red (S7) AND golden freshness; a probe that passes = stale golden
or a non-red check → re-provision the golden (delete-before-recapture; the golden must
survive — RCA #7: a failed capture run must not destroy it, the runner verifies golden
presence post-run).

## Purpose-built VM configs — match the PR's hardware class (MANDATORY)

Every PR is classified BEFORE its bed is authored (Tier-0 venue ladder / lane tier
semantics). An eval of a HARDWARE-dependent PR on a box WITHOUT that hardware is useless:

| PR | Subject | Hardware class | VM config |
|---|---|---|---|
| #9332 | hybrid GPU switching (supergfxctl → cardwire) | **GPU — the REAL cardwire GPU switching needs the passed-through GPU** | `check-omarchy-pr-<N>-vm` (drive) + `requires_exclusive: [nvidia-gpu]`, SERIAL (one GPU) |
| software PRs | (everything else, e.g. Btrfs/low-space, flatpak, keybindings, panels) | software | `check-omarchy-pr-<N>-vm` (drive, lean base) |

- **Lean class (software PRs):** the clone (COW overlay on the golden), no GPU,
  **ram 2G / cpu 1** (the committed per-PR beds are the record) — runs MANY in PARALLEL,
  ONE EVAL LANE PER CPU CORE by default (concurrency = nproc, capped so 2G × lanes ≤
  host RAM); each VM starts from the golden, no rebuild).
- **GPU class (GPU PRs):** the same clone PLUS the NVIDIA GPU passthrough
  (`requires_exclusive: [nvidia-gpu]`, whole-IOMMU-group hostdev auto-allocated by
  `charly vm create`, entity uses `backend: libvirt` + `firmware: uefi-insecure`).
  SERIAL — one GPU, one such eval at a time. NEVER evaluate a GPU PR on a lean box.
- **A system-behavior PR evaluated only in a container is a HARD FAIL** (routing rule).

## Per-channel golden bases

The lane is per-channel: the STABLE/current channel instrumented golden is
`check-omarchy-eval-base-inst` (charly + autologin + record tools incl. acpid + pr-apply
+ pre-seeded eval heads + warmed cache, captured `on_finalize: golden`). The rc / edge /
dev channel bases live in the distro-omarchy import
(`check-charly-omarchy-{rc,edge,dev}-vm`, each the stable base + its channel bootstrap,
dev hosts the `~/omarchy` source checkout — the PRIMARY upstream-code lane). A PR's
channel is chosen from its base/diff; the clone drives `from: <channel-base>:golden`
and the report records channel + base provenance (channel, ISO calver, snapshot id).

## ORACLE TEMPLATE (§Template) — the canonical dedicated per-PR config

The plan IS the per-PR config: the config-oracle analyses the PR (class, channel, tier,
changed files, `## Verification` claim, known-red markers) and authors
`pr-beds/pr-<N>/charly.yml` DIRECTLY (gate: `charly box validate`; NO hand-edits; no
`run:` steps — mutation lives in candies, RCA #2). No separate plan JSON: the charly.yml
is the single artifact (the M4-era `pr-plans/eval-plan-<N>.json` orchestrator files
were removed in the legacy cut — the charly.yml is the only plan artifact).

> REDO-INFRA CLASS (measured 2026-08-08): a vm-build `Failed to get "write" lock`
> (the shared-overlay race between overlapping lanes) is an INFRA redo-run trigger,
> never a bed or oracle defect — re-gate the lane per the sequencing skill.
>
> RUNTIME-FIXED (measured 2026-08-08): the clone-ENTITY grammar (source.kind: clone +
> from_vm/from_snapshot/ram/cpu) VALIDATES but is REJECTED at RUNTIME vm-build on the
> current charly ("source.from_snapshot is required for clone" — the verification run
> failed at probe vm-build). The executable clone is the **from: <base>:<tag> DRIVE**;
> the drive INHERITS the shape from its target, so per-entity ram/cpu is impossible —
> the lean 2G/1cpu sizing lives on the BASE entity (`omarchy-vm` at ram 2G / cpu 1;
> all clones inherit it). PROBE beds carry NO media loop (media skill). The CONFIG
> AUDIT MUST include a RUNTIME check (a real vm-build launch), not only `charly box
> validate`.

```yaml
check-omarchy-pr-<N>-vm:
    vm:
        from: <channel-base>:golden
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
            # … the PR-specific behavior checks (every one known-red: diff-ADDED markers,
            #   proven-landing paths; ids unique) …
            # … the FULL record:/spice: evidence loop (mandatory, rule 6):
            #   rec-start (record: start) → rec-spice-start (spice: record) → rec-drive
            #   (record: run) → rec-screen-spice (spice: screenshot) → rec-spice-stop
            #   (spice: record stop → .mjpeg) → rec-stop (record: stop → .cast) →
            #   rec-gif (record: gif) → rec-mp4 (ffmpeg transcode) …
check-omarchy-pr-<N>-vm-probe:   # RED-PROBE twin: same checks, NO apply — must FAIL (exit 2)
    vm:
        from: omarchy-vm-clone-<N>
        disposable: true
        lifecycle: dev
        add_candy: [plugin-record, plugin-spice pins]
        plan:
            # … the SAME PR-specific checks, no pr-apply step …
```

Media contract (rule 6): every evaluation produces a terminal asciinema `.cast` AND a
screen recording; the record: and spice: steps pull every artifact onto the host; the
EVAL RUNNER assembles them into the gitignored `media/<pr>-<calver>/` (pi file tools, no
scripts) and the COLD READER grades them (vision on the frames + the deterministic .cast
text).

Expected-phase budget (per-PR ram/cpu/phase estimates feeding stage 3 anomaly detection)
belongs to the oracle's plan.

The SUPERVISOR agent maintains the verdict ledger (the `.check/` summaries ARE the
data; the golden sha256 sidecar keys staleness — a re-provisioned golden invalidates
every older verdict). Unchanged heads are skipped by the supervisor's ledger; reports
render from `eval/PR-EVAL-TEMPLATE.md` with channel + base provenance. No scripts —
the agents read the native artifacts directly.

### The ORACLE marker rule (mandatory)

A PR-specific check marker MUST be a **diff-ADDED token** (a string in the PR's added
lines, never a word that pre-exists in the base). Verified against the base before the
bed ships: a probe that does NOT fail (exit 2) on the golden = **RED-PROBE-BROKEN = a
PROCESS block** — no eval is valid from that bed (S7).

### The ORACLE path rule (mandatory)

A check path must be from a **PROVEN-LANDING class** (`bin/`, `shell/`, `migrations/` —
verified by pr-apply) or verified against the post-apply tree. An `etc/` path that does
not land at its expected installed location makes the check path wrong by construction.

## NO VALIDATION is a LAST RESORT — never the default

A report that says NO VALIDATION is an admission that the evaluation itself failed.
Before that verdict is ever written, ALL of these must have been exhausted, in order:

1. **Run the PR's own test suites** (`test/cli`, `test/shell`, `test/shell.d/*`)
   on the live system — the PR's own "## Verification" claims are the first thing to
   measure, and they are almost always runnable.
2. **Try to install the missing software for real** (rule 4): the package repository,
   AUR, the project's own releases. A tool that exists on AUR is installable — "not in
   the omarchy repo" is NOT a blocker when AUR has it.
3. **Test the real behavior with the real tools** on the live VM (Tier-2): real pacman,
   real df/findmnt, real config trees, real services. Script-level logic (detection,
   fallbacks, error paths, install paths) is testable even when the full hardware cycle
   is not.
4. **Record what WAS tested** — a PARTIAL verdict with the real evidence (which suites
   passed, which real behaviors were measured, which branches were not triggered and
   why) is always better than NO VALIDATION.

Only a genuinely impossible test (hardware the machine does not have, a credential the
environment does not have, a package in no reachable repository) stays untested — with
the exact blocker documented. Canonical counter-example: pr-9332 was reported NO
VALIDATION because "cardwire is not in the omarchy package repository" — but cardwire
IS on AUR, the PR's own test suites run, and the scripts' real behavior (detection
fallback, install-path failure) is measurable. The re-evaluation found all of it.
