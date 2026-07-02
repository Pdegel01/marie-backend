"""Atmospheric correction and aerosol model selection for clean maritime scenes."""

from __future__ import annotations

import numpy as np
import xarray as xr


def is_clean_maritime(scene_aod: xr.DataArray, cfg) -> xr.DataArray:
    """Return a boolean mask — True where aerosol loading is within cfg thresholds."""
    ...


def rayleigh_optical_depth(wavelength_nm: float, pressure_hpa: float) -> float:
    """Compute Rayleigh optical depth for a given wavelength and surface pressure."""
    ...


def aerosol_phase_matrix(scattering_angle: np.ndarray, model: str) -> np.ndarray:
    """Return the 4×4 aerosol Mueller phase matrix at the given scattering angles."""
    ...
