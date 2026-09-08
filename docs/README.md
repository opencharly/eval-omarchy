# Documentation

- Status: active documentation index
- Owner: eval-omarchy maintainers
- Source of truth: the linked repository files; the lane contract is
  eval/PR-EVAL-LANE.md (+ skills/)
- Update when: a document is added, retired, moved, changes lifecycle, or gains a new
  canonical owner

This is a MAP, not another manual. Start with the goal below; the binding knowledge is
always the linked file.

## Start here

| Goal | First page | Next step |
|---|---|---|
| Understand the evaluation boundary | VISION.md | CONTRIBUTING.md |
| Set up a checkout + requirements | CONTRIBUTING.md | docs/golden-vm.md (provision the golden) |
| Run one PR evaluation | .agents/skills/omarchy-eval-lane/SKILL.md (the lane contract) | .agents/skills/omarchy-eval-full-loop/SKILL.md (the grading/redo loop) |
| Understand the golden test environments | docs/golden-vm.md | /charly-vm:vm |
| Interpret evidence + media | docs/evidence-and-media.md | .agents/skills/omarchy-eval-media/SKILL.md |
| Land a change to this repo | CONTRIBUTING.md (PR contract) | AGENTS.md |

## Document lifecycle

Evergreen pages are in one of these states; the state is named at the top of the page:

- **active** — current guidance for a supported surface
- **proposed** — a future design/runbook that grants no execution approval
- **compatibility-only** — retained for still-readable state or a migration boundary
- **historical** — completed proof or decision history (see CHANGELOG/ for dated entries)

## Update triggers

The relevant pages move in the same change when any of these surfaces move:

| Surface | Pages to review in the same change |
|---|---|
| charly.yml golden chain entities | docs/golden-vm.md + .agents/skills/omarchy-eval-golden/SKILL.md |
| distro-omarchy import pin bump / channel state change | docs/golden-vm.md (re-provision trigger) |
| oracle generation template (pr-beds/pr-<N>) | .agents/skills/omarchy-eval-oracle/SKILL.md + docs/golden-vm.md |
| The lane state machine / standing rules | eval/PR-EVAL-LANE.md + VISION.md |
| Recording/evidence steps | .agents/skills/omarchy-eval-media/SKILL.md + docs/evidence-and-media.md |
| Schema floor bump | CONTRIBUTING.md (charly migrate) + README.md |
| Posting/publication policy | VISION.md + CONTRIBUTING.md |

## Cross-references

- charly skills: /charly-distros:omarchy-eval (the general eval procedure),
  /charly-check:check, /charly-vm:vm, /charly-internals:disposable.
- The pi package: /pi-omarchy-eval (lane skills + prompts).
