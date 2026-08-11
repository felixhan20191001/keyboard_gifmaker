# Six-Panel Anime RT100 Pro GIF Design

## Goal

Create a compact, keyboard-ready looping GIF from the supplied six-second square MP4, prioritising a short, action-focused segment with the cleanest practical loop.

## Source and Selection

- Input: `/Users/hanpengfei/Downloads/grok-video-ff69830c-b11d-498b-ae7d-65ced10494b6.mp4`.
- The source is a decodable 544x544 H.264 video lasting about 6.04 seconds.
- Use the most active `4.2-5.9` second source window inside the approved `2.9-5.9` second interval.
- Play the 17 sampled frames forward, then frames 15 through 1 in reverse, avoiding duplicate endpoint frames and producing a clean 3.2-second loop.
- Preserve the existing square six-panel composition without cropping or camera changes.
- Remove audio from GIF output.

## Rendering

1. Create a temporary full-length GIF at display size to confirm that the source converts correctly and to review the complete motion.
2. Render the approved high-motion source window directly from the original MP4, rather than recompressing the temporary GIF.
3. Produce a 240x240 GIF at 10fps with up to 256 colours, infinite looping, and 32 frames.
4. Use palette generation and palette application to retain detail and smooth gradients at keyboard-screen size.

## Quality Gates and Cleanup

- Confirm the retained source MP4 is nonempty, decodable, square, and has positive duration.
- Inspect the beginning, middle, and end of the selected interval for readable faces, visible motion, stable panel boundaries, and an acceptable loop transition.
- Deliver only if the bundled RT100 Pro verifier passes and independent metadata inspection confirms GIF data, 240x240 dimensions, 30 or fewer expected frames, and infinite looping.
- Retain only `six-panel-anime-source.mp4` and `six-panel-anime-rt100pro.gif` for this run in `output/rt100pro/`.
- Remove the temporary full-length GIF, extracted review frames, contact sheets, and any failed current-run candidates only after the final GIF passes verification.
