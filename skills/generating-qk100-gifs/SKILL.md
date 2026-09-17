---
name: generating-qk100-gifs
description: >
  Create, animate, convert, or optimize a GIF for the Qwertykeys QK100 Mk2
  customizable color LCD / Dynamic Island screen from a reference image or video.
  Use for QK100 Mk2 mini-screen GIFs, QK Config uploads, 135x240 9:16 delivery
  GIFs, or when the user runs /generating-qk100-gifs.
---

# Generating QK100 Mk2 GIFs

For every QK100 / QK100 Mk2 request, follow this fixed pipeline in order: inspect the supplied still; **if it is not a full-body photo, first generate a full-body still of the same character**; generate a **native looping** source video **only from that full-body still** (first and last frame pinned to the same image); approve the source animation; render the GIF; approve the delivery file; then perform mandatory post-delivery cleanup. The user may override motion, framing, duration, or mood, but never the **135×240** resolution spec, the full-body-still-before-video rule, the **native first+last-frame loop**, the source-video and final-file quality gates, or the final cleanup requirement. **Convert-only exception:** a user-supplied looping MP4 skips still generation and Imagine — encode with the looping-source even-sample path.

## Product facts (researched)

Qwertykeys QK100 Mk2 is a compact full-size / 1800-style prebuilt with **dual screens**: a color LCD used for custom GIFs / Dynamic Island themes, plus a separate interactive **dot-matrix** display. Custom GIFs are uploaded through **QK Config** (wired USB; official tutorial: connect keyboard, `Fn+H`, Fun Screen / Display, import GIF).

### Hard GIF-panel spec (do not invent another size)

These numbers come from QK family LCD documentation and must be used strictly:

| Parameter | Spec | Source |
|-----------|------|--------|
| Resolution | **135×240** (W×H) | QK100 LCD setup notes (Swagkeys Notion): 해상도 **135x240**, 비율 **9:16** |
| Aspect | **exactly 9:16** | Official [QK100 Wireless PCB Guide](https://qwertykeys.notion.site/QK100-Wireless-PCB-Guide-2a172f718bf14d1b8e8679b5f12a96a7): “the best ratio is **9:16**”; other ratios are cropped or shrunk |
| Orientation | **portrait** (tall strip between the main cluster and numpad) | Same LCD family as original QK100; Mk2 keeps a vertical GIF / Dynamic Island panel |
| Max frames | **128** | QK100 LCD notes: “128 프레임까지 지원” |
| Frame rate | **10 fps** (100 ms/frame) | Looping source: even-sample (not `fps=10`); delays 100 ms |
| Loop | **infinite** (`loop=0`) | Required |
| Colors | **256** palette GIF | `palettegen` + `sierra2_4a` |
| Soft size ceiling | **~2.5 MB** | Shrink if QK Config rejects the file |

**135:240 = 9:16 exactly.** Deliver **135×240**, never 240×240, never RT85 320×172, never 240×135 unless the user pastes a QK Config crop that literally shows that size.

Community notes that list `240×135` are the same 9:16 panel with axes swapped; this skill always writes **width 135, height 240**.

Mk2 marketing (“upload your own gif/image”, “GIFs for Dynamic Island”) does not publish a different pixel table. Treat the QK100 LCD **135×240 / 9:16 / ≤128 frames** table as the Mk2 GIF-screen spec.

Keep QK100 work in `output/qk100/`. Do not mix with `output/rt85/` or `output/rt100pro/`.

## 1. Prepare the Reference and Motion

Inspect the supplied image or video. If neither is supplied, ask for one. Keep all intermediates and final files in `output/qk100/`; name a generated full-body still `*-fullbody.png` (or `.jpg`), the source `*-source.mp4`, and the final `*-qk100.gif`.

### Full-body still first (mandatory if the user image is not full body)

Before any `reference_to_video` call, decide whether the user still already shows the **entire character**:

- **Full body already:** head, hair, both hands, torso, legs, and feet (plus cape, tail, weapon, or other attached props) are all visible with usable margins. Use that image (after 9:16 / home-pose edit if needed) as `$FULLBODY_STILL`.
- **Not full body:** half-body, chest-up, headshot, seated crop, missing feet, or any cut-off limbs. **Do not animate this crop.** First generate a new **9:16 full-body photograph/illustration** of the **same character** with `image_edit` (preferred in Grok Build) or Imagine image editing via `grok --single`. Follow **Identity lock**. Complete the unseen lower body consistently with the visible costume. Compact upright **home pose**: feet together, arms relaxed at the sides, small margins, never overhead. Save it as `output/qk100/*-fullbody.png`. Inspect the new still **against the original reference**: if feet, head, or hands are still missing, or Identity lock failed, edit once more. Only then set `$FULLBODY_STILL` to this generated file.

Never call `reference_to_video` / `image_to_video` on a non-full-body user crop. Never invent a different character.

### Identity lock (required)

The figure in every generated still and video must stay **highly consistent** with the **user's original reference**. This is strictest on the **first-frame still** (`$FULLBODY_STILL`): crop and pose may change to the home pose / 9:16, but it must still be **that same person in that same drawing style**.

Lock these from the original: face shape, eyes (color, shape), hair (color, length, style, ornaments), body type, outfit (cut, colors, materials, accessories), and **medium** (2D painterly / anime illustration stays 2D; do not convert to photoreal 3D or CGI, and vice versa).

When `image_edit` creates that still: pass the reference **twice**; name those locked traits in the prompt. Then **compare the still side by side with the original reference**. Reject and redo if the face, hair, eyes, outfit, body type, or style drifted — including a prettier face, different eye color, restyled hair, slimmer body, or a photoreal restyle of an illustration.

Video frames must keep this locked identity.

### Portrait composition (required)

The QK100 Mk2 GIF panel is a **tall 9:16 strip**, 135 px wide. Do **not** reuse RT85 landscape framing, RT100 Pro square overhead-hands framing, or a chest-up crop.

- Compose for **portrait 9:16**, then scale **exactly to 135×240**.
- The character must be **full body in frame** for the reference still and every video frame: head, hair, both hands, torso, legs, and feet (plus cape, tail, weapon, or other attached props). Leave a small margin on all four sides so nothing is clipped.
- Center the subject; 135 px is very narrow, so keep the stance compact and upright. Shoulder-height fists are allowed; a full T-pose is not — elbows stay close enough that both arms remain inside the 9:16 frame.
- Hands stay at or below the head. Expected beats use shoulder-height fists, a chest-height palm push toward camera, a hand on the hip, and both hands meeting at the chest. Hands must never rise above the head.
- Avoid chest-up crops, head-and-shoulders close-ups, and any pose that needs horizontal space.

### Default motion contract

Use every explicit motion instruction. Otherwise, use this **QK100-only** default: a **seamless full-body portrait loop** of the in-place phrase below. Do **not** apply the RT100 Pro overhead-hands dance, the RT85 landscape lounge, or a slow languid sway.

Keep the full body inside the 9:16 frame for the entire clip. Hands stay at or below the head; keep elbows compact enough that both arms remain inside the portrait. Feet stay on the ground with only small in-place steps.

Drive this phrase on every default run (include every beat in the video prompt):

1. **Home pose** — centred, feet together, arms relaxed at the sides, slight smile, facing camera.
2. **Shoulder-fist bounce** — both hands rise to loose fists at shoulder height and pump on the beat; springy knee bounce; small left-right weight hop in place.
3. **Hip-pop camera-push** — one hand drops to the hip; the other palm pulses toward the camera at chest height; hips pop hard to the side with a waist body-wave; knees keep bouncing.
4. **Chest-frame** — both hands briefly meet or cross at the chest, then open.
5. Return to the **home pose**.

Hair, clothing, cape, and jewelry follow a half-beat behind. For clearly adult characters, keep the mood fun, flirtatious, and energetic—tasteful, non-explicit. For childlike or age-ambiguous subjects, keep the same geometry but cute/playful only. No overhead arms, no big jumps that leave the ground for long, no travel that walks the figure out of frame, and no camera-only fake motion.

**Native loop (mandatory — Grok Build):** every source video **must** use **`reference_to_video`** with **`first_frame` and `last_frame` both set to the same `$FULLBODY_STILL`** (9:16 home pose). **Forbidden:** `image_to_video` alone as a fake loop. The prompt describes the in-place dance **between** those identical frames (locked camera, full body every frame, every default-phrase beat unless the user overrides motion). Do **not** require timed 0.4 s / 5.4 s returns. Preserve identity, anatomy, outfit, and mood. Do not generate an open-ended clip. Do not fake the seam with a freeze, fade, or ffmpeg trim.

## 2. Produce the Source MP4 through Local Grok Imagine

If the user supplies a usable MP4, use it as `$SOURCE_MP4` and start at Gate 1. **If that MP4 already loops, skip Imagine and encode with the looping-source even-sample path.** Otherwise generate a real animated source with Grok Build **`reference_to_video`** (`first_frame`=`last_frame`=`$FULLBODY_STILL`). Do not substitute a nonexistent `imagine-video` command or a still-image animation.

**Preferred in a Grok Build / Grok TUI session:**

1. Resolve `$FULLBODY_STILL` as above. If the user image was not full body, this **must** be the newly generated full-body still, not the original crop.
2. If `$FULLBODY_STILL` is full body but not yet the dance **home pose** or not 9:16, `image_edit` it into a **full-body home pose**: feet together, arms relaxed at the sides, compact, facing camera. Follow **Identity lock**. Do **not** convert the pose to overhead hands or crop to chest-up. Compare the result with the original reference before using it.
3. Call **`reference_to_video`** on `$FULLBODY_STILL` (locked camera, ~6 s unless the user sets duration) with **`first_frame`=`last_frame`=`$FULLBODY_STILL`**. The video prompt must require **full body in every frame** and every default-phrase beat (shoulder-fist bounce, hip-pop camera-push, chest-frame) unless the user overrides motion — mid-clip action only, no timed return hard gate. Copy the MP4 to `output/qk100/*-source.mp4`.

**Otherwise (Codex or shell-only):**

```zsh
mkdir -p output/qk100
grok --single "$PROMPT" --max-turns 8 --permission-mode auto --always-approve \
  --no-alt-screen --output-format plain
```

If `reference_to_video` (with `first_frame`/`last_frame`) is unavailable, report `REFERENCE_TO_VIDEO_LOOP_UNAVAILABLE` and stop — do not silent-downgrade to `image_to_video`-only. Never replace it with zoom, pan, scale, parallax, a slideshow, or another static-image fallback.

Request one locked-camera, **9:16 portrait**, looping source MP4 (default 6 s). Pin **first and last frame** to **`$FULLBODY_STILL`**. The prompt must name that still (the generated full-body photo when the user crop was incomplete), **full body in every frame**, and required motion (every default-phrase beat when no user motion is supplied).

## Gate 1 — Approve the Source Before Converting

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p output/qk100/source-check
ffmpeg -hide_banner -loglevel error -ss 0 -i "$SOURCE_MP4" -frames:v 1 output/qk100/source-check/early.png
ffmpeg -hide_banner -loglevel error -ss "$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SOURCE_MP4" | awk '{printf "%.3f", $1/2}')" -i "$SOURCE_MP4" -frames:v 1 output/qk100/source-check/middle.png
ffmpeg -hide_banner -loglevel error -sseof -0.04 -i "$SOURCE_MP4" -frames:v 1 output/qk100/source-check/late.png
```

Reject a zero-byte, incomplete, static, or whole-frame-only scale/translation source. **Convert-only** of a user-supplied looping MP4: probe decode, confirm first≈last (same Gate 2 loop test), then even-sample — do not require the default dance phrase.

When the default loop-dance contract applies, also reject identity drift versus the **original user reference** (face, hair, eyes, outfit, body type, drawing style). Early / middle / late frames must show the **entire body** (head, hands, feet, and attached props) inside the **9:16** frame. Mid-clip must show the default phrase. Do **not** hard-fail on first≈last pixel MAE for a generated native loop — the loop is closed by `first_frame`=`last_frame`=`$FULLBODY_STILL`. The middle frame must show the default phrase: a **shoulder-fist bounce** and/or the **hip-pop + camera-push**, with springy knees. Reject chest-up crops, cropped feet or head, overhead hands, frozen arms, a sleepy or near-still sway, missing hip-pop, missing bounce, or abrupt snaps. If motion/identity fails, regenerate with `reference_to_video` and `first_frame`=`last_frame`=`$FULLBODY_STILL`. Do not treat endpoint MAE as a hard loop gate on generated native-loop sources. Never repair with ffmpeg.

## 3. Render the QK100 Mk2 GIF

Render a **strict 135×240** portrait GIF, 256 colours, infinite loop, **≤128 frames**. **Even-sample** the full source uniformly into the frame budget (default ~60 frames from ~6 s; always **≤128**). Do **not** irregularly skip frames. Do **not** trim off the pinned last frame as a seam hack.

### Looping source — even-sample (required)

Use this whenever `$SOURCE_MP4` already loops (Gate 2: endpoint MAE is not both above 12 and above 1.3× step MAE), including a **user-supplied looping MP4**.

- If the user sent mixed videos and did not name a device: **9:16 / portrait → QK100**; 16:9 / widescreen → RT85; 1:1 → RT100 Pro.
- Even-sample from source **frame 0 through the last frame**. GIF first = source first; GIF last = source last. Indices: `round(i * (N-1) / (n-1))` for `i = 0..n-1`.
- `n = min(128, N, max(2, round(duration_seconds * 10)))`. **Never** more than 128 frames. If duration × 10 would exceed 128, even-sample 128 across the whole clip (plays slightly faster).
- Do **not** use `fps=10` (from 24 fps it drops 2-2-3 and can miss the last frame).
- Scale only: `scale=135:240:flags=lanczos`. Do not crop. Do not pad/letterbox.
- Every frame delay **100 ms**. Palette 256 + `sierra2_4a`, `loop=0`. Do not copy the first frame onto the last.
- User-supplied convert: write `output/qk100/<中文名>-qk100.gif` at the model-folder **root** (short Chinese name, no spaces, no per-video subfolder) unless the user asks for a folder.

If mid-clip motion fails on a **generated** source, regenerate with `reference_to_video` and `first_frame`=`last_frame`=`$FULLBODY_STILL`; do not add fades or static fake animation. A user-supplied clip that does not loop is not this path.

Never scale to 240×240, 320×172, or 240×135.

## Gate 2 — Approve the Delivery GIF

```zsh
VERIFY=""
for p in \
  "$HOME/.grok/skills/generating-qk100-gifs/scripts/verify_qk100_gif.py" \
  "$HOME/.codex/skills/generating-qk100-gifs/scripts/verify_qk100_gif.py"; do
  [ -f "$p" ] && VERIFY="$p" && break
done
python3 "$VERIFY" "$OUTPUT_GIF"
ffprobe -v error -show_entries format=format_name,duration,size:stream=codec_name,width,height,nb_frames,avg_frame_rate \
  -of default=noprint_wrappers=1 "$OUTPUT_GIF"
```

Deliver only when the verifier passes, the file is GIF data, it is **exactly 135×240**, it has **2–128 frames** and `loop=0`, mid-clip motion/identity pass, and frames stay legible at 135×240 (endpoint MAE is warn-only, not a hard fail when `first_frame`=`last_frame` was set). When the default loop-dance applies, representative frames must keep the **full body** in frame and a readable default phrase (shoulder-fist bounce, hip-pop, camera-push). First and last delivery frames must match closely enough that the loop is seamless.

State the final path, **135×240**, duration, frame count, and file size. Upload with the **QK100 Mk2 connected by USB** through **QK Config** (Fun Screen / Display / import GIF). Official connect hint: `Fn+H`.

## 4. Mandatory Post-Delivery Cleanup

After Gate 2 passes, keep exactly these two current-run deliverables in `output/qk100/` for a **generated** run:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified QK100 GIF, named `*-qk100.gif`.

**Convert-only** of a user-supplied looping MP4: keep the GIF at `output/qk100/<中文名>-qk100.gif`. Do not copy the user's original into the output folder unless they asked.

Delete every other resource created for that run: generated `*-fullbody` stills, 9:16 reference images, source-check frames, contact sheets, failed candidates, and loop diagnostics. Use an explicit per-run manifest; never wildcard-delete unrelated historical files. Do not clean up until Gate 2 passes.

Re-verify the final GIF after cleanup. The handoff lists only the retained source MP4 and final GIF.
