# eval-omarchy

Dedicated home for the **omarchy PR evaluation test environments** and their **eval results**.

> **External, non-authoritative:** every evaluation in this repo is an **EXTERNAL,
> NON-AUTHORITATIVE evaluation** performed by **opencharly.ai**. It is informational
> only: it does not represent, endorse, or bind omacom/omarchy or its maintainers, is
> not a substitute for upstream review, and does not approve, block, or gate the PR's
> merge. Hardware-bound classes may be PARTIAL/NOT-EVALUABLE — never faked.

Every evaluation answers one binary question — **does the PR actually work?** — on a
real omarchy system, the way another user would try it. The PR's files are applied at
RUNTIME to a lean clone of a **golden VM image** (built from the official Omarchy
installer ISO), the behavior is asserted with known-red checks, both recording lanes
run, and a cold reader grades the artifact packet before anything is finalized.

> **What is charly?** charly is the open-source tool that builds and runs these test
> environments. A **candy** is a small, reusable software package charly installs into
> an environment; a **check bed** is the declarative recipe that builds, deploys,
> probes, and tears down one environment. You do not need to know charly to read an
> evaluation — every report is written in plain language.

## The golden VM image (from the downloaded Omarchy ISO)

`charly.yml` holds the golden chain — the reproducible base every evaluation clones:

| Entity | What it is |
|---|---|
| `omarchy-vm` | The VM template: `source.kind: iso` downloads the official **Omarchy installer ISO** (`https://iso.omarchy.org/omarchy-4.0.1.iso`, sha256-checked), runs the unattended install (user `user`, hostname `omarchy`), 40G disk / 4G RAM / 4 vCPU, q35 + UEFI, libvirt, SPICE + guest agent |
| `check-omarchy-eval-base` | Provisions that VM and captures an external **`golden` snapshot** at install-finalize; adds the charly toolchain |
| `check-omarchy-eval-base-inst` | The **INSTRUMENTED golden** (the stable/current channel's base): the base golden + autologin, the record tooling (incl. acpid), the `pr-apply` helper, asciinema + the record/spice plugin providers — then bakes the current channel state (full upgrade + omarchy channel update), cleans the pacman cache, pre-seeds the eval-head git objects and warms the charly cache — captured as its own golden |
| `check-charly-omarchy-{dev,edge,rc}-vm` | The **per-channel bases** (in the distro-omarchy import): the stable base + each channel's bootstrap — dev hosts the `~/omarchy` source checkout (the primary upstream-code lane) |

Every evaluation clones the PR's **channel golden** as a lean COW overlay
(**40G / 2G / 1 vCPU**, SPICE + guest agent — the committed per-PR beds are the
record), so each VM starts in seconds from the immutable golden. The golden survives
every re-provision (RCA #7); a missing golden after capture is a BLOCK. The full
provision/re-provision runbook (delete-before-recapture, dual-state cleanup,
golden-presence gates, head-freshness) is the `skills/omarchy-eval-golden` skill.

## The evaluation workflow (the pi-agent lane)

The pipeline runs on **pi agents** committed in the opencharly umbrella
(`.pi/agents/omarchy-{config-oracle,eval-runner,eval-supervisor,cold-reader}.md`) and
driven by the **skills in this repo** (`skills/omarchy-eval-lane` is the entry). There
is no GitHub Action in the eval path.

1. **TRIAGE + PLAN (config-oracle).** Classify the PR (class, channel, tier); read the
diff + the PR's `## Verification` claim; design PR-specific known-red checks (diff-ADDED
markers at proven-landing paths). **The plan IS the config**: the oracle authors a
DEDICATED `pr-beds/pr-<N>/charly.yml` per PR (clone entity from the channel golden at
2G/1cpu, RED-PROBE twin that must fail, eval bed with the `pr-apply` seam + the FULL
record:/spice: evidence loop). Gate: `charly box validate`. No JSON plans.
2. **RED-PROBE (eval-runner).** `charly check run check-omarchy-pr-<N>-vm-probe` —
must FAIL (exit 2): every PR-specific check is red on the golden (known-red + golden
freshness). Exit 0 = RED-PROBE-BROKEN = a process block, never an eval.
3. **EVAL.** `charly check run check-omarchy-pr-<N>-vm` — applies the PR via the single
`pr-apply <N> <sha> <files...>` seam, runs the known-red behavior checks, and the media
loop (asciinema `.cast`/`.gif` + SPICE screen capture → `screen.mp4`), all in one
disposable run (build → deploy → check live → fresh update → teardown).
4. **FULL EVIDENCE EVALUATION.** The runner evaluates ALL available resources — the PR
code/diff, the check results (summary.yml + per-step logs), the screencast (.cast
text), the media frames/video — and assembles the evidence packet. **The runner never
leaves a VM running when done** (probe-fail VM + eval teardown destroyed, domstate
gone, zero residual domains/locks).
5. **COLD-READ (cold-reader).** A fresh-context reader re-evaluates EVERYTHING from the
ARTIFACTS ONLY (never a running VM): SUBJECT (PASS/FAIL/NO VALIDATION) + PROCESS
(known-red, tier compliance, media quality, timing in budget), each finding tied to
an artifact. A report that fails the cold read is FIXED, not posted.
6. **THE FULL LOOP.** Every stage grades the work of the stage before it and can
trigger a change: `redo-plan` (the oracle re-authors the config when it does not set
the PR up for a proper eval — the runner CONFIG AUDIT), `redo-run` (infra/media-pull
errors), `redo-read` (incomplete media), `escalate` (loop guard ≥3 redo entrances →
council/operator — never a silent re-run). Contract:
`skills/omarchy-eval-full-loop`. **Nothing posts to omacom/omarchy automatically** —
publication is operator-gated.

Lean PRs run in parallel — **ONE EVAL LANE PER CPU CORE** (nproc-derived, capped so
2G × lanes ≤ host RAM); GPU-class PRs run SERIAL (`requires_exclusive: [nvidia-gpu]`).
The supervisor owns the lane board, the evals/min telemetry (target ≤60 s/eval), and
the REDO state machine.

## The skills (this repo's `skills/`)

The lane instructions live as proper skills (frontmatter + body):

| Skill | Covers |
|---|---|
| `omarchy-eval-lane` | The entry: the state machine, the 10 standing rules, the class-based per-PR §Template index, the work-lane schema |
| `omarchy-eval-tiers` | What each tier proves (container vs live VM vs visual/GPU) + the mandatory routing rule |
| `omarchy-eval-oracle` | The per-PR config the oracle authors: lean sizing, per-channel goldens, the ORACLE TEMPLATE, pr-apply seam, marker/path rules |
| `omarchy-eval-golden` | The golden VM chain runbook: provision/re-provision, golden-presence gates, per-PR clones, head-freshness |
| `omarchy-eval-sequencing` | Lane sequencing, orphan discipline, concurrency (one lane per core) |
| `omarchy-eval-media` | The mandatory record:/spice: loop + the three-artifact media contract |
| `omarchy-eval-cold-reader` | The cold-reader rubric: artifacts-only grading, SUBJECT + PROCESS verdicts |
| `omarchy-eval-work-lane` | The eval/pr-<N>.md frontmatter schema + routing table |
| `omarchy-eval-full-loop` | The grading/redo loop: triggers, the runner CONFIG AUDIT, the loop guard |

`eval/PR-EVAL-LANE.md` is a thin signpost at the long-standing path — the bodies live
in the skills.

## Layout

| Path | Purpose |
|---|---|
| `charly.yml` | The hand-authored golden chain config (VM template + bases + per-channel routing) |
| `candy/omarchy-pr-apply/` | The ONE runtime apply seam (`pr-apply <pr> <sha> <files...>`; the git-fetch block lives here and nowhere else) |
| `candy/omarchy-eval-record/` `candy/omarchy-eval-harden/` | The recording + hardening candies baked into the instrumented golden |
| `pr-beds/pr-<N>/charly.yml` | Dedicated per-PR configs (the charly.yml IS the plan) — clone + RED-PROBE twin + eval bed |
| `skills/` | The lane instructions as proper skills (see above) |
| `eval/PR-EVAL-LANE.md` | Thin signpost to the skills |
| `eval/PR-EVAL-TEMPLATE.md` | The report/comment template (user-testing voice, disclaimer verbatim, Assisted-by footer) |
| `eval/pr-<N>.md` | Per-PR evaluation reports |
| `eval/evidence/` | Committed small evidence per pr+calver (summary, verdict, stage findings, TELEMETRY) |
| `media/` | Recording artifacts — **gitignored** |
| `.check/` | check-run artifacts per bed+calver — **gitignored** |
| `docs/` | The docs map (golden-vm, evidence-and-media) |

## Running a test environment

```bash
charly check run check-omarchy-pr-<N>-vm-probe   # RED-PROBE first — must FAIL (exit 2)
charly check run check-omarchy-pr-<N>-vm          # the eval bed in pr-beds/pr-<N>/
```

Requires a charly binary supporting the schema (v2026.244+; `charly box validate` on
the tree must be green) and a libvirt session. The environment is `disposable: true`
— the full sequence runs unattended end to end. In normal operation the lane is
driven by the pi agents and the skills, not by hand.

## Contributing / landing changes

See `CONTRIBUTING.md` (requirements, the lane, the publication gate) and `VISION.md`
(the external, non-authoritative boundary). Changes land PR-only on `feat/` branches;
the org-wide `charly/pr-validator` gates the merge and `tag-on-merge` writes the
CHANGELOG from the PR body. This repo is an umbrella submodule — the umbrella records
the gitlink after the merge.
