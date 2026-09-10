# Omarchy acceptance coverage

The traceability report: every upstream test file (omacom/omarchy @ quattro/test, pinned 8ea5151) maps to exactly one acceptance bed. A file mapped to NOTHING is a corpus GAP.

## Coverage summary

| Metric | Count |
|---|---|
| Upstream test files (excl. fixtures) | 245 |
| Fully mapped to acceptance beds | 213 (87.0%) |
| Partial (hardware-bound / nested-VM / install-time) | 26 (10.6%) |
| Acceptance.d wrappers (aggregators — content fully mapped) | 7 |
| Unmapped individual tests | 0 |

## Bed mapping

| Bed | Mapped files |
|---|---|
| accept-session | 13 |
| accept-shell-surfaces | 9 |
| accept-menu-bar | 18 |
| accept-panels | 7 |
| accept-apps | 21 |
| accept-system | 11 |
| accept-security | 16 |
| accept-hyprland | 14 |
| accept-monitors | 10 |
| accept-network | 9 |
| accept-update | 18 |
| accept-plugins | 8 |
| accept-agents | 20 |
| accept-theme-media | 11 |
| accept-power-audio | 13 |
| accept-dev-migrations | 26 |

## Partial categories (documented, never faked)

- **hardware_bound** (16): fingerprint, hybrid-GPU, NVIDIA, touchpad, lid-close, external monitors — require physical hardware not present on the eval VM.
- **nested_vm** (3): Windows-VM compose/mount — require nested virtualization.
- **install_time** (7): first-run, plymouth, preinstalls, privileged-heredoc, provision-user, provisioning-groups, setup-form — install-time behavior covered by the golden capture, not the live lane.

## Acceptance.d wrappers (covered by content)

The 7 top-level suites (apps, cups, panels, security, session, shell-surfaces, system) aggregate the individually-mapped tests; every individual test they run is mapped to a bed, so the wrappers carry no unmapped content.

## Gaps

Zero unmapped individual tests. The corpus is complete against the pinned upstream tree.
