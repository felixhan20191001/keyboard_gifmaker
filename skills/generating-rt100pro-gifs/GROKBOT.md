# Grok Bot override — generating-rt100pro-gifs

Read **`../GROKBOT-BACKEND.md`** first, then this file, then `SKILL.md` for motion contracts / gates / cleanup.

## Replace SKILL.md §2 (Produce the Source MP4)

- Square stills / #888888 isolation: **Grok CLI** `image_edit` (pass still twice for 1:1).
- Source MP4(s): **web Imagine** via Imagine出片 + plan file.
  - Motion A → one 1:1 Video from the square still. **Start image and Add last frame = the exact same still** (native loop). Prompt: energetic in-place K-pop dance, locked camera, #888888 when default bg applies. No 5.4 s pose-reset requirement.
  - Motion B → three 1:1 Videos then trim/concat per SKILL.md.
- Delivery still **240×240**.

## Script paths

Prefer repo checkout `skills/generating-rt100pro-gifs/scripts/`; fall back to `~/.grok/skills/…`.
