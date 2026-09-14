# Keyboard GIF Maker — Grok Bot edition (`grokbot` branch)

This branch adapts the three keyboard GIF skills for **Grok Bot** agents.

| Keyboard | Skill folder | Delivery |
|----------|--------------|----------|
| EPOMAKER RT100 Pro | `skills/generating-rt100pro-gifs` | 240×240 |
| EPOMAKER RT85 | `skills/generating-rt85-gifs` | 320×172 landscape |
| Qwertykeys QK100 Mk2 | `skills/generating-qk100-gifs` | 135×240 portrait |

## Backend split (required on this branch)

| Step | Tooling |
|------|---------|
| Stills / `image_edit` / `image_gen` | **Grok CLI** on box or Mac: `grok -p "…" --always-approve` (native image tools) |
| Source **video** MP4 | **Grok web Imagine** `https://grok.com/imagine` — write a plan under `/workspace/imagine-pipeline/plans/`, hand off to **Imagine出片** (computerUse). Do **not** call CLI `image_to_video` / `reference_to_video` as the primary path. |
| GIF encode + verify | Existing `scripts/` + `ffmpeg` / `python3` (unchanged) |

Motion contracts, resolutions, Gate 1/2, and cleanup rules stay in each package’s `SKILL.md`.
**Generation backends** are overridden by that package’s `GROKBOT.md` — Grok Bot agents **must** read `GROKBOT.md` before section 2 of `SKILL.md`.

Shared notes: `skills/GROKBOT-BACKEND.md`.

## Install into Grok Bot

1. Keep this repo available (clone on Mac / box, or fetch via GitHub MCP).
2. Copy or adapt each needed `SKILL.md` + `GROKBOT.md` + `scripts/` into a Grok Bot shared skill (`update_state` skill write), **or** instruct the agent to `Read` these paths from a local checkout.
3. Ensure `ffmpeg` and `python3` exist on the machine that runs Gate scripts.
4. Imagine out片 bot + `/workspace/imagine-pipeline/` must be available for video.

## Aspect vs Felix Imagine defaults

Felix’s Imagine pipeline defaults (9:16 / 10s / 480p) are **overridden** by each keyboard skill’s source aspect and duration when running these skills (e.g. RT85 source **16:9**, RT100 Pro **1:1**, QK100 **9:16**).

## Master branch

`master` remains the Grok Build / Codex install (`~/.grok/skills/…`). Do not mix install paths.
