# Grok Bot — delivery, Imagine session, box cleanup

Applies to GIFmaker runs on the `grokbot` branch.

## After Gate 2 passes

1. **DM Felix the final GIF** as a chat attachment for review (every run).
2. Ask whether it **passes**.
3. **Remind him**: if it passes, **save the file to his local computer first**, then reply e.g. `通过，已存本地`.

## Delete everything on the box for that run (dual confirmation — Felix 2026-09-15)

“Cloud artifacts” means **all intermediates, temps, and working copies of this generation on the box**, not a separate archive label.

**Still dual confirmation:** only after he **passes review** **and** confirms **already saved locally** (e.g. `通过，已存本地` / `我保存了`), then delete. Never delete on pass alone or save alone.

Delete **everything for that run**, including:

- the entire `$RUN_DIR` (stills, face/curl crops, gate frames, checks, source MP4s, final GIF, leftover script output, pick-rounds, logs, prompts)
- **his uploaded character/outfit reference** copies for that run (chat-materialized refs under the run dir / refs folder — not skill pose-refs)
- matching files under `/workspace/imagine-pipeline/outputs/gifmaker/`
- that run’s `imagine-pipeline/refs/…` and plan copies under `imagine-pipeline/plans/`
- keyboard_gifmaker `output/<keyboard>/<中文名>/` working copies for that piece
- curl / litterbox download caches, `/tmp` crops, and Grok Build session images for that workdir when they belong to this run
- any other files created only for that run (inbox drops, etc.)

**Do not** delete:

- other runs’ folders or outputs
- repo skill assets (e.g. `skills/.../refs/motion-a-recline-pose-ref.png` and other packaged pose refs)
- unrelated characters’ outputs

Until dual confirmation, keep them. If he rejects, revise; do not wipe the last candidate until a replacement is approved or he orders cleanup.

## Same Imagine chat when re-rolling video

If GIFmaker (or Felix) asks to **regenerate video** and the **reference images did not change**, and he did not ask for a new chat:

- write `reuse_imagine_chat: true`
- Imagine出片 **must continue in the same grok.com Imagine conversation** (`active-session.md` / last `imagine_chat_url`)
- do **not** open extra Imagine threads

New chat only when refs changed or he explicitly says 换对话／新开对话.
