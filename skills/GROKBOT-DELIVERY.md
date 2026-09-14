# Grok Bot — delivery & cloud cleanup

Applies to GIFmaker runs on the `grokbot` branch.

## After Gate 2 passes

1. **DM Felix the final GIF** as a chat attachment for review (every run).
2. Ask whether it **passes**.
3. **Remind him**: if it passes, **save the file to his local computer first**, then reply e.g. `通过，已存本地`.

## Delete cloud artifacts only after dual confirmation

Delete `$RUN_DIR`, related source MP4s, and `/workspace/imagine-pipeline/outputs/gifmaker/` files for that run **only when**:

- he says the GIF **passed**, **and**
- he confirms it is **already saved locally**.

Until then, keep the final GIF (and usable MP4s). If he rejects, revise; do not delete the last good candidate until a replacement is approved or he orders cleanup.
