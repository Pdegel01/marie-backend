"""Concrete InstrumentReader for PARASOL/POLDER-3 HDF5 level-1 files."""

from __future__ import annotations

from pathlib import Path

from polcal.ingestion.base import InstrumentReader, Scene


class ParasolReader(InstrumentReader):
    """Reads PARASOL L1B HDF5 granules and normalises them into a Scene."""

    def read(self, path: Path) -> Scene:
        """Parse a single PARASOL HDF5 granule into a Scene."""
        ...

    def list_granules(self, root: Path, date_range: tuple[str, str]) -> list[Path]:
        """Glob PARASOL granules under root matching the given date range."""
        ...

    def filter_sunglint(self, scene: Scene, cfg) -> Scene:
        """Mask PARASOL pixels outside the sunglint cone specified in cfg."""
        ...
