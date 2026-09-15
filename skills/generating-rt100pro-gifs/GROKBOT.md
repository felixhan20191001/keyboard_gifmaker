# Grok Bot override — generating-rt100pro-gifs

Read **`../GROKBOT-BACKEND.md`** first, then this file, then `SKILL.md` for motion contracts / gates / cleanup.

## Imagine video defaults (required unless user overrides)

| Setting | Default |
|---------|---------|
| Aspect | **1:1** Square |
| Resolution | **480p** |
| Duration | **6s** |

Write these into the Imagine plan (`settings.aspect_ratio: 1:1`, `settings.duration: 6s`, `settings.resolution: 480p`). Do not use the pipeline’s global 9:16 / 10s defaults.

## Replace SKILL.md §2 (Produce the Source MP4)

- Square stills / #888888 isolation: **默认 Grok Build**／`grok -p`；reference 锁脸锁衣，画幅 1:1。
- Source MP4(s): **web Imagine** via Imagine出片 + plan file (defaults above).
  - Motion A → one 1:1 Video from the square still. **`loop_via_image_menu: true`**；起始图三点菜单开「循环」；若有 Add last frame 再选同一静帧（双保险）。 Prompt: energetic in-place K-pop dance, locked camera, #888888 when default bg applies. No 5.4 s pose-reset requirement.
  - Motion B → three 1:1 Videos then trim/concat per SKILL.md.
- Delivery GIF still **240×240**.

## Script paths

Prefer repo checkout `skills/generating-rt100pro-gifs/scripts/`; fall back to `~/.grok/skills/…`.
