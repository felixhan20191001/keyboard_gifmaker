---
name: generating-rt85-gifs
description: >
  Create, animate, convert, or optimize a GIF for the EPOMAKER RT85 keyboard
  1.47-inch landscape rectangular TFT screen from a reference image or video.
  Use for RT85 mini-screen GIFs, Grok Imagine reference_to_video / image_to_video
  animation, landscape loop source MP4s, 320x172 delivery GIFs, RT85
  upload-ready media, or when the user runs /generating-rt85-gifs.
---

# Generating RT85 GIFs

For every RT85 request, follow this fixed pipeline in order: inspect the supplied still; **if it is not a full-body photo, first generate a full-body still of the same character**; **pixel-crop a 16:9 feet-band start frame and a 16:9 idle-face still**; make or accept a real MP4 whose **camera rises from the feet to the face and returns**, using those crops plus the full-body still as **visual references**; approve the source animation, render the GIF, approve the delivery file, then perform mandatory post-delivery cleanup. The user may override motion, framing, duration, or mood, but never the source-video and final-file quality gates or the final cleanup requirement.

## Product facts (researched)

Public product materials consistently describe the EPOMAKER RT85 as:

- **Screen**: embedded **1.47-inch TFT** (not the detachable square-ish 1.54" mini-TV on RT100 / RT100 Pro)
- **Shape**: **landscape rectangle, not square** (wide horizontal panel in the key cluster)
- **Media page**: DIY **pictures or GIFs**
- **Upload path**: **EPOMAKER Driver / software** over a **wired USB** connection
- **Other screen modes**: info (connection / OS / battery / date), custom RGB / volume UI

### Delivery defaults (important)

EPOMAKER does **not** publish an official public pixel table for the RT85 GIF crop. The industry-standard panel for **1.47" rectangular TFT** modules is **320×172** landscape (same ST7789-class 172×320 physical panel oriented horizontally; also used by Adafruit / Waveshare 1.47" modules and several 1.47" keyboard screens). This skill therefore delivers **landscape 320×172**, not 240×240 and not portrait 172×320.

| Parameter | Default | Notes |
|-----------|---------|--------|
| Resolution | **320×172** (W×H) | **Landscape rectangle**, not square |
| Aspect | **≈16:9** (exact 320:172 ≈ 1.86:1) | Compose for wide screen; closest Imagine aspect **16:9** |
| Frame rate | **10 fps** (100 ms/frame) | Same cadence as RT100 Pro skill |
| Max frames | **56** | Soft cap; ≤55 preferred via 5.5 s @ 10 fps |
| Max duration | **5.5 s** | From a 6 s Imagine source |
| Loop | **infinite** (`loop=0`) | Required |
| Colors | **256** palette GIF | `palettegen` + `sierra2_4a` |
| Soft size ceiling | **~2.5 MB** | Shrink if the driver rejects upload |

**Do not** use the RT100 Pro square `240×240` defaults for RT85.  
**Do not** deliver portrait `172×320` unless the user or driver explicitly requires it.

If the user's EPOMAKER driver crop UI shows a different size, honor that size: re-render with the driver-stated `W×H` and pass `--width` / `--height` to the verifier. Keep all other gates.

Keep RT85 work in `output/rt85/` and RT100 Pro work in `output/rt100pro/`.

## 1. Prepare the Reference and Motion

Inspect the supplied image or video. If neither is supplied, ask for one. Keep all intermediates and final files in `output/rt85/`; name a generated full-body still `*-fullbody.png` (or `.jpg`), the 16:9 feet start `*-scan-start.png`, the 16:9 idle-face still `*-face.png`, the one-eye wink still `*-wink.png`, the source `*-source.mp4`, and the final `*-rt85.gif`.

### Full-body still first (mandatory if the user image is not full body)

The default clip **scans every body region**. Before any video call, decide whether the user still already shows the **entire character**:

- **Full body already:** head, hair, both hands, torso, legs, and feet (plus cape, tail, weapon, or other attached props) are all visible with usable margins. Use that image as `$FULLBODY_STILL`.
- **Not full body:** half-body, chest-up, headshot, seated crop, missing feet, or any cut-off limbs. **Do not animate this crop.** First generate a new **full-body photograph/illustration** of the **same character** with `image_edit` (preferred in Grok Build) or Imagine image editing via `grok --single`. Preserve exact face, hair, outfit, **body type**, and style. Complete the unseen lower body consistently with the visible costume. Upright standing pose, small margins, both hands in the collarbone-to-waist band, never overhead. Save it as `output/rt85/*-fullbody.png`. Inspect the new still: if feet, head, or hands are still missing, or the body no longer matches the user image, edit once more. Only then set `$FULLBODY_STILL` to this generated file.

Never call a video tool on a non-full-body user crop. Never invent a different character. Do not slim, enlarge, or restyle the body when the user asked to keep the reference unchanged.

### 16:9 stills (pixel crop, not a redraw)

From `$FULLBODY_STILL`, make two **pixel crops** into 16:9. Do **not** default to `image_edit`: a redraw often changes the face, body, or garment.

- `*-scan-start.png` — **feet / lower-leg band** (boots and a bit of calf or cape hem). This is the loop start and end.
- `*-face.png` — idle face (hair inside the top edge, chin / neckline in the lower third; upper chest allowed so the silhouette stays true).

Composite onto a matching background if the source has alpha. Inspect both crops against `$FULLBODY_STILL`. Only use `image_edit` if a crop cannot reach 16:9 without cutting the subject; then pass the still twice so 16:9 is honored, and reject the result if identity drifted.

Also make `*-wink.png` from `*-face.png`: same framing and identity, **one eye closed and the other clearly open**. Video models turn “wink” into both eyes shut unless they see this still. Reject a wink still where both eyes are closed.

A start crop is only the **first** frame. The clip must not stay on the feet.

### Landscape composition (required)

Because the RT85 panel is a **wide horizontal rectangle**, not a square, **do not reuse the RT100 Pro overhead-hands framing**, and **do not lock the whole clip to a chest-up close-up**.

- Compose for **landscape** framing (target aspect **16:9**, final scale **320×172**).
- Each default frame is a **tight horizontal band** of the body: the current region fills the 172 px height; the subject stays horizontally centered with small left/right margins.
- The camera, not a single static crop, reveals the figure: face, neck, shoulders, chest, waist, hips, thighs, legs, and feet appear in turn.
- Do **not** keep the entire standing figure tiny inside a wide empty frame for the whole loop. Do **not** stay on a chest-up MCU for the whole loop.
- Avoid RT100 Pro overhead-arm poses.

### Default motion contract

Use every explicit motion instruction. Otherwise, use this **RT85-only** default: a **vertical body-scan loop that starts at the feet**. The camera travels **up** the standing figure so every body region crosses the wide short screen, reaches the face, then travels **down** the same path and ends on the identical feet crop. On the **upward arrival at the face** the character does a **one-eye wink**, then a **small cute follow-up** (hand to cheek, small head tilt). Do **not** apply the RT100 Pro overhead-hands dance, a locked-camera chest-band lounge, a face-first wink at clip start, or an ffmpeg Ken Burns of a still.

**Camera (required):** start on the 16:9 **feet crop**. Hold ~0.4 s. Travel **up** in one continuous move: feet → legs → thighs → hips → waist → chest → neck → face. The face fills the frame around the midpoint (~2.6–3.2 s). Then travel **down** the same path and return to the identical feet crop by ~5.2 s. Hold the last ~0.8 s on those feet. Do not jump regions or cut. Begin and end at the **same camera height** (the feet).

**Idle vs face action (required):** while the camera is on legs, hips, waist, or torso, the character stays **idle** — hands down at the sides, both eyes would be open, no wink, no cheek touch, no frozen face-pose. The default face beat starts **only after the face has filled the frame on the way up from below**: first a clear **one-eye wink** (one eye closed, the other open — not both eyes shut), then a **natural cute gesture** (gloved or bare hand lifts to the cheek, small head tilt). Release back to idle **before** the camera leaves the face. Never wink at clip start. Never hold the wink or cheek pose during the downward travel. Motion stays smooth and natural.

**Character (required):** idle travel may include a small natural weight shift or breath. Motion stays physically plausible: no overhead arms, no jumps, no walking out of the scan line. Preserve identity, anatomy, outfit, and body type.

For clearly adult characters, keep the mood confident and tasteful. For childlike or age-ambiguous subjects, keep the same up-down geometry but playful/cute only. Include every listed beat in the Grok prompt unless the user requests different motion.

The default **does** use real camera travel. Still reject a still-image pan, zoom, scale, or parallax made in ffmpeg. Naming the full-body path in a text prompt is **not** enough to lock the lower body — the video call must see `$FULLBODY_STILL` as an image.

## 2. Produce the Source MP4 through Local Grok Imagine

If the user supplies a usable MP4, use it as `$SOURCE_MP4` and start at Gate 1. Otherwise generate a real animated source with Imagine. Do not substitute a nonexistent `imagine-video` command or a still-image animation.

**Preferred in a Grok Build / Grok TUI session:**

1. Resolve `$FULLBODY_STILL` as above. If the user image was not full body, this **must** be the newly generated full-body still, not the original crop.
2. Pixel-crop `*-scan-start.png` (feet) and `*-face.png` (idle face) from `$FULLBODY_STILL`. Always make `*-wink.png` from the idle face (one eye closed, the other open). Do **not** convert the pose to overhead hands.
3. Call native **`reference_to_video`** (16:9, 6 s) with those stills, not a face-only `image_to_video`:
   - `<IMAGE_0>` = `*-scan-start.png` (feet; loop start / end)
   - `<IMAGE_1>` = `$FULLBODY_STILL` (identity, body, and full garment)
   - `<IMAGE_2>` = `*-face.png` (idle face)
   - `<IMAGE_3>` = `*-wink.png` (one-eye wink)
4. The prompt must require: hold `<IMAGE_0>` ~0.4 s; travel **up** the **exact** idle body in `<IMAGE_1>` (same garment coverage — a sealed catsuit must stay a sealed catsuit, not a leotard, skirt, or bare-hip cut; hands down; no face-pose); only when `<IMAGE_2>` fills the frame, match the one-eye wink in `<IMAGE_3>` then a cute cheek-touch, and release to idle; travel **down** idle; return to the identical `<IMAGE_0>` feet by ~5.2 s and hold so the last frame matches the first. Copy the MP4 to `output/rt85/*-source.mp4`.

A face-only `image_to_video` call invents the unseen lower body and routinely changes garment type or proportions. Use it **only** if `reference_to_video` is unavailable. If you must fall back, the prompt still has to name every garment region from `$FULLBODY_STILL`, and Gate 1 must be stricter on outfit and body.

**Otherwise (Codex or shell-only):** invoke the local `grok` CLI so it loads `$imagine`, verifies `reference_to_video` (or `image_to_video` as fallback), and produces the MP4:

```zsh
mkdir -p output/rt85
grok --single "$PROMPT" --max-turns 8 --permission-mode auto --always-approve \
  --no-alt-screen --output-format plain
```

If no Imagine video tool is available, report `IMAGE_TO_VIDEO_UNAVAILABLE` and stop. Never replace a missing video tool with an ffmpeg zoom, pan, scale, parallax, slideshow, or another static-image fallback MP4/GIF.

Request one **landscape**, 6-second source MP4 whose **camera travels vertically** along the body. Prefer generating landscape natively; do not depend on later letterboxing a square or portrait video into a wide screen.

## Gate 1 — Approve the Source Before Converting

Require a nonzero, decodable MP4 with positive duration. Extract stations along the scan — face-only endpoints hide mid-body drift:

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p output/rt85/source-check
for t in 0 1.2 2.6 3.0 3.2 4.4 5.8; do
  ffmpeg -hide_banner -loglevel error -ss "$t" -i "$SOURCE_MP4" \
    -frames:v 1 "output/rt85/source-check/t${t}.png"
done
```

Reject a zero-byte, incomplete, static, or whole-frame-only scale/translation source. When the default body-scan contract applies, the stations must prove **travel + idle timing + identity**. Quartile samples miss a one-beat wink — that is why 2.6 s and 3.2 s are required.

- **~0 s:** 16:9 **feet / boots**, idle. Same crop as `*-scan-start.png`.
- **~1.2 s:** thighs / hips. Hands **down**, idle, no wink-pose. Garment **type and coverage** match `$FULLBODY_STILL`.
- **~3.0 s:** **face** has arrived. The default **one-eye wink** (then cute cheek gesture) starts **here** (or in the 2.6–3.4 s extras), not at 0 s and not as a pose frozen from earlier.
- **~4.4 s:** mid-body going **down**, idle again — hands down, no held wink or cheek touch.
- **~5.8 s:** back on the **same feet crop** as ~0 s.

Compare 1.2 s and 4.4 s to `$FULLBODY_STILL`, not only to each other. Reject and regenerate when the camera stays locked on one band, never reaches the face or the feet, shows the whole figure tiny in a wide empty frame, jumps regions, winks before the upward arrival, holds a wink/cheek pose during body travel, has no character motion, snaps, changes garment class or coverage, slims or restyles the body, or fails to return to the starting feet. Reject both-eyes-closed as the only face beat. Regenerate with `reference_to_video` (or the fallback video tool); never repair it with ffmpeg. If the MP4 does not materialize, allow one concise Grok continuation naming the images, output path, required tool, and verification; then report failure rather than falling back.

## 3. Render the RT85 GIF

Render a **320×172** landscape GIF at **10 fps**, 256 colours, infinite loop, and at most **5.5 seconds**. This yields no more than **55 frames**, within the default **56-frame** soft cap. The 6-second Imagine source is deliberately trimmed here.

Use cover-crop scaling so non-landscape sources still fill the wide panel without letterboxing:

```zsh
SEARCH=""
for p in \
  "$HOME/.grok/skills/generating-rt85-gifs/scripts/search_rt85_loop.py" \
  "$HOME/.codex/skills/generating-rt85-gifs/scripts/search_rt85_loop.py"; do
  [ -f "$p" ] && SEARCH="$p" && break
done
python3 "$SEARCH" "$SOURCE_MP4"
# If "best" is set: -ss AFTER -i, frame-accurate, use start_seconds / duration_seconds.
# If "assemble" is set instead: extract 10 fps 320x172 PNGs, keep
# [start_frame, start_frame+keep_head) plus the last keep_tail frames through
# end_frame (drop only return-travel frames, never the face-arrival beat),
# then palette-GIF that sequence. Do NOT time-stretch the whole clip with
# setpts — that breaks endpoint MAE.
ffmpeg -hide_banner -loglevel error -i "$SOURCE_MP4" -ss "$START" -t "$DURATION" \
  -filter_complex "[0:v]fps=10,scale=320:172:force_original_aspect_ratio=increase:flags=lanczos,crop=320:172,split[frames][palette_source];[palette_source]palettegen=max_colors=256:stats_mode=diff[palette];[frames][palette]paletteuse=dither=sierra2_4a" \
  -loop 0 "$OUTPUT_GIF"
```

Search a **real motion segment** (prefer the **longest** window with endpoint MAE ≤ 12 at **320×172**). A 6 s boot-to-boot source often matches at ~60 frames but fails a 55-frame trim; then use the script's **assemble** plan. Do not add fade crossfades or static fake animation. If neither a trim nor an assemble pair passes, regenerate the source — hold the feet crop longer at both ends — rather than shipping a jump.

**Portrait override only if the driver demands it:** if the driver requires `172×320`, swap the scale/crop numbers and verifier flags accordingly.

## Gate 2 — Approve the Delivery GIF

Run the bundled verifier and independently inspect representative frames at actual screen size:

```zsh
VERIFY=""
for p in \
  "$HOME/.grok/skills/generating-rt85-gifs/scripts/verify_rt85_gif.py" \
  "$HOME/.codex/skills/generating-rt85-gifs/scripts/verify_rt85_gif.py"; do
  [ -f "$p" ] && VERIFY="$p" && break
done
python3 "$VERIFY" "$OUTPUT_GIF"
# portrait override example (only if driver requires it):
# python3 "$VERIFY" --width 172 --height 320 "$OUTPUT_GIF"
ffprobe -v error -show_entries format=format_name,duration,size:stream=codec_name,width,height,nb_frames,avg_frame_rate \
  -of default=noprint_wrappers=1 "$OUTPUT_GIF"
```

Deliver only when the verifier passes, the file is GIF data, it is **320×172** (or the driver-override size) with **56 or fewer frames** and `loop=0`, its endpoint is visually clean, the soft size ceiling is respected, and the display-sized frames remain legible on a **wide** panel. When the default body-scan applies, first and last frames must be the **same feet band**; a mid-body frame must be idle with matching garment; inspect frames **between** the quartiles (~mid-clip) for the one-eye wink and cute cheek beat — that beat will not sit on the first/last/mid samples. Descent frames must be idle again.

State the final path, duration, frame count, resolution, and file size. Upload with the **RT85 connected by USB cable** through the current **EPOMAKER Driver** (media / DIY GIF page).

## 4. Mandatory Post-Delivery Cleanup

After Gate 2 passes, clean up the current run before reporting completion. Keep exactly these two current-run deliverables in `output/rt85/`:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified RT85 GIF, named `*-rt85.gif`.

Delete every other resource created for that run: generated `*-fullbody` stills, `*-scan-start` / `*-face` / `*-wink` frames, landscape reference images, source-check frames, contact sheets, loop-assemble PNG folders, temporary downloads or copies, failed candidate MP4/GIF files, loop-duration diagnostics, and other conversion artifacts. Use an explicit per-run manifest or staging list; never use a broad wildcard or recursive deletion that could remove unrelated historical deliverables. Do not clean up until the final GIF passes Gate 2. If cleanup would affect an ambiguous or unrelated file, stop and resolve the target rather than deleting it.

Verify after cleanup that both retained files are nonzero and still present, and that the final GIF still passes the bundled verifier. The final handoff for each run must list only the retained source MP4 and final GIF.
