# AGENTS.md — rules for agent workers in eval-omarchy

> The single rulebook for every harness working in this repo. `CLAUDE.md` is a
> symlink to this file (Claude Code reads that name), so there is no copy to keep in
> sync — edit here.

## What this repo is

eval-omarchy is the home of the **omarchy PR evaluation test environments** and their
**eval results**. It evaluates omacom/omarchy PRs the way **another user would** —
apply the PR to a real omarchy system, use it, and report what happened — on
disposable test environments, with the full evidence rigor.

Every evaluation is **EXTERNAL, NON-AUTHORITATIVE** (performed by opencharly.ai,
informational only, never gates the PR's merge). Hardware-bound classes may be
PARTIAL/NOT-EVALUABLE — never a faked test environment.

## The eval rules (every PR evaluation)

The standing rules live **ONCE** in `eval/PR-EVAL-LANE.md` (+ `eval/references/`) —
every agent and skill points there, never restates. In short: never mock; test like
a user; Assisted-by footer on every posted comment; install missing software before
declaring "couldn't be tested"; test to the maximum extent on a live system; record
both lanes; create reusable packages when software is missing; triage before
authoring; every PR-specific check known-red; every result cold-read validated.

## What each tier proves (honest semantics)

A claim in a report is only as strong as the tier that produced it. Never claim
live-system behavior from a container run.

- **Tier-1 container (pod):** proves the PR's files are applied to the installed
  tree, and the script-level logic with the container's REAL tools (e.g. real
  pacman, real commands, real file state). It does NOT prove live system behavior:
  real hardware switching, real filesystem/snapshot behavior, a real session
  environment, real network state, real keypresses, real service behavior. No
  mocked tools, ever.
- **Tier-2 live VM (omarchy-vm):** proves the PR's behavior on a real omarchy
  system — real cardwire, real btrfs snapshots, real flatpak, real network, real
  desktop. This is the tier for system-behavior claims.
- **Tier-2 visual / L3 GPU:** desktop evidence and hardware-bound classes
  (PARTIAL/NOT-EVALUABLE when the hardware is unavailable — never a faked bed).

The full semantics — the routing rule, the binary purpose of a validation, the
strict prohibition, and honesty about testing — live ONCE in
`eval/references/tiers.md`; every agent and skill points there, never restates.

## The per-PR artifact pattern

Every evaluated PR gets three artifacts, following the established pattern:

| Artifact | Purpose |
|---|---|
| `candy/omarchy-pr-apply/` | The ONE runtime apply seam: `pr-apply <pr> <sha> <files...>` fetches the PR head (SHA-pinned) and installs only its changed files over the installed tree. The git-fetch block lives here and nowhere else (S9) |
| `pr-beds/pr-<N>/charly.yml` | The per-PR test environments, AUTHORED by the config-oracle from its per-PR analysis (§Template in eval/references/oracle-rules.md) — the charly.yml IS the plan: the clone entity (2G/1cpu from the channel golden) + the RED-PROBE bed (same checks, NO apply — must FAIL) + the eval bed (apply via the single seam + known-red behavior checks + the FULL record:/spice: evidence loop). Gate: `charly box validate`; NO hand-edits; NO `run:` steps |
| `charly.yml` | The stable hand-authored config (VM template + golden bases + shared clone); per-PR test environments are oracle-generated into `pr-beds/pr-<N>/` |

The checks must be **known-red**: every PR-specific check fails without the PR
applied. A behavior that cannot be tested with the container's real tools is routed
to the Tier-2 live VM, never mocked.

## The report contract

- Every report (`eval/pr-<N>.md`) and every posted PR comment is rendered from
  `eval/PR-EVAL-TEMPLATE.md` — in user-testing voice, carrying the EXTERNAL,
  NON-AUTHORITATIVE disclaimer verbatim and the Assisted-by footer.
- Claims are scoped to the tier that produced them; untested live behavior is stated
  explicitly ("requires the Tier-2 VM lane").
- Every evaluation result is validated by a **cold reader** against the criteria before
  it is finalized or posted — a fresh reader who did not author the evaluation checks
  never-mock, known-red, tier compliance, scoped claims, non-empty recordings, the
  Assisted-by footer, the disclaimer, and triage. A report that fails the cold read
  is fixed, not posted.
- Reports are **plain language** — understandable to an average user and to an agent
  that knows nothing about opencharly. No charly-internal jargon (R-numbers, ADE,
  RDD, NestedExecutor, keeper, spike, bed, venue, allowlist, etc.). Real config keys
  and file paths are kept as-is; the prose explains them.
- Evidence: `.check/<bed>/<calver>/summary.yml` + per-check logs (gitignored);
  recordings in `media/<pr>-<calver>/` (gitignored); small evidence committed in
  `eval/evidence/`.

## Engineering rules

- **R1 — RCA every anomaly.** Every failure, warning, or divergence from the README
  contract gets root-cause analysis before remediation. No "pre-existing", "out of
  scope", or "follow-up PR" classifications.
- **R3 — No duplication.** One canonical implementation per behavior. The standing
  rules live once in `eval/PR-EVAL-LANE.md` (+ `eval/references/`); the template and
  AGENTS.md point there, never copy them.
- **R4 — No workarounds.** No sleeps, blind retries, or manual fixes. The never-mock
  rule is the fix, not a workaround.
- **R5 — Delete legacy completely.** A cutover removes the old path in the same PR.
- **R6 — Git safety.** `git status` before destructive actions. No force-push, no
  hook bypass, no direct push to `main`.
- **R7 — Prove the gate.** Run `charly box validate` (dev-worktree binary) on the
  final tree and paste the output.
- **R10 — Fresh disposable proof.** Verify from the final committed tree, never from
  an edited state. Every test environment runs the full fresh-rebuild sequence
  (build → check → deploy → check live → fresh update → check again → teardown).

## Git workflow

- Every change lands through a **pull request** on a `feat/` branch — no direct
  push to `main`. The org-wide `charly/pr-validator` gates the merge;
  `tag-on-merge` writes the CHANGELOG from the PR body.
- PR body contract: `## Summary`, `## How tested` (pasted evidence), `## Rulebook
  compliance`, `## Change classification`, and the `*Assisted-by:*` footer.
- Catch up with `origin/main` before finalizing a PR (`git fetch origin main` +
  diff against CURRENT main).
- The umbrella records this repo as a submodule gitlink; a dirty submodule fails the
  umbrella's `verify`.

## Command hygiene

- Bound every command's output (`grep -m N`, redirect to a file, then read bounded).
- Never pipe unbounded grep into `head`/`awk`/`sed`.
- Never re-issue the same diagnostic command in a loop — change approach on
  truncation.

## Skills first (R0)

Before the first tool call of a task, load the relevant skills from the marketplace:

- `omarchy-eval` — the omarchy PR evaluation procedure (never mock, tier semantics,
  known-red fixture, live-VM routing)
- `check` — check beds, plan authoring, R10
- `record` — asciinema + full-screen recording
- `vm` / `local-deploy` / `local-spec` — the live VM lane and the `local:` apply
  seam
- `strict-policy` / `root-cause-analyzer` — R1-R5 discipline
- `git-workflow` — PR-only landing


## Permanent eval-guidance additions (M4, 2026-09-04)

The M4-era guidance — the ORACLE marker rule, the ORACLE path rule, the RUNNER
orphan-sequencing rule — lives ONCE in present-tense standing form:
`eval/references/oracle-rules.md` and `eval/references/lane-sequencing.md`. Its
dated origin (the 16-lane batch, 2026-09-04, with the caught-live examples) is
archived in `CHANGELOG/2026.250.1700.md`. Agents point there; AGENTS.md never
restates the rules.