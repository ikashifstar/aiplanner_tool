"""Generate a structured script based on title and video type."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ScriptSection:
    heading: str
    voice_over: str
    visuals: str


class ScriptGenerator:
    """Generate lightweight scripts for the pipeline."""

    def generate(self, title: str, video_type: str) -> List[ScriptSection]:
        outline = [
            "Introduction",
            "Problem Statement",
            "Solution Walkthrough",
            "Key Takeaways",
            "Closing Thoughts",
        ]
        sections: List[ScriptSection] = []
        for index, heading in enumerate(outline, start=1):
            voice_over = (
                f"{heading}: This {video_type} titled '{title}' explains the core idea "
                f"with clear, concise narration."
            )
            visuals = (
                f"Scene {index}: Visuals highlighting {heading.lower()} with simple "
                f"graphics related to {title}."
            )
            sections.append(ScriptSection(heading=heading, voice_over=voice_over, visuals=visuals))
        return sections


__all__ = ["ScriptGenerator", "ScriptSection"]
