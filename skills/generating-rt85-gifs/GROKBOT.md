**Outfit lock:** 服装须与原参考图高度一致。

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

- Stills (`*-fullbody`, `*-face`, Motion B inner crops): **默认 Grok Build**／`grok -p`（`image_edit`／`image_gen`）。人物 reference 锁脸锁衣锁身材。**Motion A 每次生静帧**（含重出／修姿）必须同时传入姿势参考 `refs/motion-a-recline-pose-ref.png`。默认**不**出 `*-curl.png`（除非点名旧勾手）。
- Source MP4(s): **web Imagine** via Imagine出片 + plan file (defaults above). Map:
  - Motion A → Video + `$FULLBODY_STILL`（+ face）；still = pose-ref 横卧托下巴；**视频提示只写变化量**（默认：转头对镜＋浅笑再收回，见 `SKILL.md` Motion A `final_prompt` 模板）；**禁止**在视频提示里重写整段横卧姿势。**`loop_via_image_menu: true`**；三点只开「循环」。No timed 5.4 s pose-reset。
  - Motion B → three Video runs (cover / upper / face) then ffmpeg concat as in SKILL.md.
  - Motion C → one Video from prone `$FULLBODY_STILL`. **`loop_via_image_menu: true`**；三点「循环」+ 可选 Add last frame 同静帧。No 0.4 s start hold / 5.4 s return requirement.
- Never invent ffmpeg Ken Burns as a substitute.
- Delivery GIF still **320×172**; source compose **16:9**.

## Script paths

Prefer scripts next to this package in the repo checkout; fall back to `~/.grok/skills/generating-rt85-gifs/scripts/` if present.
