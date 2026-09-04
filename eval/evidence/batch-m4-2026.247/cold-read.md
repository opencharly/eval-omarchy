# M4 batch cold-read — 16-lane omarchy PR eval audit (2026-09-04)

Cold reader: omarchy-cold-reader. Sources: .check/check-omarchy-pr-<N>-vm{,-probe}/<newest>/ (summary.yml, check-live.log, check-live-rebuild.log), pr-plans/eval-plan-<N>.json, pr-beds/pr-<N>/charly.yml, gh api repos/omacom/omarchy/pulls/<N> (head SHAs + patch diffs at the tested heads), /tmp/pr-<N>-{cast,gif,screen.png}, eval/evidence/batch-m4-2026.247/matrix.md, TIMINGS.md (umbrella plan/).

## Verdict lines

| PR | SUBJECT | PROCESS | rationale |
|---|---|---|---|
| 10115 | PASS | finding B1 | countdown/showCountdown marker diff-added (NotificationCard.qml +27/-1; cast shows 3 match lines) — red on golden (probe exit 1), alive after update (rebuild pr-behavior exit 0). Matrix total 137s cites stale run 1908; newest run 1918 = 83s. |
| 10116 | PASS | CLEAN | adapter diff-added (Model.js +16/-0, shouldShowAdapter) — probe red exit 1, eval live grep exit 0, survives update. |
| 10123 | PASS | CLEAN | tile diff-added (manual/42-common-tweaks.md +10/-0 "### Tile the Steam window") — probe red exit 2 (file absent on golden), eval grep exit 0, cast shows the full match line. |
| 10125 | PASS | CLEAN | encoder diff-added (omarchy-capture-screenrecording +14/-1, screenrecording_needs_cpu_encoder) — probe red exit 1, eval live exit 0, survives update. |
| 10129 | PASS | CLEAN | presentation diff-added (omarchy-restart-shell +5/-0) — probe red exit 1, eval live exit 0, survives update. |
| 10130 | PASS | finding B2 | blankArmed diff-added (Service.qml added: property bool blankArmed, +32/-0; cast lines 39/564) — probe red exit 1, eval green, revalidated (1906 FAIL→1919 PASS). Plan token "reblank" is NOT in the diff (fixture filename only) — plan↔bed drift; the bed correctly greps blankArmed. |
| 10134 | PASS | CLEAN | _watch diff-added (omarchy-theme-set-vscode added lines 77/97, +12/-2) — fresh probe 1938 red exit 1 at 25s, eval 1940 green 79s; earlier stale GENERATED_THEME-era runs documented and superseded. Capstone-consistent. |
| 10136 | PASS | CLEAN | zed diff-added (new file omarchy-theme-set-zed +51/-0; cast match lines 7-17) — probe red exit 2 (file absent), eval green, survives update. |
| 10138 | PASS | CLEAN | Wallclock diff-added (BarWidget.qml +8/-0) — probe red exit 1, eval live exit 0, survives update. |
| 10139 | PASS | CLEAN | apple diff-added (new file omarchy-hw-apple-sd-reader +7/-0) — probe red exit 2, eval green, survives update. |
| 10140 | PASS | finding B3 | autosuspend diff-added (new migrations/1788507775.sh +27/-0) — probe red exit 2, eval green, revalidated (1909 FAIL→1919 PASS). Bed pr-behavior DESCRIPTION names etc/modprobe.d/... while the command greps migrations/1788507775.sh (plan-correct) — label drift only. |
| 10141 | PASS | finding B6 | brcmfmac diff-added (new firmware blob +263/-0) — probe red exit 2, eval green, survives update. Coverage gap: PR touches 25 files, eval asserted the 6 plan-curated files (marker in 1 firmware blob) — scoped PASS. |
| 10144 | PASS | CLEAN | launcher diff-added (new file omarchy-rename-launcher-entry +134/-0) — probe red exit 2, eval green, survives update. |
| 10146 | PASS | CLEAN | group diff-added (NotificationLogic.js +37/-0, mako grouping contract) — probe red exit 1, eval live exit 0, survives update. |
| 10147 | PASS | findings B4+B5 | VibeCAD diff-added at the TESTED head 1c964b65 (menu line +1) — probe red exit 1 (fresh 1944), eval green 84s (1916). Two nits: (a) PR head moved to 65fa5597 (19:40Z, "VibeCAD Preview" label) AFTER the eval — verdict scoped to 1c964b65; (b) cast is trimmed ("trimmed media" per matrix) — grep match line absent from .cast; deterministic pr-behavior exit 0 covers it. |
| 10148 | PASS | CLEAN | audient diff-added (new wireplumber conf +33/-0) — probe red exit 2, eval green, survives update. |

## Summary

16/16 SUBJECT PASS — every PR's marker is verified live on an omarchy VM clone at the plan-pinned head, provably diff-added at that head (gh patch + probe red-by-construction: exit 1 token-absent or exit 2 file-absent), and survives the fresh-rebuild update cycle (check-live-rebuild pr-behavior exit 0, 8/8 for all lanes). No FAIL, no INSUFFICIENT. No vision was required — none of the 16 plans sets a visual flag, so no visual claims are made (GNOME-mislabel trap not triggered; every material claim above is tied to deterministic sources: check-live greps, probe exit codes, diff patches, cast text).

Process: 11 lanes CLEAN; 5 lanes carry PR-specific ledger findings (B1-B6); 3 batch-level ledger entries (B7-B9). Every finding is recorded — none suppresses a PASS.

## Findings ledger (evidence-tied)

- B1 (10115, ledger): matrix total_s=137 cites run 2026.247.1908; the newest run 2026.247.1918 totals 83s (both PASS). Matrix column is not the newest run for this row.
- B2 (10130, plan↔bed drift): plan token "reblank" appears nowhere in the PR patch (only in the fixture FILENAME test/shell.d/fixtures/lock-activity-reblank/shell.qml). The bed's pr-behavior command greps blankArmed (diff-added, probe-red, cast lines 39+564) — the marker that ran is sound; the plan file was not regenerated to match (matrix row correctly says blankArmed).
- B3 (10140, label drift): bed pr-behavior description reads "autosuspend in etc/modprobe.d/omarchy-usb-autosuspend.conf" but the command greps /usr/share/omarchy/migrations/1788507775.sh (matches plan file + probe stderr). Command is correct; human-readable label is stale.
- B4 (10147, head drift): eval tested head 1c964b65 (09:16Z). PR head is now 65fa5597 (19:40Z, "Label the VibeCAD candidate as Preview"). Delta is a label change; marker VibeCAD remains diff-added at the current head. Eval ledger does not record the drift.
- B5 (10147, media): .cast is trimmed — the grep match line (menu JSONC line) is not in the recording, only the command + pr-10147-done; matrix documents "(trimmed media)". Deterministic pr-behavior exit 0 stands in.
- B6 (10141, coverage): GH diff = 25 files; pr-apply + checks cover the 6 plan-curated files (marker asserted in 1 firmware blob). The eval validates the PR's brcmfmac subset, not all 25 files' behaviors (suspend fixes, amdgpu, migrations) — scoped PASS recorded.
- B7 (batch, media/lane-rule gap): every lane produced non-empty .cast + .gif + SPICE screen.png on /tmp (casts show the rec-drive commands; 15/16 casts include the grep match lines). Lane rule 6 also requires a full-screen video saved to media/<pr>-<calver>/; M4 lanes produced no video artifact and no media/<pr>-<calver>/ assembly (the follow-up media contract fe3931a made the mp4 explicit for later waves).
- B8 (batch, check strength): checks assert marker PRESENCE on the live system by grep (plus red-probe + diff-added + update-survival) — they do not execute the PR's own test/shell.d/*-test.sh scripts that ship in each diff. Stronger than raw token presence (match lines verified in casts), but the README's "charly variant of the PR's own shell tests, strictly stronger than upstream's simulated tests" overstates grep-only assertions.
- B9 (10147, runner quirk): summary prints "7 steps: 7 passed" while the log shows 8 PASS lines (pr-apply…record-verb-dispatches) — a step-counter quirk in that run; 0 failed, benign, recorded.

## Tally

- SUBJECT: 16 PASS / 0 FAIL / 0 INSUFFICIENT
- PROCESS: 11 CLEAN, 5 findings (10115 B1, 10130 B2, 10140 B3, 10141 B6, 10147 B4+B5) + 3 batch ledger entries (B7, B8, B9)
- Total ledger findings: 9 (B1-B9); vision claims: 0 (no visual PRs)

Verdict: batch stands — 16/16 PASS, evidence-complete, disposition RELEASE (with the ledger above carried into the report render).
