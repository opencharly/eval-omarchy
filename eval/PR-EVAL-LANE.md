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

## Spike (decision gate, before the lane is claimed)

1. snapshot metadata survives `charly update`'s domain destroy+recreate (internal qcow2)?
2. non-destructive layer re-apply path on a running VM?
3. revert-and-start leaves the guest usable for `charly check live`?
4. dev channel: `omarchy-channel-set dev` + update rebuild from `~/omarchy` (checkout
   layout, rebuild trigger)?
5. 4-keepers resource footprint on the host?

Results land in this file when the channel-keepers cutover runs them.
