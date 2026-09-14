# Grok Bot generation backends

Applies to all three keyboard packages on the `grokbot` branch.

## 1. Stills (优先自出；失败则 Grok Build 兜底)

**Primary:** GIFmaker generates stills itself (Cursor `GenerateImage`) with:

- `reference_image_paths` pointing at the user reference (and edited masters as needed)
- the required aspect (`1:1` / `16:9` / `9:16`)
- prompts that **hard-lock identity**: same face, hair, body type, outfit, accessories as the reference — no restyle, no slim/enlarge, no new character

Save outputs under `$RUN_DIR`. Reject and regenerate on identity drift before any video handoff.

**Fallback:** if `GenerateImage` fails, use Grok Build CLI (`grok -p` + native `image_edit` / `image_gen`), pass the reference twice for the required aspect, keep hard identity lock.

## 2. Video (Grok web Imagine)

Do **not** rely on CLI `image_to_video` / `reference_to_video`.

1. Build the final video prompt(s) exactly as `SKILL.md` motion contracts require.
2. Write `/workspace/imagine-pipeline/plans/YYYYMMDD-<keyboard>-<name>.md` with at least:
   - `status: confirmed` (after user OK, or auto if user said to run through)
   - `mode: Video`
   - `source_asset` / reference paths or `@Name` chips
   - `reuse_imagine_chat: true` unless refs changed or user asked for a new chat
   - `settings.aspect_ratio` / `duration` / `resolution` from **this skill** (not global 9:16 defaults unless they match). Package defaults: **RT100 Pro** → `1:1` / `6s` / `480p`; **RT85** → `16:9` / `6s` / `480p`
   - For **RT100 Pro Motion A**, **RT85 Motion A**, **RT85 Motion C** (native loop only): set `loop_via_image_menu: true` and `last_frame: <same still as start>`. Imagine出片 **must** open the upload thumbnail 三点菜单「循环」, and if Add last frame is still shown, set it to that same still (belt-and-suspenders). See `/workspace/imagine-pipeline/loop-via-image-menu.md`. Do **not** enable 循环 for Motion B or when the plan omits the flag.
   - `final_prompt`
   - `return_to` / `deliver_mp4` / `deliver_mp4_to` when handing back to GIFmaker
   - `handoff_to: Imagine出片`
3. Message **Imagine出片** with the plan path; wait for completion; copy/download MP4 into `$RUN_DIR/*-source.mp4` (or the per-shot paths Motion B needs).
4. Continue Gate 1 → GIF → Gate 2 → cleanup from `SKILL.md`.

If web Imagine cannot attach multiple refs the way CLI `reference_to_video` did, approximate with Uploads + `@` References (max ~3) and a prompt that names which image is composition lock vs face vs curl — document what you used in the plan.

## 3. GIF / verify

Unchanged: call package `scripts/` with `python3` + `ffmpeg` as in `SKILL.md`.
Also search skill paths under a local checkout of this repo, not only `~/.grok/skills/`.
