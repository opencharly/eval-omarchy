# PR eval — omacom/omarchy#<N>

*Rendered from `eval/PR-EVAL-TEMPLATE.md` — every omarchy PR evaluation starts here.
Fill every section; mark `N/A — <reason>` where a section genuinely does not apply (an
empty section is not a valid answer). Delete the "Render instructions" block before saving.*

> ## EXTERNAL, NON-AUTHORITATIVE evaluation — read first
>
> This is an **EXTERNAL, NON-AUTHORITATIVE evaluation** of omacom/omarchy#<N>
> performed by **opencharly.ai** via the opencharly/eval-omarchy beds. It is
> informational only: it does not represent, endorse, or bind omacom/omarchy or its
> maintainers, is not a substitute for upstream review, and does not approve, block,
> or gate the PR's merge. Hardware-bound classes may be PARTIAL/NOT-EVALUABLE.

## Evaluation identity

- **Title:** <PR title>
- **Author:** <author> · **Base:** <base branch> · **Head:** <head branch> @ <full SHA>
- **Changed files:** <n> (<what changed>) · +<adds>/−<dels>
- **Channel evaluated:** `stable` | `rc` | `edge` | `dev` — <why this channel>
- **Bed(s):** <one per line> · **Run calver:** <YYYY.DDD.HHMM>
- **charly version:** <ver> · **Evaluated:** <YYYY-MM-DD>
- **Base provenance:** base VM <name> · ISO calver <ver> · clean snapshot <id/date>

## Verdict

**Verdict:** `PASS` | `PARTIAL` | `NOT-EVALUABLE`

**Evaluated head:** <sha> — **verdicts can go STALE**: compare with the PR's current
head before acting or posting; a stale verdict is re-run, never re-certified.

**Tier (evidence-based):** `PASS` = fully tested — bed green, **zero warnings**, R10
fresh-rebuild anchor ran · `PARTIAL` = analysed on a live system — snapshot lane or a
branch/edge not executed · `NOT-EVALUABLE` = hardware-bound class, never faked.

<One-paragraph justification tied to the evidence below — why this verdict, which
checks decided it, which findings cap the tier.>

## Tier 0 — classification & venue

- **Class:** <script migration · QML/theme · install-script · migrations · update-channel · docs>
- **Channel routing:** `dev` = source-checkout lane (PR head in ~/omarchy) · `edge`/`rc`/`stable` =
  package-level lane (per-PR candy over the installed tree) · `rc` adds the release-validation
  flow (channel-set + update + migrations).
- **Venue ladder:** Tier-1 pod (build-time) · Tier-2 VM (deploy-time) · visual (wl loop) ·
  hybrid-GPU (hardware; → PARTIAL/NOT-EVALUABLE, never a faked bed).
- **PR's own "## Verification" claim:** <quote verbatim — a claim, not a fact; measured below>

## Evidence

<One block per bed, the validator's per-bed line format, plus base provenance>

```yaml
bed: <bed>
channel: <stable|rc|edge|dev>
calver: <run calver>
steps:
  - name: <step>       ok: <true|false>   <sec>s
  # ...
total_seconds: <n>
diagnostics: errors <n>, warnings <n> (<allowlisted ids>)
ok: <true|false>
```

All beds above ran on charly <version>; base provenance as in Evaluation identity.

## Recordings

Recording artifacts from the beds, when the change class puts them in scope (the two lanes are
charly surfaces — author the steps per plan §4.3 in the per-PR bed, then reference the evidence):

- **Terminal lane (asciinema):** `.cast` of the flow — `record: start` → `record: run|cmd` →
  `record: stop` with `artifact:` + `artifact_min_bytes`/`artifact_min_cast_events`; playback on
  the host with `asciinema play` / `asciinema convert -f raw <file>.cast -`.
- **SPICE video lane (VM display):** `.mjpeg` of the display during the flow — `spice: {method:
  record, action: start, fps}` → drive steps → `spice: {method: record, action: stop,
  artifact:}`; reality-check with `ffprobe` + a frame extract (`ffmpeg -i <file>.mjpeg -frames:v 1
  out.png`, vision-verified).

Per recording: file path (host, after teardown), bytes, format, event/frame count, playback proof.
Artifacts are pulled host-side at `record: stop`/the stop step — BEFORE the disposable bed's
teardown destroys the venue — and copied into `eval/evidence/<pr>-<calver>/` with the summary.

`N/A — <reason>` when the class does not put recordings in scope (e.g. docs-only).

## Per-check matrix

| # | Check | Context | Verdict |
|---|---|---|---|
| 1 | <id> — <what it asserts> | build/runtime | PASS / FAIL |

## Findings

1. <finding> — tied to evidence: <check/run/log reference>.
2. ...

## Eval checklist (one evidence line, or `N/A — <reason>`)

- **Template-conform:** rendered from `eval/PR-EVAL-TEMPLATE.md`; no empty sections.
- **Disclaimer:** EXTERNAL, NON-AUTHORITATIVE header present verbatim here AND in any posted comment.
- **No faked bed:** hardware-bound classes PARTIAL/NOT-EVALUABLE; every check ran on a real bed.
- **Evidence persisted:** `eval/evidence/<pr>-<calver>/summary.yml` + per-check log committed in-repo.
- **Zero warnings:** gate output has no surviving warnings (allowlisted ones named).
- **Head-SHA freshness:** evaluated head recorded; stale check documented in the posted comment.
- **Base provenance:** channel, ISO calver, snapshot id recorded (snapshot-lane runs).
- **R10 fresh-rebuild:** full fresh-install anchor run for this batch recorded, or `N/A — <reason>`.

## Provenance

*Evaluated by opencharly.ai (opencharly/eval-omarchy) · charly <ver> · channel <ch> · base
<ISO calver>/snapshot <id> · <date> · evaluated head <sha>*

---

## Render instructions (delete before saving)

1. Copy this file to `eval/pr-<N>.md` and fill every section with EVIDENCE, not promises.
2. Render the PR comment from Verdict + Findings + Evidence (verdict line + per-check matrix
   first), disclaimer header verbatim on top.
3. POST the comment **only behind the operator approval gate** — never unapproved.
4. SHA-keyed cache: unchanged heads are skipped, not re-run (`scripts/omarchy-rollup.py`).
5. Mark the report FINAL only after evidence is committed to `eval/evidence/<pr>-<calver>/`.
