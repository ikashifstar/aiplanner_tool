"""Convert script sections into timed scene plans."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

from .script_generator import ScriptSection


@dataclass
class Scene:
    index: int
    start_time: int
    end_time: int
    visuals: str
    narration: str


class ScenePlanner:
    """Generate temporal scene planning from script sections."""

    def plan(self, sections: Sequence[ScriptSection], total_duration: int) -> List[Scene]:
        if not sections:
            return []

        per_scene = max(1, total_duration // len(sections))
        scenes: List[Scene] = []
        current_start = 0

        for idx, section in enumerate(sections, start=1):
            end_time = min(total_duration, current_start + per_scene)
            scenes.append(
                Scene(
                    index=idx,
                    start_time=current_start,
                    end_time=end_time,
                    visuals=section.visuals,
                    narration=section.voice_over,
                )
            )
            current_start = end_time

        # Ensure final scene aligns with total duration
        if scenes and scenes[-1].end_time < total_duration:
            scenes[-1].end_time = total_duration
        return scenes


__all__ = ["ScenePlanner", "Scene"]
