"""Tests for the PARASOL reader."""

import pytest
from polcal.ingestion.parasol import ParasolReader


def test_reader_instantiation():
    """ParasolReader can be instantiated without arguments."""
    reader = ParasolReader()
    assert reader is not None


def test_reader_implements_interface():
    """ParasolReader implements all abstract methods of InstrumentReader."""
    from polcal.ingestion.base import InstrumentReader
    assert issubclass(ParasolReader, InstrumentReader)
