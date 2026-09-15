# AGENTS.md — rules for agent workers in eval-omarchy

> The single rulebook for every harness working in this repo. `CLAUDE.md` is a
> symlink to this file (Claude Code reads that name), so there is no copy to keep in
> sync — edit here.

## What this repo is

eval-omarchy is the home of the **omarchy PR evaluation test environments** and their
**eval results**. It evaluates omacom/omarchy PRs the way **another user would** —
apply the PR to a real omarchy system, use it, and report what happened — on
disposable test environments, with the full evidence rigor.

Every evaluation runs on the disposable golden-VM lane described in the skills and
reports what was tested and how it went; a class the machine cannot test is recorded as
PARTIAL/NOT-EVALUABLE with the blocker, as part of the test record.

## The eval rules (every PR evaluation)

The standing rules live **ONCE** in the `omarchy-eval` skill entity in
`candy/eval-pr/charly.yml` (+ its `omarchy-eval-oracle` and
`omarchy-eval-cold-reader` siblings, generated to `marketplace/distros/skills/`) —
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
strict prohibition, and honesty about testing — live ONCE in the entry
`omarchy-eval` skill entity (`candy/eval-pr/charly.yml`, "The one experiment" +
"The terminal states"); every agent and skill points there, never restates.

The **FULL LOOP** (every stage grades the previous stage and can trigger a change;
the artifacts-only cold-read; the bounded redo budget) is the `eval-pr-plan`
pipeline's `redo:` edges + the `cold-read` stage contract in `charly.yml` — the
runner never leaves a VM running when done; the cold-reader grades the artifact
packet only.

## The per-PR artifact pattern

Every evaluated PR gets ONE self-contained directory, following the established pattern:

| Artifact | Purpose |
|---|---|
| `candy/omarchy-pr-apply/` | The ONE runtime apply seam: `pr-apply <pr> <sha> <files...>` fetches the PR head (SHA-pinned) and installs only its changed files over the installed tree. The git-fetch block lives here and nowhere else (S9) |
| `eval/pr-<N>/charly.yml` | The per-PR eval + control beds, RENDERED by the pipeline's `render` stage from the config-oracle's reply (the §Template is the `bed_template` block of the `eval-pr-plan` pipeline, `charly.yml`; the oracle contract is the `omarchy-eval-oracle` skill entity, `candy/eval-pr/charly.yml`) — the charly.yml IS the plan: the treatment bed `check-omarchy-pr-<N>-vm` (the clone `from: ${golden}` + apply via the single seam + known-red behavior checks + the FULL record:/spice: evidence loop) and the control twin `check-omarchy-pr-<N>-control` in the SAME file. Gate: `charly box validate` (run by the render stage's validate script); NO hand-edits; NO `run:` steps |
| `eval/pr-<N>/eval.yml` | The single self-contained record: the oracle decision + eval + control + gates + media links + cold read + the user-voice report. The record needs no other file to be read |
| `eval/pr-<N>/media/` | The recordings (gitignored) |
| `charly.yml` | The hand-authored config (VM template + the per-channel instrumented goldens + the `eval-pr-plan` pipeline); the per-PR beds + record are rendered into `eval/pr-<N>/` and COMMITTED so a clone can rerun every eval |

The checks must be **known-red**: every PR-specific check fails without the PR
applied. A behavior that cannot be tested with the container's real tools is routed
to the Tier-2 live VM, never mocked.

## The report contract

- Every report (the `report:` section of `eval/pr-<N>/eval.yml`) and every posted PR
  comment is rendered from the inline `report.template` of the `eval-pr-plan` pipeline
  in `charly.yml` — in user-testing voice, carrying the Assisted-by and Tested-by
  footers.
- Claims are scoped to the tier that produced them; untested live behavior is stated
  explicitly (the lane's claims are Tier-2 live-VM claims — a real omarchy system).
- Every evaluation result is validated by a **cold reader** against the criteria before
  it is finalized or posted — a fresh reader who did not author the evaluation checks
  never-mock, known-red, tier compliance, scoped claims, non-empty recordings, the
  Assisted-by footer, and triage. A report that fails the cold read
  is fixed, not posted.
- Reports are **plain language** — understandable to an average user and to an agent
  that knows nothing about opencharly. No charly-internal jargon (R-numbers, ADE,
  RDD, NestedExecutor, keeper, spike, bed, venue, allowlist, etc.). Real config keys
  and file paths are kept as-is; the prose explains them.
- Evidence: `.check/<bed>/<calver>/summary.yml` + per-check logs (gitignored);
  recordings in `eval/pr-<N>/media/` (gitignored); the committed record is
  `eval/pr-<N>/eval.yml`.

## Engineering rules

- **R1 — RCA every anomaly.** Every failure, warning, or divergence from the README
  contract gets root-cause analysis before remediation. No "pre-existing", "out of
  scope", or "follow-up PR" classifications.
- **R3 — No duplication.** One canonical implementation per behavior. The standing
  rules live once in `candy/eval-pr/charly.yml` (the `omarchy-eval`,
  `omarchy-eval-oracle`, and `omarchy-eval-cold-reader` `skill:` entities); the
  pipeline templates and AGENTS.md point there, never copy them.
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

Before the first tool call of a task, load the relevant skills. From the marketplace:

- `omarchy-eval` — the omarchy PR evaluation procedure (never mock, tier semantics,
  known-red fixture, live-VM routing)
- `check` — check beds, plan authoring, R10
- `record` — asciinema + full-screen recording
- `vm` / `local-deploy` / `local-spec` — the live VM lane and the `local:` apply
  seam
- `strict-policy` / `root-cause-analyzer` — R1-R5 discipline
- `git-workflow` — PR-only landing

Plus the REPO skills authored as `skill:` entities in `candy/eval-pr/charly.yml`
(the binding lane contract, generated to `marketplace/distros/skills/` — in addition
to the marketplace procedure): `omarchy-eval` (the entry: the one experiment, the
terminal states, the per-PR artifact), `omarchy-eval-oracle` (the triage contract +
the control re-author contract), and `omarchy-eval-cold-reader` (the cold-read rubric
+ the packet verdict).


## Permanent eval-guidance additions (M4, 2026-09-04)

The M4-era guidance — the ORACLE marker rule (author assertions that are red by
construction: they reference the PR's own added lines) and the ORACLE path rule
(assert at ABSOLUTE system paths) — lives ONCE in present-tense standing form in the
`omarchy-eval-oracle` skill entity
(`candy/eval-pr/charly.yml`, "The triage steps" 3–4). Its dated origin (the 16-lane
batch, 2026-09-04, including the caught-live orphan-sequencing incidents) is archived
in `CHANGELOG/2026.250.1700.md`. Agents point there; AGENTS.md never restates the
rules.