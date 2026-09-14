#!/usr/bin/env python3
"""Verify delivery constraints for a Qwertykeys QK100 / QK100 Mk2 GIF screen.

Hard panel spec used by QK Config / QK100 LCD docs:
  135x240 portrait (exactly 9:16), up to 128 frames.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def rgb_mae(a: Image.Image, b: Image.Image) -> float:
    return sum(ImageStat.Stat(ImageChops.difference(a.convert("RGB"), b.convert("RGB"))).mean) / 3


def loop_metrics(frames_rgb: list[Image.Image]) -> tuple[float, float, float]:
    if len(frames_rgb) < 2:
        return 0.0, 0.0, 0.0
    endpoint_mae = rgb_mae(frames_rgb[0], frames_rgb[-1])
    step_maes = [
        rgb_mae(frames_rgb[i], frames_rgb[i + 1]) for i in range(len(frames_rgb) - 1)
    ]
    step_mae = float(statistics.median(step_maes))
    endpoint_ratio = (endpoint_mae / step_mae) if step_mae > 0 else 0.0
    return endpoint_mae, step_mae, endpoint_ratio


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gif", type=Path, help="GIF to inspect")
    parser.add_argument(
        "--width",
        type=int,
        default=135,
        help="Expected width (QK100 Mk2 GIF panel is 135)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=240,
        help="Expected height (QK100 Mk2 GIF panel is 240)",
    )
    parser.add_argument("--max-frames", type=int, default=128)
    parser.add_argument("--frame-ms", type=int, default=100)
    parser.add_argument(
        "--max-endpoint-mae",
        type=float,
        default=12.0,
        help="Warn if endpoint RGB MAE exceeds this; not a fail by itself",
    )
    parser.add_argument(
        "--max-endpoint-ratio",
        type=float,
        default=1.3,
        help="Fail if endpoint MAE exceeds this multiple of median consecutive-frame MAE",
    )
    parser.add_argument(
        "--max-size-bytes",
        type=int,
        default=2_500_000,
        help="Soft size ceiling; shrink if QK Config rejects the upload",
    )
    args = parser.parse_args()

    issues: list[str] = []
    warnings: list[str] = []
    if not args.gif.is_file() or args.gif.stat().st_size == 0:
        print(f"FAIL: missing or empty GIF: {args.gif}", file=sys.stderr)
        return 1

    with args.gif.open("rb") as file:
        if file.read(6) not in {b"GIF87a", b"GIF89a"}:
            print(f"FAIL: not GIF data: {args.gif}", file=sys.stderr)
            return 1

    try:
        image = Image.open(args.gif)
        image.load()
    except Exception as exc:
        print(f"FAIL: unreadable GIF: {exc}", file=sys.stderr)
        return 1

    frame_count = getattr(image, "n_frames", 1)
    size_bytes = args.gif.stat().st_size
    if image.format != "GIF":
        issues.append(f"format is {image.format}, not GIF")
    if image.size != (args.width, args.height):
        issues.append(
            f"dimensions are {image.size[0]}x{image.size[1]}, "
            f"not the QK100 Mk2 spec {args.width}x{args.height}"
        )
    if image.size[0] == image.size[1]:
        issues.append(
            f"panel is square ({image.size[0]}x{image.size[1]}); "
            "QK100 Mk2 GIF delivery must be 135x240 portrait"
        )
    if image.width > image.height and (args.width, args.height) == (135, 240):
        issues.append(
            f"panel is landscape ({image.size[0]}x{image.size[1]}); "
            "QK100 Mk2 GIF panel is portrait 135x240"
        )
    if not 2 <= frame_count <= args.max_frames:
        issues.append(f"frame count is {frame_count}, expected 2-{args.max_frames}")
    if image.info.get("loop") != 0:
        issues.append("GIF is not marked for infinite looping (loop=0)")

    durations: list[int] = []
    frames_rgb: list[Image.Image] = []
    for index in range(frame_count):
        image.seek(index)
        durations.append(int(image.info.get("duration", 0)))
        frames_rgb.append(image.convert("RGB"))
    if any(duration != args.frame_ms for duration in durations):
        issues.append(f"frame delays are not all {args.frame_ms} ms (10 fps)")

    endpoint_mae, step_mae, endpoint_ratio = loop_metrics(frames_rgb)
    if endpoint_mae > args.max_endpoint_mae:
        warnings.append(
            f"endpoint MAE is {endpoint_mae:.2f}, above {args.max_endpoint_mae:.2f} "
            "(high-texture warn; fail only if ratio also exceeds cap)"
        )
    if frame_count >= 2 and step_mae <= 0:
        if endpoint_mae > args.max_endpoint_mae:
            issues.append(
                f"endpoint MAE is {endpoint_mae:.2f}, above {args.max_endpoint_mae:.2f}; "
                "the loop likely jumps"
            )
    elif (
        endpoint_ratio > args.max_endpoint_ratio
        and endpoint_mae > args.max_endpoint_mae
    ):
        issues.append(
            f"endpoint MAE {endpoint_mae:.2f} is {endpoint_ratio:.2f}x consecutive "
            f"step MAE {step_mae:.2f}, above {args.max_endpoint_ratio:.2f}x "
            f"and above {args.max_endpoint_mae:.2f}; the loop likely jumps"
        )
    if size_bytes > args.max_size_bytes:
        issues.append(
            f"file size is {size_bytes} bytes, above soft ceiling {args.max_size_bytes}"
        )

    orientation = (
        "portrait"
        if image.height > image.width
        else "landscape"
        if image.width > image.height
        else "square"
    )
    report = {
        "path": str(args.gif),
        "format": image.format,
        "width": image.width,
        "height": image.height,
        "orientation": orientation,
        "frames": frame_count,
        "loop": image.info.get("loop"),
        "frame_delays_ms": sorted(set(durations)),
        "duration_seconds": round(sum(durations) / 1000, 3),
        "endpoint_mae": round(endpoint_mae, 2),
        "step_mae": round(step_mae, 2),
        "endpoint_ratio": round(endpoint_ratio, 2),
        "size_bytes": size_bytes,
        "product": "Qwertykeys QK100 Mk2",
        "screen": "QK Config GIF / Dynamic Island color LCD",
        "expected_default": "135x240 portrait 9:16",
        "max_frames_spec": 128,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if warnings:
        print("WARN: " + "; ".join(warnings), file=sys.stderr)
    if issues:
        print("FAIL: " + "; ".join(issues), file=sys.stderr)
        return 1
    print("PASS: QK100 Mk2 GIF delivery checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
