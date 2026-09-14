#!/usr/bin/env python3
"""Find the longest 10 fps window whose endpoints loop.

A window passes when blurred/downscaled endpoint MAE stays under the
structure cap, and the seam is either within 1.3x median consecutive-frame
MAE or under the absolute RGB MAE cap. Prints JSON with the best start
time and duration for ffmpeg -ss / -t. Does not write a GIF.
"""

from __future__ import annotations

import argparse
import json
import shutil
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter, ImageStat


def rgb_mae(a: Image.Image, b: Image.Image) -> float:
    return sum(ImageStat.Stat(ImageChops.difference(a.convert("RGB"), b.convert("RGB"))).mean) / 3


def structure_frame(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB").filter(ImageFilter.GaussianBlur(2))
    width, height = rgb.size
    return rgb.resize(
        (max(16, width // 6), max(16, height // 6)),
        Image.Resampling.BILINEAR,
    )


def is_loop(
    endpoint_mae: float,
    ratio: float,
    struct_mae: float,
    max_struct: float,
    max_ratio: float,
    max_mae: float,
) -> bool:
    if struct_mae > max_struct:
        return False
    return ratio <= max_ratio or endpoint_mae <= max_mae


def window_row(
    start: int,
    end: int,
    endpoint_mae: float,
    step_mae: float,
    ratio: float,
    struct_mae: float,
) -> dict[str, float | int]:
    frames = end - start + 1
    return {
        "mae": round(endpoint_mae, 2),
        "step_mae": round(step_mae, 2),
        "ratio": round(ratio, 2),
        "struct_mae": round(struct_mae, 2),
        "start_frame": start,
        "end_frame": end,
        "frames": frames,
        "start_seconds": round(start / 10, 1),
        "duration_seconds": round(frames / 10, 1),
        "end_seconds": round(end / 10, 1),
    }


def extract_frames(src: Path, width: int, height: int, dest: Path) -> list[Path]:
    dest.mkdir(parents=True, exist_ok=True)
    vf = (
        f"fps=10,scale={width}:{height}:force_original_aspect_ratio=increase"
        f":flags=lanczos,crop={width}:{height}"
    )
    subprocess.check_call(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-vf",
            vf,
            str(dest / "%03d.png"),
        ]
    )
    return sorted(dest.glob("*.png"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source MP4")
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--height", type=int, default=172)
    parser.add_argument("--max-frames", type=int, default=51)
    parser.add_argument("--min-frames", type=int, default=20)
    parser.add_argument(
        "--max-mae",
        type=float,
        default=12.0,
        help="Absolute RGB MAE still accepted on quiet clips",
    )
    parser.add_argument(
        "--max-endpoint-ratio",
        type=float,
        default=1.3,
        help="Accept when endpoint MAE <= this multiple of median step MAE",
    )
    parser.add_argument(
        "--max-struct-mae",
        type=float,
        default=16.0,
        help="Max blurred/downscaled endpoint MAE; pose/layout cap",
    )
    args = parser.parse_args()

    if not args.source.is_file() or args.source.stat().st_size == 0:
        print(f"FAIL: missing or empty source: {args.source}", file=sys.stderr)
        return 1

    tmp = Path(tempfile.mkdtemp(prefix="rt85-loop-"))
    try:
        files = extract_frames(args.source, args.width, args.height, tmp / "frames")
        if len(files) < args.min_frames:
            print(f"FAIL: only {len(files)} frames extracted", file=sys.stderr)
            return 1
        imgs = [Image.open(p).convert("RGB") for p in files]
        structs = [structure_frame(im) for im in imgs]
        n = len(imgs)
        steps = [rgb_mae(imgs[i], imgs[i + 1]) for i in range(n - 1)]
        max_dur = min(args.max_frames, n)
        hits: list[dict[str, float | int]] = []
        pairs: list[dict[str, float | int]] = []
        for start in range(0, n - args.min_frames + 1):
            for end in range(start + args.min_frames - 1, n):
                endpoint = rgb_mae(imgs[start], imgs[end])
                step_mae = float(statistics.median(steps[start:end]))
                ratio = (endpoint / step_mae) if step_mae > 0 else (0.0 if endpoint == 0 else float("inf"))
                struct_mae = rgb_mae(structs[start], structs[end])
                if not is_loop(
                    endpoint,
                    ratio,
                    struct_mae,
                    args.max_struct_mae,
                    args.max_endpoint_ratio,
                    args.max_mae,
                ):
                    continue
                row = window_row(start, end, endpoint, step_mae, ratio, struct_mae)
                pairs.append(row)
                if int(row["frames"]) <= max_dur:
                    hits.append(row)
        hits.sort(key=lambda row: (-int(row["frames"]), float(row["struct_mae"]), float(row["ratio"]), float(row["mae"])))
        pairs.sort(key=lambda row: (float(row["struct_mae"]), float(row["ratio"]), float(row["mae"]), -int(row["frames"])))
        best_pair = pairs[0] if pairs else None
        assemble = None
        if (
            not hits
            and best_pair is not None
            and int(best_pair["frames"]) > args.max_frames
        ):
            start = int(best_pair["start_frame"])
            end = int(best_pair["end_frame"])
            drop = int(best_pair["frames"]) - args.max_frames
            keep_tail = min(8, args.max_frames // 5)
            keep_head = args.max_frames - keep_tail
            assemble = {
                "start_frame": start,
                "end_frame": end,
                "drop_frames": drop,
                "keep_head": keep_head,
                "keep_tail": keep_tail,
            }
        report = {
            "source": str(args.source),
            "extracted_frames": n,
            "width": args.width,
            "height": args.height,
            "max_mae": args.max_mae,
            "max_endpoint_ratio": args.max_endpoint_ratio,
            "max_struct_mae": args.max_struct_mae,
            "candidates": len(hits),
            "best": hits[0] if hits else None,
            "best_pair": best_pair,
            "assemble": assemble,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        if hits:
            print(
                "PASS: use ffmpeg -i SOURCE -ss "
                f"{hits[0]['start_seconds']} -t {hits[0]['duration_seconds']}",
                file=sys.stderr,
            )
            return 0
        if assemble is not None:
            print(
                "PASS: no ≤"
                f"{args.max_frames}-frame trim; assemble frames "
                f"{assemble['start_frame']}-{assemble['end_frame']} "
                f"keeping head {assemble['keep_head']} + tail "
                f"{assemble['keep_tail']} (drop {assemble['drop_frames']} "
                "from return travel). Do not time-stretch the clip.",
                file=sys.stderr,
            )
            return 0
        print(
            f"FAIL: no window of {args.min_frames}+ frames has "
            f"struct MAE <= {args.max_struct_mae} and "
            f"(ratio <= {args.max_endpoint_ratio} or MAE <= {args.max_mae})",
            file=sys.stderr,
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
