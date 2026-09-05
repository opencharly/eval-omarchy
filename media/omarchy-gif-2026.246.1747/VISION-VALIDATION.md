# Vision validation — omarchy-gif-2026.246.1747

Validated with vision_ask (ollama-cloud/qwen3.5:397b) on extracted frames (ffmpeg, 2fps):

- **Frame 1** — valid terminal session, dark theme (#2D2F3A), white monospaced text, prompt `[user@charly-check-omarchy-record-gif ~]$` (the omarchy record-gif container hostname).
- **Frame 10/12** — the command and its output:
  - Line 1: `[user@charly-check-omarchy-record-gif ~]$ echo OMARCHY_RECORD_GIF_OK`
  - Line 2: `OMARCHY_RECORD_GIF_OK` (command output)
  - Line 3: new prompt with cursor

**Verdict: PASS** — the GIF is a valid terminal recording showing the expected command and output.

Artifacts: omarchy-gif.gif (13861 bytes, GIF 89a, 790x560, 20 frames @ 2fps), omarchy-gif.cast (586 bytes), frames 01/10/12.
