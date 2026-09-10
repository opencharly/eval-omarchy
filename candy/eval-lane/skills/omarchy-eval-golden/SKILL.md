# omarchy-eval-golden

The golden provisioning contract.

- The instrumented golden (check-omarchy-eval-base-inst) carries the eval
  tooling: charly, autologin, the record tools, pr-apply, the harden candy
  (the screenlocker disabled, the always-on shell unit).
- Per-PR evals clone from the golden; per-eval add_candy carries ONLY the
  record/spice PLUGIN providers (verbs register at check-run time).
- The golden is disposable: true. Re-provision = delete-before-recapture +
  golden-presence verification.
- The runner stops the domain after capture.
