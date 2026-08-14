# Keyboard GIF Maker

Pipelines for making loop GIFs that fit keyboard mini-screens:

| Keyboard | Skill | Delivery |
|----------|--------|----------|
| EPOMAKER RT100 Pro | `skills/generating-rt100pro-gifs` | 240×240 |
| EPOMAKER RT85 | `skills/generating-rt85-gifs` | 320×172 landscape |
| Qwertykeys QK100 Mk2 | `skills/generating-qk100-gifs` | 135×240 portrait |

Each skill is a standalone package: `SKILL.md`, `scripts/`, and `agents/`.

## Install a skill

Copy or symlink one package into your Grok / Codex skills directory:

```bash
ln -sfn "$(pwd)/skills/generating-rt85-gifs" ~/.grok/skills/generating-rt85-gifs
ln -sfn "$(pwd)/skills/generating-rt85-gifs" ~/.codex/skills/generating-rt85-gifs
```

Zipped copies live in `skills/packages/`.

## Layout

- `skills/` — the three screen-GIF skills
- `output/rt100pro/`, `output/rt85/`, `output/qk100/` — generated GIFs and source MP4s
- `tools/` — local helpers used by earlier RT100 Pro runs
- `docs/` — design notes for the six-panel RT100 Pro GIF

Run a skill from Grok / Codex with `/generating-rt85-gifs` (or the matching name). Keep each keyboard’s files in its own `output/` folder.
