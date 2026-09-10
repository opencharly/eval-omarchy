# omarchy-eval-media

The media contract.

- Every eval captures BOTH lanes: the terminal recording (.cast -> .gif) and
  the SPICE display capture (MJPEG -> MP4) plus a screenshot (PNG).
- The media gate asserts the artifacts exist with the min sizes and are not
  uniform (a blank capture is a failure).
- The evidence packet is linked in the report, never inlined.
- Media presence NEVER implies verification: the recording runs before the
  checks. The executed-check count is the verification signal, not the media.
