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

1. **NEVER mock anything — ever.** A check that substitutes a fake tool for the real
   one proves nothing about the PR. Every check must exercise the REAL tool, the REAL
   system state, the REAL behavior. If a behavior cannot be tested with the real
   tools available in the current tier (e.g. real cardwire, real btrfs snapshots, a
   real flatpak session), it must be tested on the live VM tier (Tier-2) — or not
   claimed at all. A mocked check is not evidence; a report built on mocks is
   useless. This rule is first because it is the whole point: an evaluation that
   mocks is not an evaluation.
2. **Test like a user, not a validator.** Reports and posted comments are
   first-person: what I did, what worked, what did not, what I could not do and why.
   The evidence rigor stays (step matrix, per-check matrix, findings tied to
   evidence) — only the framing changes. Every report is rendered from
   `eval/PR-EVAL-TEMPLATE.md`.
3. **Assisted-by footer on every posted comment.** Every PR comment ends with
   `*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*`.
4. **Install missing software in the test environment — REQUIRED before any NO
   VALIDATION.** When a check fails or a test environment cannot complete because a
   tool/package is missing, the evaluator MUST install it — by creating a reusable
   install candy (per rule 7) or an in-venue install — and re-run. NO VALIDATION is
   ONLY valid after installation was genuinely attempted and proved impossible
   (package in no reachable repository), with the exact blocker documented.
   Declaring NO VALIDATION because a tool was not installed is a validation
   failure, not a result.
5. **Test to the maximum extent possible — on a live system.** Run every applicable
   test environment (container, virtual machine, visual, GPU when hardware is
   available), exercise the PR's own "## Verification" claims, and probe edge cases
   (idempotence, failure paths, clean-install vs upgrade). System-behavior PRs MUST
   be tested on a live omarchy VM (Tier-2), never only in a container. Do not stop at
   the first green check.
6. **Record every evaluation — both lanes.** Every PR evaluation produces a terminal
   asciinema `.cast` AND a full-screen video (desktop recording or VM display
   recording), saved to the gitignored `media/<pr>-<calver>/`. Check output must be
   surfaced on the system's desktop and visible in the recording frames.
7. **Create reusable software packages when software is missing.** When a PR needs
   software or tooling that does not exist yet, create a small reusable package for
   it — following the established rules (scaffold with the scaffolding tool; every
   package needs a description + at least one automated check; one generic package
   per concern, no duplication) — so future PR evaluations reuse it.
8. **Triage before authoring a validation.** Is the PR useful (real problem, not
   trivial/duplicative/WIP/"do not merge")? Would the evaluation add new insight?
   Can the core behavior be tested on the available hardware? Which tier proves the
   behavior? A PR that fails triage gets a short triage note, not a report.
9. **Every PR-specific check must fail without the PR (the known-red fixture).** A
   check that passes on the base image without the PR proves nothing about the PR.
   General sanity checks (e.g. "bash is installed") are labeled non-PR-specific and
   never counted as PR proof.

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

**Routing rule:** a PR whose core behavior is system-level (hardware switching,
filesystem/snapshot behavior, session environment, network state, keybindings,
service behavior) MUST be evaluated on a live VM (Tier-2), not just the container.

**The validation's purpose: does it actually work?** The report answers this in a
friendly, first-person voice — like another user who tried the PR — and is
crystal clear about what works and what still needs to be fixed. There are NO
binary PASS/FAIL judgments: the report says "this part works" (verified on a live
system), "this part does not work" (verified on a live system), and "this part is
not yet tested on a live system" (no claim).

**Every "works" claim MUST be verified on a live system.** A part that was not
tested on a live system is never claimed to work — it is stated as "not yet
tested on a live system", clearly, so the PR author knows exactly what still
needs to be fixed or verified. A pod-only eval is NOT a validation: the container
tier cannot test live system behavior, so a container run of a system-behavior PR
proves nothing about the PR and must never be presented as a validation. If the
validation cannot test the thing on a live system, the validation itself fails —
the result is NO VALIDATION, and no report is produced.

## Live-VM SSH contract

SSH on an omarchy VM is established by the DEPLOY flow (seed authorized_keys → sshd +
firewall at install; EnsureIsoGuestSudo → passwordless sudo). A bare `charly vm
create` + `start` does NOT run the deploy and does NOT guarantee sshd. ALWAYS stand up
a live eval base via the existing keeper bed (`charly check run check-charly-omarchy-vm`)
or `charly fleet add`, and verify with `charly vm ssh` — never bare vm create, never
raw ssh, never send-key typing.

## The per-PR artifact pattern

Every evaluated PR gets three artifacts, following the established pattern:

| Artifact | Purpose |
|---|---|
| `candy/omarchy-pr-<N>/charly.yml` | Per-PR package: fetches the PR head (SHA-pinned) and installs its changed files over the installed tree at build time |
| `box/omarchy-suite-base-pr<N>/charly.yml` | Per-PR image: the suite-base + the PR package + the declarative behavior checks (REAL tools only, never mocks) |
| `charly.yml` | The `check-omarchy-suite-pod-pr<N>` test environment (container PR injection) |

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
  rules live once in `eval/PR-EVAL-LANE.md`; the template references them, never
  copies them.
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
