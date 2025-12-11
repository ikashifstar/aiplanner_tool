"""Assemble scenes and images into a timeline placeholder."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

from .scene_planner import Scene


class VideoAssembler:
    """Stub video assembler that writes a timeline description."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.video_dir = self.output_dir / "video"
        self.video_dir.mkdir(parents=True, exist_ok=True)

    def assemble(self, scenes: Iterable[Scene], images: Dict[int, str], resolution_label: str) -> str:
        timeline_file = self.video_dir / "timeline.txt"
        lines = [f"Resolution: {resolution_label}"]
        for scene in scenes:
            image_path = images.get(scene.index, "unknown")
            lines.append(
                f"Scene {scene.index} [{scene.start_time}-{scene.end_time}] | "
                f"Image: {image_path} | Narration: {scene.narration}"
            )
        timeline_file.write_text("\n".join(lines), encoding="utf-8")
        return str(timeline_file)


__all__ = ["VideoAssembler"]
