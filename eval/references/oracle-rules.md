# Oracle rules — the apply seam, the ORACLE TEMPLATE, the check-plan contract

## The apply seam — the ONE runtime seam (pr-apply), no nested templates

The PR is applied at RUNTIME by the single helper `pr-apply <pr> <sha> <changed-files...>`
(candy/omarchy-pr-apply — the git-fetch block lives THERE and nowhere else; S9 guard:
`grep 'git fetch .* pull/'` matches only that candy). The helper is baked into the
instrumented golden, so the eval bed's apply step is exactly one line. Mutation lives in
candies (bed-plan `run:` steps are dead code in VM beds — RCA #2); the eval/probe beds
carry only `check:` steps.

## The check-plan contract (known-red + golden freshness)

The probe proves known-red (S7) AND golden freshness; a probe that passes = stale golden
or a non-red check → re-provision the golden (delete-before-recapture; the golden must
survive — RCA #7: a failed capture run must not destroy it, the runner verifies golden
presence post-run). Class routing, channel choice, vCPU/RAM sizing and the expected-phase
budget (feeding plan stage 3) belong to the oracle (Tier-0 venue ladder; GPU class SERIAL
`requires_exclusive: [nvidia-gpu]`; a system-behavior PR evaluated only in a container is
a HARD FAIL).

The SUPERVISOR agent maintains the verdict ledger (the `.check/` summaries ARE the
data; the golden sha256 sidecar keys staleness — a re-provisioned golden invalidates
every older verdict). Unchanged heads are skipped by the supervisor's ledger; reports
render from `eval/PR-EVAL-TEMPLATE.md` with channel + base provenance. No scripts —
the agents read the native artifacts directly.

### The ORACLE marker rule (mandatory)

A PR-specific check marker MUST be a **diff-ADDED token** (a string in the PR's added
lines, never a word that pre-exists in the base). Verified against the base before the
bed ships: a probe that does NOT fail (exit 2) on the golden = **RED-PROBE-BROKEN = a
PROCESS block** — no eval is valid from that bed (S7).

### The ORACLE path rule (mandatory)

A check path must be from a **PROVEN-LANDING class** (`bin/`, `shell/`, `migrations/` —
verified by pr-apply) or verified against the post-apply tree. An `etc/` path that does
not land at its expected installed location makes the check path wrong by construction.

## NO VALIDATION is a LAST RESORT — never the default

A report that says NO VALIDATION is an admission that the evaluation itself failed.
Before that verdict is ever written, ALL of these must have been exhausted, in order:

1. **Run the PR's own test suites** (`test/cli`, `test/shell`, `test/shell.d/*`)
   on the live system — the PR's own "## Verification" claims are the first thing to
   measure, and they are almost always runnable.
2. **Try to install the missing software for real** (rule 4): the package repository,
   AUR, the project's own releases. A tool that exists on AUR is installable — "not in
   the omarchy repo" is NOT a blocker when AUR has it.
3. **Test the real behavior with the real tools** on the live VM (Tier-2): real pacman,
   real df/findmnt, real config trees, real services. Script-level logic (detection,
   fallbacks, error paths, install paths) is testable even when the full hardware cycle
   is not.
4. **Record what WAS tested** — a PARTIAL verdict with the real evidence (which suites
   passed, which real behaviors were measured, which branches were not triggered and
   why) is always better than NO VALIDATION.

Only a genuinely impossible test (hardware the machine does not have, a credential the
environment does not have, a package in no reachable repository) stays untested — with
the exact blocker documented. Canonical counter-example: pr-9332 was reported NO
VALIDATION because "cardwire is not in the omarchy package repository" — but cardwire
IS on AUR, the PR's own test suites run, and the scripts' real behavior (detection
fallback, install-path failure) is measurable. The re-evaluation found all of it.
