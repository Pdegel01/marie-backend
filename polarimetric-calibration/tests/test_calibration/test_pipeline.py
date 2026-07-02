"""Tests for the main calibration pipeline."""

import pytest
from polcal.calibration.pipeline import run_calibration


def test_pipeline_returns_dataset():
    """run_calibration must return an xr.Dataset with correction coefficients."""
    ...


def test_pipeline_bands_present():
    """Output dataset must contain one entry per configured spectral band."""
    ...
