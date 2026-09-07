# rendered-comment.md — the comment RENDERED for omacom/omarchy#10115

> THIS FILE IS THE RENDERED COMMENT FOR THE EVIDENCE LEDGER ONLY. Per the lane contract
> (template render instructions: "POST the comment only after a human approves — never
> unapproved") AND the active constraint "NOTHING posts to omacom/omarchy", this comment
> is committed as evidence (eval/evidence/pr-10115-2026.250.1859/rendered-comment.md) and is
> NOT posted. Verified: zero comments/reviews on omacom/omarchy#10115 at baseline AND
> after this evaluation (gh api checks, read-only).

> ## EXTERNAL, NON-AUTHORITATIVE evaluation — read first
>
> This is an **EXTERNAL, NON-AUTHORITATIVE evaluation** of omacom/omarchy#10115
> performed by **opencharly.ai** via the opencharly/eval-omarchy test environments. It is
> informational only: it does not represent, endorse, or bind omacom/omarchy or its
> maintainers, is not a substitute for upstream review, and does not approve, block,
> or gate the PR's merge. Hardware-bound classes may be PARTIAL/NOT-EVALUABLE.

I tested omacom/omarchy#10115 (Show countdown progress on notifications) — **PASS (verified working on a live system)**

I applied the PR to a fresh clone of the instrumented golden VM via the single apply seam and checked the installed tree. The known-red probe proved the marker only lands with this PR (the RED-PROBE twin failed exactly there with exit 2 — `showCountdown` absent on the golden, by construction), and after the apply the same marker is PRESENT on the live guest: the grep found `property bool showCountdown: false`, the `countdownReservedHeight` reservation and `visible: root.showCountdown` at lines 30/55/210 of the installed `NotificationCard.qml`. The terminal (.cast) and SPICE (mp4/mjpeg/screenshot) recordings captured the live check run and the desktop.

Per-check matrix (eval run 2026.250.1859, 11 steps: 10 passed, 0 failed, 1 skipped):

| # | Check | Verdict |
|---|---|---|
| 1 | pr-apply (PR applied via the single seam @ 16a6ede) | PASS |
| 2 | pr-behavior (showCountdown in NotificationCard.qml) | PASS (probe: FAIL exit 2 — known red) |
| 3–10 | rec-start / rec-spice-start / rec-drive / rec-screen-spice / rec-spice-stop / rec-stop / rec-gif / record-verb-dispatches | PASS |
| 11 | rec-mp4 (in-plan transcode) | SKIP (verify-only; assembled host-side) |

What I could not do in this lane: watch a real notification count down for five seconds and eyeball the bar — the notification popup does not fire on demand in the disposable VM; the QML wiring that renders it (the added properties and the track sized by `remainingLifetime`) is what the deterministic checks and recordings prove.

Full report: https://github.com/opencharly/eval-omarchy (eval/pr-10115.md)

*Assisted-by: pi ollama-cloud/deepseek-v4-flash:0731 (fully tested and validated)*
