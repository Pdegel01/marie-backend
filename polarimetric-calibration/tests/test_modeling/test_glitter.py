"""Tests for the Cox-Munk glitter model."""

import pytest
from polcal.modeling.glitter import cox_munk_slope_pdf


def test_slope_distribution_positive():
    """Cox-Munk slope distribution must be non-negative everywhere."""
    ...


def test_slope_distribution_normalised():
    """Cox-Munk slope distribution must integrate to 1 over the hemisphere."""
    ...
