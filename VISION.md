# OpenCharly — Eval-omarchy: The Vision

*The thesis behind the taster's bench.*

An omarchy PR is a candy claim: its author says it works. Eval-omarchy is where
that claim is tasted — not with a mock palate, but on a real omarchy system, the
way another user would. The evaluation answers one binary question: **does it
actually work?** It is an EXTERNAL, NON-AUTHORITATIVE evaluation performed by
opencharly.ai: informational only, never a substitute for upstream review, never
a gate on the PR's merge.

## The tenets

1. **Real taste, never a photograph.** A check that substitutes a fake tool for
the real one proves nothing about the candy. Every check exercises the REAL tool,
the REAL system state, the REAL behavior — on the tier whose semantics justify
the claim. A mocked check is not evidence; an evaluation built on mocks is
useless.
   → the lane's never-mock rule (eval/PR-EVAL-LANE.md), charly's RDD tenet
   (charly/VISION.md tenet 5).

2. **Binary verdicts, or no validation.** The only valid verdicts are PASS
(verified working on a live system) and FAIL (verified not working). A
"might work" that was never verified on a live system is strictly forbidden —
the validation itself fails, and NO VALIDATION is the honest result.
   → the lane's tier semantics + the strict prohibition (eval/PR-EVAL-LANE.md).

3. **Test like a user, judge like a fresh reader.** Reports are first-person, the
way another user who tried the PR would report them. Every result is validated by
a cold reader — someone who did not author the evaluation — against the rubric
before it is finalized or posted.
   → charly's ADE tenet (charly/VISION.md tenet 6), the cold-reader rubric
   (eval/PR-EVAL-LANE.md).

4. **Honest tiers, honest hardware.** A container run proves the PR's files are
applied and the script logic with real tools; a live VM proves system behavior.
Hardware-bound classes are PARTIAL/NOT-EVALUABLE when the hardware is absent —
never a faked bed, never a container claim smuggled in as a system proof.
   → tier semantics (eval/PR-EVAL-LANE.md, /charly-distros:omarchy-eval).

5. **One golden bench, many tastings.** Every evaluation runs on a clone of the
instrumented golden VM — the reproducible system that makes evaluations
comparable and fast. Every PR-specific check must fail on the golden (the
known-red fixture): a probe that passes without the PR proves nothing.
   → the golden chain (docs/golden-vm.md, /charly-vm:vm), the known-red rule
   (eval/PR-EVAL-LANE.md).

6. **The cookbook never lies.** Lessons are written down true, in the present
tense, in the lane contract — and what merely happened (dated RCA narratives,
measured runs) belongs in the CHANGELOG, never on the standing pages.
   → charly's cookbook tenet (charly/VISION.md tenet 10), the lane-split
   convention (eval/PR-EVAL-LANE.md + skills/).

7. **The bench evaluates itself.** The pipeline is pi agents driving disposable
charly beds — the evaluation loop is part of the factory that builds the factory:
factory-in-the-loop, self-hosting verification.
   → charly's tenet 12 (charly/VISION.md), the pi-agent lane
   (/pi-omarchy-eval, umbrella .pi/agents/omarchy-*).

## Where the evaluation is heading

- **Wider, deeper taste:** more classes covered live — visual, GPU, hybrid — as
  the hardware and beds allow; never a faked result in their absence.
- **Faster benches:** 16-way lanes, a lean golden clone lane, evals/min as the
  measured cadence instead of a hoped-for number.
- **The bench everywhere:** the lane runs through pi packages and the charly
  marketplace corpus — any system with the umbrella, any harness with the corpus.
- **Self-maintaining honesty:** the cold-reader loop keeps the cookbook true;
  every batch re-audits the rubric against reality (R1) instead of trusting it.
