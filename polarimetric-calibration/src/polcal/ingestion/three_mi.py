"""Concrete InstrumentReader for 3MI/MetOp-SG NetCDF4 level-1 files (not yet available)."""

from __future__ import annotations

from pathlib import Path

from polcal.ingestion.base import InstrumentReader, Scene


class ThreeMIReader(InstrumentReader):
    """Reads 3MI L1B NetCDF4 granules and normalises them into a Scene."""

    def read(self, path: Path) -> Scene:
        """Parse a single 3MI NetCDF4 granule into a Scene."""
        ...

    def list_granules(self, root: Path, date_range: tuple[str, str]) -> list[Path]:
        """Glob 3MI granules under root matching the given date range."""
        ...

    def filter_sunglint(self, scene: Scene, cfg) -> Scene:
        """Mask 3MI pixels outside the sunglint cone specified in cfg."""
        ...
