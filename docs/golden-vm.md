# The golden VM chain

- Status: **active** — the operator contract for the golden test environments.
- Owner: eval-omarchy maintainers; the config lives in charly.yml (the single source).
- Source of truth: this page for the OPERATOR view; the binding lane rules in the
  `omarchy-eval-golden` skill entity (`candy/eval-lane/charly.yml`); VM mechanics in
  /charly-vm:vm and /charly-internals:disposable.

## The chain

    omarchy-vm  (ISO installer template, kind: vm; omarchy-4.0.3.iso)
      → check-omarchy-eval-base      (provisions the VM, captures snapshot `golden` — external)

    omarchy.omarchy-vm  (the distro import template)
      → check-omarchy-eval-base-inst (the STABLE instrumented golden: charly, autologin, the
                                      record tools incl. acpid, pr-apply, the harden candy,
                                      omarchy-corpus — captured as its own `golden`)
      → check-omarchy-eval-edge-inst (the EDGE twin: channel-bootstrap edge + omarchy-migrate
                                      + the same eval payload; the acceptance corpus clones it)
      → check-omarchy-eval-rc-inst   (the RC twin)
      → check-omarchy-eval-dev-inst  (the DEV twin)
      → per-PR clones (oracle-generated `pr-beds/pr-<N>/charly.yml`:
                      from: <channel-golden>:golden)

The instrumented goldens are `disposable: true`, `lifecycle: dev` deploys with
`snapshot: {on_finalize: golden, mode: external, keep_venue: true}`; per-PR beds are
disposable with `lifecycle: dev` and `update_gate: restart-only`. Disposability is a
DEPLOY property, never a VM-entity field (/charly-internals:disposable).

## When to re-provision the golden

- The omarchy channel state must move (a fresh lane bakes a full system upgrade +
  channel update + the pending migrations into the instrumented twin).
- The pre-seeded eval-head set (`inst-preseed-ok`) must grow/shrink.
- A golden is corrupt/missing (the golden-presence gate fails).
- The distro-omarchy import pin or the schema floor bumps (charly migrate first).

## Provision / re-provision operator loop (condensed)

The BINDING rules (dual-state delete-before-recapture, libvirt metadata, stop-after-capture,
golden-presence verification) are in the `omarchy-eval-golden` skill entity
(`candy/eval-lane/charly.yml`) — run that contract.
Operator summary: clear BOTH the charly store snapshot AND the libvirt metadata, destroy the
old bed domain, run the FRESH lane (`check-omarchy-eval-base` → the channel twins), stop the
domain so the golden is never held exclusively, then VERIFY `snapshots/golden/disk.qcow2`
exists — a missing golden after capture is a BLOCK.

## Per-PR clones

- The eval bed + the negative-control twin are oracle-generated (config-oracle) into
  `pr-beds/pr-<N>/charly.yml` and `pr-beds/pr-<N>-control/charly.yml`; never
  hand-edited; `charly box validate` gates any change. The committed beds let a
  fresh clone rerun every eval.
- Before any run: head-freshness preflight (plan headSha == live PR head).

## Update triggers

- charly.yml golden chain changes → this page + the `omarchy-eval-golden` skill entity.
- VM snapshot/clone/disposability semantics change → the skills (/charly-vm:vm,
  /charly-internals:disposable), referenced here, never restated.
