# eval-omarchy

Dedicated home for the **omarchy PR evaluation test environments** and their **eval results**.

> **External, non-authoritative:** every evaluation in this repo is an **EXTERNAL,
> NON-AUTHORITATIVE evaluation** performed by **opencharly.ai**. It is informational
> only: it does not represent, endorse, or bind omacom/omarchy or its maintainers, is
> not a substitute for upstream review, and does not approve, block, or gate the PR's
> merge. Hardware-bound classes may be PARTIAL/NOT-EVALUABLE.

The test environments derive from the shipped [opencharly/distro-omarchy](https://github.com/opencharly/distro-omarchy)
boxes (imported as the `omarchy` namespace) and inject an omacom/omarchy PR's
files at **BUILD time** via a per-PR package (`candy/omarchy-pr-<N>`), then assert
the PR's **behavior** with checks that verify the actual system state — the charly
variant of the PR's own shell tests, strictly stronger than upstream's simulated tests.

> **What is charly?** charly is the open-source testing tool that builds and runs these
> test environments. A **candy** is a small, reusable software package that charly
> installs into a test environment. You do not need to know charly to read an
> evaluation — every report is written in plain language.

Every evaluation is written the way **another user who tried the PR** would report it —
first person, what worked, what did not, what could not be done and why — while keeping
the full evidence rigor (step matrix, per-check matrix, findings tied to evidence).
Claims are scoped to the tier that produced them: a container run proves script logic
and file application with REAL tools, never live system behavior and never with mocked
tools — system-behavior PRs are tested on a live omarchy VM, and every PR-specific
check must fail without the PR applied. The validation's purpose is binary: does
it actually work? The only valid verdicts are PASS (verified working on a live
system) and FAIL (verified not working). Any "might work" evaluation not verified
on a live system is strictly forbidden — a system-behavior PR whose core behavior
cannot be tested on a live system gets NO VALIDATION (the validation itself
fails); a pod-only eval is not a validation.

## Layout

| Path | Purpose |
|---|---|
| `candy/omarchy-pr-<N>/charly.yml` | Per-PR package: fetches the PR head and installs its changed files over the installed omarchy tree at build time |
| `box/omarchy-suite-base-pr<N>/charly.yml` | Per-PR image: the suite-base + the PR package + the declarative behavior checks |
| `charly.yml` | The `check-omarchy-suite-pod-pr<N>` test environments (container PR injection) |
| `eval/PR-EVAL-TEMPLATE.md` | **The PR-eval template** — every evaluation report (`eval/pr-<N>.md`) and every posted PR comment is rendered from it, in user-testing voice, carrying its EXTERNAL, NON-AUTHORITATIVE disclaimer verbatim and the Assisted-by footer |
| `eval/PR-EVAL-LANE.md` | The eval lane + standing rules (install missing software, test to the max, record both lanes, reusable packages, snapshot-VM + local apply mechanics) |
| `eval/pr-<N>.md` | Per-PR evaluation reports (what I tested, how it went, what I ran, what I noticed) |
| `eval/evidence/` | Committed small evidence (summary.yml + per-check logs per pr+run-date) |
| `media/` | Recording artifacts (asciinema `.cast` + full-screen video per pr+run-date) — **gitignored** |
| `.check/` | check-run artifacts (summary.yml per test environment + run date) — gitignored |

## Running a test environment

```bash
charly check run check-omarchy-suite-pod-pr9332
```

Requires a charly binary that supports the schema (v2026.244+). The test environment is
`disposable: true` — the full sequence (build → check image → deploy → check live →
fresh update → teardown) runs unattended.

## Eval results

Every evaluation report is rendered from **`eval/PR-EVAL-TEMPLATE.md`** and carries
its EXTERNAL, NON-AUTHORITATIVE disclaimer verbatim. PRs are triaged before a
validation is authored: a PR that is not useful, adds no new insight, or cannot be
tested on the available hardware gets a short triage note instead of a full report. Each `eval/pr-<N>.md` records:
what was tested (channel, base provenance, the PR's own Verification claim), how it went
(the overall result + first-person justification), what was run (check-run summary +
run log), the per-check verdict matrix, the recordings (both lanes, saved to the
gitignored `media/`), and what was noticed (findings tied to evidence, including
hardware-bound classes that are PARTIAL/NOT-EVALUABLE, never faked). Every posted PR
comment ends with the `*Assisted-by: …*` footer. Every evaluation result is
validated by a cold reader against the criteria before it is finalized or posted.
