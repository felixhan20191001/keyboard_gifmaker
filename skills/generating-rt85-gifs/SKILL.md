---
name: generating-rt85-gifs
description: >
  Create, animate, convert, or optimize a GIF for the EPOMAKER RT85 keyboard
  1.47-inch landscape rectangular TFT screen from a reference image or video.
  Use for RT85 mini-screen GIFs, Grok Build `reference_to_video` (native loop via first_frame=last_frame)
  animation, landscape loop source MP4s, recumbent micro-act GIFs, three-shot
  recumbent editorial GIFs, prone calf-swing GIFs, 320x172 delivery GIFs, RT85
  upload-ready media, or when the user runs /generating-rt85-gifs.
---

# Generating RT85 GIFs

For every RT85 request, follow this fixed pipeline in order: **ask which motion contract to use** (unless already named); inspect the supplied still; **if it is not a 16:9 still that matches the chosen contract, first generate that still** (Motion A: match pose-ref mid-recline crop, not necessarily full-body — **no background requirement**; Motion B/C still need full-body for their contracts); prepare the stills for the chosen contract; make or accept a real landscape MP4; approve the source animation, render the GIF, approve the delivery file, then perform mandatory post-delivery cleanup. The user may override motion, framing, duration, mood, or background, but never the source-video and final-file quality gates or the final cleanup requirement.

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
| Frame rate | **10 fps** (100 ms/frame) | Looping 6 s source: even-sample, ~8.5 fps; delays 100–120 ms |
| Max frames | **51** | **Hard cap.** Never deliver more |
| Duration | **dynamic** | Follow the kept window. Do not force 6.0 s or 5.1 s |
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

This skill has **three default motion contracts**. They are separate. Never mix them in one clip. Never use the RT100 Pro standing step-touch or standing 回身 here.

If the user has not already named a motion, **stop and ask before any `image_edit` or video call**. Present exactly these three options, in the user's language, and wait:

1. **Recumbent micro-act / 横卧微动** — one locked-camera 16:9 shot matching `skills/generating-rt85-gifs/refs/motion-a-recline-pose-ref.png` **composition + pose** (mid-recline crop is OK — **not required to show full body / feet**); chin-hand recline still; video is a **subtle head-turn + soft smile cycle** (pose already locked by the still — video prompt writes **deltas only**). Far/lower legs may exit the right frame edge.
2. **Three-shot recumbent editorial** — three hard-cut **landscape** photobook pages in a **supermodel recline**, still lying down: recumbent full-body cover, recumbent upper-body inner page, recumbent face close-up. Each shot holds its pose; hair and clothes blow in a side wind; every shot does a slow camera push-in.
3. **Prone calf-swing / 趴卧摇腿** — one locked **side-camera** 16:9 full-body shot; she lies **prone on her stomach** on the ground; calves kick playfully back and forth; the upper body stays in **simple continuous motion** (forearm weight shift, slight head turn, tiny shoulder roll) then settles back — it must **not look frozen**; **facial expression changes**; **native loop** by pinning the **same** `$FULLBODY_STILL` as both `first_frame` and `last_frame` on `reference_to_video` (no timed 0.4 s / 5.4 s reset).

Do not pick one silently. Do not start generating until they choose. Skip the question only when they already named one of these (选项 A / 横卧微动 / 对镜浅笑 / Motion A, or legacy 勾手 / come-hither → still use A still pose but prefer the new micro-act video unless they insist on curl; or 回眸 / 三镜头 / glance / 写真; or 趴卧 / 摇腿 / 趴着 / prone / calf-swing), or gave a different explicit motion (that explicit motion still overrides all three).

### Recumbent still first

All three contracts **show the figure lying across the wide screen**. Before any video call, `$FULLBODY_STILL` must be a **16:9** still of the **same character** in that contract's pose (**Motion A:** pose-ref mid-recline crop is enough; **Motion B/C:** still require full-body for their contracts).

- **Usable already (A):** framing and pose **highly match** `refs/motion-a-recline-pose-ref.png` — head left, body extending right, typically cropped around mid/upper thighs (feet **not** required); head, hair, both hands, torso, and the visible near thigh are in frame; **Motion A chin-hand recline** (torso and hips twisted toward the camera, supporting elbow on the ground with that hand under the chin, free hand on the upper thigh/hip (home pose)); far/lower leg may straighten and exit the right edge; landscape 16:9. **No background requirement** (keep source scene, pose-ref scene, or any clean backdrop — do not force #888888).
- **Usable already (B):** head, hair, both hands, torso, legs, and feet (plus cape, tail, or other attached props) are all visible with small margins, the figure is in the **supermodel side-recline** (head one side, feet the other), and the frame is landscape. Motion B has **no background restriction** — keep the source environment.
- **Usable already (C):** the same full-body completeness in landscape, but she is **lying prone on her stomach**, seen from a **side camera**, knees bent, **calves already lifted**, **facing the camera**, and **looking at the camera**. Do not accept an A/B side-recline, an overhead bird's-eye, calves lying flat, a profile head, or a gaze that looks away as Motion C's still.
- **Not usable:** standing, seated, chest-up MCU that loses the hip/thigh hand, portrait crop, or the figure is tiny in a wide empty frame. **Motion B/C:** also reject half-body / missing feet when their contracts need full-body. **Motion A:** do **not** reject for missing feet or mid-thigh crop if the pose-ref composition matches; do **not** reject on background (any backdrop OK). **Do not animate this crop.** First generate a new **16:9** illustration of the **same character** with `image_edit` (preferred in Grok Build). Pass the reference **twice** so 16:9 is honored. Preserve exact face, hair, outfit, **body type**, and style. Motion A: match pose-ref composition + chin-hand recline (not Motion B's supermodel recline); lower legs may exit frame; **do not force a background change**. Motion B: keep the source background; complete full-body as before. Motion C: use the prone side-view full-body pose below, not the A/B recline.

**Pose + composition (required, Motion A) — chin-hand recline (Felix 2026-09-15):** match **both** the body language **and the framing** of `refs/motion-a-recline-pose-ref.png` on a **16:9** canvas. **Full body / feet are NOT required.** Prefer the pose-ref mid-recline crop: head + hair + both arms + torso + near hip/thigh fill the frame; lower/far leg may straighten and **exit the right edge**. She lies across the screen with **head toward the left** and body extending **right**, but this is **not** a pure side silhouette: **torso and hips twist toward the camera** so the chest and near thigh read clearly. **Supporting arm:** the near/down elbow rests on the ground; that hand is lightly **under the chin** (chin rest), framing the face. **Free arm:** hand rests on the **upper thigh / hip** in the home pose. **Legs:** softly bent where visible; the near thigh sits more forward / prominent; far leg may be straighter and clipped by the frame. Eyes **open**, looking at the camera. **Background: no requirement** — keep whatever backdrop fits (source scene, pose-ref scene, or neutral fill); do not force #888888. Never overhead. Never two locked arms pushing the torso up. Do not put a staff, weapon, or other prop in the free hand; omit it unless the user asked to keep it. Do **not** use Motion B's tucked-elbow supermodel recline or Motion C's prone calf-lift as Motion A's still.

**Pose-ref on every Motion A still (required):** whenever generating or fixing a Motion A `$FULLBODY_STILL` / face still (or a legacy curl still if requested), **always** pass `refs/motion-a-recline-pose-ref.png` as an extra reference image together with the character reference — via Grok Build `image_edit` / `image_gen` (pass character reference twice when aspect must be locked). Use the pose-ref for **body language / hand placement / hip twist only**; lock face, hair, outfit, and body type to the **character** reference. Never invent Motion A pose from text alone when this file is available.

**Pose (required, Motion B):** keep the original **Vogue supermodel editorial recline** on her side, **head at the left** of the frame and **feet at the right**, entire figure from hair/crown to feet with **small margins**. She lies in the source scene; no background swap. Weight rests on the down hip and thigh; torso stays close to the ground. She props on the **down-side elbow only**, forearm tucked close to the ribs. Long S-curve through the spine. Bottom leg extended toward the feet; top knee softly bent. The free hand rests on the waist. Never overhead. Never two locked arms pushing the torso up. **Motion C:** do not use either A or B recline; use the prone side-view pose in Motion C.

**Background:** **Motion A:** **no requirement** — do not force #888888 or strip the scene. Keep source / pose-ref / any clean backdrop unless the user asks to change it. **Motion B:** no background restriction. Keep the source environment. **Motion C:** a simple floor that reads as ground from the side. Do not require #888888. Do not keep a busy original scene unless the user asked.

**Garment physics (required):** skirts, gowns, sashes, and capes **cover the hips and the tops of the thighs**, then **pool on the ground by gravity** in natural folds (Motion A: whatever ground/backdrop is in the still). Do not wedge fabric between the legs so it reads as shorts, a leotard, or a bikini. A high slit may show a lower thigh if the source costume already has one.

Inspect the new still: if feet, head, or hands are missing, the gown is bunched as underwear, a staff is still in a free near hand, she is hovering on two straight arms, or identity drifted, edit once more. Motion A: also reject a pose that is not the **chin-hand recline** (missing chin-rest support hand, free hand not on thigh/hip, pure side silhouette with hips not twisted toward camera, or a Motion B tucked-elbow supermodel recline). Motion B: also reject a pose that is not the supermodel recline. Motion C: also reject a pose that is not prone with calves lifted, a camera that is not a side view, a profile head, or a face that is not turned toward the camera. Motion A: do **not** reject on background. Motion B: do not reject the original scene. Motion C: do not reject a simple dark floor. Only then set `$FULLBODY_STILL` to this generated file.

Never call a video tool on a crop that fails the chosen contract (Motion A: pose-ref mid-recline OK; Motion B/C: need full-body). Never invent a different character. Do not slim, enlarge, or restyle the body when the user asked to keep the reference unchanged.

### Landscape composition (required)

Because the RT85 panel is a **wide horizontal rectangle**, not a square, **do not reuse RT100 Pro square standing framing**, and **do not** treat a chest-up MCU as the only shot of Motion A.

- Compose every still and clip for **landscape** (target aspect **16:9**, final scale **320×172**).
- Do **not** keep the figure tiny inside a wide empty frame.
- Avoid RT100 Pro overhead-arm poses and standing full-body 回身.
- Motion C stays a **side-view full body** for the whole clip; do not treat a chest-up as the shot.

### Motion A — Recumbent micro-act / 横卧微动（Felix 2026-09-15）

Use this contract only after the user chose it (or named equivalent motion such as 横卧微动 / 对镜浅笑 / Motion A; legacy 勾手／come-hither still maps here for the **still**, but the **default video** is the micro-act below unless they explicitly demand the old index-finger curl).

#### Still (pose lock — do this first)

`$FULLBODY_STILL` is the **Motion A chin-hand recline** home pose (see pose section + `refs/motion-a-recline-pose-ref.png`). Pixel-crop `*-face.png` into 16:9 (hair inside the top edge, chin / neckline in the lower third; the support hand under the chin may stay in frame). Do **not** default to `image_edit` for this crop: a redraw often changes the face. If the source has alpha, composite onto a solid fill sampled from the still's backdrop (any color OK — do not force #888888). Only use `image_edit` if a crop cannot reach 16:9 without cutting the subject; then pass the still twice so 16:9 is honored, and reject the result if identity drifted.

**Do not require `*-curl.png` for the default Motion A video.** (Only make a curl still if Felix explicitly asks for the legacy come-hither finger cycle.)

The chin-hand-recline still (pose-ref mid-crop OK) is the **loop start and end**. Do not start the clip on a feet close-up.

#### Video prompt rule (required)

The still already locks recline / chin-rest / framing. The Imagine **video prompt must NOT re-describe that pose from scratch**. Write **deltas only**:

1. Camera lock + anti-drift (no stand-up / no big pose change / keep the still's crop)
2. Primary action timeline
3. Secondary motion (breath / hair)
4. Loop back to the still (first≈last)

#### Default Motion A action (~6 s loop)

- **~0–1 s:** hold the still (chin-rest + thigh/hip home hand).
- **~1–3 s:** head yaws slightly so she faces the camera more directly; lips go neutral → soft smile; free hand may slide a little up the thigh; tiny torso weight shift.
- **~3–5 s:** smile eases back to neutral; head returns toward the still's starting angle.
- **~5–6 s:** settle on the exact still pose for loop close.

**Camera:** stay on the exact 16:9 crop of `$FULLBODY_STILL` for the whole ~6 s. No zoom, no pan, no standing up. First frame matches last.

**Supporting motion:** subtle hair sway with the head turn, light breath. Motion must stay **readable at 320×172** but **restrained** — face/head carry the beat, not a big arm flourish. No overhead arms, jumps, or walk-out. Preserve identity, anatomy, outfit, body type.

**Loop (required — Grok Build):** `reference_to_video` with `first_frame`=`last_frame`=`$FULLBODY_STILL`. No timed 5.4 s pose-reset requirement for the default micro-act.

**Default Imagine `final_prompt` template (English; paste into the plan / `reference_to_video` prompt):**

```text
Use the uploaded still as composition + identity lock. Call reference_to_video with first_frame and last_frame BOTH set to this exact still (perfect loop).
Do NOT re-pose the body — keep the still's recline, chin-rest hand, framing, outfit, and background.
CAMERA LOCK: exact same 16:9 mid-recline crop for the whole clip. NO zoom, NO pan, NO stand-up.
PRIMARY (~6s): 0–1s hold; 1–3s slight head yaw to face camera + soft smile + tiny free-hand slide up the thigh + tiny torso weight shift; 3–5s smile fades to neutral + head returns toward start angle; 5–6s settle on the still for loop.
SECONDARY: subtle hair sway / breath only — keep it restrained; readable at 320×172 via face/head, not big arm flourishes.
Eyes open. Preserve exact face and outfit from the still.
```

For childlike or age-ambiguous subjects, keep the same micro head-turn but use a smaller, friendlier smile (no inviting curl).

Reject a still-image pan, zoom, scale, or parallax made in ffmpeg. The video call must see `$FULLBODY_STILL` as an image.

### Motion B — Three-shot recumbent editorial

Use this contract only after the user chose it (or named equivalent motion such as 回眸 / 三镜头 / glance / 写真).

Do **not** stand the figure up. Do **not** copy RT100 Pro's square standing 回身. The GIF plays **three hard-cut 16:9 photobook pages**, then loops. Hold the **supermodel recline** from `$FULLBODY_STILL` on every page. Drama is the **cut between poses**, not the same 回眸 three times. Inside each shot the pose **holds**; a **gentle side wind** moves hair and clothes; a **slow camera push-in** runs on **every** shot, including the first two, the same way the face page already feels closer.

1. **Cover — recumbent full body** (~1.6 s in the GIF) — head left, feet right, figure filling the wide frame (same crop as `$FULLBODY_STILL`). Supermodel recline: down-elbow tucked, free hand on the waist, top knee bent. She looks **toward her feet**. Wind in the hem, cape, and hair ends.
2. **Inner page — recumbent upper body** (~1.7 s) — 16:9 window from crown to hips; face, shoulders, and the waist hand readable at 320×172. Same recline; she looks at the camera; the free hand stays on the waist as a held editorial gesture. Wind in hair and sleeve/gown folds.
3. **Close-up — recumbent face** (~1.7 s) — 16:9 (hair inside the top edge, chin / neckline in the lower third). Direct gaze held. Wind in hair strands and earrings; one slow blink is allowed **mid-shot**. **The last frame of this 1.7 s face trim must show eyes open** — never end the face page on a closed blink.

Do not repeat a full 回眸 on every shot. Do not mix in the come-hither curl. She does not sit up, stand, crawl, or spin. Hips and feet stay planted. Wind is continuous and light — readable at 320×172, never a hair whip.

**Push-in (required on all three shots):** native Imagine slow dolly/push-in along the lens axis. Keep it small so the **shot class does not change**: shot 1 still shows heels at the end of the 1.6 s trim; shot 2 still reads crown-to-hips at the end of 1.7 s; shot 3 keeps hair in the top edge and chin/neckline in frame. No pan. No pull-back. **Never** fake the push-in with an ffmpeg zoom, scale, crop-pan, Ken Burns, or parallax.

From `$FULLBODY_STILL` (cover pose, looking toward the feet), `image_edit` one **inner** still of the same recumbent figure: eyes on camera, waist hand held, same garment coverage, **same background as `$FULLBODY_STILL`** (do not replace it with #888888). Prefer **pixel-crop** `*-upper` and `*-face` from that inner still. Use `image_edit` for those crops only if a 16:9 window cannot cover crown-to-hips or the face without cutting the subject; then pass the still twice, 16:9, and reject identity drift.

Because a face close-up cannot match a full-body first frame, **bookend the assembled GIF with a copy of the first full-body frame** as the last frame so the loop returns to the cover. Do not crossfade the cuts.

### Motion C — Prone calf-swing / 趴卧摇腿

Use this contract only after the user chose it (or named equivalent motion such as 趴卧 / 摇腿 / 趴着 / prone / calf-swing).

Do **not** use the A/B supermodel side-recline. Do **not** mix in the come-hither curl or the three-shot cuts. Do **not** use an overhead bird's-eye. She lies **prone on her stomach** on the ground, photographed from a **locked side camera**, entire figure from crown to boots filling the 16:9 frame: **head at the left, feet at the right**.

**Still:** `$FULLBODY_STILL` is that side-view prone full body. Knees stay bent and **both calves are already lifted** as the loop-home pose. The **head is turned toward the camera** so she **faces the viewer** (three-quarter or more, not a profile looking along the body). Eyes are **open and looking at the camera**; expression is a small playful smile. Forearms rest on the floor — not two locked arms pushing the torso up. The still is the **loop start and end**.

**Camera:** stay on the exact 16:9 side-view full-body composition of `$FULLBODY_STILL` for the whole 6 s. No zoom, no pan, no push-in, no pull-back, no standing the figure up.

**Legs:** the bent calves and boots kick **playfully back and forth** in a regular cute idle. The swing must be **visible at 320×172**. Hips stay on the floor. She does not crawl, sit up, stand, or dance.

**Face:** expression **changes** mid-clip and is readable at 320×172 — a shifting smile, a playful beat — not a frozen mask. Eyes stay open (a brief mid-clip blink is allowed). Do **not** require a timed face return by 5.4 s — the API first=last still closes the loop.

**Upper body:** **simple continuous motion**, not a freeze and not a big pose change. Cycle: a forearm weight shift, a slight head turn, a tiny shoulder roll, then she settles back. Hands stay on the floor. The torso must **not look static** at 320×172. Stay prone.

**Loop (required — Grok Build):** call **`reference_to_video`** with `first_frame` and `last_frame` both set to the **same** `$FULLBODY_STILL` absolute path (perfect loop). Do **not** use `image_to_video` alone to fake a loop. Do **not** require a 0.4 s start hold or a timed return by 5.4 s — write **mid-clip action only**. When burning the GIF, **even-sample** the whole source into **≤51 frames** (fill the keyboard frame budget uniformly — do not skip frames irregularly; do not rely on `search_rt85_loop` as the primary path). Do not generate an open-ended clip. Do not fake the seam by copying the first frame onto the last or by fading.

For clearly adult characters, keep the mood playful and cute rather than come-hither. For childlike or age-ambiguous subjects, keep the same prone camera and calf-swing; keep the upper-body motion even smaller.

Reject a still-image pan, zoom, scale, or parallax made in ffmpeg. The video call must see `$FULLBODY_STILL` as an image.

## 2. Produce the Source MP4 through Local Grok Imagine

If the user supplies a usable MP4, use it as `$SOURCE_MP4` and start at Gate 1. Otherwise generate a real animated source with Imagine. Do not substitute a nonexistent `imagine-video` command or a still-image animation.

**Preferred in a Grok Build / Grok TUI session:**

1. Resolve `$FULLBODY_STILL` as above. If the user image was not a 16:9 full-body still that matches the chosen contract, this **must** be the newly generated still, not the original crop.

**Motion A (native loop — Grok Build):** Pixel-crop `*-face.png`. **Do not** make `*-curl.png` unless Felix asks for legacy come-hither. Call **`reference_to_video`** (16:9, ~6 s). **Required params:** `first_frame` and `last_frame` both set to the **same** `$FULLBODY_STILL` path (perfect loop). You may also pass `$FULLBODY_STILL` / face in `images` for identity. **Forbidden:** using only `image_to_video` to fake a loop; omitting `first_frame`/`last_frame` when the tool supports them (stop and report — do not silent-downgrade).

**Prompt = deltas only** (see Motion A **Default Imagine `final_prompt` template** above). Do **not** re-describe the recline / chin-rest pose. Do **not** write timed 0.4 s / 5.4 s return hard gates. Copy the MP4 to `$RUN_DIR/*-source.mp4`.

**Motion B:** do not animate the original standing crop. After `$FULLBODY_STILL` (cover) and the inner still plus pixel-crops, one 6 s clip per page:

1. Call **`image_to_video`** (16:9, 6 s) from that shot's still (cover full body, inner upper crop, inner face crop). Use **`reference_to_video`** with the same still twice if you need a tighter identity lock. Save the three 6 s clips as `$RUN_DIR/*-cover.mp4`, `*-upper.mp4`, and `*-face.mp4`. **Reuse:** if those three files already exist in `$RUN_DIR` and still pass Gate 1, do **not** regenerate them — only re-trim.
2. The prompt must require: hold the exact recumbent pose of the still; a gentle continuous side wind on hair and clothes (no whip); a **slow gentle camera push-in** on the same axis as the face page; no pan, no sit-up, no stand-up, no pull-back; shot 1 keeps looking toward the feet and keeps the heels in frame; shot 2 keeps the gaze and the waist hand and stays crown-to-hips; shot 3 holds the gaze (one slow blink allowed mid-shot; eyes open at the end) and keeps hair in the top edge; keep the still's background stable every frame (do not replace it with #888888); eyes stay open except for that optional blink. Fall back to `image_to_video` if `reference_to_video` is unavailable.
3. After Gate 1 on each clip, trim **16 + 17 + 17 frames** at 10 fps (1.6 s cover, 1.7 s inner, 1.7 s face) from the portion where wind and the push-in are both visible. **Shift the face window if needed so its last frame has eyes open**; do not keep a closed blink as the face tail. Concatenate full → upper → face, then append **one** copy of the first full-body frame (**51 frames**). That assembled timeline is `$SOURCE_MP4`.

**Motion C (native loop — Grok Build):** do not animate a standing, seated, overhead, or A/B side-recline crop. After `$FULLBODY_STILL` is the approved prone side-view, call **`reference_to_video`** (16:9, ~6 s) with **`first_frame` and `last_frame` both set to the same `$FULLBODY_STILL`**. **Forbidden:** `image_to_video`-only fake loops. The prompt must require: lock the side camera on the exact full-body framing of `$FULLBODY_STILL`; she stays prone; calves kick playfully back and forth; the upper body does **simple continuous motion** (forearm weight shift / slight head turn / tiny shoulder roll) and must **not look frozen**; **facial expression changes** mid-clip; **no** timed 0.4 s start hold or 5.4 s return hard gate — the identical first/last still closes the loop; no sit-up, crawl, stand, dance, zoom, or pan; eyes stay open. Copy the MP4 to `$RUN_DIR/*-source.mp4`. Do not run Motion A's loop-search trim as the primary path.

A face-only `image_to_video` call invents the unseen lower body and routinely changes garment type or proportions. For **native loop** contracts (A/C), `reference_to_video` with `first_frame`=`last_frame`=`$FULLBODY_STILL` is **mandatory** when the tool exposes those fields — do not substitute `image_to_video` alone. If you must fall back, the prompt still has to name every garment region from `$FULLBODY_STILL`, and Gate 1 must be stricter on outfit and body.

**Otherwise (Codex or shell-only):** invoke the local `grok` CLI so it loads `$imagine`, verifies **`reference_to_video` with `first_frame`=`last_frame`** for native loop A/C (do not silent-fallback to `image_to_video`-only for those contracts), and produces the MP4:

```zsh
mkdir -p "$RUN_DIR"
grok --single "$PROMPT" --max-turns 8 --permission-mode auto --always-approve \
  --no-alt-screen --output-format plain
```

If no Imagine video tool is available, report `IMAGE_TO_VIDEO_UNAVAILABLE` and stop. Never replace a missing video tool with an ffmpeg zoom, pan, scale, parallax, slideshow, or another static-image fallback MP4/GIF.

Prefer generating landscape natively; do not depend on later letterboxing a square or portrait video into a wide screen. Do not rely on camera motion **alone** to simulate animation — wind, a held pose, or Motion C's calf-swing must still move. Motion B's native slow push-in is required; Motion C forbids camera moves. ffmpeg zoom, scale, crop-pan, Ken Burns, and parallax stay forbidden.

## Gate 1 — Approve the Source Before Converting

Require a nonzero, decodable MP4 with positive duration.

**Motion A** — extract stations along the clip (mid beats hide a missing head-turn / smile):

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p "$RUN_DIR/source-check"
DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$SOURCE_MP4")
for t in 0 1.0 2.0 3.0 4.0; do
  ffmpeg -hide_banner -loglevel error -ss "$t" -i "$SOURCE_MP4" \
    -frames:v 1 "$RUN_DIR/source-check/t${t}.png"
done
ffmpeg -hide_banner -loglevel error -ss "$(python3 -c "print(max(0, float('$DUR')*0.7))")" -i "$SOURCE_MP4" \
  -frames:v 1 "$RUN_DIR/source-check/late-mid.png"
ffmpeg -hide_banner -loglevel error -sseof -0.04 -i "$SOURCE_MP4" \
  -frames:v 1 "$RUN_DIR/source-check/last.png"
```

Reject a zero-byte, incomplete, static, or whole-frame-only scale/translation source. Stations must prove **locked Motion A framing + micro head-turn/smile timing + identity + loop**.

- **~0 s:** same crop as `$FULLBODY_STILL` (chin-hand recline mid-crop OK), eyes open, free hand on thigh/hip home. Background unrestricted.
- **~1–3 s:** visible **head yaw toward camera** and/or **soft smile** (and optional tiny free-hand slide). No stand-up, no big pose change, no overhead arms. Garment matches `$FULLBODY_STILL`.
- **~3–5 s / late-mid:** smile easing back / head returning; still same locked crop.
- **Last frame:** matches `$FULLBODY_STILL` / first frame. Do **not** fail only because a mid timestamp is not yet on the home pose.

Compare mid-clip frames to `$FULLBODY_STILL`, not only to each other. Reject and regenerate when the camera zooms away from the locked crop, stands the figure up, shows the figure tiny in a wide empty frame, has **no** head-turn/smile micro-act (frozen still), holds both eyes shut as the only face beat, snaps, changes garment class or coverage, slims or restyles the body, reintroduces a removed staff, or has a broken first/last loop seam.

**Motion B:** Gate 1 each 6 s shot **before** trimming. Pose holds. Background stays the same as that shot's still; do not require #888888. Eyes open except one optional blink mid-shot on shot 3; the face clip must still contain open-eye frames at the end of the 1.7 s trim. Mid-clip must show **wind** in hair/clothes (shots 1–2 at least) and a **slow push-in** that is tighter than frame 0 but does **not** change shot class (full body still shows heels; upper still crown-to-hips; face still includes hair and neckline). Reject a frozen painting, a sit-up, a walk-out, a pull-back, a whip of hair, a push-in so hard that shot 1 becomes MCU, or an ffmpeg zoom. Regenerate the failed shot; do not repair motion with ffmpeg.

**Motion C** — extract stations along the clip (endpoints hide a missing calf-swing):

```zsh
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 "$SOURCE_MP4"
mkdir -p "$RUN_DIR/source-check"
for t in 0 1.2 2.4 3.6 5.4 5.8; do
  ffmpeg -hide_banner -loglevel error -ss "$t" -i "$SOURCE_MP4" \
    -frames:v 1 "$RUN_DIR/source-check/t${t}.png"
done
ffmpeg -hide_banner -loglevel error -sseof -0.04 -i "$SOURCE_MP4" \
  -frames:v 1 "$RUN_DIR/source-check/last.png"
```

- **~0 s and last frame:** same 16:9 **prone side-view full body** as `$FULLBODY_STILL`, calves lifted, same crop. Camera has not moved. Last frame matches the first-frame calf angle, arms, head, and hair.
- **Mid stations (~1.2–3.6 s):** calves at a **different swing angle** than frame 0; **visible upper-body motion** (forearm weight shift / slight head turn / tiny shoulder roll — the torso is **not frozen**); and a **changed expression** versus frame 0. She is still prone. Full body still in frame.
- Mid-clip (not endpoints): calves at a **different** swing angle than home; upper body not frozen; expression changed. Do **not** fail only because a mid timestamp is not yet on the home pose (loop is closed by `first_frame`=`last_frame`).
- **~5.8 s:** still holding that start pose.

Reject a zoom, pan, sit-up, crawl, stand, dance, overhead camera, A/B side-recline, a frozen torso (only calves moving), or a last frame that does not match the still. Compare mid-clip frames to `$FULLBODY_STILL`, not only to each other. Regenerate a failed source; do not repair motion with ffmpeg.

**Motion A has no background gate.** Do not reject on backdrop. Motion B has no default background contract — do not reject the source scene. Motion C: do not require #888888; reject only if the floor disappears or the original busy scene returns unasked. Never repair motion failures with ffmpeg. If the MP4 does not materialize, allow one concise Grok continuation naming the images, output path, required tool, and verification; then report failure rather than falling back.

## 3. Render the RT85 GIF

**Even-sample rule (native loop A/C):** regardless of source duration, **uniformly** sample into **≤51 frames** to meet the RT85 frame budget — do **not** irregularly skip frames, and do **not** use `search_rt85_loop` / assemble as the primary path (last-resort only if the source was not produced with `first_frame`=`last_frame`).

Render a **320×172** landscape GIF, 256 colours, infinite loop, **≤51 frames**.

**If `$SOURCE_MP4` is ~6 s and its first and last frames already match** (same loop gate as Gate 2: endpoint MAE is not both above 12 and above 1.3× step MAE), it is a looping source. Even-sample **≤51 frames** from first source frame through last. Then, if the **tail is a long freeze** (consecutive frames whose step MAE is well below the clip's median step, and that already match the home pose), **drop extra still frames**. Keep a **short** home hold at the end (about 1–2 frames), not a long pause. Same optional trim on a long start hold, always keeping frame 0. **Do not force a target duration** — the GIF length is whatever remains. Do not stretch the leftover frames back to 6.0 s. Delays stay 100–120 ms to match the sample cadence.

**Otherwise** (source is not a 6 s loop): 10 fps, **≤51 frames**. Duration follows the kept window.

**Motion A:** if the 6 s source already loops (first≈last as above), use that even-sample path, then drop extra still tail if needed. If it does not loop, trim a **real motion segment** (prefer the **longest** window at **320×172** whose blurred endpoint MAE is ≤ 16 and whose seam is either ≤ **1.3×** median consecutive-frame MAE or ≤ 12 absolute RGB MAE), **≤51 frames** @ 10 fps. A 6 s source often matches at ~60 frames but fails a 51-frame trim; then use the script's **assemble** plan. Do not add fade crossfades or static fake animation. If neither a trim nor an assemble pair passes, regenerate the source — hold the start pose longer at both ends — rather than shipping a jump.

```zsh
SEARCH=""
for p in \
  "$HOME/.grok/skills/generating-rt85-gifs/scripts/search_rt85_loop.py" \
  "$HOME/.codex/skills/generating-rt85-gifs/scripts/search_rt85_loop.py"; do
  [ -f "$p" ] && SEARCH="$p" && break
done
python3 "$SEARCH" --max-frames 51 "$SOURCE_MP4"
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

**Motion B:** do not run `search_rt85_loop.py` over one 6 s clip. From each approved shot, extract 10 fps **320×172** frames covering wind + push-in: **16** from full-body, **17** from upper, **17** from face (1.6 + 1.7 + 1.7 s). The **17th face frame must show eyes open**; if it is a blink, pick a different 1.7 s window. Concatenate full-body, then upper-body, then face, then **one** copy of the first full-body frame (**51 frames**). Palette-GIF that sequence (`loop=0`). Do not time-stretch with `setpts`. Hard cuts only. Never add the push-in in ffmpeg.

**Motion C:** do not run `search_rt85_loop.py`. The 6 s source must already loop (Gate 1 last frame is home). Even-sample ≤51 frames from t=0 through the last source frame, scale/crop to 320×172, then **drop extra still frames at the end** if that hold is long — keep 1–2 home frames. Duration is whatever remains. Palette-GIF (`loop=0`). If first/last of the source do not match, regenerate the source; do not even-sample a jumping clip and do not copy the first frame onto the tail.

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
python3 "$VERIFY" --max-frames 51 "$OUTPUT_GIF"
# portrait override example (only if driver requires it):
# python3 "$VERIFY" --width 172 --height 320 "$OUTPUT_GIF"
ffprobe -v error -show_entries format=format_name,duration,size:stream=codec_name,width,height,nb_frames,avg_frame_rate \
  -of default=noprint_wrappers=1 "$OUTPUT_GIF"
```

Deliver only when the verifier passes, the file is GIF data, it is **320×172** (or the driver-override size) with `loop=0`, **≤51 frames**, its endpoint is visually clean, the soft size ceiling is respected, and the display-sized frames remain legible on a **wide** panel. Pass `--max-frames 51`. Duration is not a fixed 6.0 s or 5.1 s. The loop check fails only when endpoint RGB MAE is **both** above **1.3×** median consecutive-frame MAE **and** above 12. A raw MAE above 12 alone is a warn. The first-to-last transition must not jump.

**Motion A:** first and last frames must be the **same chin-hand recline crop** as `$FULLBODY_STILL` (pose-ref mid-recline OK); a mid-clip frame must still show the locked crop with matching garment; inspect frames **between** the quartiles for the **head-turn / soft smile** beat. Motion A: no background check after palette conversion.

**Motion B:** the GIF must contain three distinct **landscape** photobook framings in order (recumbent full-body cover looking toward the feet, recumbent upper-body inner page looking at the camera, recumbent face close-up). A mid-shot frame in each must show wind (hair / hem on shots 1–2; hair / earring on shot 3) and a slightly tighter crop than that shot's first frame. The last face frame (immediately before the bookend) must show **eyes open**. First and last frames must be the same full-body recumbent start (the bookend). No standing figure.

**Motion C:** first and last frames must be the **same prone side-view full-body crop** as `$FULLBODY_STILL`, calves lifted, arms / head / hair back on the first-frame pose. A mid-clip frame must show a **different calf angle**, **visible upper-body motion** (not a frozen torso), and a **changed expression**. The camera stays locked. No standing figure, no overhead shot, no come-hither, no three-shot cuts. Frame count **≤51**. The end hold must be short if the source tail was a long freeze.

Motion A: no background check after palette conversion. Motion B: keep the source scene; do not require #888888. Motion C: keep the simple floor; do not require #888888. State the final path, duration, frame count, resolution, and file size. Upload with the **RT85 connected by USB cable** through the current **EPOMAKER Driver** (media / DIY GIF page).

## 4. Mandatory Post-Delivery Cleanup

After Gate 2 passes, clean up the current run before reporting completion.

**Motion A — keep two files** in `$RUN_DIR`:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified RT85 GIF, named `*-rt85.gif`.

**Motion C — keep two files** in `$RUN_DIR`, same names as Motion A:

- the final Grok-generated source video, named `*-source.mp4`;
- the final verified RT85 GIF, named `*-rt85.gif`.

**Motion B — keep five files** in `$RUN_DIR`:

- the three 6 s per-shot clips, named `*-cover.mp4`, `*-upper.mp4`, and `*-face.mp4` (do **not** delete these; reuse them on duration-only re-renders);
- the assembled source video, named `*-source.mp4`;
- the final verified RT85 GIF, named `*-rt85.gif`.

Delete every other resource created for that run: generated `*-fullbody` stills, `*-inner` / `*-curl` / `*-upper` / `*-face` still frames (not the `.mp4` shot clips), landscape reference images, source-check frames, contact sheets, loop-assemble PNG folders, temporary downloads or copies, failed candidate MP4/GIF files, loop-duration diagnostics, and other conversion artifacts. Use an explicit per-run manifest or staging list; never use a broad wildcard or recursive deletion that could remove unrelated historical deliverables. Do not clean up until the final GIF passes Gate 2. If cleanup would affect an ambiguous or unrelated file, stop and resolve the target rather than deleting it.

Verify after cleanup that the retained files are nonzero and still present, and that the final GIF still passes the bundled verifier. The final handoff lists those retained files only.
