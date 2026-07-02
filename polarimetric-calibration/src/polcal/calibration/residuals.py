"""Residual analysis between measured and simulated Stokes vectors."""

from __future__ import annotations

import numpy as np
import xarray as xr


def compute_residuals(measured: xr.Dataset, simulated: xr.Dataset) -> xr.Dataset:
    """Return pixel-wise residuals (measured − simulated) for all Stokes components."""
    ...


def residual_statistics(residuals: xr.Dataset) -> xr.Dataset:
    """Compute mean, std, RMSE and bias of residuals per band and view angle."""
    ...


def flag_outliers(residuals: xr.Dataset, n_sigma: float = 3.0) -> xr.DataArray:
    """Return a boolean mask flagging pixels with residuals beyond n_sigma."""
    ...
