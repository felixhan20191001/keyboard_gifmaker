#!/usr/bin/env python3
"""Find the longest 10 fps window whose 320x172 endpoints stay under MAE.

Prints JSON with the best start time and duration for ffmpeg -ss / -t.
Does not write a GIF.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


def mae(a: Image.Image, b: Image.Image) -> float:
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 4


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
    parser.add_argument("--max-frames", type=int, default=55)
    parser.add_argument("--min-frames", type=int, default=20)
    parser.add_argument("--max-mae", type=float, default=12.0)
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
        imgs = [Image.open(p).convert("RGBA") for p in files]
        n = len(imgs)
        max_dur = min(args.max_frames, n)
        hits: list[dict[str, float | int]] = []
        for start in range(0, n - args.min_frames + 1):
            for dur in range(args.min_frames, min(max_dur, n - start) + 1):
                end = start + dur - 1
                score = mae(imgs[start], imgs[end])
                if score <= args.max_mae:
                    hits.append(
                        {
                            "mae": round(score, 2),
                            "start_frame": start,
                            "end_frame": end,
                            "frames": dur,
                            "start_seconds": round(start / 10, 1),
                            "duration_seconds": round(dur / 10, 1),
                        }
                    )
        hits.sort(key=lambda row: (-int(row["frames"]), float(row["mae"])))
        pairs: list[dict[str, float | int]] = []
        for start in range(0, n - args.min_frames + 1):
            for end in range(start + args.min_frames - 1, n):
                score = mae(imgs[start], imgs[end])
                if score <= args.max_mae:
                    pairs.append(
                        {
                            "mae": round(score, 2),
                            "start_frame": start,
                            "end_frame": end,
                            "frames": end - start + 1,
                            "start_seconds": round(start / 10, 1),
                            "end_seconds": round(end / 10, 1),
                        }
                    )
        pairs.sort(key=lambda row: (float(row["mae"]), -int(row["frames"])))
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
            # Drop from the later half (return travel), keep the first
            # third (rise) and the last few endpoint frames.
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
            f"FAIL: no window of {args.min_frames}+ frames "
            f"has endpoint MAE <= {args.max_mae}",
            file=sys.stderr,
        )
        return 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
