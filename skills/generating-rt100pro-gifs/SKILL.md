---
name: generating-rt100pro-gifs
description: >
  Create, animate, convert, or optimize a GIF for the EPOMAKER RT100 Pro keyboard
  screen from a reference image or video. Use for keyboard mini-screen GIFs,
  Grok Imagine image_to_video animation, loop dance source MP4s, 240x240 delivery
  GIFs, RT100 Pro upload-ready media, or when the user runs /generating-rt100pro-gifs.
---

# Generating RT100 Pro GIFs

For every RT100 Pro request, follow this fixed pipeline in order: prepare the reference, make or accept a real MP4, approve the source animation, render the GIF, approve the delivery file, then perform mandatory post-delivery cleanup. The user may override motion, framing, duration, or mood, but never the source-video and final-file quality gates or the final cleanup requirement.

## 1. Prepare the Reference and Motion

Inspect the supplied image or video. If neither is supplied, ask for one. Keep all intermediates and final files in `output/rt100pro/`; name the source `*-source.mp4` and final `*-rt100pro.gif`.

Use every explicit motion instruction. Otherwise, make this the complete default motion contract for every human or humanoid character: a natural, sensual loop dance with both hands kept continuously above the head and fully inside the square frame. Keep the overhead silhouette soft and lifelike—elbows slightly bent rather than a stiff Y-pose, arms framing the face, wrists rolling in small alternating languid pulses, and fingers loosely open or gently curling instead of locked. Drive the body with a smooth even left-right weight shift, a fluid waist-and-hip sway (soft figure-eight or slow hip roll), a subtle torso/ribcage undulation that follows the beat, a soft shoulder roll, a gentle knee bounce, and a light head tilt or nod. Prefer continuous, physically plausible follow-through over abrupt pose snaps: hair, clothing, cape, jewelry, wings, tails, flames, or particles lag a half-beat behind the body as secondary motion. For clearly adult characters, keep the mood flirtatious and body-aware—slow confident rhythm, readable hip and waist emphasis, relaxed breathing through the chest and shoulders—while remaining tasteful and non-explicit. For childlike or age-ambiguous subjects, keep the same overhead-hands geometry and loop structure but switch the mood to playful/cute only (no sensual styling). The dance must stay rhythmic with deliberate even left-right timing; no dropped hands, no limbs leaving the square frame, and no camera-only fake motion. Begin and end in the same centred upright overhead-hands pose, with matching hand placement, elbow bend, and follow-through, so the movement loops cleanly. Include every listed beat in the Grok prompt unless the user explicitly requests different motion. Preserve identity, anatomy, outfit, and mood. Keep the camera locked unless the user asks otherwise.

For the 1.54-inch screen, prioritize the face, upper torso, hands, and a distinctive prop/effect. Avoid unreadable full-body framing, text, or logos unless requested.

## 2. Produce the Source MP4 through Local Grok Imagine

If the user supplies a usable MP4, use it as `$SOURCE_MP4` and start at Gate 1. Otherwise generate a real animated source with Imagine `image_to_video`. Do not substitute a nonexistent `imagine-video` command or a still-image animation.

**Preferred in a Grok Build / Grok TUI session:** call the native `image_to_video` tool directly (and `image_edit` first when a square overhead-pose reference is needed). Copy the resulting MP4 to `output/rt100pro/*-source.mp4`.

**Otherwise (Codex or shell-only):** invoke the local `grok` CLI so it loads `$imagine`, verifies `image_to_video`, and produces the MP4:

```zsh
mkdir -p output/rt100pro
grok --single "$PROMPT" --max-turns 8 --permission-mode auto --always-approve \
  --no-alt-screen --output-format plain
```

If `image_to_video` is unavailable, report `IMAGE_TO_VIDEO_UNAVAILABLE` and stop. Never replace it with zoom, pan, scale, parallax, a slideshow, or another static-image fallback MP4/GIF. For a non-square image, use Imagine image editing to make a square source frame that retains the face and upper torso before animating it. When the default overhead-hands contract applies and the reference does not already show both hands above the head, edit that square overhead-pose frame first, then animate from the edited frame.

Request one locked-camera, 1:1, 6-second source MP4. The generation prompt must name the supplied/edited image, required visible subject motion (every default loop-dance beat when no user motion is supplied), loop seam (begin and end in the same centred overhead-hands pose), and the exact output path. Do not rely on camera motion to simulate animation.

## Gate 1 — Approve the Source Before Converting

Require a nonzero, decodable MP4 with positive duration. Extract and visually compare early, middle, and late frames:

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p output/rt100pro/source-check
ffmpeg -hide_banner -loglevel error -ss 0 -i "$SOURCE_MP4" -frames:v 1 output/rt100pro/source-check/early.png
ffmpeg -hide_banner -loglevel error -ss 3 -i "$SOURCE_MP4" -frames:v 1 output/rt100pro/source-check/middle.png
ffmpeg -hide_banner -loglevel error -ss 5.8 -i "$SOURCE_MP4" -frames:v 1 output/rt100pro/source-check/late.png
```

Reject a zero-byte, incomplete, static, or whole-frame-only scale/translation source. When the default loop-dance contract applies, the early, middle, and late frames must confirm that both hands remain above the head with a natural soft elbow bend (not a rigid stick-figure Y-pose), and that the languid wrist rhythm, even left-right weight shift, shoulder roll, torso/ribcage undulation, and waist-and-hip sway are visible and continuous. Reject and regenerate a source where hands drop, arms look stiff or frozen, the left-right timing is erratic, the hip/waist motion is missing, or the motion snaps abruptly. Regenerate it with `image_to_video`; never repair it with ffmpeg. If the MP4 does not materialize, allow one concise Grok continuation naming the image, output path, required tool, and verification; then report failure rather than falling back.

## 3. Render the RT100 Pro GIF

Render a 240x240 GIF at 10 fps, 256 colours, infinite loop, and at most 5.5 seconds. This yields no more than 55 frames, within the RT100 Pro 56-frame limit. The 6-second Imagine source is deliberately trimmed here.

```zsh
ffmpeg -hide_banner -loglevel error -t 5.5 -i "$SOURCE_MP4" \
  -filter_complex "[0:v]fps=10,scale=240:240:flags=lanczos,split[frames][palette_source];[palette_source]palettegen=max_colors=256:stats_mode=diff[palette];[frames][palette]paletteuse=dither=sierra2_4a" \
  -loop 0 "$OUTPUT_GIF"
```

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

Deliver only when the verifier passes, the file is GIF data, it is 240x240 with 56 or fewer frames and `loop=0`, its endpoint is visually clean, and the display-sized frames remain legible. When the default motion applies, representative delivery frames must also retain the natural overhead-hands pose (soft elbows, hands fully above the head) and make the languid wrist pulse, shoulder roll, waist/hip sway, and even left-right rhythm readable at display size. State the final path, duration, frame count, and file size. Upload with the RT100 Pro connected by cable through the current EPOMAKER driver.

## 4. Mandatory Post-Delivery Cleanup

After Gate 2 passes, clean up the current run before reporting completion. Keep exactly these two current-run deliverables in `output/rt100pro/`:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified RT100 Pro GIF, named `*-rt100pro.gif`.

Delete every other resource created for that run: square reference images, source-check frames, contact sheets, temporary downloads or copies, failed candidate MP4/GIF files, loop-duration diagnostics, and other conversion artifacts. Use an explicit per-run manifest or staging list; never use a broad wildcard or recursive deletion that could remove unrelated historical deliverables. Do not clean up until the final GIF passes Gate 2. If cleanup would affect an ambiguous or unrelated file, stop and resolve the target rather than deleting it.

Verify after cleanup that both retained files are nonzero and still present, and that the final GIF still passes the bundled verifier. The final handoff for each run must list only the retained source MP4 and final GIF.
