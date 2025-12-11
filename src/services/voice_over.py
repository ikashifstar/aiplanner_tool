"""Stub voice-over synthesis and integration."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .scene_planner import Scene


class VoiceOverGenerator:
    """Generate placeholder voice-over audio for scenes."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.audio_dir = self.output_dir / "audio"
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def synthesize(self, scenes: Iterable[Scene]) -> str:
        audio_file = self.audio_dir / "voice_over.txt"
        lines = []
        for scene in scenes:
            lines.append(f"Scene {scene.index}: {scene.narration}")
        audio_file.write_text("\n".join(lines), encoding="utf-8")
        return str(audio_file)


__all__ = ["VoiceOverGenerator"]
