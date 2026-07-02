"""Data ingestion layer — abstract interface and per-instrument loaders."""

from polcal.ingestion.base import InstrumentReader, Scene

__all__ = ["InstrumentReader", "Scene"]
