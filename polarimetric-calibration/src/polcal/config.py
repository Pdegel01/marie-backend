"""Load and validate configuration from YAML files."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class Config:
    """Holds the merged runtime configuration."""

    def __init__(self, data: dict[str, Any]) -> None:
        ...

    def __getattr__(self, name: str) -> Any:
        ...


def load_config(path: Path | None = None, instrument: str | None = None) -> Config:
    """Load default.yaml, optionally merge an instrument-specific config, and return a Config."""
    ...


def resolve_paths(cfg: Config) -> Config:
    """Expand environment variables and relative paths inside cfg.paths."""
    ...
