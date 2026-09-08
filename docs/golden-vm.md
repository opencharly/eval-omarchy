# The golden VM chain

- Status: **active** — the operator contract for the golden test environments.
- Owner: eval-omarchy maintainers; the config lives in charly.yml (the single source).
- Source of truth: this page for the OPERATOR view; the binding lane rules in
.agents/skills/omarchy-eval-golden/SKILL.md; VM mechanics in /charly-vm:vm and
/charly-internals:disposable.

## The chain

    omarchy-vm  (ISO installer template, kind: vm)
      → check-omarchy-eval-base      (provisions the VM, captures snapshot `golden` — external)
      → check-omarchy-eval-base-inst (the INSTRUMENTED golden: charly, autologin, record tools incl.
                                      acpid, pr-apply, pre-seeded eval-head objects, warmed charly cache
                                      — captured as its own `golden`)
      → per-PR clones (oracle-generated `pr-beds/pr-<N>/charly.yml`:
                      source.kind: clone, from_vm: check-omarchy-eval-base-inst, from_snapshot: golden)

The two golden bases are `disposable: true` deploys (snapshot capture `on_finalize: golden`,
external mode, `keep_venue: true`); per-PR beds are disposable with `lifecycle: dev`.
Disposability is a DEPLOY property, never a VM-entity field (/charly-internals:disposable).

## When to re-provision the golden

- The omarchy channel state must move (a fresh lane bakes a full system upgrade +
  channel update into the instrumented base).
- The pre-seeded eval-head set (`inst-preseed-pr-apply`) must grow/shrink.
- A golden is corrupt/missing (the golden-presence gate fails).
- The distro-omarchy import pin or the schema floor bumps (charly migrate first).

## Provision / re-provision operator loop (condensed)

The BINDING rules (dual-state delete-before-recapture, libvirt metadata, stop-after-capture,
golden-presence verification) are in .agents/skills/omarchy-eval-golden/SKILL.md — run that contract.
Operator summary: clear BOTH the charly store snapshot AND the libvirt metadata, destroy the
old bed domain, run the FRESH lane (check-omarchy-eval-base → check-omarchy-eval-base-inst),
stop the domain so the golden is never held exclusively, then VERIFY
snapshots/golden/disk.qcow2 exists — a missing golden after capture is a BLOCK.

## Per-PR clones

- Clone entity + RED-PROBE twin are oracle-generated (config-oracle) into
  pr-beds/pr-<N>/charly.yml from the committed template; never hand-edited;
  `charly box validate` gates any change.
- Before any run: head-freshness preflight (plan headSha == live PR head).

## Update triggers

- charly.yml golden chain changes → this page + .agents/skills/omarchy-eval-golden/SKILL.md.
- VM snapshot/clone/disposability semantics change → the skills (/charly-vm:vm,
  /charly-internals:disposable), referenced here, never restated.
