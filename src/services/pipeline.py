"""Pipeline orchestrator to tie together the generation steps."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from src.services.exporter import Exporter
from src.services.image_generator import ImageGenerator
from src.services.scene_planner import ScenePlanner
from src.services.script_generator import ScriptGenerator
from src.services.video_assembler import VideoAssembler
from src.services.voice_over import VoiceOverGenerator
from src.utils.validation import Metadata, ValidationError, validate_and_normalize_metadata

logger = logging.getLogger(__name__)


class Pipeline:
    """Builds a simple video using stubbed components."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.script_generator = ScriptGenerator()
        self.scene_planner = ScenePlanner()
        self.image_generator = ImageGenerator(output_dir)
        self.voice_over_generator = VoiceOverGenerator(output_dir)
        self.video_assembler = VideoAssembler(output_dir)
        self.exporter = Exporter(output_dir)

    def run(
        self,
        title: str,
        resolution: str,
        duration: float,
        video_type: str,
        defaults_path: Optional[str] = None,
    ) -> str:
        logger.info("Validating metadata")
        metadata: Metadata = validate_and_normalize_metadata(
            title=title,
            resolution=resolution,
            duration=duration,
            video_type=video_type,
            defaults_path=defaults_path or "config/defaults.yaml",
        )

        logger.info("Generating script")
        sections = self.script_generator.generate(metadata.title, metadata.video_type)

        logger.info("Planning scenes")
        scenes = self.scene_planner.plan(sections, total_duration=metadata.duration_seconds)

        logger.info("Generating images")
        images = self.image_generator.generate(scenes)

        logger.info("Generating voice-over")
        audio_path = self.voice_over_generator.synthesize(scenes)

        logger.info("Assembling video timeline")
        timeline_path = self.video_assembler.assemble(
            scenes=scenes, images=images, resolution_label=metadata.resolution.label
        )

        logger.info("Exporting final media")
        final_path = self.exporter.export(
            timeline_path=timeline_path,
            audio_path=audio_path,
            output_format=metadata.output_format,
        )

        logger.info("Pipeline completed: %s", final_path)
        return final_path


__all__ = ["Pipeline"]
