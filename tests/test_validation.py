import pytest

from src.utils.validation import ValidationError, validate_and_normalize_metadata


def test_validate_and_normalize_metadata_success(tmp_path):
    defaults = tmp_path / "defaults.yaml"
    defaults.write_text(
        """
allowed_resolutions:
  720p:
    width: 1280
    height: 720
supported_video_types:
  - tutorial
min_duration_seconds: 10
max_duration_seconds: 120
output_format: mp4
""",
        encoding="utf-8",
    )

    metadata = validate_and_normalize_metadata(
        title="Test Video",
        resolution="720p",
        duration=60,
        video_type="tutorial",
        defaults_path=str(defaults),
    )

    assert metadata.title == "Test Video"
    assert metadata.resolution.width == 1280
    assert metadata.duration_seconds == 60
    assert metadata.video_type == "tutorial"


def test_validate_and_normalize_metadata_invalid_resolution(tmp_path):
    defaults = tmp_path / "defaults.yaml"
    defaults.write_text(
        """
allowed_resolutions:
  1080p:
    width: 1920
    height: 1080
supported_video_types:
  - promo
min_duration_seconds: 10
max_duration_seconds: 120
output_format: mp4
""",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        validate_and_normalize_metadata(
            title="Example",
            resolution="4k",
            duration=50,
            video_type="promo",
            defaults_path=str(defaults),
        )
