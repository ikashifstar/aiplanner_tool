"""Command-line entrypoint for video generation pipeline."""
from __future__ import annotations

import argparse
import logging

from src.services.pipeline import Pipeline

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate videos from metadata inputs")
    parser.add_argument("--title", required=True, help="Title of the video")
    parser.add_argument(
        "--resolution",
        required=True,
        help="Target resolution key (e.g., 720p, 1080p)",
    )
    parser.add_argument(
        "--duration",
        required=True,
        type=float,
        help="Duration in seconds",
    )
    parser.add_argument(
        "--video-type",
        required=True,
        dest="video_type",
        help="Type of video (e.g., explainer, promo)",
    )
    parser.add_argument(
        "--defaults-path",
        default="config/defaults.yaml",
        help="Path to YAML defaults for validation",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to place generated assets",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = Pipeline(output_dir=args.output_dir)
    final_path = pipeline.run(
        title=args.title,
        resolution=args.resolution,
        duration=args.duration,
        video_type=args.video_type,
        defaults_path=args.defaults_path,
    )
    print(f"Video generated at: {final_path}")


if __name__ == "__main__":
    main()
