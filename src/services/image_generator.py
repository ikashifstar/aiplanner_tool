"""Placeholder image generation for scenes."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, List

from .scene_planner import Scene


class ImageGenerator:
    """Create placeholder images for each scene.

    In a production setting this would call an AI image generator. For now,
    it writes simple text files that represent generated assets.
    """

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, scenes: Iterable[Scene]) -> Dict[int, str]:
        image_map: Dict[int, str] = {}
        for scene in scenes:
            filename = self.images_dir / f"scene_{scene.index}.txt"
            content = (
                f"Image placeholder for scene {scene.index}:\n"
                f"Visuals: {scene.visuals}\n"
                f"Timing: {scene.start_time}-{scene.end_time}"
            )
            filename.write_text(content, encoding="utf-8")
            image_map[scene.index] = str(filename)
        return image_map


__all__ = ["ImageGenerator"]
