# eval-omarchy

Dedicated home for the **omarchy PR evaluation beds** and their **eval results**.

> **External, non-authoritative:** every evaluation in this repo is an **EXTERNAL,
> NON-AUTHORITATIVE evaluation** performed by **opencharly.ai**. It is informational
> only: it does not represent, endorse, or bind omacom/omarchy or its maintainers, is
> not a substitute for upstream review, and does not approve, block, or gate the PR's
> merge. Hardware-bound classes may be PARTIAL/NOT-EVALUABLE.

The beds derive from the shipped [opencharly/distro-omarchy](https://github.com/opencharly/distro-omarchy)
boxes (imported as the `omarchy` namespace) and inject an omacom/omarchy PR's
files at **BUILD time** via a per-PR candy (`candy/omarchy-pr-<N>`), then assert
the PR's **behavior** as charly consequence checks — the charly variant of the
PR's own shell tests, strictly stronger than upstream's mocked call sequences.

## Layout

| Path | Purpose |
|---|---|
| `candy/omarchy-pr-<N>/charly.yml` | Per-PR candy: fetches the PR head and installs its changed files over the installed omarchy tree at build time |
| `box/omarchy-suite-base-pr<N>/charly.yml` | Per-PR image: the suite-base + the PR candy + the declarative behavior checks |
| `charly.yml` | The `check-omarchy-suite-pod-pr<N>` beds (Tier-1 pod PR injection) |
| `eval/PR-EVAL-TEMPLATE.md` | **The PR-eval template** — every evaluation report (`eval/pr-<N>.md`) and every posted PR comment is rendered from it, carrying its EXTERNAL, NON-AUTHORITATIVE disclaimer verbatim |
| `eval/pr-<N>.md` | Per-PR evaluation reports (classification, evidence, verdict, findings) |
| `.check/` | charly check-run artifacts (summary.yml per bed+calver) — gitignored |

## Running a bed

```bash
charly check run check-omarchy-suite-pod-pr9332
```

Requires a charly binary that supports the schema (v2026.244+). The bed is
`disposable: true` — the full R10 sequence (build → check image → deploy →
check live → fresh update → teardown) runs unattended.

## Eval results

Every evaluation report is rendered from **`eval/PR-EVAL-TEMPLATE.md`** and carries
its EXTERNAL, NON-AUTHORITATIVE disclaimer verbatim. Each `eval/pr-<N>.md` records:
the Tier-0 diff classification and venue, the evaluated **channel** (stable/rc/edge/dev)
and base provenance, the PR's own Verification claim, the evidence (check-run summary +
run log), the per-check verdict matrix, the verdict (SHA-anchored, with the stale-check
warning), and the findings (including hardware-bound classes that are PARTIAL/
NOT-EVALUABLE, never faked).
