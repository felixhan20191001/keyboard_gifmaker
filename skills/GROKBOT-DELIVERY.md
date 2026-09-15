# Grok Bot — delivery, Imagine session, box cleanup

Applies to GIFmaker runs on the `grokbot` branch.

详规落地：`/workspace/workflow-specs/gif-pipeline-v2.md`（Felix 2026-09-15 点头）。

## Still-frame review (skip when allowed)

**Skip** private still review and go straight to plan → Imagine → Gate/GIF when **all** are true:

- same character + same main reference image path (unchanged)
- only motion/contract or video-prompt deltas (A/B/C or action segment)
- an already **passed** still archive exists for that character+ref

Then tell Felix in the handoff/DM: `复用已过目静帧 <path>，本次只审成片`.

**Still require** still review when: new/changed reference, new character, first still for that setup, Build hit the 5-round cap and is shipping best-candidate, or Felix asks to see the still.

## After Gate 2 passes

1. **DM Felix the final GIF** for review (every run).
2. Ask whether the **finished piece** passes (成片过目 — do not cancel this).
3. On delivery you may already have copied to Mac; if not, copy on pass (below).

## Failures — who shouts stop

- **Imagine / web login / quota / generate fail / session won’t open:** **Imagine出片** only — they DM Felix + notify GIFmaker `出片阻塞：…`. **GIFmaker must not also chase Felix for the same fault.**
- **Grok Build / Gate / Mac copy:** GIFmaker DMs Felix; do not dump on Imagine出片.

## Pass → path + auto-clean (no second “已存本地”)

When Felix says the piece **passes** / 可以 / OK (same meaning):

1. **Immediately** copy GIF + source MP4 to  
   `/Users/hanpengfei/Documents/RT100pro Gif/output/<rt85|rt100pro|qk100>/<中文名>/`
2. DM: Mac paths + `已开始清云产物；路径不对立刻喊停`
3. **Start cloud cleanup at once** — do **not** wait for a separate `已存本地` / `我保存了`
4. If he says path wrong / 先别删 → stop cleanup (restore per need); otherwise finish cleanup

### What to delete (same run only)

- entire `$RUN_DIR` (stills, crops, gates, MP4s, GIF, pick-rounds, logs, prompts)
- **his uploaded character/outfit ref copies** for that run (not skill pose-refs)
- matching `/workspace/imagine-pipeline/outputs/gifmaker/` files
- that run’s `imagine-pipeline/refs/…` and plan copies
- keyboard_gifmaker `output/<keyboard>/<中文名>/` working copies
- curl/litterbox caches, `/tmp` crops, Grok Build session images for that workdir
- any other files created only for that run

**Do not** delete other runs, repo skill pose-refs (e.g. `motion-a-recline-pose-ref.png`), or unrelated outputs.

Until he **passes**, keep artifacts. If he rejects, revise; don’t wipe the last candidate until a replacement is approved or he orders cleanup.

## Same Imagine chat when re-rolling video

If reference images did not change and he did not ask for a new chat:

- write `reuse_imagine_chat: true`
- Imagine出片 continues the same grok.com Imagine conversation
- do **not** open extra Imagine threads

New chat only when refs changed or he explicitly says 换对话／新开对话.
