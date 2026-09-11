# Omarchy acceptance coverage

The traceability report: every upstream test file (omacom/omarchy @ quattro/test, pinned 8ea5151) maps to exactly one acceptance bed. A file mapped to NOTHING is a corpus GAP.

## Coverage summary

| Metric | Count |
|---|---|
| Upstream test files (excl. fixtures) | 245 |
| Fully mapped to acceptance beds | 213 (86.9%) |
| Partial (hardware-bound / nested-VM / install-time) | 26 (10.6%) |
| Acceptance.d wrappers (aggregators — content fully mapped) | 7 |
| Unmapped individual tests | 0 |

## Bed mapping (per-bed counts from eval/omarchy-acceptance-mapping.yml — the single source of truth)

| Bed | Mapped files |
|---|---|
| accept-session | 13 |
| accept-shell-surfaces | 9 |
| accept-menu-bar | 18 |
| accept-panels | 6 |
| accept-apps | 20 |
| accept-system | 10 |
| accept-security | 15 |
| accept-hyprland | 13 |
| accept-monitors | 10 |
| accept-network | 8 |
| accept-update | 17 |
| accept-plugins | 7 |
| accept-agents | 19 |
| accept-theme-media | 10 |
| accept-power-audio | 12 |
| accept-dev-migrations | 26 |

## Partial categories (documented, never faked)

- **hardware_bound** (16): fingerprint, hybrid-GPU, NVIDIA, touchpad, lid-close, external monitors — require physical hardware not present on the eval VM.
- **nested_vm** (3): Windows-VM compose/mount — require nested virtualization.
- **install_time** (7): first-run, plymouth, preinstalls, privileged-heredoc, provision-user, provisioning-groups, setup-form — install-time behavior covered by the golden capture, not the live lane.

Per-bed counts sum to **213** — matching the mapping.yml and the 'Fully mapped' total.

