# eval-omarchy

Dedicated home for the **omarchy evaluation test environments** and their **eval results**.

Every evaluation answers one binary question — **does the PR actually work?** — on a
real omarchy system, the way another user would try it. The PR's files are applied at
RUNTIME to a lean clone of a **golden VM image** (built from the official Omarchy
installer ISO), the behavior is asserted with known-red checks, the negative-control
twin proves every check really is red without the PR, both recording lanes run, and a
cold reader grades the artifact packet before anything is finalized.

The repo serves **two roles**:

1. **The acceptance corpus** (`check-omarchy-accept-*`) asserts the omarchy system state
   (the shell, the bar, the panels, the update machinery, …) against the edge golden.
2. **The PR-eval lane** (`charly pipeline run eval-pr-plan`) evaluates an
   `omacom/omarchy` PR on a disposable clone of the per-channel golden that fits it.

> **What is charly?** charly is the open-source tool that builds and runs these test
> environments. A **candy** is a small, reusable software package charly installs into
> an environment; a **check bed** is the declarative recipe that builds, deploys,
> probes, and tears down one environment. You do not need to know charly to read an
> evaluation — every report is written in plain language.

## The golden VM image (from the downloaded Omarchy ISO)

`charly.yml` holds the golden chain — the reproducible bases every evaluation clones:

| Entity | What it is |
|---|---|
| `omarchy-vm` | The VM template: `source.kind: iso` downloads the official **Omarchy installer ISO** (`https://iso.omarchy.org/omarchy-4.0.3.iso`, sha256-checked), runs the unattended install (user `user`, hostname `omarchy`), 40G disk / 2G RAM / 1 vCPU, q35 + UEFI, libvirt, SPICE + guest agent |
| `check-omarchy-eval-base` | Provisions that VM and captures an external **`golden` snapshot** at install-finalize; adds the charly toolchain |
| `check-omarchy-eval-base-inst` | The **INSTRUMENTED golden** (the STABLE channel): the base golden + autologin, the record tooling (incl. acpid), the `pr-apply` helper, asciinema + the record/spice plugin providers, the harden candy, and the omarchy corpus — captured as its own golden |
| `check-omarchy-eval-edge-inst` | The EDGE channel twin (also the golden the acceptance corpus clones): channel-bootstrap `edge` + the pending migrations + the same eval payload |
| `check-omarchy-eval-rc-inst` | The RC channel twin |
| `check-omarchy-eval-dev-inst` | The DEV channel twin |

Every evaluation clones its **channel golden** as a lean COW overlay, so each VM starts
in seconds from the immutable golden. The golden survives every re-provision — the runner
verifies the golden is present before teardown; a missing golden after capture is a BLOCK. The full provision/re-provision runbook
(delete-before-recapture, golden-presence gates) is in `docs/golden-vm.md`.

## The PR-eval lane (the charly pipeline)

The lane is the `eval-pr-plan` `kind: pipeline` entity in `charly.yml`; it runs on the
`plugin-pipeline` engine and has no GitHub Action in the eval path:

1. **ORACLE (triage + plan).** Classify the PR (class, channel); pick the channel
   golden; design PR-specific **known-red** checks. The plan IS the record: the oracle
   returns ONE JSON object; the `render` stage turns it into ONE dedicated
   `eval/pr-<N>/charly.yml` carrying BOTH beds (the treatment `check-omarchy-pr-<N>-vm`
   + the negated control `check-omarchy-pr-<N>-control`). Gate: `charly box validate`
   (run by the render stage's validate script); there is no separate committed JSON plan
   file (the oracle's reply is data — the committed `eval/pr-<N>/charly.yml` IS the plan).
   The oracle's reply is cached in the committed `eval/pr-<N>/eval.yml` keyed on the PR
   head sha, so a re-run at the same head never re-triages.
2. **CONTROL.** The control bed runs the SAME checks NEGATED with NO apply — every
   negated check must PASS on the pristine golden, proving every PR-specific check is
   known-red. A control that FAILs (or cannot run) is a FAKE assertion, caught before
   the eval.
3. **EVAL.** The treatment bed applies the PR via the single
   `pr-apply <N> <sha> <files...>` seam, runs the known-red checks, and records
   (asciinema `.cast`/`.gif` + SPICE screen capture → `.mjpeg`/`.mp4`/`.png`) in one
   disposable run.
4. **GATE + REPORT + COLD-READ.** A deterministic gate reads the lane ledger
   (`executed_checks`, `control_ok`, `media_ok`); a fellow-user voice writes the Tests
   paragraph; a fresh-context cold reader grades the artifacts and the ledger facts and
   emits the packet verdict (PASS/FAIL/NO_VALIDATION) — a packet that fails is a
   SETUP_DEFECT, never a whited-out eval.
5. **RECORD.** Every stage's output renders into the ONE self-contained
   `eval/pr-<N>/eval.yml` (oracle + control + eval + gates + media links + cold read +
   the user-voice report). The record needs no other file to be read.

Lean PRs run in parallel — one eval lane per core (`--lanes 16`). Each evaluation lands
in `eval/pr-<N>/`: the committed `charly.yml` beds + `eval.yml` record and the
gitignored `media/`, so the whole run is reproducible from a fresh clone.

## The skills

The lane instructions are authored as `skill:` entities in `candy/eval-pr/charly.yml`
(family `distros`, owner `eval-omarchy`) and generated by `charly marketplace generate`
into `marketplace/distros/skills/` — the marketplace corpus that the pipeline consumes
via `skills.corpus: "$env.EVAL_UMBRELLA/marketplace/distros/skills"`:

| Skill | Covers |
|---|---|
| `omarchy-eval` | The entry: the one experiment (treatment + control), the terminal states, the never-mock and known-red rules, the Tier-2 live-VM claim, and the per-PR artifact |
| `omarchy-eval-oracle` | The triage contract: classify the PR, pick the channel golden from the registry, author the known-red checks at absolute system paths, and the control re-author contract |
| `omarchy-eval-cold-reader` | The cold-reader rubric: the deterministic gates (executed_checks >= 1, control_ok, media_ok) + the prose gates, and the packet verdict |

The stage mechanics that the v1 corpus documented as separate skills (the golden chain,
the media contract, the redo loop, the stage ordering) are now owned by the
`eval-pr-plan` pipeline blocks in `charly.yml` — the `media:` block, the `stages:`
list with its `redo:` edges, and the golden chain entities — which this README and
`docs/golden-vm.md` describe.

## Layout

| Path | Purpose |
|---|---|
| `charly.yml` | The hand-authored config: the VM template, the per-channel goldens, and the `eval-pr-plan` pipeline |
| `candy/eval-pr/charly.yml` | The lane skill corpus as `skill:` entities (generated to `marketplace/distros/skills/`) |
| `candy/omarchy-pr-apply/` | The ONE runtime apply seam (`pr-apply <pr> <sha> <files...>`; the git-fetch block lives here and nowhere else) |
| `candy/omarchy-eval-record/` `candy/omarchy-eval-harden/` | The recording + hardening candies baked into the instrumented goldens |
| `candy/omarchy-corpus/` | The charly-native corpus surfaces the lane runs per PR |
| `candy/omarchy-accept-*/` | The acceptance-corpus recording/plugin candies the `check-omarchy-accept-*` beds compose |
| `scripts/verify-media.sh` | The media-presence gate helper |
| `eval/pr-<N>/charly.yml` | The committed per-PR eval + control beds (the charly.yml IS the plan) |
| `eval/pr-<N>/eval.yml` | The single self-contained per-PR record (oracle + eval + control + gates + cold-read + report) |
| `eval/pr-<N>/media/` | Recording artifacts — **gitignored** (large binaries) |
| `.check/` | check-run artifacts per bed+calver — **gitignored** |
| `docs/` | The docs map (golden-vm, evidence-and-media) |

## Running a test environment

```bash
charly pipeline run eval-pr-plan --pr <N>       # oracle → render → control → eval → gate → report → cold-read → record
charly pipeline run check-omarchy-accept-suite  # the acceptance corpus
```

Requires a charly binary supporting the schema (`charly box validate` on the tree must be
green), a libvirt session, and `EVAL_UMBRELLA` pointing at the umbrella checkout (for the
generated skill corpus). The environments are `disposable: true` — the full sequence runs
unattended end to end.

## Contributing / landing changes

See `CONTRIBUTING.md` (requirements, the lane, the publication gate) and `VISION.md`
(what this evaluation is and how it runs). Changes land PR-only on `feat/` branches;
the org-wide `charly/pr-validator` gates the merge and `tag-on-merge` writes the
CHANGELOG from the PR body. This repo is an umbrella submodule — the umbrella records
the gitlink after the merge.
