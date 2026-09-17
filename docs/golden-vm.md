# The golden VM chain

- Status: **active** — the operator contract for the golden test environments.
- Owner: eval-omarchy maintainers; the config lives in the per-role sibling files
  (`vm.yml`, `golden.yml`, …) flat-`import:`ed by `charly.yml` (the single source).
- Source of truth: this page for the OPERATOR view; the binding golden chain entities live
  in `vm.yml` (`omarchy-vm`) + `golden.yml` (`check-omarchy-eval-base`, the four
  `check-omarchy-eval-*-inst` twins); VM mechanics in /charly-vm:vm and
  /charly-internals:disposable.

## The chain

    omarchy-vm  (ISO installer template, kind: vm; omarchy-4.0.4.iso, 2G / 2 vCPU)
      → check-omarchy-eval-base      (provisions the VM, captures snapshot `golden` — external)

    omarchy-vm  (the SAME unified template — every chain golden derives from it)
      → check-omarchy-eval-base-inst (the STABLE instrumented golden: charly, autologin, the
                                      record tools incl. acpid, pr-apply, the harden candy,
                                      omarchy-corpus — captured as its own `golden`)
      → check-omarchy-eval-edge-inst (the EDGE twin: channel-bootstrap edge + omarchy-migrate
                                      + the same eval payload; the acceptance corpus clones it)
      → check-omarchy-eval-rc-inst   (the RC twin)
      → check-omarchy-eval-dev-inst  (the DEV twin)
      → per-PR clones (oracle-rendered `eval/pr-<N>/charly.yml`:
                      from: <channel-golden>:golden)

The instrumented goldens are `disposable: true`, `lifecycle: dev` deploys with
`snapshot: {on_finalize: golden, mode: external, keep_venue: true}`; the rendered per-PR
beds are disposable with `lifecycle: dev` and `update_gate: skip`. Disposability is a
DEPLOY property, never a VM-entity field (/charly-internals:disposable).

## When to re-provision the golden

- The omarchy channel state must move (a fresh lane bakes a full system upgrade +
  channel update + the pending migrations into the instrumented twin).
- The pre-seeded eval-head set (`inst-preseed-ok`) must grow/shrink.
- A golden is corrupt/missing, OR **STALE** — its backing disk was rebuilt after the
  capture (`charly vm build` then refuses a clone with an explicit STALE error).
- The distro-omarchy import pin or the schema floor bumps (charly migrate first).

## Provision / re-provision operator loop (condensed)

The binding golden chain lives in `vm.yml` (`omarchy-vm`) → `golden.yml`
(`check-omarchy-eval-base` → the four `check-omarchy-eval-*-inst` twins) — run those
entities.
Operator summary: clear BOTH the charly store snapshot AND the libvirt metadata, destroy the
old bed domain, run the FRESH lane (`check-omarchy-eval-base` → the channel twins), stop the
domain so the golden is never held exclusively, then VERIFY `snapshots/golden/disk.qcow2`
exists — a missing golden after capture is a BLOCK.

## Per-PR clones

- The eval bed + the negative-control twin are rendered by the `render` stage from the
  oracle's reply, both into ONE committed file `eval/pr-<N>/charly.yml` (treatment
  `check-omarchy-pr-<N>-vm` + control `check-omarchy-pr-<N>-control`); never hand-edited;
  the render stage's validate gate runs `charly box validate`. The committed beds let a
  fresh clone rerun every eval.
- Head freshness: the oracle stage caches its result in the committed
  `eval/pr-<N>/eval.yml` keyed on `$env.PR_HEAD_SHA` — a cache hit skips triage; a new PR
  head (or a first run) re-authors the plan fresh.

## Update triggers

- vm.yml / golden.yml golden chain changes → this page.
- VM snapshot/clone/disposability semantics change → the skills (/charly-vm:vm,
  /charly-internals:disposable), referenced here, never restated.
