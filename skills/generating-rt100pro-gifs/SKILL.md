---
name: generating-rt100pro-gifs
description: >
  Create, animate, convert, or optimize a GIF for the EPOMAKER RT100 Pro keyboard
  screen from a reference image or video. Use for keyboard mini-screen GIFs,
  Grok Imagine image_to_video / reference_to_video animation, loop dance source
  MP4s, three-shot editorial GIFs, 240x240 delivery GIFs, RT100 Pro upload-ready
  media, or when the user runs /generating-rt100pro-gifs.
---

# Generating RT100 Pro GIFs

For every RT100 Pro request, follow this fixed pipeline in order: **ask which motion contract to use** (unless already named), prepare the reference, make or accept a real MP4, approve the source animation, render the GIF, approve the delivery file, then perform mandatory post-delivery cleanup. The user may override motion, framing, duration, or mood, but never the source-video and final-file quality gates or the final cleanup requirement.

## 1. Prepare the Reference and Motion

### Run folder (required)

Each GIF product lives in its own subdirectory: `output/rt100pro/<中文名>/`. Name the folder in **Chinese**, short, no spaces. Prefer the character name from the user's file or message (example: `阿卡丽_蓝焰半身_072.jpg` → `阿卡丽蓝焰`). If the user gives a name, use that. One folder per GIF product. Do not write a new GIF into another product's folder. If the same character is generated again, add a short distinguisher (`阿卡丽蓝焰-踏步`, `阿卡丽蓝焰-2`). Do not write deliverables into `output/rt100pro/` root. `$RUN_DIR` = `output/rt100pro/<中文名>/`. Intermediates and finals for that run go only there. Cleanup must not touch sibling folders.

Inspect the supplied image or video. If neither is supplied, ask for one. Create `$RUN_DIR` first. Keep all intermediates and final files in `$RUN_DIR`; name editorial cover/inner stills `*-cover` / `*-inner`, square face stills `*-face`, Motion B per-shot clips `*-cover.mp4` / `*-upper.mp4` / `*-face.mp4`, the assembled source `*-source.mp4`, and the final `*-rt100pro.gif`.

### Choose a motion contract (required)

This skill has **two default motion contracts**. They are separate. Never mix them in one clip.

If the user has not already named a motion, **stop and ask before any `image_edit` or video call**. Present exactly these two options, in the user's language, and wait:

1. **Step-touch dance** — one locked-camera square framing; compact four-count left-right step-touch loop.
2. **Three-shot editorial** — three hard-cut square photobook pages, standing: full-body cover, upper-body inner page, face close-up. Each shot holds its page pose with readable idle (breath, weight, hair/clothes) and a slow camera push-in.

Do not pick one silently. Do not start generating until they choose. Skip the question only when they already named one of these, or gave a different explicit motion (that explicit motion still overrides both).

Shared rules for both contracts: preserve identity, anatomy, outfit, and mood; tasteful confident energy for clearly adult characters, playful/cute only for childlike or age-ambiguous subjects; keep every hand and limb inside the square; no spins, jumps, travelling steps, or overhead arms unless the user asked. Hair, clothing, cape, jewelry, wings, tails, flames, or particles follow the body with physically plausible lag. Motion A keeps a locked camera. Motion B requires a **native slow push-in** on every shot; ffmpeg zoom, pan, scale, Ken Burns, and parallax stay forbidden. Do not fake animation with camera motion alone.

**Motion A background:** unless the user explicitly requests a different setting, remove the original background before animation and place the isolated subject on a **flat solid #888888 fill**. Same hex everywhere — no cyclorama, no floor-to-wall seam, no lighting falloff, no texture. The finished Motion A reference and video must contain no recognizable source-scene objects, source text, logos, props, cutout halos, colour spill, background texture crawling, or lighting flicker. Keep the #888888 fill identical every frame for the whole loop.

**Motion B background:** keep each still's original scene. Do not isolate onto #888888 unless the user asks for that fill.

Avoid text or logos unless requested.

### Motion A — Step-touch dance

Use this contract only after the user chose it (or named equivalent motion such as 踏步舞 / step-touch / dance loop).

The compact four-count step-touch choreography is derived from the 00:00.8–00:02.4 passage of `xnd10731_20260824_reel_3970514467695117755_1_3970514467695117755.mp4`. Start centred and upright with the feet close, elbows softly bent about 90 degrees, forearms lifted beside the torso, and relaxed hands near shoulder height. On count one, make a small step-touch to one side with a soft knee bounce and matching hip shift while both elbows and forearms pulse lightly outward and upward. On count two, pass smoothly through centre and mirror the step-touch, hip shift, and arm pulse to the other side. On count three, repeat the alternating rhythm with a subtle counter-rolling shoulder accent and a small natural head tilt; keep the wrists loose and the hands expressive rather than clenched or rigid. On count four, bring both feet, hips, shoulders, elbows, hands, and head back to the exact starting pose. Repeat this four-count cycle exactly twice during the first 5.4 seconds, returning to the starting pose at the end of each cycle and no later than 5.4 seconds. Hold that pose from 5.4 to 6.0 seconds with only near-imperceptible breathing; this protected tail ensures the 10 fps delivery GIF includes a clean reset frame. Keep the rhythm buoyant and even, the movement compact, and the subject facing mostly forward.

For the 1.54-inch screen, prioritize the face, upper torso, hands, hip shift, and enough of the legs to make the step-touch and knee bounce readable. Show the full body only when it remains legible at 240x240.

### Motion B — Three-shot editorial

Use this contract only after the user chose it (or named equivalent motion such as 回眸 / 三镜头 / glance / 回身 / 写真). Stay **standing** and **square**. Do not copy the RT85 recumbent landscape pages here.

The GIF plays **three hard-cut 1:1 photobook pages**, then loops. Drama is the **cut between poses**, not the same 回身 three times. Inside each shot the page pose **holds** while **readable idle** plays (the 240×240 square can show it — do not freeze into a still). A **slow camera push-in** runs on **every** shot, including the first two.

1. **Cover — standing full body** (~1.0 s in the GIF) — crown to heels, figure filling the square. Body mostly back / 3/4 back, looking aside. Idle: breath, a small weight shift, hair / skirt / cape in a side wind. Push-in must still show the feet at the end of the 1.0 s trim.
2. **Inner page — standing upper body** (~2.0 s) — crown to hips; face, shoulders, and the waist hand readable at 240×240. Eyes on camera; one hand rests on the waist as a held editorial gesture. Idle: breath, a small shoulder move, a tiny adjustment of the waist hand, hair and sleeves in wind. Push-in must stay crown-to-hips, not become a face-only crop.
3. **Close-up — standing face** (~2.0 s) — over-the-shoulder / frontal face filling the square. Direct gaze. Idle: one slow blink, hair strands and earrings, slight breath. Push-in keeps hair inside the top edge.

Do not repeat a full 回身 on every shot. Do not mix in the step-touch dance. No travelling, spins, or overhead arms. Idle must be visible at 240×240 but stay planted.

**Push-in (required on all three shots):** native Imagine slow dolly/push-in along the lens axis. Keep it small so the **shot class does not change**. No pan. No pull-back. **Never** fake the push-in with an ffmpeg zoom, scale, crop-pan, Ken Burns, or parallax.

If the user supplies **one image per shot**, use each file as that page's identity master. Square each to 1:1 (pass the still twice when requesting `1:1`), keep that file's original scene and pose, and do not derive inner or face from the cover.

If only one still is supplied, start from a square **cover** still (looking aside, original scene kept). `image_edit` one **inner** still of the same standing figure: eyes on camera, waist hand held, same garment, same scene. Prefer **pixel-crop** upper and face from that inner still. Use `image_edit` for those crops only if a 1:1 window cannot cover crown-to-hips or the face without cutting the subject; then pass the still twice, `1:1`, and reject identity drift.

Because a face close-up cannot match a full-body first frame, **bookend the assembled GIF with a copy of the first full-body frame** as the last frame so endpoint MAE stays ≤ 12. Do not crossfade the cuts.

## 2. Produce the Source MP4 through Local Grok Imagine

If the user supplies a usable MP4, use it as `$SOURCE_MP4` and start at Gate 1. Otherwise generate a real animated source with Imagine. Do not substitute a nonexistent `imagine-video` command or a still-image animation.

**Preferred in a Grok Build / Grok TUI session:** call the native video tool directly. For Motion A when the default background contract applies, always use `image_edit` first—even for an already-square input—to isolate the subject, remove the source background, and create the square flat solid #888888 reference. Pass the still **twice** when requesting `1:1` so the aspect is honored. For Motion B, square the page stills without replacing the original scene.

**Motion A:** one locked-camera `image_to_video` from that square still. Copy the MP4 to `$RUN_DIR/*-source.mp4`.

**Motion B:** do not animate the original crop. After the square cover still, inner still, and face still (original scenes kept), one 6 s clip per page:

1. Call **`image_to_video`** (1:1, 6 s) from that shot's still (cover full body, inner upper, face close-up). Use **`reference_to_video`** with the same still twice if you need a tighter identity lock. Save the three 6 s clips as `$RUN_DIR/*-cover.mp4`, `*-upper.mp4`, and `*-face.mp4`. Do **not** delete them after the GIF is done.
2. The prompt must require: hold the photobook pose of the still; **readable idle** (shot 1 breath + weight shift; shot 2 breath + shoulder / waist-hand; shot 3 blink + breath); a gentle continuous side wind on hair and clothes (no whip); a **slow gentle camera push-in** on the lens axis; no pan, no sit-up, no walk-out, no pull-back; shot 1 keeps looking aside and keeps the feet in frame; shot 2 keeps the gaze and the waist hand and stays crown-to-hips; shot 3 holds the gaze (one slow blink allowed) and keeps hair in the top edge; the **original scene stays stable** every frame. Fall back to `image_to_video` if `reference_to_video` is unavailable.
3. After Gate 1 on each clip, trim **10 + 20 + 20 frames** at 10 fps (1.0 s cover, 2.0 s inner, 2.0 s face) from the portion where idle, wind, and the push-in are all visible. Concatenate full → upper → face, then append **one** copy of the first full-body frame (51 frames; pad only if you must hit 55). That assembled timeline is `$SOURCE_MP4` (`$RUN_DIR/*-source.mp4`).

**Otherwise (Codex or shell-only):** invoke the local `grok` CLI so it loads `$imagine`, verifies `reference_to_video` / `image_to_video`, and produces the MP4:

```zsh
mkdir -p "$RUN_DIR"
grok --single "$PROMPT" --max-turns 8 --permission-mode auto --always-approve \
  --no-alt-screen --output-format plain
```

If no Imagine video tool is available, report `IMAGE_TO_VIDEO_UNAVAILABLE` and stop. Never replace it with zoom, pan, scale, parallax, a slideshow, or another static-image fallback MP4/GIF.

For Motion A, request one locked-camera, 1:1, 6-second source MP4. The generation prompt must name the supplied/edited image, every count of the step-touch choreography, two complete repetitions ending in the exact starting pose no later than 5.4 seconds, the protected 5.4–6.0-second tail, the #888888 background contract when it applies, and the exact output path. For Motion B, name the page still, the held photobook pose, the idle (breath / weight / blink as that shot requires), side wind, slow push-in that does not change shot class, stable original scene, and output path on each of the three calls. Do not rely on camera motion **alone** to simulate animation.

## Gate 1 — Approve the Source Before Converting

Require a nonzero, decodable MP4 with positive duration. Extract and visually compare early, middle, and late frames:

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p "$RUN_DIR/source-check"
ffmpeg -hide_banner -loglevel error -ss 0 -i "$SOURCE_MP4" -frames:v 1 "$RUN_DIR/source-check/early.png"
ffmpeg -hide_banner -loglevel error -ss 3 -i "$SOURCE_MP4" -frames:v 1 "$RUN_DIR/source-check/middle.png"
ffmpeg -hide_banner -loglevel error -ss 5.4 -i "$SOURCE_MP4" -frames:v 1 "$RUN_DIR/source-check/loop-boundary.png"
ffmpeg -hide_banner -loglevel error -ss 5.8 -i "$SOURCE_MP4" -frames:v 1 "$RUN_DIR/source-check/late.png"
```

Reject a zero-byte, incomplete, static, or whole-frame-only scale/translation source.

**Motion A:** inspect enough intermediate frames to confirm two complete four-count cycles before 5.4 seconds: alternating left-right step-touches, soft knee bounces, matching hip shifts, shoulder-height outward/upward forearm pulses, the shoulder counter-roll, and the exact centred reset pose. The hands must remain inside the square and the feet must stay grounded without sliding. The frame at 5.4 seconds must match the first frame in foot placement, hip position, head angle, elbow bend, hand position, and motion follow-through; frames from 5.4 to 6.0 seconds must hold that pose without drift. Reject and regenerate a source with missing or uneven side changes, rigid arms, spins, jumps, travelling, abrupt snaps, or a visible loop jump.

**Motion B:** Gate 1 each 6 s shot **before** trimming. Page pose holds. Original scene stays stable every frame. Mid-clip must show **idle** readable at square framing (breath / weight on shot 1; breath / shoulder or waist-hand on shot 2; blink or breath on shot 3), **wind** in hair/clothes, and a **slow push-in** that is tighter than frame 0 but does **not** change shot class (full body still shows feet; upper still crown-to-hips; face still includes hair). Reject a frozen painting, a full 回身 replayed on every shot, a walk-out, a pull-back, a whip of hair, a push-in so hard that shot 1 becomes MCU, or an ffmpeg zoom. Regenerate the failed shot; do not repair motion with ffmpeg.

When the Motion A default background contract applies, Gate 1 must also confirm a **flat solid #888888 fill**, identical every frame. Reject any cyclorama or floor-to-wall seam, lighting gradient, source-scene remnant, text, logo, prop, cutout halo, colour spill, flickering gray tone, crawling texture, or unstable shadow. For Motion B, reject a scene that morphs, pops, or gets replaced by a flat gray fill the user did not ask for. Regenerate failures with `image_edit` followed by the video tool used for that contract; never repair motion or background failures with ffmpeg. If the MP4 does not materialize, allow one concise Grok continuation naming the image, output path, required tool, and verification; then report failure rather than falling back.

## 3. Render the RT100 Pro GIF

Render a 240x240 GIF at 10 fps, 256 colours, infinite loop, and at most 5.5 seconds. This yields no more than 55 frames, within the RT100 Pro 56-frame limit.

**Motion A:** the sampled frames normally run from 0.0 through 5.4 seconds, so the step-touch completes and holds its reset by 5.4 seconds. The remaining source tail is deliberately trimmed here.

```zsh
ffmpeg -hide_banner -loglevel error -t 5.5 -i "$SOURCE_MP4" \
  -filter_complex "[0:v]fps=10,scale=240:240:flags=lanczos,split[frames][palette_source];[palette_source]palettegen=max_colors=256:stats_mode=diff[palette];[frames][palette]paletteuse=dither=sierra2_4a" \
  -loop 0 "$OUTPUT_GIF"
```

**Motion B:** do not run a single `-t 5.5` over one 6 s clip. From each approved shot, extract 10 fps 240×240 frames covering idle + wind + push-in: **10** from full-body, **20** from upper, **20** from face (1.0 + 2.0 + 2.0 s). Concatenate full-body, then upper-body, then face, then **one** copy of the first full-body frame (51 frames). Palette-GIF that sequence (`loop=0`). Do not time-stretch with `setpts`. Hard cuts only. Never add the push-in in ffmpeg.

Prefer regenerating the source video when the loop visibly jumps. Do not depend on a fragile post-production crossfade to conceal a bad animation seam.

## Gate 2 — Approve the Delivery GIF

Run the bundled verifier and independently inspect representative frames at actual screen size:

```zsh
VERIFY=""
for p in \
  "$HOME/.grok/skills/generating-rt100pro-gifs/scripts/verify_rt100pro_gif.py" \
  "$HOME/.codex/skills/generating-rt100pro-gifs/scripts/verify_rt100pro_gif.py"; do
  [ -f "$p" ] && VERIFY="$p" && break
done
python3 "$VERIFY" "$OUTPUT_GIF"
ffprobe -v error -show_entries format=format_name,duration,size:stream=codec_name,width,height,nb_frames,avg_frame_rate \
  -of default=noprint_wrappers=1 "$OUTPUT_GIF"
```

Deliver only when the verifier passes, the file is GIF data, it is 240x240 with 56 or fewer frames and `loop=0`, its endpoint is visually clean, and the display-sized frames remain legible. The first-to-last transition must not jump.

**Motion A:** representative delivery frames must make the alternating step-touch, knee bounce, hip shift, shoulder-height forearm pulse, shoulder accent, and exact centred reset readable at display size.

**Motion B:** the GIF must contain three distinct square photobook framings in order (standing full-body cover looking aside, standing upper-body inner page looking at the camera, standing face close-up). A mid-shot frame in each must show idle plus wind, and a slightly tighter crop than that shot's first frame. First and last frames must be the same full-body start (the bookend).

When the Motion A default background applies, also confirm that the #888888 fill stays flat and clean after palette conversion, and that the subject edge stays clean. State the final path, duration, frame count, and file size. Upload with the RT100 Pro connected by cable through the current EPOMAKER driver.

## 4. Mandatory Post-Delivery Cleanup

After Gate 2 passes, clean up the current run before reporting completion.

**Motion A — keep two files** in `$RUN_DIR`:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified RT100 Pro GIF, named `*-rt100pro.gif`.

**Motion B — keep five files** in `$RUN_DIR`:

- the three 6 s per-shot clips, named `*-cover.mp4`, `*-upper.mp4`, and `*-face.mp4` (do **not** delete these);
- the assembled source video, named `*-source.mp4`;
- the final verified RT100 Pro GIF, named `*-rt100pro.gif`.

Delete every other resource created for that run: square reference images, `*-cover` / `*-inner` / `*-face` stills (not the `.mp4` shot clips), source-check frames, contact sheets, loop-assemble PNG folders, temporary downloads or copies, failed candidate MP4/GIF files, loop-duration diagnostics, and other conversion artifacts. Use an explicit per-run manifest or staging list; never use a broad wildcard or recursive deletion that could remove unrelated historical deliverables or sibling `$RUN_DIR` folders. Do not clean up until the final GIF passes Gate 2. If cleanup would affect an ambiguous or unrelated file, stop and resolve the target rather than deleting it.

Verify after cleanup that the retained files are nonzero and still present, and that the final GIF still passes the bundled verifier. The final handoff lists those retained files only.
