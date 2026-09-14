# Grok Bot override — generating-rt85-gifs

Read **`../GROKBOT-BACKEND.md`** first, then this file, then `SKILL.md` for motion contracts / gates / cleanup.

## Imagine video defaults (required unless user overrides)

| Setting | Default |
|---------|---------|
| Aspect | **16:9** Widescreen (横向) |
| Resolution | **480p** |
| Duration | **6s** |

Write these into the Imagine plan (`settings.aspect_ratio: 16:9`, `settings.duration: 6s`, `settings.resolution: 480p`). Do not use the pipeline’s global 9:16 / 10s defaults.

## Replace SKILL.md §2 (Produce the Source MP4)

- Stills (`*-fullbody`, `*-face`, `*-curl`, Motion B inner crops): **优先自出**（`GenerateImage`）；失败则 **Grok Build 兜底**。人物 reference 锁脸锁衣锁身材。**Motion A 每次生静帧**（含重出／修姿）必须同时传入姿势参考 `refs/motion-a-recline-pose-ref.png`（自带生图与 Grok Build 都要带）。
- Source MP4(s): **web Imagine** via Imagine出片 + plan file (defaults above). Map:
  - Motion A multi-ref → Video + uploads of `$FULLBODY_STILL` (×2), face, curl; still must be **chin-hand recline** (`refs/motion-a-recline-pose-ref.png`); prompt locks #888888 + come-hither from the thigh hand. **`loop_via_image_menu: true`**；三点「循环」+ 可选 Add last frame 同 `$FULLBODY_STILL`。No timed 5.4 s pose-reset.
  - Motion B → three Video runs (cover / upper / face) then ffmpeg concat as in SKILL.md.
  - Motion C → one Video from prone `$FULLBODY_STILL`. **`loop_via_image_menu: true`**；三点「循环」+ 可选 Add last frame 同静帧。No 0.4 s start hold / 5.4 s return requirement.
- Never invent ffmpeg Ken Burns as a substitute.
- Delivery GIF still **320×172**; source compose **16:9**.

## Script paths

Prefer scripts next to this package in the repo checkout; fall back to `~/.grok/skills/generating-rt85-gifs/scripts/` if present.
