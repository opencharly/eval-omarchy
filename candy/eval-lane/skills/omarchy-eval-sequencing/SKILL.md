# omarchy-eval-sequencing

The sequencing gate: the deterministic ordering of the lane stages and the
concurrency budget. The lane runs one PR per lane; the batch runs lanes in
parallel up to the concurrency budget. Every stage grades the previous stage
and can trigger a change (the redo edges). The gate asserts the budget and
the golden presence before the eval.
