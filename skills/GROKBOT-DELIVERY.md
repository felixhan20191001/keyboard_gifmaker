# Grok Bot — delivery, Imagine session, box cleanup

Applies to GIFmaker runs on the `grokbot` branch.

## After Gate 2 passes

1. **DM Felix the final GIF** as a chat attachment for review (every run).
2. Ask whether it **passes**.
3. **Remind him**: if it passes, **save the file to his local computer first**, then reply e.g. `通过，已存本地`.

## Delete everything on the box for that run (dual confirmation)

“Cloud artifacts” means **all intermediates and finals of this generation on the box computer**, not a separate archive label.

Only after he says **passed** **and** **already saved locally**, delete:

- the entire `$RUN_DIR` (stills, checks, source MP4s, final GIF, leftover scripts output)
- matching files under `/workspace/imagine-pipeline/outputs/gifmaker/`
- any other files created for that run (plans copies, inbox drops, etc.)

Until then, keep them. If he rejects, revise; do not wipe the last candidate until a replacement is approved or he orders cleanup.

## Same Imagine chat when re-rolling video

If GIFmaker (or Felix) asks to **regenerate video** and the **reference images did not change**, and he did not ask for a new chat:

- write `reuse_imagine_chat: true`
- Imagine出片 **must continue in the same grok.com Imagine conversation** (`active-session.md` / last `imagine_chat_url`)
- do **not** open extra Imagine threads

New chat only when refs changed or he explicitly says 换对话／新开对话.
