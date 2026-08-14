#!/usr/bin/env python3
"""Render a visibly animated RT100 Pro source sequence from the approved crop."""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


SOURCE = Path("output/rt100pro/silver-android-sensual-idle-square.png")
FRAMES = Path("output/rt100pro/silver-android-sensual-v2-frames")
FRAME_COUNT = 45


def masked_scale(base: Image.Image, canvas: Image.Image, box: tuple[int, int, int, int], scale: float) -> None:
    x0, y0, x1, y1 = box
    crop = base.crop(box)
    width, height = crop.size
    scaled = crop.resize(
        (round(width * scale), round(height * scale)),
        Image.Resampling.LANCZOS,
    )
    mask = Image.new("L", scaled.size)
    draw = ImageDraw.Draw(mask)
    margin_x = round(scaled.width * 0.06)
    margin_y = round(scaled.height * 0.06)
    draw.ellipse((margin_x, margin_y, scaled.width - margin_x, scaled.height - margin_y), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(9))
    centre_x = (x0 + x1) // 2
    centre_y = (y0 + y1) // 2
    canvas.paste(scaled, (centre_x - scaled.width // 2, centre_y - scaled.height // 2), mask)


def cape_drift(base: Image.Image, canvas: Image.Image, box: tuple[int, int, int, int], shift: int) -> None:
    x0, y0, x1, y1 = box
    crop = base.crop(box)
    mask = Image.new("L", crop.size)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((10, 12, crop.width - 10, crop.height - 12), fill=150)
    mask = mask.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(crop, (x0 + shift, y0), mask)


def subject_alpha(image: Image.Image) -> Image.Image:
    luminance = image.convert("L")
    return luminance.point(lambda value: 0 if value < 8 else 255).filter(ImageFilter.GaussianBlur(0.7))


def add_shine(canvas: Image.Image, phase: float, alpha: Image.Image) -> Image.Image:
    width, height = canvas.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    sweep = 0.5 + 0.5 * sin(phase - 0.7)
    x = round(170 + 360 * sweep)
    draw.line((x, 155, x + 36, 655), fill=(255, 255, 255, 75), width=16)
    draw.ellipse((390 + round(35 * sin(phase)), 205, 465 + round(35 * sin(phase)), 340), fill=(255, 244, 206, 55))
    draw.ellipse((480 + round(40 * sin(phase + 0.8)), 225, 555 + round(40 * sin(phase + 0.8)), 300), fill=(255, 255, 255, 55))
    overlay = overlay.filter(ImageFilter.GaussianBlur(5))
    overlay.putalpha(ImageChops.multiply(overlay.getchannel("A"), alpha))
    return Image.alpha_composite(canvas, overlay)


def add_blink(canvas: Image.Image, frame_number: int) -> Image.Image:
    blink_strength = max(0.0, 1.0 - abs((frame_number - 22) / 2.0))
    if blink_strength == 0:
        return canvas
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    opacity = round(210 * blink_strength)
    width = 6 + round(4 * blink_strength)
    draw.line((311, 113, 342, 114), fill=(105, 76, 82, opacity), width=width)
    draw.line((391, 121, 423, 123), fill=(105, 76, 82, opacity), width=width)
    return Image.alpha_composite(canvas, overlay.filter(ImageFilter.GaussianBlur(1.1)))


def main() -> None:
    FRAMES.mkdir(parents=True, exist_ok=True)
    base = Image.open(SOURCE).convert("RGB")
    width, height = base.size

    for index in range(FRAME_COUNT):
        phase = 2 * pi * index / FRAME_COUNT
        inhale = 0.5 - 0.5 * cos(phase)
        sway = sin(phase)

        art = base.convert("RGBA")
        chest_scale = 1.0 + 0.085 * inhale
        masked_scale(base, art, (315, 180, 460, 355), chest_scale)
        masked_scale(base, art, (425, 170, 590, 365), chest_scale)
        cape_drift(base, art, (60, 245, 230, 715), round(-10 * sway))
        cape_drift(base, art, (555, 245, 715, 715), round(10 * sway))

        alpha = subject_alpha(art)
        art = add_shine(art, phase, alpha)
        art.putalpha(alpha)
        art = add_blink(art, index)

        # Character movement, not camera movement: an inhale lifts the torso while it sways slightly.
        frame = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        frame.alpha_composite(art, (round(9 * sway), round(-11 * inhale)))
        frame.convert("RGB").save(FRAMES / f"frame_{index:03d}.png", compress_level=1)

    print(f"rendered {FRAME_COUNT} frames to {FRAMES}")


if __name__ == "__main__":
    main()
