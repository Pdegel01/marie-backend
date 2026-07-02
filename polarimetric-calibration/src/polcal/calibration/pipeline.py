"""Main calibration pipeline: data selection → simulation → coefficient estimation."""

from __future__ import annotations

from pathlib import Path

import xarray as xr

from polcal.config import Config
from polcal.ingestion.base import InstrumentReader, Scene


def run_calibration(reader: InstrumentReader, data_path: Path, cfg: Config) -> xr.Dataset:
    """Run the full calibration pipeline and return estimated correction coefficients."""
    ...


def select_calibration_scenes(
    reader: InstrumentReader, data_path: Path, cfg: Config
) -> list[Scene]:
    """Filter granules to retain only scenes suitable for sunglint calibration."""
    ...


def estimate_mueller_corrections(
    measured: xr.Dataset, simulated: xr.Dataset, cfg: Config
) -> xr.Dataset:
    """Estimate per-band Mueller matrix correction coefficients by least-squares."""
    ...
