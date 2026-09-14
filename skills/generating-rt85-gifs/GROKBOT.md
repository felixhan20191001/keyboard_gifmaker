# Grok Bot override — generating-rt85-gifs

Read **`../GROKBOT-BACKEND.md`** first, then this file, then `SKILL.md` for motion contracts / gates / cleanup.

## Replace SKILL.md §2 (Produce the Source MP4)

- Stills (`*-fullbody`, `*-face`, `*-curl`, Motion B inner crops): **Grok CLI** `image_edit` / `image_gen`.
- Source MP4(s): **web Imagine** via Imagine出片 + plan file. Map:
  - Motion A multi-ref → Video + uploads of `$FULLBODY_STILL` (×2), face, curl; prompt locks #888888 + come-hither cycle. **Start image and Add last frame = the exact same `$FULLBODY_STILL`** (native loop). No timed 5.4 s pose-reset.
  - Motion B → three Video runs (cover / upper / face) then ffmpeg concat as in SKILL.md.
  - Motion C → one Video from prone `$FULLBODY_STILL`. **Start image and Add last frame = the exact same still** (native loop). No 0.4 s start hold / 5.4 s return requirement.
- Never invent ffmpeg Ken Burns as a substitute.
- Delivery still **320×172**; source compose **16:9**.

## Script paths

Prefer scripts next to this package in the repo checkout; fall back to `~/.grok/skills/generating-rt85-gifs/scripts/` if present.
