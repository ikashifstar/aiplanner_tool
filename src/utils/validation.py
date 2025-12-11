"""Validation helpers for video metadata.

This module normalizes inputs from the CLI or service layer, ensuring
values are within expected bounds.
"""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

_DEFAULTS_PATH = "config/defaults.yaml"
_YAML_AVAILABLE = importlib.util.find_spec("yaml") is not None
if _YAML_AVAILABLE:  # pragma: no cover - exercised when dependency is present
    import yaml
else:
    yaml = None  # type: ignore


@dataclass
class Resolution:
    label: str
    width: int
    height: int

    def as_tuple(self) -> Tuple[int, int]:
        return self.width, self.height


@dataclass
class Metadata:
    title: str
    resolution: Resolution
    duration_seconds: int
    video_type: str
    output_format: str


class ValidationError(ValueError):
    """Raised when metadata fails validation."""


DEFAULTS = {
    "allowed_resolutions": {
        "720p": {"width": 1280, "height": 720},
        "1080p": {"width": 1920, "height": 1080},
        "4k": {"width": 3840, "height": 2160},
    },
    "supported_video_types": ("explainer", "tutorial", "promo", "narrative"),
    "min_duration_seconds": 30,
    "max_duration_seconds": 3600,
    "output_format": "mp4",
}


def _parse_scalar(value: str):
    value = value.strip()
    if value.isdigit():
        return int(value)
    return value


def _parse_defaults_without_yaml(text: str) -> Dict:
    data: Dict = {}
    current_section = None
    current_resolution = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip())
        line = raw_line.strip()

        if indent == 0:
            key, _, value = line.partition(":")
            key = key.strip()
            if value.strip():
                data[key] = _parse_scalar(value)
                current_section = None
            else:
                current_section = key
                if key == "allowed_resolutions":
                    data[key] = {}
                elif key == "supported_video_types":
                    data[key] = []
        elif indent == 2 and current_section == "allowed_resolutions":
            current_resolution = line.rstrip(":")
            data[current_section][current_resolution] = {}
        elif indent == 4 and current_section == "allowed_resolutions" and current_resolution:
            key, _, value = line.partition(":")
            data[current_section][current_resolution][key] = _parse_scalar(value)
        elif indent >= 2 and current_section == "supported_video_types" and line.startswith("- "):
            data[current_section].append(line[2:].strip())

    return data


def _load_defaults(path: str = _DEFAULTS_PATH) -> Dict:
    path_obj = Path(path)
    if yaml and path_obj.exists():
        return yaml.safe_load(path_obj.read_text(encoding="utf-8"))
    if path_obj.exists():
        parsed = _parse_defaults_without_yaml(path_obj.read_text(encoding="utf-8"))
        merged = DEFAULTS.copy()
        merged.update(parsed)
        return merged
    return DEFAULTS.copy()


def _normalize_resolution(resolution: str, allowed: Dict[str, Dict[str, int]]) -> Resolution:
    key = str(resolution).lower()
    if key not in allowed:
        raise ValidationError(
            f"Unsupported resolution '{resolution}'. Allowed: {', '.join(sorted(allowed))}."
        )
    data = allowed[key]
    return Resolution(label=key, width=int(data["width"]), height=int(data["height"]))


def _normalize_video_type(video_type: str, allowed: Tuple[str, ...]) -> str:
    normalized = str(video_type).lower().strip()
    if normalized not in allowed:
        raise ValidationError(
            f"Unsupported video type '{video_type}'. Allowed: {', '.join(sorted(allowed))}."
        )
    return normalized


def _normalize_duration(duration: float, min_seconds: int, max_seconds: int) -> int:
    try:
        seconds = int(float(duration))
    except (TypeError, ValueError):
        raise ValidationError("Duration must be numeric.")

    if seconds < min_seconds or seconds > max_seconds:
        raise ValidationError(
            f"Duration must be between {min_seconds} and {max_seconds} seconds."
        )
    return seconds


def validate_and_normalize_metadata(
    title: str,
    resolution: str,
    duration: float,
    video_type: str,
    defaults_path: str = _DEFAULTS_PATH,
) -> Metadata:
    """Validate and normalize user-supplied metadata.

    Args:
        title: Video title.
        resolution: Named resolution key from defaults.
        duration: Duration in seconds (numeric).
        video_type: A supported video type.
        defaults_path: Optional path to YAML defaults for customization.

    Returns:
        Metadata: Normalized metadata object.

    Raises:
        ValidationError: If any value is invalid.
    """
    if not title or not str(title).strip():
        raise ValidationError("Title is required.")

    defaults = _load_defaults(defaults_path)
    allowed_resolutions = defaults.get("allowed_resolutions", {})
    supported_types = tuple(defaults.get("supported_video_types", ()))
    min_duration = int(defaults.get("min_duration_seconds", DEFAULTS["min_duration_seconds"]))
    max_duration = int(defaults.get("max_duration_seconds", DEFAULTS["max_duration_seconds"]))
    output_format = str(defaults.get("output_format", DEFAULTS["output_format"])).lower()

    normalized_resolution = _normalize_resolution(resolution, allowed_resolutions)
    normalized_type = _normalize_video_type(video_type, supported_types)
    normalized_duration = _normalize_duration(duration, min_duration, max_duration)

    return Metadata(
        title=str(title).strip(),
        resolution=normalized_resolution,
        duration_seconds=normalized_duration,
        video_type=normalized_type,
        output_format=output_format,
    )


__all__ = [
    "Metadata",
    "Resolution",
    "ValidationError",
    "validate_and_normalize_metadata",
]
