# Grok Bot generation backends

Applies to all three keyboard packages on the `grokbot` branch.

## 1. Stills (**默认 Grok Build**)

**Primary (Felix 2026-09-15):** use Grok Build CLI (`grok -p` + native `image_edit` / `image_gen`) with:

- character (and pose) references attached; pass the character reference **twice** when a specific aspect (`1:1` / `16:9` / `9:16`) must be honored
- prompts that **hard-lock identity**: same face, hair, body type, outfit, accessories as the reference — no restyle, no slim/enlarge, no new character

```bash
grok -p "$PROMPT" --always-approve --max-turns 12
```

Save outputs under `$RUN_DIR`. Reject and regenerate on identity drift before any video handoff.

**Self-check loop (Felix 2026-09-15):** after every `image_edit` / `image_gen`, Grok Build must inspect the result against the stated checklist (identity, outfit, pose, coverage, etc.). If anything fails, **automatically edit again in the same session**. **Hard cap: at most 5 edit rounds per still job** (including the first generate). If still failing after 5, stop and deliver the best candidate + honest gaps — do not keep looping. Do **not** wait for GIFmaker/Felix to review intermediates. **GIFmaker must not mid-check or steer edits** — only receive Grok Build’s final still (after ≤5 self-check rounds) and hand that to the user. Progress status to the user is OK.

**Optional:** Cursor `GenerateImage` only if Felix explicitly asks for it — not the default path.

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


## 2b. Plan field completeness (Felix 2026-09-15 — 出图优化群)

When GIFmaker writes an Imagine plan for Imagine出片, **hard-code every ops field** so the runner can preflight without guessing:

- `mode`, `status: confirmed`
- `settings.aspect_ratio` / `duration` / `resolution` / `audio` (keyboard defaults if unset: RT85 → 16:9 / 6s / 480p / off; RT100 → 1:1 / 6s / 480p / off)
- `loop_via_image_menu: true|false` explicitly (never omit when Loop is required)
- `reuse_imagine_chat: true|false` + `new_chat_reason` when false
- `source_asset` absolute path(s); `last_frame` only if needed and **not** alongside Loop
- `final_prompt` verbatim-ready
- GIFmaker line: `return_to: GIFmaker`, `deliver_mp4: true`, `deliver_mp4_to` absolute path

Incomplete plans are not handoff-ready — fill them before messaging Imagine出片.

## 3. GIF / verify

Unchanged: call package `scripts/` with `python3` + `ffmpeg` as in `SKILL.md`.
Also search skill paths under a local checkout of this repo, not only `~/.grok/skills/`.
