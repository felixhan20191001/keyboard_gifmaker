# Six-Panel Anime RT100 Pro GIF Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a verified three-second RT100 Pro looping GIF from the approved interval of the supplied square MP4.

**Architecture:** Copy the approved source into the delivery directory, validate it, and make a temporary full-length display-size GIF for conversion review. Render the approved interval directly from the MP4 with an optimised palette, verify metadata and representative frames, then remove only the explicitly named current-run temporary files.

**Tech Stack:** ffmpeg, ffprobe, bundled Python RT100 Pro GIF verifier.

## Global Constraints

- Input: `/Users/hanpengfei/Downloads/grok-video-ff69830c-b11d-498b-ae7d-65ced10494b6.mp4`.
- Retained source: `output/rt100pro/six-panel-anime-source.mp4`.
- Delivery: `output/rt100pro/six-panel-anime-rt100pro.gif`.
- Selection: `2.9-5.9` seconds, for a three-second animation.
- Output: 240x240, 10fps, up to 256 colours, infinite looping, about 30 frames.
- Preserve the square six-panel composition and render directly from the MP4 without audio.
- Retain only the named source MP4 and final GIF from this run after verification.

---

### Task 1: Prepare and approve the source

**Files:**
- Create: `output/rt100pro/six-panel-anime-source.mp4`
- Create temporarily: `output/rt100pro/six-panel-anime-full-preview.gif`
- Create temporarily: `output/rt100pro/source-check/six-panel-anime-early.png`
- Create temporarily: `output/rt100pro/source-check/six-panel-anime-middle.png`
- Create temporarily: `output/rt100pro/source-check/six-panel-anime-late.png`

**Interfaces:**
- Consumes: the user-supplied MP4.
- Produces: a retained, validated source MP4 and an approved full-length conversion preview for Task 2.

- [ ] **Step 1: Confirm the source and destination do not alias**

Run `realpath` on the input and destination parent, and confirm the input is outside `output/rt100pro/`.

- [ ] **Step 2: Copy the source to the retained delivery name**

```zsh
mkdir -p output/rt100pro/source-check
cp -p /Users/hanpengfei/Downloads/grok-video-ff69830c-b11d-498b-ae7d-65ced10494b6.mp4 output/rt100pro/six-panel-anime-source.mp4
```

- [ ] **Step 3: Validate the retained source and extract Gate 1 frames**

```zsh
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 output/rt100pro/six-panel-anime-source.mp4
ffmpeg -hide_banner -loglevel error -ss 0 -i output/rt100pro/six-panel-anime-source.mp4 \
  -frames:v 1 output/rt100pro/source-check/six-panel-anime-early.png
ffmpeg -hide_banner -loglevel error -ss 3 -i output/rt100pro/six-panel-anime-source.mp4 \
  -frames:v 1 output/rt100pro/source-check/six-panel-anime-middle.png
ffmpeg -hide_banner -loglevel error -ss 5.8 -i output/rt100pro/six-panel-anime-source.mp4 \
  -frames:v 1 output/rt100pro/source-check/six-panel-anime-late.png
```

Accept only if the source is nonempty, decodable, square, and visibly changes across the representative frames without losing the six-panel composition.

- [ ] **Step 4: Render and inspect the temporary full-length GIF**

```zsh
ffmpeg -hide_banner -loglevel error -i output/rt100pro/six-panel-anime-source.mp4 \
  -filter_complex "[0:v]fps=10,scale=240:240:flags=lanczos,split[frames][palette_source];[palette_source]palettegen=max_colors=256:stats_mode=diff[palette];[frames][palette]paletteuse=dither=sierra2_4a" \
  -loop 0 output/rt100pro/six-panel-anime-full-preview.gif
```

Confirm that it is decodable GIF data and that motion remains readable at 240x240.

### Task 2: Render, verify, and clean the delivery

**Files:**
- Create: `output/rt100pro/six-panel-anime-rt100pro.gif`
- Create temporarily: `output/rt100pro/source-check/six-panel-anime-selected-early.png`
- Create temporarily: `output/rt100pro/source-check/six-panel-anime-selected-middle.png`
- Create temporarily: `output/rt100pro/source-check/six-panel-anime-selected-late.png`
- Retain: `output/rt100pro/six-panel-anime-source.mp4`
- Retain: `output/rt100pro/six-panel-anime-rt100pro.gif`

**Interfaces:**
- Consumes: the approved source from Task 1 and the approved `2.9-5.9` second interval.
- Produces: the verified RT100 Pro GIF and exactly two retained current-run files.

- [ ] **Step 1: Render the selected interval directly from the MP4**

```zsh
ffmpeg -hide_banner -loglevel error -ss 2.9 -t 3.0 \
  -i output/rt100pro/six-panel-anime-source.mp4 \
  -filter_complex "[0:v]fps=10,scale=240:240:flags=lanczos,split[frames][palette_source];[palette_source]palettegen=max_colors=256:stats_mode=diff[palette];[frames][palette]paletteuse=dither=sierra2_4a" \
  -loop 0 output/rt100pro/six-panel-anime-rt100pro.gif
```

- [ ] **Step 2: Run the delivery verifier and independent metadata check**

```zsh
python3 /Users/hanpengfei/.codex/skills/generating-rt100pro-gifs/scripts/verify_rt100pro_gif.py \
  output/rt100pro/six-panel-anime-rt100pro.gif
ffprobe -v error \
  -show_entries format=format_name,duration,size:stream=codec_name,width,height,nb_frames,avg_frame_rate \
  -of default=noprint_wrappers=1 output/rt100pro/six-panel-anime-rt100pro.gif
```

Expected: verifier pass, GIF data, 240x240, 10fps, infinite loop, and no more than 30 frames for the approved interval.

- [ ] **Step 3: Extract and visually inspect representative delivery frames**

```zsh
ffmpeg -hide_banner -loglevel error -ss 0 -i output/rt100pro/six-panel-anime-rt100pro.gif \
  -frames:v 1 output/rt100pro/source-check/six-panel-anime-selected-early.png
ffmpeg -hide_banner -loglevel error -ss 1.5 -i output/rt100pro/six-panel-anime-rt100pro.gif \
  -frames:v 1 output/rt100pro/source-check/six-panel-anime-selected-middle.png
ffmpeg -hide_banner -loglevel error -ss 2.9 -i output/rt100pro/six-panel-anime-rt100pro.gif \
  -frames:v 1 output/rt100pro/source-check/six-panel-anime-selected-late.png
```

Accept only if faces remain legible, the six vertical panels remain stable, motion is visible, and the final-to-first transition is acceptable at 240x240.

- [ ] **Step 4: Remove only the explicit current-run temporary files**

Move these seven named files to the Trash after verification: the full preview GIF, the three Gate 1 PNGs, and the three delivery PNGs. Also move any failed current-run candidate by its exact name if one is created during execution. Do not use a wildcard or recursive deletion.

- [ ] **Step 5: Re-run verification after cleanup**

```zsh
test -s output/rt100pro/six-panel-anime-source.mp4
test -s output/rt100pro/six-panel-anime-rt100pro.gif
python3 /Users/hanpengfei/.codex/skills/generating-rt100pro-gifs/scripts/verify_rt100pro_gif.py \
  output/rt100pro/six-panel-anime-rt100pro.gif
```

Expected: both retained deliverables are nonempty and the verifier still passes.
