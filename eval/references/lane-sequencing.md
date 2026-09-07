# Lane sequencing — orphans, gates, launch, preflight, concurrency

### The RUNNER orphan-sequencing rule (mandatory)

A FAILED probe leaves the VM running "for debugging"; `charly check stop` releases the
flock but does NOT destroy the VM — the eval's clone vm-build collides on the overlay
write-lock. Sequence: probe verdict → `charly check stop` → `charly vm destroy
<entity> --domain <bed>` → eval.

### HARD lane-sequencing gate

A batch may launch ONLY when ALL hold:

1. ZERO live batch VMs (`ps aux | grep qemu-system | grep -oE 'guest=charly-check-omarchy-pr-[0-9]+-vm'`
   = empty; the anchored residents are expected and budgeted).
2. ZERO in-flight `charly check run` processes for the batch beds.
3. The golden disk EXISTS (nonzero) and NO base-inst VM holds its lock.
4. RAM budget: lanes × 2G + residents + OS ≤ usable RAM; load1 < 20 before launch.
5. Between a stop and a relaunch: `charly check stop` each leftover run, THEN destroy
   each VM (domstate check), THEN verify the count is zero.
6. The ugate/evidence or keeper-run VM must conclude before a measurement batch (shared
   golden + shared host).

### Launch sequencing

A wave launches ONLY after the lock table is verified clean:

1. `ps aux | grep -cE '/charly/bin/charly check run'` == 0 (no live run procs).
2. No bed `.check/check-omarchy-pr-<N>-vm/.lock` is HELD (the flock, not just the file
   — a stale file is free; a live holder blocks).
3. Then launch, THEN re-verify: the running unit count for the wave equals the expected
   lane count.

### Run preflight — the stale ssh-fragment stanza

BEFORE every run: drop the bed's alias from the managed ssh fragment
(`~/.config/charly/ssh_config` — the `Host charly-check-omarchy-pr-<N>-vm` stanza:
`sed`/regex-remove the block) so the create re-publishes the CURRENT passt port. A
re-run against a stale stanza parks the pre-deploy readiness gate (zero CPU, zero
children, no probe). The deeper charly fix (the publish should always refresh the port
on re-runs) is recorded for the plugin-vm lifecycle PR.

### Concurrency guidance (16-lane) — standing form of the 16/32-lane lessons

- **Golden-lock:** a batch NEVER starts while a golden-provisioning run is active (the
  golden is held — concurrent launches crash on it).
- **Shared ssh-config state:** the shared `~/.config/charly/ssh_config` rewrite races
  across parallel lanes (deploy-add "Could not resolve hostname"); a retry after the
  config settles succeeds. Recorded as an upstream candidate.
- **Lane ceiling:** lane count stays ≤ 16 unless the per-lane cost shrinks further —
  beyond 16 concurrent VM lifecycles the vm-store/libvirt queue inflates the late
  slots and throughput goes DOWN (measured at 32).
- **Launch detachment:** long lanes MUST be launched detached —
  `setsid <cmd> </dev/null > log 2>&1 &`. A plain nohup inside a tool-call session
  dies when the caller's call is cancelled.
- **Oversubscription:** while the host materialized-tree cache is absent, stay at
  ≤16 lanes / 1 vCPU (the oversubscription amplifier).

### The host/guest responsibility split

- `target: local` deploy inside a VM: the guest = an SSHExecutor target
  (`ssh user@127.0.0.1:37xxx`); `host: local` = the ShellExecutor (direct shell on
  that machine). The install plan walks via the shared out-of-process walk; the steps
  the deploy:local plugin cannot render (`BuilderStep`/`LocalPkgInstallStep`/
  `SystemPackagesStep`/`OpStep`/…) marshal to the charly on the host over the
  EXECUTOR REVERSE CHANNEL.
- The loader routes the merged-tree materialization to the host
  (`ResolveMergedDeployTreeViaExecutor` → the executor `HostBuild` seam) — the guest
  does NOT re-unify per child in-guest; the HOST re-materializes the merged CUE unify
  PER CHILD (no cache).
- The root fix = the host materialized-tree cache at the executor seam — later children
  reuse one unify.
- ANY future "why is the guest slow" RCA must first check the marshaling layer: which
  step runs where (guest vs host) + whether the host-side op is cached.

## Expected-phase budget (oracle-owned, feeds plan stage 3)

Class routing, channel choice, vCPU/RAM sizing and the expected-phase budget belong to
the oracle. The expected-phase budget (per-phase expected durations) feeds plan stage 3:
every phase's expected duration is budgeted before launch; a run that materially
exceeds its budget is investigated via the per-eval stats (stats-signature discipline),
never accepted blindly.
