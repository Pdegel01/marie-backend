"""Abstract base class that every instrument reader must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import xarray as xr


@dataclass
class Scene:
    """Minimal radiometric + geometric data for one overpass."""

    radiance: xr.Dataset
    stokes_q: xr.Dataset
    stokes_u: xr.Dataset
    geometry: xr.Dataset
    metadata: dict


class InstrumentReader(ABC):
    """Common interface for loading level-1 data from any instrument."""

    @abstractmethod
    def read(self, path: Path) -> Scene:
        """Read a single granule/file and return a normalised Scene."""
        ...

    @abstractmethod
    def list_granules(self, root: Path, date_range: tuple[str, str]) -> list[Path]:
        """Return paths to all granules within date_range under root."""
        ...

    @abstractmethod
    def filter_sunglint(self, scene: Scene, cfg) -> Scene:
        """Retain only pixels inside the sunglint window defined by cfg."""
        ...
