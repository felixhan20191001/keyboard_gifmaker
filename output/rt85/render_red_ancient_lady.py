#!/usr/bin/env python3
"""Render a breathing + blinking + candle-flicker loop for RT85 320x172 GIF.

All animation is derived procedurally from the source still:
- 45-frame full sin/cos cycle so frame 0 and frame 44 match (seamless loop)
- Overall vertical drift + chest-region masked scale = breathing
- Single blink burst near frame 20
- Candle flame flicker in bottom-right
"""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

SOURCE = Path("output/rt85/red-ancient-lady-source.png")
FRAMES_DIR = Path("output/rt85/red-ancient-lady-frames")
FRAME_COUNT = 45
WORK_W, WORK_H = 960, 540
FINAL_W, FINAL_H = 320, 172


def crop_16_9(img: Image.Image) -> Image.Image:
    """Crop to 16:9 with a slight upward bias so the face stays prominent."""
    w, h = img.size
    target_h = int(w * 9 / 16)
    top = (h - target_h) // 3
    return img.crop((0, top, w, top + target_h))


def masked_scale(
    base: Image.Image, canvas: Image.Image, box: tuple[int, int, int, int], scale: float
) -> None:
    """Scale a rectangular region of *base* and paste onto *canvas* with a soft elliptical mask."""
    x0, y0, x1, y1 = box
    crop = base.crop(box)
    w, h = crop.size
    scaled = crop.resize(
        (round(w * scale), round(h * scale)),
        Image.Resampling.LANCZOS,
    )
    mask = Image.new("L", scaled.size)
    draw = ImageDraw.Draw(mask)
    mx = round(scaled.width * 0.10)
    my = round(scaled.height * 0.10)
    draw.ellipse((mx, my, scaled.width - mx, scaled.height - my), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    canvas.paste(scaled, (cx - scaled.width // 2, cy - scaled.height // 2), mask)


def add_blink(canvas: Image.Image, frame: int) -> Image.Image:
    """One blink burst centred on frame 20, 3 frames each side with soft falloff."""
    centre = 20
    half_width = 3
    dist = abs(frame - centre)
    if dist > half_width:
        return canvas

    strength = {0: 1.0, 1: 0.65, 2: 0.30, 3: 0.10}.get(dist, 0.0)
    if strength <= 0:
        return canvas

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    eyelid = (155, 115, 105, int(220 * strength))
    line_w = int(3 + 3 * strength)

    # Character's right eye (screen-left): ~(700,122)-(740,124)
    draw.line((698, 123, 742, 125), fill=eyelid, width=line_w)
    # Character's left eye (screen-right): ~(748,112)-(785,114)
    draw.line((746, 113, 788, 115), fill=eyelid, width=line_w)

    overlay = overlay.filter(ImageFilter.GaussianBlur(1.2))
    return Image.alpha_composite(canvas, overlay)


def add_candle_flicker(canvas: Image.Image, phase: float) -> Image.Image:
    """Two candle flames in the bottom-right flicker at independent rates."""
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Flame 1 (left candle): base ~(916, 472)
    f1 = 0.5 + 0.4 * sin(phase * 3.1) + 0.1 * sin(phase * 7.3)
    h1 = int(48 + 10 * f1)
    draw.ellipse((907, 472 - h1, 926, 476), fill=(255, 215, 110, 90))
    draw.ellipse((912, 472 - h1 + 6, 921, 474), fill=(255, 250, 190, 140))

    # Flame 2 (right candle): base ~(962, 482)
    f2 = 0.5 + 0.4 * sin(phase * 2.7 + 1.3) + 0.1 * sin(phase * 6.5 + 0.5)
    h2 = int(46 + 9 * f2)
    draw.ellipse((953, 482 - h2, 971, 486), fill=(255, 215, 110, 90))
    draw.ellipse((957, 482 - h2 + 6, 966, 484), fill=(255, 250, 190, 140))

    overlay = overlay.filter(ImageFilter.GaussianBlur(3.5))
    return Image.alpha_composite(canvas, overlay)


def main() -> None:
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    base = Image.open(SOURCE).convert("RGB")
    base = crop_16_9(base)
    base = base.resize((WORK_W, WORK_H), Image.Resampling.LANCZOS)

    for index in range(FRAME_COUNT):
        phase = 2 * pi * index / FRAME_COUNT
        inhale = 0.5 - 0.5 * cos(phase)  # 0 at frame 0, 1 at frame 22, 0 at frame 44
        sway = sin(phase)

        # Whole-body drift: inhale lifts the torso a few pixels
        shift_x = int(1.5 * sway)
        shift_y = int(-3 * inhale)

        # Start from the base still
        art = base.copy()

        # Chest expansion via masked scale (soft elliptical mask)
        chest_scale = 1.0 + 0.028 * inhale
        masked_scale(base, art, (570, 235, 895, 435), chest_scale)

        # RGBA for overlays
        art_rgba = art.convert("RGBA")
        art_rgba = add_blink(art_rgba, index)
        art_rgba = add_candle_flicker(art_rgba, phase)

        # Compose onto a dark-red background with the breathing shift
        frame = Image.new("RGBA", (WORK_W, WORK_H), (18, 8, 10, 255))
        frame.alpha_composite(art_rgba, (shift_x, shift_y))

        # Downscale to final RT85 resolution
        final = frame.convert("RGB").resize((FINAL_W, FINAL_H), Image.Resampling.LANCZOS)
        final.save(FRAMES_DIR / f"frame_{index:03d}.png", compress_level=1)

    print(f"Rendered {FRAME_COUNT} frames to {FRAMES_DIR}")


if __name__ == "__main__":
    main()
