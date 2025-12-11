"""Finalize export by merging timeline and audio placeholders."""
from __future__ import annotations

from pathlib import Path


class Exporter:
    """Write a placeholder final media file."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, timeline_path: str, audio_path: str, output_format: str = "mp4") -> str:
        final_path = self.output_dir / f"final_output.{output_format}"
        timeline_content = Path(timeline_path).read_text(encoding="utf-8")
        audio_content = Path(audio_path).read_text(encoding="utf-8")
        final_content = (
            "--- Timeline ---\n" + timeline_content + "\n\n--- Audio ---\n" + audio_content
        )
        final_path.write_text(final_content, encoding="utf-8")
        return str(final_path)


__all__ = ["Exporter"]
