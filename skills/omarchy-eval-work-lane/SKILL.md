---
name: omarchy-eval-work-lane
description: |-
  The eval/pr-<N>.md frontmatter schema (triage|tier|known_red|cold_read|verdict) and the routing table. Use when authoring or consuming reports.
---

# Work-lane schema — eval/pr-<N>.md frontmatter

Binding route: the eval lane contract lives in eval/PR-EVAL-LANE.md (the entry) and
the sibling references in this directory. This file defines the structured frontmatter
that makes every report machine-routable — the work-lane analog of the review-lane
fields in ClawSweeper's work-lane (structure only; the eval has no close/merge lanes).

## Frontmatter fields (new evals — existing reports GRANDFATHERED)

New evaluation reports (eval/pr-<N>.md) carry this frontmatter:

```yaml
---
eval:
  pr: <N>
  title: <PR title>
  head_sha: <evaluated head — compare with the live PR head before trusting>
  triage: pass | skip-note            # standing rule 8
  class: <system | script | visual | hardware | package | other>
  channel: stable | rc | edge | dev
  tier: pod | vm | visual | gpu       # the tier that produced the core claim
  known_red: verified | broken        # RED-PROBE outcome
  cold_read: pending | pass | fail
  verdict: PASS | FAIL | NO_VALIDATION
  hardware_bound: <class> | null      # PARTIAL/NOT-EVALUABLE when set
  posted: false                       # the publication gate; comments are operator-owned
---
```

## Routing table

| Field combination | Route |
|---|---|
| triage: skip-note | No report — a short triage note under eval/ (rule 8), never a validation. |
| known_red: broken (RED-PROBE exit 0) | PROCESS BLOCK — never an eval; stop and RCA (process finding). |
| verdict: NO_VALIDATION | The validation itself failed — no report is produced (strict prohibition: a pod-only eval of a system-behavior PR is NOT a validation). |
| verdict: PASS/FAIL + cold_read: pass | Finalize + render from eval/PR-EVAL-TEMPLATE.md; posting still requires the operator gate (posted stays false until an operator posts). |
| cold_read: fail | The report is FIXED, never posted (cold-reader judge rule). |
| hardware_bound set | The class is PARTIAL/NOT-EVALUABLE — never a faked bed, never claimed. |
| head_sha ≠ live PR head | The verdict is STALE — regenerate the bed before using the report (head-freshness rule). |
| tier: pod for a system-behavior class | HARD FAIL (wrong-tier eval); the routing rule is mandatory. |

## Ownership

- The schema is defined ONCE here; the cold-reader rubric grades against it
  (eval/references/cold-reader.md); the report template (eval/PR-EVAL-TEMPLATE.md)
  renders from these fields. Nothing else restates it (R3).
