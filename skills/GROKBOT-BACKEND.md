# Grok Bot generation backends

Applies to all three keyboard packages on the `grokbot` branch.

## 1. Stills (Grok CLI)

Use local Grok Build CLI (not Cursor `user-X`):

```bash
grok -p "$PROMPT" --always-approve --max-turns 8
```

Ask the model to use native **`image_gen` / `image_edit`** (and save files under `$RUN_DIR`).
Pass reference images twice when a specific aspect (1:1 / 16:9 / 9:16) must be honored — same as the original skills.

## 2. Video (Grok web Imagine)

Do **not** rely on CLI `image_to_video` / `reference_to_video`.

1. Build the final video prompt(s) exactly as `SKILL.md` motion contracts require.
2. Write `/workspace/imagine-pipeline/plans/YYYYMMDD-<keyboard>-<name>.md` with at least:
   - `status: confirmed` (after user OK, or auto if user said to run through)
   - `mode: Video`
   - `source_asset` / reference paths or `@Name` chips
   - `reuse_imagine_chat: true` unless refs changed or user asked for a new chat
   - `settings.aspect_ratio` / `duration` / `resolution` from **this skill** (not global 9:16 defaults unless they match)
   - For **RT100 Pro Motion A** (and any other contract that needs a native loop): set **Add last frame** to the **same still** as the start image; document that in the plan (`last_frame` / `workflow_note` / `settings.other`)
   - `final_prompt`
   - `return_to` / `deliver_mp4` / `deliver_mp4_to` when handing back to GIFmaker
   - `handoff_to: Imagine出片`
3. Message **Imagine出片** with the plan path; wait for completion; copy/download MP4 into `$RUN_DIR/*-source.mp4` (or the per-shot paths Motion B needs).
4. Continue Gate 1 → GIF → Gate 2 → cleanup from `SKILL.md`.

If web Imagine cannot attach multiple refs the way CLI `reference_to_video` did, approximate with Uploads + `@` References (max ~3) and a prompt that names which image is composition lock vs face vs curl — document what you used in the plan.

## 3. GIF / verify

Unchanged: call package `scripts/` with `python3` + `ffmpeg` as in `SKILL.md`.
Also search skill paths under a local checkout of this repo, not only `~/.grok/skills/`.
