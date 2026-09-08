---
name: omarchy-eval-full-loop
description: |-
  The full loop: every stage grades the previous stage and can trigger a change (redo-plan/redo-run/redo-read/escalate; the runner CONFIG AUDIT; the loop guard). Use when orchestrating or disputing an eval.
---

# The full loop — every stage grades the previous stage, any stage can trigger a change

The lane is not a one-way pipe: EVERY stage fully evaluates the work of the agent BEFORE
it and can TRIGGER A CHANGE. The trigger is deterministic evidence, never opinion: a
dispute settles on the artifacts first, then a bounded council (supervisor-mediated,
2–3 advisors, one cross-exam — see the supervisor contract), then the owner decision in
the memo.

## Stage handoffs (the ledger rows)

Each stage writes its verdict ON the previous stage's artifact into
`eval/evidence/<pr>-<calver>/stage-findings.yml`:

```yaml
stage: <oracle|runner|cold-reader>
grading: <the stage whose work is being graded>
verdict: ok | needs-change
findings:               # every finding: evidence reference + proposed trigger
  - {id, severity, evidence, trigger}
trigger: none | redo-plan | redo-run | redo-read | escalate
```

## The triggers

| Trigger | Meaning | Next action |
|---|---|---|
| `redo-plan` | The CONFIG/CHECKS do not set the PR up for a proper eval (wrong marker, non-known-red check, invalid path, missing media loop step, wrong channel base, wrong sizing, missing pr-apply seam) | The config-oracle RE-AUTHORS `pr-beds/pr-<N>/charly.yml` incorporating the findings (a real diff — re-emitting the identical config is a loop-guard violation), `charly box validate` green, then the runner re-runs probe → eval → evidence → cold-read |
| `redo-run` | The bed/config is sound but the run failed (infra, lock, timeout, media pull failure) | The runner re-runs probe → eval on the SAME config after the infra RCA |
| `redo-read` | The cold-read's own evidence was incomplete (e.g. media not assembled before grading, a lane missing) | The runner completes EVIDENCE, then the cold-reader re-reads |
| `escalate` | Loop guard reached: ≥3 REDO entrances for one PR, or a dispute whose council does not settle | The supervisor escalates to the operator with the full finding chain — NEVER a silent re-run |

A finding CLOSES only with a setup change + re-run evidence (the trigger's next action must
have executed). An empty re-run with no config/cause change is forbidden (B14).

## The runner's CONFIG AUDIT (grades the oracle) — runs BEFORE and AFTER the beds

Before RED-PROBE, and again after the EVAL, the runner audits the authored bed; ANY
failure here is a `redo-plan` trigger, never a silent eval on a defective config:

1. **pr-apply seam present** in the eval bed (the ONE `pr-apply <N> <sha> <files...>` step).
2. **Every PR-specific behavior check is present** in BOTH beds (eval + probe twin), each
   with a known-red justification: the marker is a **diff-ADDED token** (verified against
the base) at a **proven-landing path** (bin/, shell/, migrations/ or verified post-apply).
3. **The FULL record:/spice: evidence loop present** in the eval bed (rec-start,
   rec-spice-start, rec-drive, rec-screen-spice, rec-spice-stop, rec-stop, rec-gif,
   rec-mp4) — a bed without both recording lanes is not a proper eval (rule 6).
4. **add_candy has ONLY the record + spice plugin provider candies** (verbs register at
   check-run time; baking them failed historically).
5. **The clone entity points at the PR's CHANNEL golden** (stable base-inst / rc / edge /
   dev keeper) and carries the lean shape **ram 2G / cpu 1** (GPU-class PRs:
   `requires_exclusive: [nvidia-gpu]`, SERIAL).
6. **charly box validate green** on the authored tree.

## The cold-reader's PROCESS verdict (grades the runner AND the oracle)

On top of SUBJECT (PASS/FAIL/NO VALIDATION), the PROCESS verdict maps findings to
triggers:

- config fit (the CONFIG AUDIT items, re-verified from the artifacts) → `redo-plan`
- known-red / tier compliance / media quality (both lanes, non-empty, gradable) →
  `redo-plan` or `redo-read` (media incomplete → redo-read)
- timing in budget (expected-phase vs measured) → finding, `none` unless budget-busting
  indicates a wrong-tier config → `redo-plan`

An ACCEPT (report finalize/post path) requires: SUBJECT valid, PROCESS clean (or all
findings dispositioned), trigger `none` or `escalate` resolved by the operator.

## The loop guard (supervisor)

- Track REDO entrances per PR in the ledger (stage-findings.yml rows + the lane board).
- ≥3 redo entrances for one PR → `escalate` (council, then the owner decision) — never
  silent re-run.
- Every redo round must carry the finding evidence + the config/cause diff; identical
  re-emission is a guard violation and a supervisor finding.

The loop contract is the single source: agents and skills point here, never restate.
