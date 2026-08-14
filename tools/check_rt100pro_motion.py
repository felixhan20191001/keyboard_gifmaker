#!/usr/bin/env python3
"""Fail when an RT100 Pro GIF is technically valid but visually static."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def load_frames(path: Path) -> list[Image.Image]:
    image = Image.open(path)
    frames: list[Image.Image] = []
    try:
        while True:
            frames.append(image.convert("RGB").copy())
            image.seek(image.tell() + 1)
    except EOFError:
        return frames


def mean_difference(first: Image.Image, second: Image.Image) -> float:
    difference = ImageChops.difference(first, second)
    return sum(ImageStat.Stat(difference).mean) / 3


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_rt100pro_motion.py <gif>")

    path = Path(sys.argv[1])
    frames = load_frames(path)
    if not frames:
        raise SystemExit("FAIL: GIF has no decodable frames")
    if frames[0].size != (240, 240):
        raise SystemExit(f"FAIL: expected 240x240, got {frames[0].size}")
    if len(frames) > 56:
        raise SystemExit(f"FAIL: expected at most 56 frames, got {len(frames)}")

    subject = [frame.crop((45, 0, 225, 240)) for frame in frames]
    adjacent = [
        mean_difference(frame, subject[(index + 1) % len(subject)])
        for index, frame in enumerate(subject)
    ]
    quarter = mean_difference(subject[0], subject[len(subject) // 4])
    half = mean_difference(subject[0], subject[len(subject) // 2])

    if sum(adjacent) / len(adjacent) < 1.2:
        raise SystemExit("FAIL: adjacent subject motion is below the visible-motion threshold")
    if quarter < 6.0 or half < 5.0:
        raise SystemExit("FAIL: the character pose changes too little across the loop")

    print(
        "PASS: visible subject motion "
        f"(adjacent_avg={sum(adjacent) / len(adjacent):.3f}, "
        f"quarter={quarter:.3f}, half={half:.3f}, frames={len(frames)})"
    )


if __name__ == "__main__":
    main()
