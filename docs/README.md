# Documentation

- Status: active documentation index
- Owner: eval-omarchy maintainers
- Source of truth: the linked repository files; the lane contract is the
  `omarchy-eval` skill entity in `candy/eval-pr/charly.yml` (generated to
  `marketplace/distros/skills/`)
- Update when: a document is added, retired, moved, changes lifecycle, or gains a new
  canonical owner

This is a MAP, not another manual. Start with the goal below; the binding knowledge is
always the linked file.

## Start here

| Goal | First page | Next step |
|---|---|---|
| Understand the evaluation boundary | VISION.md | CONTRIBUTING.md |
| Set up a checkout + requirements | CONTRIBUTING.md | docs/golden-vm.md (provision the golden) |
| Run one PR evaluation | marketplace/distros/skills/omarchy-eval/SKILL.md (the lane contract) | the `eval-pr-plan` pipeline in charly.yml (the stage list + redo edges) |
| Understand the golden test environments | docs/golden-vm.md | /charly-vm:vm |
| Interpret evidence + media | docs/evidence-and-media.md | the `eval-pr-plan` `media:` block in charly.yml |
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
| charly.yml golden chain entities | docs/golden-vm.md |
| distro-omarchy import pin bump / channel state change | docs/golden-vm.md (re-provision trigger) |
| oracle bed template (`eval/pr-<N>/charly.yml`) | the `omarchy-eval-oracle` skill entity + docs/golden-vm.md |
| The lane state machine / standing rules | `candy/eval-pr/charly.yml` + VISION.md |
| Recording/evidence steps | the `eval-pr-plan` `media:` block in charly.yml + docs/evidence-and-media.md |
| Schema floor bump | CONTRIBUTING.md (charly migrate) + README.md |
| Posting/publication policy | VISION.md + CONTRIBUTING.md |

## Cross-references

- charly skills: /charly-distros:omarchy-eval (the general eval procedure, sourced
  from this repo's `omarchy-eval` entity), /charly-check:check, /charly-vm:vm,
  /charly-internals:disposable.
