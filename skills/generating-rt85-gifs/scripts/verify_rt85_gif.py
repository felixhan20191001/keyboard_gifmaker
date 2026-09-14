#!/usr/bin/env python3
"""Verify the delivery constraints for an EPOMAKER RT85 screen GIF.

Default panel is the common 1.47\" rectangular TFT in landscape: 320x172.
Override with --width/--height if the EPOMAKER driver crop differs
(e.g. portrait 172x320).
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
        default=320,
        help="Expected width (default 320 for landscape 1.47\" TFT)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=172,
        help="Expected height (default 172 for landscape 1.47\" TFT)",
    )
    parser.add_argument("--max-frames", type=int, default=51)
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
        help="Soft size ceiling; raise if the EPOMAKER driver accepts larger files",
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
            f"not {args.width}x{args.height}"
        )
    if image.size[0] == image.size[1]:
        issues.append(
            f"panel is square ({image.size[0]}x{image.size[1]}); "
            "RT85 delivery must be rectangular landscape (default 320x172)"
        )
    if image.width < image.height and (args.width, args.height) == (320, 172):
        issues.append(
            f"panel is portrait ({image.size[0]}x{image.size[1]}); "
            "RT85 default delivery is landscape 320x172"
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
    if any(duration not in (100, 110, 120) for duration in durations):
        issues.append(
            "frame delays must be 100, 110, or 120 ms "
            "(10 fps or even-sampled loop); duration is not a fixed 6.0 s"
        )

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
        "product": "EPOMAKER RT85",
        "screen": "1.47-inch landscape rectangular TFT",
        "expected_default": "320x172 landscape",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if warnings:
        print("WARN: " + "; ".join(warnings), file=sys.stderr)
    if issues:
        print("FAIL: " + "; ".join(issues), file=sys.stderr)
        return 1
    print("PASS: RT85 GIF delivery checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
