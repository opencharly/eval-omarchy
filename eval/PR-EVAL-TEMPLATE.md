# I tested omacom/omarchy#<N>

*Rendered from `eval/PR-EVAL-TEMPLATE.md` — every omarchy PR evaluation starts here.
Fill every section; mark `N/A — <reason>` where a section genuinely does not apply (an
empty section is not a valid answer). Delete the "Render instructions" block before saving.*

> ## EXTERNAL, NON-AUTHORITATIVE evaluation — read first
>
> This is an **EXTERNAL, NON-AUTHORITATIVE evaluation** of omacom/omarchy#<N>
> performed by **opencharly.ai** via the opencharly/eval-omarchy test environments. It is
> informational only: it does not represent, endorse, or bind omacom/omarchy or its
> maintainers, is not a substitute for upstream review, and does not approve, block,
> or gate the PR's merge. Hardware-bound classes may be PARTIAL/NOT-EVALUABLE.

## What I tested

- **Title:** <PR title>
- **Author:** <author> · **Base:** <base branch> · **Head:** <head branch> @ <full SHA>
- **Changed files:** <n> (<what changed>) · +<adds>/−<dels>
- **Update channel tested:** `stable` | `rc` | `edge` | `dev` — <why this channel>
- **Test environment(s):** <one per line> · **Run date:** <YYYY.DDD.HHMM>
- **Testing tool version:** <ver> · **Tested on:** <YYYY-MM-DD>
- **What the test system was based on:** base VM <name> · installer version <ver> · clean snapshot <id/date>

## How it went

**Overall:** it works / mostly works / I couldn't fully test it

**What I did:** <one first-person paragraph — I applied the PR to a fresh omarchy
install, ran the checks, and here is what happened. What worked, what did not, what I
could not do and why.>

**Head tested:** <sha> — **results can go STALE**: compare with the PR's current head
before acting or posting; a stale result is re-run, never re-certified.

<One-paragraph justification tied to the evidence below — why this overall result, which
checks decided it, which findings cap it.>

## What the PR claims

- **Class:** <script migration · QML/theme · install-script · migrations · update-channel · docs>
- **Channel routing:** `dev` = source-checkout lane (PR head in ~/omarchy) · `edge`/`rc`/`stable` =
  package-level lane (per-PR package over the installed tree) · `rc` adds the release-validation
  flow (channel-set + update + migrations).
- **Test environments:** container (build-time) · virtual machine (deploy-time) · visual (desktop loop) ·
  GPU (hardware; → PARTIAL/NOT-EVALUABLE, never a faked test environment).
- **PR's own "## Verification" claim:** <quote verbatim — a claim, not a fact; measured below>

## What I ran

<One block per test environment, the run's step matrix, plus what the test system was based on>

```yaml
bed: <test environment>
channel: <stable|rc|edge|dev>
calver: <run date>
steps:
  - name: <step>       ok: <true|false>   <sec>s
  # ...
total_seconds: <n>
diagnostics: errors <n>, warnings <n> (<approved ids>)
ok: <true|false>
```

All test environments above ran on testing tool version <version>; base provenance as in "What I tested".

## Recordings

Every PR evaluation records BOTH lanes — this is mandatory, not optional. The recording
steps are authored in the per-PR test environment (per the lane doc's "Standing rules"
and "Recordings" sections), then referenced here:

- **Terminal lane (asciinema):** `.cast` of the flow — `record: start` → `record: run|cmd` →
  `record: stop` with `artifact:` + `artifact_min_bytes`/`artifact_min_cast_events`; playback on
  the host with `asciinema play` / `asciinema convert -f raw <file>.cast -`.
- **Full-screen lane:** desktop video via `record: {record_mode: desktop}`
  (pixelflux/wf-recorder) on desktop systems, or SPICE video of the VM display —
  `spice: {method: record, action: start, fps}` → drive steps → `spice: {method: record,
  action: stop, artifact:}`; reality-check with `ffprobe` + a frame extract
  (`ffmpeg -i <file>.mjpeg -frames:v 1 out.png`, checked by an AI vision model).

Per recording: file path (host, after teardown), bytes, format, event/frame count, playback proof.
Artifacts are pulled host-side at `record: stop`/the stop step — BEFORE the disposable test
environment is torn down — and saved into `media/<pr>-<calver>/` (gitignored; the report
references them; small evidence stays committed in `eval/evidence/<pr>-<calver>/`).

## Per-check matrix

| # | Check | Context | Verdict |
|---|---|---|---|
| 1 | <id> — <what it asserts> | build/runtime | PASS / FAIL |

## What I noticed

1. <finding, first-person, tied to evidence: <check/run/log reference>>.
2. ...

## What I checked

- **Triage:** the PR is useful, the evaluation adds new insight, and the core behavior
  is testable on the available hardware — or the reason it is not (a PR that fails
  triage gets a short triage note, not a full report).
- **Template-conform:** rendered from `eval/PR-EVAL-TEMPLATE.md`; no empty sections.
- **Disclaimer:** EXTERNAL, NON-AUTHORITATIVE header present verbatim here AND in any posted comment.
- **No faked test environment:** hardware-bound classes PARTIAL/NOT-EVALUABLE; every check ran on a real test environment.
- **Evidence persisted:** `eval/evidence/<pr>-<calver>/summary.yml` + per-check log committed in-repo.
- **Recordings:** both lanes captured and saved to `media/<pr>-<calver>/` (gitignored), referenced above.
- **Missing software:** anything missing in the test environment was installed (extra software package /
  install step / the system's own package installer) and the run re-done — recorded in "What I noticed";
  only a genuinely impossible install stays NOT-EVALUABLE, with the exact blocker documented.
- **Max extent:** every applicable test environment ran; the PR's own Verification claim was exercised;
  edge cases probed (idempotence, failure paths, clean-install vs upgrade).
- **Zero warnings:** gate output has no surviving warnings (approved ones named).
- **Head-SHA freshness:** tested head recorded; stale-check documented in the posted comment.
- **Base provenance:** channel, installer version, snapshot id recorded (snapshot-based runs).
- **Fresh install from scratch:** a full fresh-install verification run for this batch recorded, or `N/A — <reason>`.

## Who ran this

*Tested by opencharly.ai (opencharly/eval-omarchy) · testing tool <ver> · channel <ch> · base
<installer version>/snapshot <id> · <date> · tested head <sha>*

*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*

---

## Render instructions (delete before saving)

1. Triage first (lane standing rule 7): if the PR is not useful, adds no new insight,
   or cannot be tested on the available hardware, do NOT render a report — record a short
   triage note instead. Only PRs that pass triage get a full report.
2. Copy this file to `eval/pr-<N>.md` and fill every section with EVIDENCE, not promises.
3. Render the PR comment from "How it went" + "What I noticed" + "What I ran" (overall line +
   per-check matrix first), disclaimer header verbatim on top. Write it the way a user who
   tried the PR would — first person, what worked, what did not, what I could not do.
4. End EVERY posted comment with the Assisted-by footer:
   `*Assisted-by: <Harness> <Provider Full Model Name> (<confidence>)*`
   (e.g. `*Assisted-by: pi ollama-cloud/deepseek-v4-flash:0731 (fully tested and validated)*`).
5. POST the comment **only after a human approves** — never unapproved.
6. Result cache: unchanged heads are skipped, not re-run (`scripts/omarchy-rollup.py`).
7. Mark the report FINAL only after evidence is committed to `eval/evidence/<pr>-<calver>/`
   and recordings to `media/<pr>-<calver>/`.
