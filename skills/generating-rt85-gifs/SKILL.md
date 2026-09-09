---
name: generating-rt85-gifs
description: >
  Create, animate, convert, or optimize a GIF for the EPOMAKER RT85 keyboard
  1.47-inch landscape rectangular TFT screen from a reference image or video.
  Use for RT85 mini-screen GIFs, Grok Imagine reference_to_video / image_to_video
  animation, landscape loop source MP4s, recumbent come-hither GIFs, three-shot
  recumbent editorial GIFs, 320x172 delivery GIFs, RT85 upload-ready media, or when
  the user runs /generating-rt85-gifs.
---

# Generating RT85 GIFs

For every RT85 request, follow this fixed pipeline in order: **ask which motion contract to use** (unless already named); inspect the supplied still; **if it is not a 16:9 full-body recumbent photo of the same character, first generate that still** (Motion A also requires a flat solid #888888 backdrop; Motion B does not); prepare the stills for the chosen contract; make or accept a real landscape MP4; approve the source animation, render the GIF, approve the delivery file, then perform mandatory post-delivery cleanup. The user may override motion, framing, duration, mood, or background, but never the source-video and final-file quality gates or the final cleanup requirement.

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
**Do not** copy the RT100 Pro **standing** three-shot 回身 onto this panel — a standing figure is tiny in 320×172. RT85 three-shot stays **recumbent** and **landscape**.

If the user's EPOMAKER driver crop UI shows a different size, honor that size: re-render with the driver-stated `W×H` and pass `--width` / `--height` to the verifier. Keep all other gates.

Keep RT85 work in `output/rt85/` and RT100 Pro work in `output/rt100pro/`.

### Run folder (required)

Each generation lives in its own subdirectory: `output/rt85/<中文名>/`. Name the folder in **Chinese**, short, no spaces. Prefer the character name from the user's file or message (example: `阿卡丽_蓝焰半身_072.jpg` → `阿卡丽蓝焰`). If the user gives a name, use that. One folder per character; re-renders of the same character reuse that folder so Motion B shot clips stay findable. Do not write deliverables into `output/rt85/` root. Do not mix two characters in one folder. `$RUN_DIR` = `output/rt85/<中文名>/`. Intermediates and finals for that run go only there. Cleanup must not touch sibling folders.

## 1. Prepare the Reference and Motion

Inspect the supplied image or video. If neither is supplied, ask for one. Create `$RUN_DIR` first. Keep all intermediates and final files in `$RUN_DIR`; name a generated recumbent still `*-fullbody.png` (or `.jpg`), editorial cover/inner stills `*-cover` / `*-inner`, landscape face stills `*-face.png`, come-hither stills `*-curl.png`, Motion B per-shot clips `*-cover.mp4` / `*-upper.mp4` / `*-face.mp4`, the assembled source `*-source.mp4`, and the final `*-rt85.gif`.

### Choose a motion contract (required)

This skill has **two default motion contracts**. They are separate. Never mix them in one clip. Never use the RT100 Pro standing step-touch or standing 回身 here.

If the user has not already named a motion, **stop and ask before any `image_edit` or video call**. Present exactly these two options, in the user's language, and wait:

1. **Recumbent come-hither** — one locked-camera 16:9 full-body shot; she lies across the wide screen and hooks an index finger toward the camera.
2. **Three-shot recumbent editorial** — three hard-cut **landscape** photobook pages in a **supermodel recline**, still lying down: recumbent full-body cover, recumbent upper-body inner page, recumbent face close-up. Each shot holds its pose; hair and clothes blow in a side wind; every shot does a slow camera push-in.

Do not pick one silently. Do not start generating until they choose. Skip the question only when they already named one of these (勾手 / come-hither, or 回眸 / 三镜头 / glance / 写真), or gave a different explicit motion (that explicit motion still overrides both).

### Recumbent full-body still first

Both contracts **show the figure lying across the wide screen**. Before any video call, `$FULLBODY_STILL` must be a **16:9 recumbent full-body** of the **same character**.

- **Usable already:** head, hair, both hands, torso, legs, and feet (plus cape, tail, or other attached props) are all visible with small margins, the figure is **lying on its side** (head one side, feet the other), and the frame is landscape. Motion A also requires a **flat solid #888888 fill** with no original scene and **no bench, slab, or board**. Motion B has **no background restriction** — keep the source environment. Use that image as `$FULLBODY_STILL`.
- **Not usable:** standing, seated, half-body, chest-up, missing feet, portrait crop, or the figure is tiny in a wide empty frame. Motion A is also not usable when the original forest / throne / architecture / crowd is still behind the figure, the figure is lying on a bench, stone slab, or board, or the background is a cyclorama, studio gradient, or textured gray rather than a flat solid #888888 fill. **Do not animate this crop.** First generate a new **16:9 full-body recumbent illustration** of the **same character** with `image_edit` (preferred in Grok Build). Pass the reference **twice** so 16:9 is honored. Preserve exact face, hair, outfit, **body type**, and style. Complete the unseen lower body consistently with the visible costume. Motion B: keep the source background; do not replace it with #888888.

**Pose (required):** a **Vogue supermodel editorial recline** on her side, **head at the left** of the frame and **feet at the right**, entire figure from hair/crown to feet with **small margins** so the character **fills** the 16:9 frame. Motion A: she lies **directly on the flat solid #888888 ground**. Motion B: she lies in the source scene; no background swap. Weight rests on the down hip and thigh; torso stays close to the ground. She props on the **down-side elbow only**, forearm tucked close to the ribs. Long S-curve through the spine. Bottom leg extended toward the feet; top knee softly bent. Motion B: the free hand rests on the waist. Motion A: that free hand is reserved for the come-hither. Never overhead. Never two locked arms pushing the torso up off the ground. Do not put a staff, weapon, or other prop in a free near hand; omit it unless the user asked to keep it.

**Background:** **Motion A (required):** replace the source scene with a **flat solid #888888 fill**. Same hex everywhere — no cyclorama, no floor-to-wall seam, no lighting falloff, no texture. The figure lies **on that solid gray**, not on a bench, stone slab, table, or board. Do not keep the original environment unless the user asked to keep it. **Motion B:** no background restriction. Keep the source environment. Do not replace it with #888888 unless the user asked.

**Garment physics (required):** skirts, gowns, sashes, and capes **cover the hips and the tops of the thighs**, then **pool on the ground by gravity** in natural folds (Motion A: the solid #888888 ground). Do not wedge fabric between the legs so it reads as shorts, a leotard, or a bikini. A high slit may show a lower thigh if the source costume already has one.

Inspect the new still: if feet, head, or hands are missing, the gown is bunched as underwear, a staff is still in a free near hand, she is hovering on two straight arms, the pose is not the supermodel recline, or identity drifted, edit once more. Motion A only: also reject a bench / slab / board under the figure, a cyclorama / lighting gradient / texture, or the original scene still in the background. Motion B: do not reject the original scene. Only then set `$FULLBODY_STILL` to this generated file.

Never call a video tool on a non-full-body user crop. Never invent a different character. Do not slim, enlarge, or restyle the body when the user asked to keep the reference unchanged.

### Landscape composition (required)

Because the RT85 panel is a **wide horizontal rectangle**, not a square, **do not reuse RT100 Pro square standing framing**, and **do not** treat a chest-up MCU as the only shot of Motion A.

- Compose every still and clip for **landscape** (target aspect **16:9**, final scale **320×172**).
- Do **not** keep the figure tiny inside a wide empty frame.
- Avoid RT100 Pro overhead-arm poses and standing full-body 回身.

### Motion A — Recumbent come-hither

Use this contract only after the user chose it (or named equivalent motion such as 勾手 / come-hither).

From `$FULLBODY_STILL`, the **near hand is free at collarbone-to-chest height** (palm toward the camera, index ready to hook). Pixel-crop `*-face.png` into 16:9 (hair inside the top edge, chin / neckline in the lower third; the raised beckon hand may stay in frame). Do **not** default to `image_edit` for this crop: a redraw often changes the face. Composite onto matching #888888 if the source has alpha. Only use `image_edit` if a crop cannot reach 16:9 without cutting the subject; then pass the still twice so 16:9 is honored, and reject the result if identity drifted.

Also make `*-curl.png` from `$FULLBODY_STILL`: **same recumbent framing and identity**, only the beckon hand changes — **index finger hooked inward** in a come-hither, other fingers softly curled, palm toward the camera. Video models skip the curl unless they see this still. Reject a curl still that is a wave, a point-at-the-sky, a salute, or both-eyes-closed.

The recumbent full-body still is the **loop start and end**. Do not start the clip on a feet close-up.

**Camera:** stay on the exact 16:9 recumbent full-body composition of `$FULLBODY_STILL` for the whole 6 s, including the **flat solid #888888 fill**. No zoom to the face, no pan that loses the feet, no standing the figure up, no bench / slab / board, no restoring the original scene. First frame matches last.

**Come-hither:** the raised hand stays at **collarbone-to-chest height**, palm toward the camera. Over the clip the **index finger curls inward** (match `*-curl.png`), then relaxes, **two or three times**. The other hand stays resting. Eyes stay **open** and look at the camera. Do not turn the gesture into a wave, a salute, or a point at the sky.

**Supporting motion:** hair, hanging hem, and a small breath may move. Motion must be **visible at 320×172** — reject a frozen painting. Keep it physically plausible: no overhead arms, no jumps, no walking out of frame. Preserve identity, anatomy, outfit, and body type.

The raised come-hither hand must stay **legible at 320×172** (chest-height, not a tiny speck). The **entire recumbent figure** fills the frame for the whole loop.

For clearly adult characters, keep the mood confident and alluring. For childlike or age-ambiguous subjects, keep the same recumbent full-body camera but replace the come-hither with a **simple friendly wave** (no inviting curl).

Reject a still-image pan, zoom, scale, or parallax made in ffmpeg. Naming the full-body path in a text prompt is **not** enough to lock the lower body — the video call must see `$FULLBODY_STILL` as an image.

### Motion B — Three-shot recumbent editorial

Use this contract only after the user chose it (or named equivalent motion such as 回眸 / 三镜头 / glance / 写真).

Do **not** stand the figure up. Do **not** copy RT100 Pro's square standing 回身. The GIF plays **three hard-cut 16:9 photobook pages**, then loops. Hold the **supermodel recline** from `$FULLBODY_STILL` on every page. Drama is the **cut between poses**, not the same 回眸 three times. Inside each shot the pose **holds**; a **gentle side wind** moves hair and clothes; a **slow camera push-in** runs on **every** shot, including the first two, the same way the face page already feels closer.

1. **Cover — recumbent full body** (~1.8 s in the GIF) — head left, feet right, figure filling the wide frame (same crop as `$FULLBODY_STILL`). Supermodel recline: down-elbow tucked, free hand on the waist, top knee bent. She looks **toward her feet**. Wind in the hem, cape, and hair ends.
2. **Inner page — recumbent upper body** (~1.8 s) — 16:9 window from crown to hips; face, shoulders, and the waist hand readable at 320×172. Same recline; she looks at the camera; the free hand stays on the waist as a held editorial gesture. Wind in hair and sleeve/gown folds.
3. **Close-up — recumbent face** (~1.8 s) — 16:9 (hair inside the top edge, chin / neckline in the lower third). Direct gaze held. Wind in hair strands and earrings; one slow blink is allowed **mid-shot**. **The last frame of this 1.8 s face trim must show eyes open** — never end the face page on a closed blink.

Do not repeat a full 回眸 on every shot. Do not mix in the come-hither curl. She does not sit up, stand, crawl, or spin. Hips and feet stay planted. Wind is continuous and light — readable at 320×172, never a hair whip.

**Push-in (required on all three shots):** native Imagine slow dolly/push-in along the lens axis. Keep it small so the **shot class does not change**: shot 1 still shows heels at the end of the 1.8 s trim; shot 2 still reads crown-to-hips at the end of 1.8 s; shot 3 keeps hair in the top edge and chin/neckline in frame. No pan. No pull-back. **Never** fake the push-in with an ffmpeg zoom, scale, crop-pan, Ken Burns, or parallax.

From `$FULLBODY_STILL` (cover pose, looking toward the feet), `image_edit` one **inner** still of the same recumbent figure: eyes on camera, waist hand held, same garment coverage, **same background as `$FULLBODY_STILL`** (do not replace it with #888888). Prefer **pixel-crop** `*-upper` and `*-face` from that inner still. Use `image_edit` for those crops only if a 16:9 window cannot cover crown-to-hips or the face without cutting the subject; then pass the still twice, 16:9, and reject identity drift.

Because a face close-up cannot match a full-body first frame, **bookend the assembled GIF with a copy of the first full-body frame** as the last frame so endpoint MAE stays ≤ 12. Do not crossfade the cuts.

## 2. Produce the Source MP4 through Local Grok Imagine

If the user supplies a usable MP4, use it as `$SOURCE_MP4` and start at Gate 1. Otherwise generate a real animated source with Imagine. Do not substitute a nonexistent `imagine-video` command or a still-image animation.

**Preferred in a Grok Build / Grok TUI session:**

1. Resolve `$FULLBODY_STILL` as above. If the user image was not a 16:9 recumbent full body, this **must** be the newly generated still, not the original crop.

**Motion A:** Pixel-crop `*-face.png`. Always make `*-curl.png`. Call native **`reference_to_video`** (16:9, 6 s), not a face-only `image_to_video`:

- `<IMAGE_0>` = `$FULLBODY_STILL` (loop start / end; composition lock)
- `<IMAGE_1>` = `$FULLBODY_STILL` (identity, body, and full garment)
- `<IMAGE_2>` = `*-face.png` (idle face)
- `<IMAGE_3>` = `*-curl.png` (come-hither)

The prompt must require: lock the camera on the exact recumbent full-body framing of `<IMAGE_0>` from first frame to last, including the **flat solid #888888 fill** (no bench, slab, or board; no cyclorama or lighting gradient); preserve the **exact garment coverage** in `<IMAGE_1>` (a hanging gown must stay a hanging gown, not a leotard, shorts, or bare-hip cut); the raised hand matches the come-hither cycle of `<IMAGE_3>` two or three times, then returns so the last frame matches the first; eyes stay open on the idle face of `<IMAGE_2>`; no staff in the beckon hand if it was removed. Copy the MP4 to `$RUN_DIR/*-source.mp4`.

**Motion B:** do not animate the original standing crop. After `$FULLBODY_STILL` (cover) and the inner still plus pixel-crops, one 6 s clip per page:

1. Call **`image_to_video`** (16:9, 6 s) from that shot's still (cover full body, inner upper crop, inner face crop). Use **`reference_to_video`** with the same still twice if you need a tighter identity lock. Save the three 6 s clips as `$RUN_DIR/*-cover.mp4`, `*-upper.mp4`, and `*-face.mp4`. **Reuse:** if those three files already exist in `$RUN_DIR` and still pass Gate 1, do **not** regenerate them — only re-trim.
2. The prompt must require: hold the exact recumbent pose of the still; a gentle continuous side wind on hair and clothes (no whip); a **slow gentle camera push-in** on the same axis as the face page; no pan, no sit-up, no stand-up, no pull-back; shot 1 keeps looking toward the feet and keeps the heels in frame; shot 2 keeps the gaze and the waist hand and stays crown-to-hips; shot 3 holds the gaze (one slow blink allowed mid-shot; eyes open at the end) and keeps hair in the top edge; keep the still's background stable every frame (do not replace it with #888888); eyes stay open except for that optional blink. Fall back to `image_to_video` if `reference_to_video` is unavailable.
3. After Gate 1 on each clip, trim **18 + 18 + 18 frames** at 10 fps (1.8 s cover, 1.8 s inner, 1.8 s face) from the portion where wind and the push-in are both visible. **Shift the face window if needed so its last frame has eyes open**; do not keep a closed blink as the face tail. Concatenate full → upper → face, then append **one** copy of the first full-body frame (55 frames). That assembled timeline is `$SOURCE_MP4`.

A face-only `image_to_video` call invents the unseen lower body and routinely changes garment type or proportions. Use it **only** if `reference_to_video` is unavailable. If you must fall back, the prompt still has to name every garment region from `$FULLBODY_STILL`, and Gate 1 must be stricter on outfit and body.

**Otherwise (Codex or shell-only):** invoke the local `grok` CLI so it loads `$imagine`, verifies `reference_to_video` (or `image_to_video` as fallback), and produces the MP4:

```zsh
mkdir -p "$RUN_DIR"
grok --single "$PROMPT" --max-turns 8 --permission-mode auto --always-approve \
  --no-alt-screen --output-format plain
```

If no Imagine video tool is available, report `IMAGE_TO_VIDEO_UNAVAILABLE` and stop. Never replace a missing video tool with an ffmpeg zoom, pan, scale, parallax, slideshow, or another static-image fallback MP4/GIF.

Prefer generating landscape natively; do not depend on later letterboxing a square or portrait video into a wide screen. Do not rely on camera motion **alone** to simulate animation — wind or a held pose must still move. Motion B's native slow push-in is required; ffmpeg zoom, scale, crop-pan, Ken Burns, and parallax stay forbidden.

## Gate 1 — Approve the Source Before Converting

Require a nonzero, decodable MP4 with positive duration.

**Motion A** — extract stations along the clip (endpoints hide a missing curl):

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p "$RUN_DIR/source-check"
for t in 0 1.2 2.6 3.0 3.2 4.4 5.8; do
  ffmpeg -hide_banner -loglevel error -ss "$t" -i "$SOURCE_MP4" \
    -frames:v 1 "$RUN_DIR/source-check/t${t}.png"
done
```

Reject a zero-byte, incomplete, static, or whole-frame-only scale/translation source. Stations must prove **locked full-body framing + curl timing + identity**.

- **~0 s:** 16:9 **recumbent full body** lying **on the flat solid #888888 ground**, eyes open, beckon hand visible. Same crop as `$FULLBODY_STILL`. No bench, slab, or board.
- **~1.2–3.2 s:** at least one clear **index-finger come-hither** (match `*-curl.png`). Hands not overhead. Garment **type and coverage** match `$FULLBODY_STILL`. Backdrop still flat solid #888888.
- **~4.4 s:** still the same recumbent full body, idle or mid-cycle, no both-eyes-closed hold.
- **~5.8 s:** back on the **same recumbent crop** as ~0 s.

Compare mid-clip frames to `$FULLBODY_STILL`, not only to each other. Reject and regenerate when the camera zooms to a chest-up that hides the legs, stands the figure up, shows the whole figure tiny in a wide empty frame, has no finger-curl, holds both eyes shut as the only face beat, snaps, changes garment class or coverage, slims or restyles the body, reintroduces a removed staff, puts the figure on a bench / slab / board, restores the original scene behind the figure, or fails to return to the starting pose.

**Motion B:** Gate 1 each 6 s shot **before** trimming. Pose holds. Background stays the same as that shot's still; do not require #888888. Eyes open except one optional blink mid-shot on shot 3; the face clip must still contain open-eye frames at the end of the 1.8 s trim. Mid-clip must show **wind** in hair/clothes (shots 1–2 at least) and a **slow push-in** that is tighter than frame 0 but does **not** change shot class (full body still shows heels; upper still crown-to-hips; face still includes hair and neckline). Reject a frozen painting, a sit-up, a walk-out, a pull-back, a whip of hair, a push-in so hard that shot 1 becomes MCU, or an ffmpeg zoom. Regenerate the failed shot; do not repair motion with ffmpeg.

When the **Motion A** default background contract applies, Gate 1 must also confirm a **flat solid #888888 fill**, identical every frame. Reject any cyclorama or floor-to-wall seam, lighting gradient, source-scene remnant, text, logo, prop, cutout halo, colour spill, flickering gray tone, crawling texture, or unstable shadow. Motion B has no default background contract — do not reject the source scene. Regenerate Motion A background failures with `image_edit` followed by the video tool used for that contract; never repair motion or background failures with ffmpeg. If the MP4 does not materialize, allow one concise Grok continuation naming the images, output path, required tool, and verification; then report failure rather than falling back.

## 3. Render the RT85 GIF

Render a **320×172** landscape GIF at **10 fps**, 256 colours, infinite loop, and at most **5.5 seconds**. This yields no more than **55 frames**, within the default **56-frame** soft cap.

**Motion A:** the 6-second Imagine source is deliberately trimmed here. Search a **real motion segment** (prefer the **longest** window with endpoint MAE ≤ 12 at **320×172**). A 6 s source often matches at ~60 frames but fails a 55-frame trim; then use the script's **assemble** plan. Do not add fade crossfades or static fake animation. If neither a trim nor an assemble pair passes, regenerate the source — hold the start pose longer at both ends — rather than shipping a jump.

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
# end_frame (drop only non-beckon return frames, never the come-hither beat),
# then palette-GIF that sequence. Do NOT time-stretch the whole clip with
# setpts — that breaks endpoint MAE.
ffmpeg -hide_banner -loglevel error -i "$SOURCE_MP4" -ss "$START" -t "$DURATION" \
  -filter_complex "[0:v]fps=10,scale=320:172:force_original_aspect_ratio=increase:flags=lanczos,crop=320:172,split[frames][palette_source];[palette_source]palettegen=max_colors=256:stats_mode=diff[palette];[frames][palette]paletteuse=dither=sierra2_4a" \
  -loop 0 "$OUTPUT_GIF"
```

**Motion B:** do not run `search_rt85_loop.py` over one 6 s clip. From each approved shot, extract 10 fps **320×172** frames covering wind + push-in: **18** from full-body, **18** from upper, **18** from face (1.8 + 1.8 + 1.8 s). The **18th face frame must show eyes open**; if it is a blink, pick a different 1.8 s window. Concatenate full-body, then upper-body, then face, then **one** copy of the first full-body frame (55 frames). Palette-GIF that sequence (`loop=0`). Do not time-stretch with `setpts`. Hard cuts only. Never add the push-in in ffmpeg.

Prefer regenerating the source video when the loop visibly jumps. Do not depend on a fragile post-production crossfade.

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

Deliver only when the verifier passes, the file is GIF data, it is **320×172** (or the driver-override size) with **56 or fewer frames** and `loop=0`, its endpoint is visually clean, the soft size ceiling is respected, and the display-sized frames remain legible on a **wide** panel. The first-to-last transition must not jump.

**Motion A:** first and last frames must be the **same full-body recumbent crop** lying **on the flat solid #888888 ground**; a mid-clip frame must still show the whole lying figure with matching garment and #888888 fill, **no bench / slab / board**; inspect frames **between** the quartiles for the index-finger curl — that beat will not sit on the first/last samples. The curl must remain readable at 320×172.

**Motion B:** the GIF must contain three distinct **landscape** photobook framings in order (recumbent full-body cover looking toward the feet, recumbent upper-body inner page looking at the camera, recumbent face close-up). A mid-shot frame in each must show wind (hair / hem on shots 1–2; hair / earring on shot 3) and a slightly tighter crop than that shot's first frame. The last face frame (immediately before the bookend) must show **eyes open**. First and last frames must be the same full-body recumbent start (the bookend). No standing figure.

When the **Motion A** default background applies, also confirm that the #888888 fill stays flat and clean after palette conversion. Motion B: keep the source scene; do not require #888888. State the final path, duration, frame count, resolution, and file size. Upload with the **RT85 connected by USB cable** through the current **EPOMAKER Driver** (media / DIY GIF page).

## 4. Mandatory Post-Delivery Cleanup

After Gate 2 passes, clean up the current run before reporting completion.

**Motion A — keep two files** in `$RUN_DIR`:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified RT85 GIF, named `*-rt85.gif`.

**Motion B — keep five files** in `$RUN_DIR`:

- the three 6 s per-shot clips, named `*-cover.mp4`, `*-upper.mp4`, and `*-face.mp4` (do **not** delete these; reuse them on duration-only re-renders);
- the assembled source video, named `*-source.mp4`;
- the final verified RT85 GIF, named `*-rt85.gif`.

Delete every other resource created for that run: generated `*-fullbody` stills, `*-inner` / `*-curl` / `*-upper` / `*-face` still frames (not the `.mp4` shot clips), landscape reference images, source-check frames, contact sheets, loop-assemble PNG folders, temporary downloads or copies, failed candidate MP4/GIF files, loop-duration diagnostics, and other conversion artifacts. Use an explicit per-run manifest or staging list; never use a broad wildcard or recursive deletion that could remove unrelated historical deliverables. Do not clean up until the final GIF passes Gate 2. If cleanup would affect an ambiguous or unrelated file, stop and resolve the target rather than deleting it.

Verify after cleanup that the retained files are nonzero and still present, and that the final GIF still passes the bundled verifier. The final handoff lists those retained files only.
