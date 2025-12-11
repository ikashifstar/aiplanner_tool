from pathlib import Path

from src.services.pipeline import Pipeline


def test_pipeline_creates_output(tmp_path):
    output_dir = tmp_path / "output"
    pipeline = Pipeline(output_dir=str(output_dir))

    final_path = pipeline.run(
        title="Sample",
        resolution="720p",
        duration=90,
        video_type="explainer",
        defaults_path="config/defaults.yaml",
    )

    assert Path(final_path).exists()
    content = Path(final_path).read_text(encoding="utf-8")
    assert "Timeline" in content
    assert "Audio" in content
