# Grok Bot override — generating-qk100-gifs

Read **`../GROKBOT-BACKEND.md`** first, then this file, then `SKILL.md` for motion / gates / cleanup.

## Replace SKILL.md §2 (Produce the Source MP4)

- Full-body / home-pose stills: **Grok CLI** `image_edit` (9:16).
- Source MP4: **web Imagine** Video with first-frame still; if UI supports last-frame / Add last frame, set **same** `$FULLBODY_STILL` as last frame for native loop. Else prompt hard for first=last home pose and Gate 1 strictly.
- Delivery still **135×240** (skill aspect already matches Felix’s common 9:16 default).

## Script paths

Prefer repo checkout `skills/generating-qk100-gifs/scripts/`; fall back to `~/.grok/skills/…`.
